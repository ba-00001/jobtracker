# Job Application Tracker - PostgreSQL Version

This is a PostgreSQL version of the Job Application Tracker project. It mirrors the MySQL app structure, but uses PostgreSQL for the backend database instead.

## Features

- Dashboard with quick project statistics and recent applications
- Full CRUD support for all four required database tables
- PostgreSQL schema with foreign keys and JSONB columns for skill lists
- Job Match view that calculates a percentage score for each application
- Responsive HTML/CSS interface built with Jinja templates

## Project Structure

- `app.py`: main Flask application and route handlers
- `database.py`: PostgreSQL connection logic and CRUD queries
- `schema.sql`: database creation script
- `templates/`: Jinja HTML templates
- `static/`: CSS styling
- `AI_USAGE.md`: required GenAI usage documentation
- `requirements.txt`: Python dependencies

## Setup Instructions

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Create a PostgreSQL database.
5. Set these environment variables before starting the app:

```powershell
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="job_application_tracker_pg"
$env:FLASK_SECRET_KEY="change-me"
```

6. Start the Flask server with `python app.py`.
7. Open `http://127.0.0.1:5000` in your browser.

## Demo Data

You can add users, companies, jobs, and applications manually through the interface, or load your own mock data for testing.

## Video Requirement

The course submission also requires a 3 to 7 minute recorded demo video showing the client, server, and database working together. Upload that video file to this repository before submitting.

## Note

This version is for practice and comparison. The course submission version is in `../mysql-app`.
