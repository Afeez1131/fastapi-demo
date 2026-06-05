# FastAPI Demo — Products API

Simple FastAPI project with PostgreSQL + Redis cache. No auth. Built for learning.

## Stack

- FastAPI + async SQLAlchemy (asyncpg)
- PostgreSQL
- Redis (response caching)
- Faker (seed data)

## Project Structure

```
app/
├── main.py           # entrypoint, lifespan, router registration
├── config.py         # settings from .env
├── database.py       # async engine + session
├── cache.py          # redis helpers (get, set, invalidate)
├── models/
│   └── product.py    # SQLAlchemy model
├── schemas/
│   └── product.py    # Pydantic in/out schemas
├── routers/
│   └── product.py    # route handlers (thin)
└── services/
    └── product.py    # business logic + cache logic (fat)
seed.py               # populate DB with dummy data
```

## Setup

```bash
# 1. Clone and enter project
cd fastapi-demo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# edit .env with your DB and Redis URLs

# 5. Start PostgreSQL and Redis (or use Docker)
docker run -d --name pg -e POSTGRES_PASSWORD=password -e POSTGRES_DB=demo -p 5432:5432 postgres:15
docker run -d --name redis -p 6379:6379 redis:7

# 6. Seed the database
python seed.py

# 7. Run the server
uvicorn app.main:app --reload
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /products/ | List all active products (cached) |
| GET | /products/{id} | Get single product (cached) |
| POST | /products/ | Create product (invalidates cache) |
| PATCH | /products/{id} | Update product (invalidates cache) |
| DELETE | /products/{id} | Delete product (invalidates cache) |
| GET | /health | Health check |

## How Caching Works

- `GET /products/` — checks Redis first (`products:all`), hits DB on miss, caches result for 60s
- `GET /products/{id}` — checks Redis first (`products:{id}`), hits DB on miss, caches result for 60s
- Any write operation (POST, PATCH, DELETE) — invalidates relevant cache keys immediately

## Docs

Visit `http://localhost:8000/docs` for the interactive Swagger UI.
