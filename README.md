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

## Recommended Enhancements

1. **Cache Expiry**: Invalidate and refresh cache entries older than a set duration (e.g., 1 hour) by comparing `fetched_at` timestamps in `fetch_external()`.
2. **OpenAPI / Swagger Documentation**: Integrate `flask-restx` to generate interactive Swagger UI at `/` showing all endpoints, models, and schemas.
3. **Generic Sync Endpoint**: Create a parameterized `/sync` route (e.g., `/sync?url=<URL>&table=<TABLE>&mapping=<JSON>`) to support dynamic synchronization for different JSON structures and tables.

---

*This document summarizes the usage and key features of the Simple API project.*
