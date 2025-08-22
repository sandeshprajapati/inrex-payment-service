import sys
from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base

print("=== Database Initialization ===")

def init_db():
    """Initialize database tables"""
    try:
        # Test connection
        print("\n1. Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"Connected to: {version}")

        # Create all tables
        print("\n2. Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        print("\n3. Database initialization completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
