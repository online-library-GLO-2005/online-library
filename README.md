# 📚 Online Library

A full-stack web application for browsing and managing an online library. Users can track reading progress, bookmark favourites, and leave reviews. Admins can manage content and moderate reviews.

---

## 🏗️ Architecture

Three-tier architecture with each tier running in its own Docker container:

```
Vite React (Frontend)  →  Flask (Backend)  →  MySQL (Database)
   :3000                    :5000                  :3306
```

> Ports shown are for development. Production uses :80 (frontend) and :8000 (backend).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Tailwind CSS, Vite |
| Backend | Python, Flask |
| Database | MySQL 8 |
| Auth | JWT (Flask-JWT-Extended) |
| Validation | Marshmallow |
| Containerization | Docker, Docker Compose |
| Testing | pytest |

---

## 📁 Project Structure

```
online-library/
├── docker-compose.yml
├── docker-compose.prod.yml
├── frontend/
│   ├── Dockerfiles/
│   │   ├── Dockerfile.dev
│   │   └── Dockerfile.release
│   ├── src/
│   └── ...
└── backend/
    ├── Dockerfiles/
    │   ├── Dockerfile.dev
    │   └── Dockerfile.release
    ├── run.py
    ├── requirements.txt
    ├── db/
    │   ├── 01_init.sql
    │   ├── 02_triggers.sql
    │   ├── 03_indexes.sql
    │   ├── 04_procedures.sql
    │   └── 05_seed.sql
    └── app/
        ├── __init__.py     ← app factory
        └── ...
```

> More details about the backend and frontend structure are available in the documentation folder.

---

## ⚙️ Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running
  - [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
  - [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
  - [Linux](https://docs.docker.com/desktop/setup/install/linux/)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/online-library-glo-2005/online-library.git
cd online-library
```

### 2. Environment variables

`.env` files are committed for simplicity (school project). No configuration needed — everything works out of the box.

### 3a. Development — build and run

> Make sure ports `3000`, `5000`, and `3306` are free before starting.

First time, or after changing a `Dockerfile`, `requirements.txt`, or `package.json`:

```bash
docker compose up --build
```

For subsequent runs:

```bash
docker compose up
```

> add a `-d` if you want containers to run in the background (detached mode), freeing your terminal.

### 3b. Production — run from pre-built images

Pull and start the latest images from GitHub Container Registry:

```bash
docker compose -f docker-compose.prod.yml up -d
```

To run a specific release by tag:

```bash
IMAGE_TAG=<tag> docker compose -f docker-compose.prod.yml up -d
```

### 4. Stop

```bash
docker compose down
```

If .env changed and the container and volume was built once already, do this for a fresh start (careful this deletes all stored data of the container):

```bash
docker-compose down -v
```

---

## 🌐 Servers

### Dev servers

| Service | URL | Notes |
|---|---|---|
| Frontend | http://localhost:3000 | React dev server (Vite) |
| Backend | http://localhost:5000 | Flask API |
| MySQL | localhost:3306 | Dev only — connect via MySQL Workbench |

> ⚠️ The MySQL port (3306) is exposed in development only. It is not available in production.

### Prod servers
| Service | URL | Notes |
|---|---|---|
| Frontend | http://localhost (:80 default port)| Served by Nginx |
| Backend | http://localhost:8000 | Gunicorn (Flask) |

---

## 🗄️ Database

The database is initialized automatically on first boot. All SQL files in `backend/db/` are executed in order.

To inspect the database, connect via **MySQL Workbench** by dev composer:

| Field | Value |
|---|---|
| Host | localhost |
| Port | 3306 |
| User | `myuser` (app user) or `root` (admin) |
| Password | `mypassword`(app user) or `secret`(admin) |

> Password and User depends on the .env variables of backend. So if there are changes there this will change
---

## 🔄 When to Rebuild

Run `docker compose up --build` when you change:

- A `Dockerfile`
- `requirements.txt` (Python dependencies)
- `package.json` (JS dependencies)

For regular code changes (`.py`, `.tsx`, etc.), volume mounts pick up changes automatically — no rebuild needed.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/health` | Health check |

> More endpoints are documented in the documentation folder as the project grows.

---

## 🧪 Testing

Via Docker (recommended):

```bash
docker compose exec backend pytest
```

Or locally with a virtual environment:

```bash
cd backend
pip install -r requirements.txt
pytest
```