from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
import models


TEST_DATABASE_URL = "postgresql+psycopg://postgres:Rahul123@localhost:5432/movie_booking_test_db"

test_engine = create_engine(TEST_DATABASE_URL)

Base.metadata.create_all(bind=test_engine)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

