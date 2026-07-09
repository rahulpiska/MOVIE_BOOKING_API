from fastapi import FastAPI

from routes import users,auth, movies, theatres, screens, shows,bookings

app = FastAPI(
    title = "Movie Booking API"
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(theatres.router)
app.include_router(screens.router)
app.include_router(shows.router)
app.include_router(bookings.router)