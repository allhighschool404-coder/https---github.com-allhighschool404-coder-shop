# All Converter

Flask-based file conversion and photo editing web application.

## Render deployment

Deploy this repository as a **Render Web Service**, not a Static Site.

- Runtime: Python 3
- Build command: `pip install --upgrade pip && pip install -r requirements.txt`
- Start command: `gunicorn App:app --workers 1 --threads 8 --timeout 300 --bind 0.0.0.0:$PORT`
- Health check: `/`

Set these environment variables in Render:

- `ADMIN_USER`: admin username
- `ADMIN_PASSWORD`: strong admin password

MS Word/Excel COM conversion is available only on Windows and is not supported on Render Linux. The app retains native Python fallbacks.
