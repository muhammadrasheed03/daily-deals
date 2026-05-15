from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

#load variables from .env file into the environment
#this is how DATABASE_URL becomes available without hardcoding it
load_dotenv()

#get the database URL from environment variables
#if it's not set, crash immediately with a clear error
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

#the engine is the core connection to database
#it manages the connection pool - a set of reusable connections
#so i am not opening a closing a new connection on every request
engine = create_engine(
    DATABASE_URL,
    #print all SQL statements to the console - useful for learning
    #set to False in production'
    echo=True
)

#SessionLocal is a factory that creates database sessions
# a session is like a conversation with the database -
# make changes, then commit() to save them, or rollback() to undo
SessionLocal = sessionmaker(
    autocommit=False, #don't save changes automatically - i control when
    autoflush=False,  #don't send changes to DB until explicitly flush
    bind=engine       #use engine (connection) for this session
)
#Base is the parent class all my SQLAlchemy models will inherit from
# it is what connects my pyhton classes to actual database tables
Base = declarative_base()

#this is a FastAPI dependency - it creates a session for each request
#and gurantees it gets closed when the request is done
#even if an error occurs (that's what the try/finally does)
def get_db():
    db = SessionLocal() #opens a new session
    try:
        yield db        #give the session to the route that needs it
    finally:
        db.close        # always close, no matter what happens