"""
Main entry point for the backend application.
This file serves as the entry point when running the backend as an executable.
"""

import uvicorn

from backend.api import app


def main():
    # Run the uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
