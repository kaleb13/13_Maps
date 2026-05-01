# 🗺️ RouteOpt — Route Optimization SaaS

AI-powered route optimization platform built with **FastAPI**, **Vue 3**, **PostgreSQL**, and **OSRM**.

---

## 📁 Project Structure

```
13_Maps/
├── backend/                  # FastAPI Python API
│   ├── app/
│   │   ├── core/             # Config, DB, Security
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── routes/           # FastAPI routers
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   └── services/         # Business logic & OSRM integration
│   ├── alembic/              # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                 # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── api/              # Axios API modules
│   │   ├── assets/           # Global CSS design system
│   │   ├── router/           # Vue Router
│   │   ├── stores/           # Pinia state stores
│   │   └── views/            # Page components
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .env.example
│
├── osrm-backend-master/      # OSRM source (existing)
├── osrm-data/                # Place pre-processed .osrm map files here
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Copy environment files

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Edit `.env` and `backend/.env` with your real credentials.

### 2. Prepare OSRM map data

```bash
mkdir osrm-data
# Download a PBF file, e.g. for Ethiopia:
# https://download.geofabrik.de/africa/ethiopia-latest.osm.pbf

# Pre-process (run once):
docker run -t -v ${PWD}/osrm-data:/data osrm/osrm-backend \
  osrm-extract -p /opt/car.lua /data/ethiopia-latest.osm.pbf

docker run -t -v ${PWD}/osrm-data:/data osrm/osrm-backend \
  osrm-partition /data/ethiopia-latest.osrm

docker run -t -v ${PWD}/osrm-data:/data osrm/osrm-backend \
  osrm-customize /data/ethiopia-latest.osrm
```

Update the `osrm` service command in `docker-compose.yml` with the correct `.osrm` file name.

### 3. Start all services

```bash
docker-compose up --build
```

| Service  | URL                              |
|----------|----------------------------------|
| Frontend | http://localhost                 |
| Backend  | http://localhost:8000            |
| API Docs | http://localhost:8000/docs       |
| OSRM     | http://localhost:5000            |
| DB       | localhost:5432                   |

---

## 🛠️ Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env       # edit DATABASE_URL to point to local PG
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔌 API Endpoints

| Method | Path                     | Description              | Auth |
|--------|--------------------------|--------------------------|------|
| GET    | /api/v1/health           | API health check         | ✗    |
| GET    | /api/v1/health/db        | DB health check          | ✗    |
| GET    | /api/v1/health/osrm      | OSRM health check        | ✗    |
| POST   | /api/v1/auth/register    | Register user            | ✗    |
| POST   | /api/v1/auth/token       | Login → JWT              | ✗    |
| GET    | /api/v1/routes           | List route requests      | ✔    |
| POST   | /api/v1/routes           | Create route request     | ✔    |
| GET    | /api/v1/routes/{id}      | Get route request        | ✔    |
| PATCH  | /api/v1/routes/{id}      | Update route request     | ✔    |
| DELETE | /api/v1/routes/{id}      | Delete route request     | ✔    |
| POST   | /api/v1/optimize         | Submit optimization job  | ✔    |
| GET    | /api/v1/jobs             | List optimization jobs   | ✔    |
| GET    | /api/v1/jobs/{id}        | Get job status           | ✔    |

Full interactive docs: **http://localhost:8000/docs**

---

## 🗄️ Database Migrations (Alembic)

```bash
cd backend

# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

---

## 🏗️ Architecture

```
Browser (Vue 3 + Pinia)
    │  HTTPS / HTTP
    ▼
Nginx (reverse proxy)
    │
    ├── /          → Vue SPA (static files)
    └── /api/      → FastAPI backend
                        │
                        ├── PostgreSQL (SQLAlchemy async)
                        └── OSRM Engine (httpx async client)
```

---

## 🔐 Security

- JWT Bearer tokens (HS256, configurable expiry)
- Bcrypt password hashing
- All protected routes require authentication
- Owner-scoped queries (users can only access their own data)
- Input validation via Pydantic with strict types
- CORS restricted to configured origins
