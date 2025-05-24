# Simple API Documentation

This project is a simple Flask service that fetches data from public JSON APIs (e.g., JSONPlaceholder), caches the responses in SQLite, and provides both a proxy and data synchronization functionality.

## Requirements

* Python 3.10+
* Packages (listed in `requirements.txt`):

  * Flask
  * requests
  * flask-restx

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd simple-api

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Database

On first run, the application creates a SQLite database file named `data.db` with two tables:

* **cache**: Temporarily stores external API JSON responses
* **api\_posts**: Holds `posts` data fetched from JSONPlaceholder

Both tables are initialized automatically by the `init_db()` function when the server starts.

## Available Endpoints

| Route                  | Method | Description                                                             |
| ---------------------- | ------ | ----------------------------------------------------------------------- |
| `/`                    | GET    | Lists all available routes                                              |
| `/health`              | GET    | Returns server status (`{ "status": "OK" }`)                            |
| `/api/proxy?url=<URL>` | GET    | Proxies and caches JSON from the provided URL                           |
| `/sync-posts`          | GET    | Fetches all `posts` from JSONPlaceholder and writes them to `api_posts` |
| `/posts`               | GET    | Returns all records from the `api_posts` table                          |

### Usage Examples

#### Health Check

```bash
curl http://127.0.0.1:5000/health
# => {"status":"OK"}
```

#### Proxy Example

```bash
curl "http://127.0.0.1:5000/api/proxy?url=https://jsonplaceholder.typicode.com/posts/1"
```

#### Sync Posts

```bash
curl http://127.0.0.1:5000/sync-posts
# => {"status":"synced","count":100}
```

#### List Posts

```bash
curl http://127.0.0.1:5000/posts
```


