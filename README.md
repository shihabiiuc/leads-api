# Leads API

A simple REST API for managing sales leads, built with **FastAPI** and **PostgreSQL**. It supports full CRUD operations (create, read, update, delete) with automatic request validation, API key authentication and interactive API documentation.

**Live demo:** [leads-api-rfbr.onrender.com/docs](https://leads-api-rfbr.onrender.com/docs)

> **Note:** The demo runs on Render's free tier, which sleeps after a period of inactivity. The first request may take a little while to respond while the service wakes up.

## Features

- Create, list, view, update and delete leads
- API key authentication for write endpoints (`POST`, `PUT`, `DELETE`)
- Request validation with Pydantic (including email format checks)
- Proper HTTP status codes (`201` on create, `401` for an invalid API key, `404` when a lead doesn't exist)
- Parameterized SQL queries to prevent SQL injection
- Automatic transaction handling (commit on success, rollback on error)
- Interactive API docs generated automatically by FastAPI
- Environment-based configuration with `.env`
- Deployed on Render with a managed PostgreSQL database

## Tech Stack

- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [psycopg 3](https://www.psycopg.org/psycopg3/)
- [Pydantic](https://docs.pydantic.dev/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [uv](https://docs.astral.sh/uv/) for package and environment management
- [Render](https://render.com/) for hosting the API and database

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A PostgreSQL database (local, or hosted on a service such as Render)
- `psql` command-line client (or a GUI tool such as pgAdmin or DBeaver)

### 1. Clone the repository

```bash
git clone https://github.com/shihabiiuc/leads-api.git
cd leads-api
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Create the table

Connect to your PostgreSQL database with `psql` (or a GUI tool) and run:

```sql
CREATE TABLE leads (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100),
  budget INTEGER
);
```

### 4. Configure environment variables

Create a `.env` file in the project root with your database connection URL and an API key of your choice:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
API_KEY=your-secret-api-key
```

To generate a strong random key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

> **Note:** Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Run the development server

```bash
uv run fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI generates interactive documentation automatically:

- **Swagger UI:** `/docs` ([live](https://leads-api-rfbr.onrender.com/docs) · [local](http://127.0.0.1:8000/docs))
- **ReDoc:** `/redoc` ([live](https://leads-api-rfbr.onrender.com/redoc) · [local](http://127.0.0.1:8000/redoc))

## Endpoints

| Method   | Endpoint           | Description             | Auth |
| -------- | ------------------ | ----------------------- | ---- |
| `GET`    | `/`                | Health check            | No   |
| `GET`    | `/leads`           | List all leads          | No   |
| `GET`    | `/leads/{lead_id}` | Get a single lead       | No   |
| `POST`   | `/leads`           | Create a new lead       | Yes  |
| `PUT`    | `/leads/{lead_id}` | Update an existing lead | Yes  |
| `DELETE` | `/leads/{lead_id}` | Delete a lead           | Yes  |

## Authentication

Endpoints marked **Auth** require an `X-API-Key` header containing the API key set in your environment. Requests with a missing or invalid key are rejected.

In the interactive docs at `/docs`, click the **Authorize** button and enter your key to test protected endpoints.

### Example: Create a lead

**Request**

```bash
curl -X POST http://127.0.0.1:8000/leads \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
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

## Deployment

The live demo is deployed on [Render](https://render.com/) as a Web Service connected to a Render PostgreSQL database in the same region.

| Setting       | Value                                                      |
| ------------- | ---------------------------------------------------------- |
| Build command | `pip install uv && uv sync --frozen`                       |
| Start command | `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`      |
| Environment   | `DATABASE_URL` (the database's Internal URL) and `API_KEY` |

Every push to the `main` branch triggers an automatic redeploy.

## Project Structure

```
leads-api/
├── main.py            # FastAPI app and routes
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Locked dependency versions
├── .python-version    # Python version used by uv
├── .env               # Local environment variables (not committed)
├── .gitignore
└── README.md
```

## Roadmap

- [x] Deploy to a cloud platform
- [x] Protect write endpoints (`POST`, `PUT`, `DELETE`) with API key authentication
- [ ] Add pagination and filtering to `GET /leads`
- [ ] Add an AI-powered endpoint that extracts lead details from free-text inquiries

## Author

**Shihab** — Freelance Web Developer

- GitHub: [@shihabiiuc](https://github.com/shihabiiuc)
- Website: [shihabiiuc.com](https://shihabiiuc.com)
- LinkedIn: [shihabiiuc](https://www.linkedin.com/in/shihabiiuc)
