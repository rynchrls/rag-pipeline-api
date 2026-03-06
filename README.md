# RAG Pipeline API

> **Create your own AI Agent/Assistant without coding.**

A FastAPI-based Retrieval-Augmented Generation (RAG) backend with support for multiple LLM providers (Ollama, OpenAI, Gemini), PostgreSQL persistence, ChromaDB vector storage, and real-time Socket.IO communication.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Makefile Commands](#makefile-commands)
- [Scripts](#scripts)
- [API Routes](#api-routes)
- [Project Structure](#project-structure)

---

## Prerequisites

Install the following tools before getting started:

| Tool                    | Version | Purpose                   | Download                                                                                        |
| ----------------------- | ------- | ------------------------- | ----------------------------------------------------------------------------------------------- |
| **Python**              | 3.12+   | Runtime                   | [python.org](https://www.python.org/downloads/)                                                 |
| **uv**                  | latest  | Dependency & venv manager | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)                    |
| **PostgreSQL**          | 14+     | Primary database          | [postgresql.org](https://www.postgresql.org/download/)                                          |
| **Ollama** _(optional)_ | latest  | Local LLM inference       | [ollama.com](https://ollama.com/)                                                               |
| **make** _(optional)_   | any     | Run Makefile commands     | [GnuWin32](https://gnuwin32.sourceforge.net/packages/make.htm) / pre-installed on macOS & Linux |

> **Windows users:** `make` is not installed by default. You can install it via [Chocolatey](https://chocolatey.org/) (`choco install make`), use the `scripts/run.ps1` PowerShell script instead, or run the underlying commands manually.

---

## Environment Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd api
```

### 2. Create the virtual environment and install dependencies

This project uses **uv** for fast dependency management.

```bash
# Install uv (if not already installed)
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Create venv and install all dependencies
uv sync
```

### 3. Activate the virtual environment

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 4. Configure environment variables

Copy `.env` and fill in your values:

```bash
cp .env .env.local   # optional — .env is loaded by default
```

Edit `.env`:

```env
# Server
HOST=127.0.0.1
PORT=5000
DEBUG=True

# PostgreSQL
DATABASE_URI=postgresql://<user>:<password>@localhost:5432/rag_pipeline

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300000

# Ollama (local or cloud)
OLLAMA_HOST=http://localhost:11434
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL=deepseek-v3.1:671b-cloud

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

> You only need to fill in the API keys for the LLM provider(s) you plan to use.

---

## Database Setup

Make sure PostgreSQL is running and the database exists:

```sql
CREATE DATABASE rag_pipeline;
```

### Apply migrations

```bash
# Using make
make upgrade

# Or manually
alembic upgrade head
```

### Create a new migration (after model changes)

```bash
# Using make
make migration

# Or manually
alembic revision --autogenerate -m "describe your change"
```

---

## Running the Server

### Option A — Makefile

```bash
make run
```

### Option B — PowerShell Script (Windows)

```powershell
# Make sure your venv is activated first
.\scripts\run.ps1
```

### Option C — Manually

```bash
uvicorn app.main:app --host localhost --port 5000 --reload
```

The API will be available at:

| URL                           | Description                   |
| ----------------------------- | ----------------------------- |
| `http://localhost:5000`       | API root                      |
| `http://localhost:5000/docs`  | Swagger UI (interactive docs) |
| `http://localhost:5000/redoc` | ReDoc documentation           |

---

## Makefile Commands

| Command          | Description                                  |
| ---------------- | -------------------------------------------- |
| `make run`       | Start the development server with hot-reload |
| `make migration` | Auto-generate a new Alembic migration        |
| `make upgrade`   | Apply all pending migrations to the database |

---

## Scripts

| Script            | Platform             | Description                                           |
| ----------------- | -------------------- | ----------------------------------------------------- |
| `scripts/run.ps1` | Windows (PowerShell) | Start the dev server (ensure venv is activated first) |

---

## API Routes

All routes are prefixed with `/api/v1`.

| Method   | Endpoint                     | Description                           |
| -------- | ---------------------------- | ------------------------------------- |
| `GET`    | `/`                          | Health check                          |
| `POST`   | `/api/v1/users`              | Register user                         |
| `GET`    | `/api/v1/users`              | Get users                             |
| `POST`   | `/api/v1/pipelines`          | Create pipeline                       |
| `GET`    | `/api/v1/pipelines/all`      | Get all pipelines                     |
| `POST`   | `/api/v1/messages`           | Send message (streaming RAG response) |
| `GET`    | `/api/v1/messages/all`       | Get all messages                      |
| `POST`   | `/api/v1/conversations`      | Create conversation                   |
| `GET`    | `/api/v1/conversations`      | Get conversation with messages        |
| `GET`    | `/api/v1/conversations/all`  | Get all conversations                 |
| `DELETE` | `/api/v1/conversations/{id}` | Delete conversation                   |

> Full interactive documentation is available at `/docs` when the server is running.

Real-time events are handled via **Socket.IO** mounted at the root (`/`).

---

## Project Structure

```
api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment settings (pydantic-settings)
│   ├── db/                  # Database session & table creation
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── rag/                 # RAG pipeline logic
│   │   ├── embedding/       # Query embedding
│   │   ├── vector_search/   # ChromaDB vector similarity search
│   │   ├── augmentation/    # Prompt augmentation
│   │   └── generate/        # LLM response generation (Ollama/OpenAI/Gemini)
│   ├── v1/
│   │   ├── routers/         # FastAPI route definitions
│   │   ├── controller/      # Request handling layer
│   │   ├── service/         # Business logic layer
│   │   └── repository/      # Database access layer
│   └── utils/               # Helpers (pagination, JWT, message builder, etc.)
├── migrations/              # Alembic migration files
├── scripts/
│   └── run.ps1              # PowerShell dev server launcher
├── Makefile                 # Common dev commands
├── pyproject.toml           # Project dependencies (managed by uv)
├── alembic.ini              # Alembic configuration
└── .env                     # Environment variables (do not commit)
```
