import os
os.environ.setdefault("DATABASE_URL", "sqlite://")
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# fail early: better a clear error now than a weird one later
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")
# sqlite only allows one thread by default, but FastAPI uses several
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)
# nothing is saved until commit() is called
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# one session per request, always closed at the end (even on error)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
