# 📚 Online Library — Backend API

A RESTful backend API for an online library system, built with Flask. Supports book management with JWT-based authentication and structured layered architecture.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flask 2.3 |
| Database | MySQL (via PyMySQL) |
| Validation | Marshmallow |
| Authentication | Flask-JWT-Extended |
| Password Hashing | bcrypt |
| Environment Config | python-dotenv |
| CORS | Flask-Cors |
| Testing | pytest |

---

## 📁 Project Structure

```
online-library/
├── run.py                  # Entry point — creates and runs the app
├── requirements.txt
├── .env                    # Environment variables (not committed) #TODO: WIP
└── backend/
    └── app/
        ├── __init__.py     # App factory (create_app)
        ├── config.py       # Config loaded from .env TODO: env not integrated yet
        ├── extensions.py   # Flask extensions + DB connection
        ├── routes/
        │   ├── __init__.py
        │   └── books.py    # Book endpoints
        ├── services/
        │   ├── __init__.py
        │   └── book_service.py  # Business logic
        ├── repositories/
        │   ├── __init__.py
        │   └── book_repo.py     # Raw SQL queries
        ├── schemas/
        │   ├── __init__.py
        │   └── book_schema.py   # Marshmallow schemas
        └── utils/
            ├── __init__.py
            └── errors.py        # Custom error classes
```

---

## ⚙️ Architecture

This project follows a **3-layer architecture** to separate concerns:

```
Request → Route → Service → Repository → Database
```

| Layer | Responsibility |
|---|---|
| **Routes** (`routes/`) | Handle HTTP requests and responses |
| **Services** (`services/`) | Business logic, validation rules |
| **Repositories** (`repositories/`) | Database queries (raw SQL) |
| **Schemas** (`schemas/`) | Input validation and output serialization |
| **Utils** (`utils/`) | Shared helpers (error classes, decorators) |

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10+
- MySQL server running locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/online-library.git
cd online-library
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **PowerShell:** `venv\Scripts\Activate.ps1`
- **CMD:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment variables
// THIS IS WORK IN PROGRESS
// TODO
Create a `.env` file at the project root:

```env
JWT_SECRET_KEY=your-long-random-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=onlineLibrary
FLASK_DEBUG=true
```

### 5. Set up the database
// TODO STILL
Create the MySQL database and tables:

```sql
CREATE DATABASE onlineLibrary;

USE onlineLibrary;

CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);
```

### 6. Run the server

```bash
python backend/run.py
```

The API will be available at `http://127.0.0.1:5000`.

---

## 📡 API Endpoints
// THIS IS INCOMPLETE, FOR NOW JUST AN EXAMPLE
### Books

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/books/` | Get all books | No |
| `POST` | `/books/` | Add a new book | No |

---

### `GET /books/`

Returns a list of all books.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "title": "The Great Gatsby",
    "author_id": 2
  }
]
```

---

### `POST /books/`

Creates a new book.

**Request Body:**
```json
{
  "title": "The Great Gatsby",
  "author_id": 2
}
```

| Field | Type | Required |
|---|---|---|
| `title` | string | ✅ Yes |
| `author_id` | integer | ❌ No |

**Response `201 Created`:**
```json
{
  "message": "Book added"
}
```

**Response `422 Unprocessable Entity`** (validation error):
```json
{
  "error": "ValidationError",
  "message": "title: Missing data for required field."
}
```

---

## 🔐 Authentication
// TODO: NOT IMPLEMENTED YET
Authentication is handled via **JWT (JSON Web Tokens)** using `Flask-JWT-Extended`.

> Auth-protected endpoints are not yet implemented on books. JWT is configured and ready for use on future routes (e.g. user login, protected mutations).

To authenticate, include the token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

---

## ❌ Error Handling
// TODO: TEST ERRORS
All errors are returned in a consistent format via a global error handler:

```json
{
  "error": "ErrorClassName",
  "message": "Human-readable message"
}
```

| Status Code | Meaning |
|---|---|
| `400` | Bad request / validation error |
| `401` | Unauthorized |
| `404` | Resource not found |
| `500` | Internal server error |

---

## 🧪 Testing
// NO TESTS ARE DONE YET
```bash
pytest
```

Tests are located in the `tests/` directory.

---

## 📝 Notes

- Raw SQL is used intentionally instead of an ORM (e.g. SQLAlchemy) for learning purposes.
- A new database connection is opened per request — connection pooling should be added before production use.
- Never commit your `.env` file. Add it to `.gitignore`.