"""Migration script to add name column to user table."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Remove the query parameters for connection string manipulation
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgresql+psycopg2://"):
    # For PostgreSQL, we need to connect directly and add the column
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Check if the name column already exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'user' AND column_name = 'name'
        """))

        if result.fetchone() is None:
            # Add the name column to the user table
            conn.execute(text("ALTER TABLE \"user\" ADD COLUMN name VARCHAR(255)"))
            conn.commit()
            print("Added 'name' column to 'user' table")
        else:
            print("'name' column already exists in 'user' table")
else:
    print("This migration is for PostgreSQL. For SQLite, the schema would need to be handled differently.")