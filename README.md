# 🎬 Movie Booking REST API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy)

![Alembic](https://img.shields.io/badge/Alembic-Migrations-green)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063)

![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![REST API](https://img.shields.io/badge/API-REST-blueviolet)


</div>

A production-style **Movie Booking REST API** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

This project simulates the core workflow of an online movie ticket booking platform such as **BookMyShow** by implementing authentication, movie management, theatre management, show scheduling, automatic seat generation, real-time seat availability, and ticket booking.

---

## 🚀 Features

### Authentication
- User Registration
- JWT Authentication
- Login
- Current Logged-in User (`/auth/me`)
- Role-based Authorization (Admin / User)

### Movies
- Create Movie (Admin)
- View All Movies
- View Movie by ID
- Update Movie (Admin)
- Delete Movie (Admin)
- View Shows for a Movie

### Theaters
- Create Theater
- View Theaters
- Update Theater
- Delete Theater

### Screens
- Create Screen
- Automatic Seat Generation
- View Screens
- Update Screen
- Delete Screen

### Shows
- Create Show
- Automatic End Time Calculation
- Show Overlap Validation
- View Shows
- View Show by ID
- View Seat Availability
- Update Show
- Delete Show

### Bookings
- Book Multiple Seats
- Real-time Seat Availability Check
- Prevent Double Booking
- Booking History
- Booking Details
- Cancel Booking
- Transaction-safe Booking Creation

---

# 🎯 Booking Workflow

```text
Register/Login
        │
        ▼
Browse Movies
        │
        ▼
Select Movie
        │
        ▼
View Available Shows
        │
        ▼
Choose Show
        │
        ▼
View Available Seats
        │
        ▼
Select Seats
        │
        ▼
Book Tickets
        │
        ▼
View Booking History
        │
        ▼
Cancel Booking
```

---

# 🏗 Database Design

The project uses a normalized relational database.

```text
User
 │
 └──────────────┐
                │
             Booking
                │
        ┌───────┴────────┐
        │                │
       Show        BookingSeat
        │                │
        │               Seat
        │
      Screen
        │
     Theater

Movie
  │
  └────────────► Show
```

---

# ⚙️ Business Logic Implemented

This project focuses on solving real backend problems instead of only CRUD operations.

### ✅ JWT Authentication

Secure authentication using access tokens.

---

### ✅ Role-based Authorization

Only administrators can:

- Create Movies
- Update Movies
- Delete Movies
- Manage Theaters
- Manage Screens
- Manage Shows

Regular users can only perform booking-related operations.

---

### ✅ Automatic Seat Generation

When a new screen is created, seats are automatically generated.

Example:

```
Rows : 5
Seats per Row : 5
```

Generated seats:

```
A1 A2 A3 A4 A5
B1 B2 B3 B4 B5
C1 C2 C3 C4 C5
D1 D2 D3 D4 D5
E1 E2 E3 E4 E5
```

---

### ✅ Show Overlap Validation

A screen cannot have two overlapping shows.

Example:

```
Movie A
9:00 AM - 11:30 AM

Movie B
10:30 AM - 1:00 PM

❌ Rejected
```

---

### ✅ Automatic End Time Calculation

Only the show start time is provided.

End time is calculated automatically using:

```
Movie Duration
+
Show Start Time
=
Show End Time
```

---

### ✅ Seat Availability

Before booking, the system checks:

- Seat belongs to the selected screen
- Seat exists
- Seat has not already been booked for the selected show

---

### ✅ Prevent Double Booking

The same seat cannot be booked twice for the same show.

---

### ✅ Transaction-safe Booking

Booking creation uses database transactions.

If any step fails:

- Booking is rolled back
- Seat records are rolled back

ensuring database consistency.

---

# 🛠 Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic v2
- Passlib (bcrypt)
- Python-Jose (JWT)
- Uvicorn

---

# 📁 Project Structure

```
MOVIE_BOOKING_API
│
├── alembic/
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
├── database.py
├── models.py
├── schemas.py
├── utils.py
├── main.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🔐 Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost/movie_booking_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# ⚡ Installation

Clone the repository

```bash
git clone https://github.com/rahulpiska/MOVIE_BOOKING_API.git
```

Move into the project

```bash
cd MOVIE_BOOKING_API
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 Database Migration

Run migrations

```bash
alembic upgrade head
```

---

# ▶️ Run Server

```bash
uvicorn main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 📌 API Overview

## Users

- POST `/users`

---

## Authentication

- POST `/auth/login`
- GET `/auth/me`

---

## Movies

- POST `/movies`
- GET `/movies`
- GET `/movies/{id}`
- GET `/movies/{movie_id}/shows`
- PUT `/movies/{id}`
- DELETE `/movies/{id}`

---

## Theaters

- POST `/theaters`
- GET `/theaters`
- GET `/theaters/{id}`
- PUT `/theaters/{id}`
- DELETE `/theaters/{id}`

---

## Screens

- POST `/screens`
- GET `/screens`
- GET `/screens/{id}`
- PUT `/screens/{id}`
- DELETE `/screens/{id}`

---

## Shows

- POST `/shows`
- GET `/shows`
- GET `/shows/{id}`
- GET `/shows/{show_id}/seats`
- PUT `/shows/{id}`
- DELETE `/shows/{id}`

---

## Bookings

- POST `/bookings`
- GET `/bookings`
- GET `/bookings/{id}`
- PATCH `/bookings/{id}/cancel`

---

# 📚 Future Improvements

- Docker
- Pytest
- Pagination
- Logging
- CI/CD
- Redis Caching
- Background Tasks
- Payment Gateway Integration

---

# 👨‍💻 Author

**Rahul Piska**

GitHub:
https://github.com/rahulpiska
