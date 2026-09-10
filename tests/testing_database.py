from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
import models
from dotenv import load_dotenv

import os
load_dotenv()


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
test_engine = create_engine(TEST_DATABASE_URL)

Base.metadata.create_all(bind=test_engine)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

