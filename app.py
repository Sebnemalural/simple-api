from flask import Flask, jsonify, request
import requests
import sqlite3
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# --- 1) Veritabanı yolu ve init fonksiyonu ---
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # cache tablosu
    c.execute('''
      CREATE TABLE IF NOT EXISTS cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT UNIQUE,
        response_json TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    ''')
    
    # api_posts tablosu
    c.execute('''
      CREATE TABLE IF NOT EXISTS api_posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    ''')
    conn.commit()
    conn.close()

# --- 2) Helper: DB bağlantısı ---
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- 3) Helper: dış API’dan çek ve cache’e kaydet ---
def fetch_external(endpoint_url):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT response_json, fetched_at FROM cache WHERE endpoint = ?", (endpoint_url,))
    row = cur.fetchone()
    if row:
        response_json, fetched_at_str = row['response_json'], row['fetched_at']
        # fetched_at string’ini datetime’a çevir
        fetched_at = datetime.fromisoformat(fetched_at_str)

        # 2) Eğer 1 saatten eski değilse, direkt döndür
        if datetime.utcnow() - fetched_at < timedelta(hours=1):
            conn.close()
            return json.loads(response_json)

        # 3) Eskiyse cache’den sil (ya da üzerine yazacağız)
        cur.execute("DELETE FROM cache WHERE endpoint = ?", (endpoint_url,))
        conn.commit()

# --- 4) Veriyi DB’ye yazan fonksiyon ---
def store_posts(posts):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for post in posts:
        cur.execute('''
          INSERT OR REPLACE INTO api_posts (id, user_id, title, body)
          VALUES (?, ?, ?, ?)
        ''', (
          post['id'],
          post['userId'],
          post['title'],
          post['body']
        ))
    conn.commit()
    conn.close()

# --- 5) Health check ---
@app.route('/health')
def health():
    return jsonify({'status': 'OK'})

# --- 6) Proxy endpoint ---
@app.route('/api/proxy')
def proxy():
    source_url = request.args.get('url')
    if not source_url:
        return jsonify({'error': 'url parametresi eksik'}), 400
    try:
        data = fetch_external(source_url)
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Dış servise bağlanamadı', 'details': str(e)}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- 7) Sync endpoint ---
@app.route('/sync-posts')
def sync_posts():
    external_url = 'https://jsonplaceholder.typicode.com/posts'
    posts = fetch_external(external_url)
    try:
        store_posts(posts)
        return jsonify({'status': 'synced', 'count': len(posts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/posts')
def list_posts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM api_posts ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)


# --- 8) Uygulama başlatma ---
if __name__ == '__main__':
    init_db()
    print("⚙️  Starting Flask…")
    app.run(host='0.0.0.0', port=5000, debug=True)
