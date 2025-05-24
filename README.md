# Simple API Documentation

Bu proje, JSONPlaceholder gibi herkese açık JSON API’lerinden veri çekip SQLite veritabanına yazan ve proxy olarak kullanan basit bir Flask servistir.

## Gereksinimler

* Python 3.10+
* Paketler (requirements.txt içinde):

  * Flask
  * requests

## Kurulum

```bash
git clone <repo-url>
cd simple-api
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

## Veritabanı

Uygulama `data.db` adında SQLite dosyası oluşturur ve iki temel tablo barındırır:

* `cache`: Dış API yanıtlarını geçici saklama
* `api_posts`: JSONPlaceholder’dan çekilen `posts` verisi

Uygulama ilk çalıştırıldığında tablolar `init_db()` fonksiyonuyla otomatik oluşturulur.

## Mevcut Endpoint’ler

| Yol                  | Metot | Açıklama                                                               |
| -------------------- | ----- | ---------------------------------------------------------------------- |
| `/`                  | GET   | Mevcut route’ları listeler                                             |
| `/health`            | GET   | Servisin durumunu kontrol eder (`OK`)                                  |
| `/api/proxy?url=...` | GET   | Verilen URL’den JSON çeker ve cache’ler                                |
| `/sync-posts`        | GET   | JSONPlaceholder’dan tüm post’ları çeker ve `api_posts` tablosuna yazar |
| `/posts`             | GET   | `api_posts` tablosundaki tüm kayıtları döner                           |

### Kullanım Örnekleri

#### Health Check

```bash
curl http://127.0.0.1:5000/health
# => {"status":"OK"}
```

#### Proxy Kullanımı

```bash
curl "http://127.0.0.1:5000/api/proxy?url=https://jsonplaceholder.typicode.com/posts/1"
```

#### Senkronizasyon

```bash
curl http://127.0.0.1:5000/sync-posts
# => {"status":"synced","count":100}
```

#### Verileri Listeleme

```bash
curl http://127.0.0.1:5000/posts
```

## Önerilen İyileştirmeler

1. **Cache Expiry**: `cache` tablosundaki verilerin belirli bir süre sonra (örn. 1 saat) yeniden fetch edilmesi.
2. **OpenAPI / Swagger Dokümantasyonu**: `flask-swagger` veya `flask-restx` ile otomatik API dokümantasyonu.
3. **Genel Sync Mekanizması**: `/sync?url=<URL>&table=<TABLO>&mapping=<JSON>` gibi parametreli bir endpoint.

---

*Bu doküman, projenin kullanımını ve temel özelliklerini özetler.*
