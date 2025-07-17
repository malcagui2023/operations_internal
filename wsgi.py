#!/usr/bin/env python3
import sys
import os

# Add your project directory to the sys.path if needed
# sys.path.insert(0, "/home/YOUR_USERNAME/public_html/paschoalotto/")

from app import app  # Import your Flask app instance

# Expose as 'application' for Gunicorn
application = app

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
