# Leads API

A simple REST API for managing sales leads, built with **FastAPI** and **MySQL**. It supports full CRUD operations (create, read, update, delete) with automatic request validation and interactive API documentation.

## Features

- Create, list, view, update and delete leads
- Request validation with Pydantic (including email format checks)
- Proper HTTP status codes (`201` on create, `404` when a lead doesn't exist)
- Parameterized SQL queries to prevent SQL injection
- Interactive API docs generated automatically by FastAPI
- Environment-based configuration with `.env`

## Tech Stack

- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyMySQL](https://github.com/PyMySQL/PyMySQL)
- [Pydantic](https://docs.pydantic.dev/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [uv](https://docs.astral.sh/uv/) for package and environment management
- MySQL / MariaDB

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running MySQL or MariaDB server (for example, via XAMPP)

### 1. Clone the repository

```bash
git clone https://github.com/shihabiiuc/leads-api.git
cd leads-api
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create the database

Run the following SQL in phpMyAdmin or the MySQL command line:

```sql
CREATE DATABASE leads_db;
USE leads_db;

CREATE TABLE leads (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  budget INT
);
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=leads_db
```

> **Note:** Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the development server

```bash
uv run fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI generates interactive documentation automatically:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Endpoints

| Method   | Endpoint           | Description             |
| -------- | ------------------ | ----------------------- |
| `GET`    | `/`                | Health check            |
| `GET`    | `/leads`           | List all leads          |
| `GET`    | `/leads/{lead_id}` | Get a single lead       |
| `POST`   | `/leads`           | Create a new lead       |
| `PUT`    | `/leads/{lead_id}` | Update an existing lead |
| `DELETE` | `/leads/{lead_id}` | Delete a lead           |

### Example: Create a lead

**Request**

```bash
curl -X POST http://127.0.0.1:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"name": "Rahim", "email": "rahim@example.com", "budget": 500}'
```

**Response** (`201 Created`)

```json
{
  "id": 1,
  "name": "Rahim",
  "email": "rahim@example.com",
  "budget": 500
}
```

### Lead fields

| Field    | Type    | Required | Notes                 |
| -------- | ------- | -------- | --------------------- |
| `name`   | string  | Yes      |                       |
| `email`  | string  | No       | Must be a valid email |
| `budget` | integer | Yes      |                       |

## Project Structure

```
leads-api/
├── main.py           # FastAPI app and routes
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Locked dependency versions
├── .env              # Local environment variables (not committed)
├── .gitignore
└── README.md
```

## Roadmap

- [ ] Deploy to a cloud platform
- [ ] Add pagination and filtering to `GET /leads`
- [ ] Add an AI-powered endpoint that extracts lead details from free-text inquiries

## Author

**Shihab** — Freelance Web Developer

- GitHub: [@shihabiiuc](https://github.com/shihabiiuc)
- Website: [shihabiiuc.com](https://shihabiiuc.com)
- LinkedIn: [shihabiiuc](https://www.linkedin.com/in/shihabiiuc)
