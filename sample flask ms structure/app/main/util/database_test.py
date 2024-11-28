import logging
import traceback
from sqlalchemy import create_engine

# Import your database configuration
from ..model.database import DATABASE_URI

def test_database_connection():
    """
    Test database connection and provide detailed error information
    """
    try:
        # Attempt to create an engine and connect
        engine = create_engine(
            DATABASE_URI, 
            echo=True,  # Provides detailed connection logs
        )
        
        # Try to connect
        with engine.connect() as connection:
            print("Database connection successful!")
            return True
    
    except Exception as e:
        # Log full traceback for detailed debugging
        logging.error("Database Connection Error:")
        logging.error(traceback.format_exc())
        
        # More specific error messages
        if "Authentication failed" in str(e):
            print("MySQL Authentication Failed. Check username/password.")
        elif "Unknown database" in str(e):
            print("Database does not exist. Please create it first.")
        elif "Connection refused" in str(e):
            print("MySQL server not running or not accessible.")
        
        return False

# You can call this function during app initialization
if __name__ == '__main__':
    test_database_connection()