"""
Main entry point for the backend application.
This file serves as the entry point when running the backend as an executable.
"""
import uvicorn
from backend.api import app
from backend.scheduler import start_scheduler

def main():
    """Main function to start the backend server and scheduler."""
    # Start the scheduler
    start_scheduler()

    # Run the uvicorn server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
