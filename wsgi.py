import sys
import os

# 1. Add the project root to the PYTHONPATH (so imports work)
project_home = os.path.dirname(__file__)
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2. Import your Flask app and expose it as "application"
from app import app
application = app