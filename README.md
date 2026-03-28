# 📚 Online Library

A full-stack web application for browsing and managing an online library. Users can track reading progress, bookmark favourites, and leave reviews. Admins can manage content and moderate reviews.

---

## 🏗️ Architecture

Three-tier architecture with each tier running in its own Docker container:

```
React (Frontend)  →  Flask (Backend)  →  MySQL (Database)
   :3000                 :5000               :3306
```

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
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   └── ...
└── backend/
    ├── Dockerfile
    ├── run.py
    ├── requirements.txt
    ├── db/
    │   ├── init.sql        ← runs automatically on first boot
    │   └── connection.py
    └── app/
        ├── __init__.py     ← app factory
        ├── ...
```
> More about project structure of backend and frontend in the documentation folder
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
git clone https://github.com/your-username/online-library.git
cd online-library
```

### 2. Configure environment variables
==== THIS IS STILL NOT DONE, NO .env IN PROJECT STILL (WIP) ====
Create a `.env` file at the project root:

```env
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=online_library
JWT_SECRET_KEY=your-long-random-secret-key
```

### 3. Build and run

First time or after dependency changes:

```bash
docker-compose up --build
```

After that:

```bash
docker-compose up -d
```

> `-d` runs containers in the background (detached mode), freeing your terminal.

### 4. Stop

```bash
docker-compose down
```

---

## 🌐 Servers

| Service | URL | Notes |
|---|---|---|
| Frontend | http://localhost:3000 | React dev server |
| Backend | http://localhost:5000 | Flask API |
| MySQL | localhost:3306 | Dev only — open in MySQL Workbench |

> ⚠️ The MySQL port (3306) is exposed for development only. It will not be available in production.

---

## 🗄️ Database

The database is initialized automatically on first boot using `backend/db/init.sql`.

To inspect the database, connect via **MySQL Workbench**:

| Field | Value |
|---|---|
| Host | localhost |
| Port | 3306 |
| User | root |
| Password | *(your `.env` value)* |

> ⚠️ Default password is `example` — change this before any deployment. (THIS WILL BE CHANGED - WIP)
> ⚠️ Make sure ports `3000`, `5000`, and `3306` are free

---

## 🔄 When to Rebuild

Run `docker-compose up --build` when you change:

- A `Dockerfile`
- `requirements.txt` (Python dependencies)
- `package.json` (JS dependencies)

For regular code changes (`.py`, `.tsx`, etc.), the volume mounts pick up changes automatically — no rebuild needed.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API info |
| GET | `/health` | Health check |

> More endpoints are to be documented in the documentation folder as the project grows.

---

## 🧪 Testing

```bash
cd backend
pytest
```
