# 🎬 Movie Booking REST API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy\&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA81E)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic\&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker\&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?logo=pytest\&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen)

</div>

A backend **Movie Booking REST API** built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker, and Pytest**.

The application models the core workflow of a movie-ticket booking platform, including **authentication, role-based access, movie and theatre management, screen and automatic seat generation, show scheduling, seat availability, booking, and cancellation**.

The project focuses on **API design, database integrity, business-rule validation, transaction safety, automated testing, and containerized development/testing**.

---

## 🚀 Key Features

### 🔐 Authentication & Authorization

* User registration
* JWT-based authentication
* OAuth2 password login
* Authenticated-user endpoint
* Admin/User role-based authorization
* Protected admin endpoints
* Invalid-token and invalid-credential handling

### 🎬 Movie & Theatre Management

* Movie CRUD operations
* Theatre CRUD operations
* Case-insensitive duplicate validation
* Resource existence validation
* Protection against deleting resources with dependent records

### 🎟️ Screens & Seats

* Screen management
* Screen-to-theatre relationship
* Automatic seat generation
* Configurable rows and seats per row
* Seat validation
* Prevention of duplicate screen names within a theatre

Example:

```text
Rows = 3
Seats per Row = 4

A1  A2  A3  A4
B1  B2  B3  B4
C1  C2  C3  C4
```

### 🕐 Show Scheduling

* Show creation and management
* Automatic end-time calculation from movie duration
* Overlap detection on the same screen
* Back-to-back shows supported
* Simultaneous shows on different screens supported
* Seat availability endpoint
* Protection against deleting shows with bookings

### 🎫 Booking System

* Multiple-seat booking
* Seat-to-screen validation
* Duplicate seat selection validation
* Double-booking prevention
* Automatic total amount calculation
* Booking history and details
* Booking cancellation
* Seat release after cancellation
* Preserved cancelled-booking history
* Transaction-safe booking creation

---

# 🎯 Booking Workflow

```text
Register / Login
       │
       ▼
   Browse Movies
       │
       ▼
   Select Movie
       │
       ▼
    View Shows
       │
       ▼
   Select Show
       │
       ▼
 View Seat Availability
       │
       ▼
    Select Seats
       │
       ▼
   Book Tickets
       │
       ▼
 Booking History
       │
       ▼
  Cancel Booking
       │
       ▼
   Seats Released
```

---

# 🧠 Engineering Highlights

This project goes beyond basic CRUD by implementing several real backend concerns.

### JWT Authentication & RBAC

JWT access tokens protect authenticated endpoints, with separate authorization rules for **administrators and regular users**.

```text
Admin
 ├── Movies
 ├── Theaters
 ├── Screens
 └── Shows

User
 └── Bookings
```

### Automatic Seat Generation

Creating a screen automatically generates its seats based on the configured number of rows and seats per row.

### Show Conflict Detection

Shows on the same screen cannot overlap.

```text
09:30 ───────── 12:30
             │
             └── next show at 12:30 → ✅ allowed

11:30 ───────── 14:30
     overlaps → ❌ rejected
```

### Seat Integrity

Before creating a booking, the API verifies that selected seats:

* Exist
* Belong to the show's screen
* Have not already been booked
* Are not duplicated in the request

A database-level uniqueness constraint also protects against duplicate seat bookings for the same show.

### Booking Cancellation

Cancelling a booking:

```text
Booking
   │
   ├── status → Cancelled
   │
   └── BookingSeat records removed
                 │
                 ▼
            Seats released
```

The booking record remains available as historical information while the seats become available for future bookings.

### Transaction Safety

Booking creation is handled within a database transaction.

If booking creation fails:

```text
Create Booking
      │
      ├── Create BookingSeat records
      │
      └── Error
           │
           ▼
        ROLLBACK
```

This prevents partially created booking data.

---

# 🗄️ Database Design

The application uses **PostgreSQL** with **SQLAlchemy ORM**.

Core entities:

```text
User
 │
 └── Booking
       │
       └── BookingSeat
              │
              └── Seat
                    │
                    └── Screen
                          │
                          └── Theater

Movie
 │
 └── Show
       │
       └── Screen
```

### Data Integrity

The database uses constraints and relationships to enforce:

* Unique user emails
* Unique theatre names
* Unique screen names within a theatre
* Unique seat numbers within a screen
* Unique seat booking per show
* Foreign-key relationships

---

# 🧪 Automated Testing

The project includes a comprehensive **Pytest** test suite covering API behavior and business rules.

### Test Results

```text
175 tests
175 passed
0 failed
99% coverage
```

Tests cover:

* Authentication
* Authorization
* User registration
* Movies
* Theatres
* Screens
* Automatic seat generation
* Shows
* Show overlap and boundary conditions
* Seat availability
* Bookings
* Double-booking prevention
* Booking cancellation and seat reuse
* Validation errors
* Missing resources
* Duplicate resources
* Business-rule failures
* Database relationships
* Edge cases

### Test Isolation

Tests use:

* Pytest fixtures
* FastAPI dependency overrides
* Transaction rollback
* Parametrized tests
* Dedicated PostgreSQL test database
* Pytest markers
* Coverage reporting

The application database and test database are completely separate.

```text
Application
    │
    ▼
db:5432
movie_booking_docker


Pytest
    │
    ▼
test_db:5432
movie_booking_docker_test_db
```

---

# 🏷️ Test Markers

Tests are grouped by API module:

```text
users
auth
movies
theaters
screens
shows
bookings
```

Run the complete suite:

```bash
docker compose exec api pytest
```

Run with coverage:

```bash
docker compose exec api pytest --cov=. --cov-report=term-missing
```

Run a specific group:

```bash
docker compose exec api pytest -m auth
```

```bash
docker compose exec api pytest -m bookings
```

---

# 🐳 Dockerized Environment

The application and testing environment runs through **Docker Compose**.

```text
                    Docker Compose
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
       API             App DB           Test DB
    FastAPI +        PostgreSQL        PostgreSQL
      Pytest
          │
          └──────────────► Test DB
```

### Services

| Service   | Purpose                                 |
| --------- | --------------------------------------- |
| `api`     | FastAPI application + Pytest            |
| `db`      | Application PostgreSQL database         |
| `test_db` | Dedicated PostgreSQL database for tests |

This separation prevents automated tests from using the application's database.

---

# ⚙️ Tech Stack

| Technology         | Purpose                     |
| ------------------ | --------------------------- |
| **Python 3.13**    | Programming language        |
| **FastAPI**        | REST API framework          |
| **PostgreSQL 17**  | Relational database         |
| **SQLAlchemy 2.0** | ORM                         |
| **Pydantic v2**    | Request/response validation |
| **Alembic**        | Database migrations         |
| **JWT**            | Authentication              |
| **Pytest**         | Automated testing           |
| **pytest-cov**     | Test coverage               |
| **Docker Compose** | Containerized environment   |
| **Uvicorn**        | ASGI server                 |

---

# 📁 Project Structure

```text
MOVIE_BOOKING_API/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── routes/
│   ├── auth.py
│   ├── bookings.py
│   ├── movies.py
│   ├── screens.py
│   ├── shows.py
│   ├── theatres.py
│   └── users.py
│
├── tests/
│   ├── conftest.py
│   ├── testing_database.py
│   ├── test_auth.py
│   ├── test_bookings.py
│   ├── test_movies.py
│   ├── test_screens.py
│   ├── test_shows.py
│   ├── test_theaters.py
│   └── test_users.py
│
├── database.py
├── models.py
├── schemas.py
├── utils.py
├── main.py
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pytest.ini
├── requirements.txt
├── .env.example
├── test.env.example
├── .gitignore
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

* Docker Desktop
* Git

The application and test databases run inside Docker, so a local PostgreSQL installation is not required for the Docker workflow.

---

## 1. Clone the repository

```bash
git clone https://github.com/rahulpiska/MOVIE_BOOKING_API.git
cd MOVIE_BOOKING_API
```

---

## 2. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@db:5432/movie_booking_docker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Never commit real passwords, secret keys, or other sensitive credentials.**

---

## 3. Build and start the application

```bash
docker compose build
```

```bash
docker compose up -d
```

Check the services:

```bash
docker compose ps
```

---

## 4. Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

Check migration status:

```bash
docker compose exec api alembic current
```

Verify that the database schema matches the SQLAlchemy models:

```bash
docker compose exec api alembic check
```

---

## 5. Run the API

API:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## 6. Run Tests

Run all tests:

```bash
docker compose exec api pytest
```

Run with coverage:

```bash
docker compose exec api pytest --cov=. --cov-report=term-missing
```

Run a specific test group:

```bash
docker compose exec api pytest -m auth
```

---

# 📌 API Overview

| Resource           | Operations                                                |
| ------------------ | --------------------------------------------------------- |
| **Users**          | Register                                                  |
| **Authentication** | Login, current user                                       |
| **Movies**         | Create, list, retrieve, update, delete, movie shows       |
| **Theaters**       | Create, list, retrieve, update, delete                    |
| **Screens**        | Create, list, retrieve, update, delete                    |
| **Shows**          | Create, list, retrieve, update, delete, seat availability |
| **Bookings**       | Create, list, retrieve, cancel                            |

Interactive API documentation is available through **Swagger UI** at `/docs`.

---

# 🔄 Development Workflow

```text
Modify Code
    │
    ▼
Run Pytest
    │
    ▼
Check Coverage
    │
    ▼
Check Alembic
    │
    ▼
Create Migration if Required
    │
    ▼
Review Changes
    │
    ▼
Commit
    │
    ▼
Push
```

Useful commands:

```bash
git status
git add .
git commit -m "describe change"
git push
```

---

# 📊 Project Highlights

```text
REST API            → FastAPI
Database            → PostgreSQL 17
ORM                 → SQLAlchemy 2.0
Validation          → Pydantic v2
Authentication      → JWT
Migrations          → Alembic
Testing             → Pytest
Test Coverage       → 99%
Automated Tests     → 175
Containerization    → Docker Compose
Test Database       → Dedicated PostgreSQL container
```

### What this project demonstrates

* REST API development with FastAPI
* Relational database design
* SQLAlchemy ORM
* JWT authentication
* Role-based authorization
* Data validation
* Database constraints
* Transaction management
* Alembic migrations
* Dependency injection
* FastAPI dependency overrides
* Test isolation
* Parametrized testing
* Business-rule testing
* Dockerized development and testing
* Git/GitHub workflow

---

# 👨‍💻 Author

**Rahul Piska**

GitHub:
https://github.com/rahulpiska
