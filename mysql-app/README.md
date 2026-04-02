# Job Application Tracker

Job Application Tracker is a Flask and MySQL web application for organizing a job search in one place. It supports CRUD operations for users, companies, jobs, and applications, and includes a Job Match feature that compares a user's skills against a job's required skills.

## Description

This project demonstrates a complete full-stack application using Flask, MySQL, HTML, and CSS. The system allows users to manage job search information across four related database tables, perform full CRUD operations, and calculate a job match percentage based on stored user skills and job requirements.

## Demo Video


- [`Demo video`](https://youtu.be/4im3ryqtzMc)

## Screenshots

# App Screenshots

- [1. Dashboard](#1-dashboard)
- [2. Users](#2-users)
- [3. Companies](#3-companies)
- [4. Jobs](#4-jobs)
- [5. Applications](#5-applications)
- [6. Job Match](#6-job-match)
- [7. MySQL](#7-MySQL)

---

### 1. Dashboard
![Dashboard Screenshot](https://github.com/user-attachments/assets/2dd3aefe-a5b8-4b51-90de-c21d17abb381)

### 2. Users
![Users Screenshot](https://github.com/user-attachments/assets/f1834f5c-05b9-4068-b5fe-1dac51ea46f3)

### 3. Companies
![Companies Screenshot](https://github.com/user-attachments/assets/ce374515-a2af-4376-bbe4-21a8586b5373)

### 4. Jobs
![Jobs Screenshot](https://github.com/user-attachments/assets/ba1000a3-80bf-445a-9553-544fb1bcad38)

### 5. Applications
![Applications Screenshot](https://github.com/user-attachments/assets/20b9377b-d230-4145-ba32-688d0aea48b0)

### 6. Job Match
![Job Match Screenshot](https://github.com/user-attachments/assets/cbc61cd9-a920-4f7c-a9c8-fa96863fb577)

### 7. MySQL
![MySQL](https://github.com/user-attachments/assets/34402f7f-6cb9-44b4-90d5-6da3e43d5237)

## Features

- Dashboard with quick project statistics and recent applications
- Full CRUD support for all four required database tables
- MySQL schema with foreign keys and JSON columns for skill lists
- Job Match view that calculates a percentage score for each application
- Responsive HTML/CSS interface built with Jinja templates

## How the Job Match Feature Works

The Job Match feature compares the skills saved in a user record with the required skills saved in a job record.

Here is the logic used:

1. The user's skills are stored as a list
2. The job's required skills are also stored as a list
3. Both lists are compared in lowercase so capitalization does not affect the result
4. The app counts how many required job skills appear in the user's skill list
5. The percentage is calculated with this formula:

`match percentage = (matched required skills / total required skills) * 100`

Example:

- User skills: `Python, SQL, Flask`
- Job required skills: `Python, SQL, Git, Flask`
- Matched skills: `Python, SQL, Flask`
- Missing skill: `Git`
- Match percentage: `3 / 4 = 75%`

The Job Match page also shows:

- the match percentage
- the matched skills
- the missing skills

## Project Structure

- `app.py`: main Flask application and route handlers
- `database.py`: MySQL connection logic and CRUD queries
- `schema.sql`: database creation script
- `mock_data.sql`: optional sample records for testing
- `templates/`: Jinja HTML templates
- `static/`: CSS styling
- `AI_USAGE.md`: required GenAI usage documentation
- `requirements.txt`: Python dependencies
- `.env.example`: environment variable template

## MySQL Installation on Windows

Professor Kiavash Bahreini's Windows setup guide can be followed with the video walkthrough or the written steps below.

- Video walkthrough: `https://www.youtube.com/watch?v=Owp9yRIdk5w&t=638s`
- Search for `MySQL` on Google and open the official MySQL website
- Open the `Downloads` section
- Click `MySQL Community GPL Downloads`
- Click `MySQL Installer for Windows`
- Download the smaller MSI installer that downloads the remaining installation files
- Run the installer and allow it to make changes to your device
- Choose `Full` installation
- Review the components and click `Next`
- Keep the default installation paths unless you specifically need to change them
- Click `Execute` to install MySQL Server, MySQL Shell, MySQL Workbench, and related tools

### MySQL Configuration on Windows

- Click `Next` when product configuration begins
- Choose `Development Computer`
- Keep default networking settings:
  - TCP/IP enabled
  - MySQL Port `3306`
  - X Protocol Port `33060`
  - `Open Windows Firewall ports for network access` checked
- Choose `Use Strong Password Encryption`
- Set the root password to your chosen value
- If you are following Professor Kiavash Bahreini's setup, use `root`
- Click `Execute` and then `Finish`
- Leave MySQL Router settings as default and finish setup

### MySQL Workbench Connection on Windows

- Open MySQL Workbench
- If you do not see a local connection, click the `+` button to add one
- Set:
  - Connection Name: any name you want
  - Hostname: `127.0.0.1`
  - Port: `3306`
  - Username: `root`
- Click `Store in Vault` and enter your MySQL root password
- Click `Test Connection`
- Click `OK`
- Double-click the saved connection to open it

## MySQL Installation on macOS

Professor Kiavash Bahreini's macOS setup guide can also be followed with the steps below.

- Video walkthrough: `https://www.youtube.com/watch?v=nI6xWGFBzbY`
- Open Google and search for `MySQL`
- Open the official MySQL website
- Go to `Downloads`
- Open the MySQL Community Server download page
- Select the correct macOS build:
  - `x86 64-bit` for Intel Macs
  - `arm 64-bit` for Apple Silicon Macs
- Download the DMG archive
- Run the PKG installer
- Follow the prompts and install for all users
- Set a root password during setup
- Install MySQL Workbench separately from the MySQL Workbench download page
- In Workbench, create a new connection using:
  - Hostname: `127.0.0.1`
  - Port: `3306`
  - Username: `root`
- Store the password in Keychain and test the connection

## Python Environment Setup

`requirements.txt` does not create a virtual environment by itself. It only installs Python packages into whichever Python environment is currently active. That means a new clone should first create a virtual environment, then activate it, and only then run `pip install -r requirements.txt`.

Recommended order after cloning:

1. Open a terminal in `mysql-app`
2. Create the virtual environment
3. Activate the virtual environment
4. Install packages from `requirements.txt`
5. Copy `.env.example` to `.env`
6. Fill in your database values in `.env`
7. Run `schema.sql` in MySQL Workbench
8. Optionally run `mock_data.sql`
9. Start the app with `python app.py`

### Windows PowerShell

```powershell
cd "c:\Users\Telsa\Documents\Google Alien\0 - SPRING 2026\COP 4751 Advanced Database\Course Project Job Application Tracker\mysql-app"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS Terminal

```bash
cd /path/to/mysql-app
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and replace the placeholder values with your own MySQL settings.

### Create the `.env` file

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS Terminal

```bash
cp .env.example .env
```

Example `.env` file:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
FLASK_SECRET_KEY=replace-this-secret
```

Professor Kiavash Bahreini's guide uses a common local configuration like:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=job_application_tracker
FLASK_SECRET_KEY=your-secret-key-here
```

`FLASK_SECRET_KEY` is not a MySQL value. It is just a private secret string for Flask sessions.

## Database Setup

### Create the database and tables

1. Open MySQL Workbench
2. Connect to your local MySQL instance
3. Open `schema.sql`
4. Click the lightning bolt icon to run the full file

This script creates:

- `users`
- `companies`
- `jobs`
- `applications`

### Optional sample data

If you want preloaded records for testing:

1. Open `mock_data.sql`
2. Click the lightning bolt icon to run the full file

This inserts sample rows into all four tables.

## Running the App

Before starting the app, make sure:

1. Your virtual environment has already been created
2. Your virtual environment is activated
3. `pip install -r requirements.txt` has already been run inside that environment
4. Your `.env` file exists and has the correct database values
5. Your MySQL database and tables have already been created by running `schema.sql`

If your virtual environment is not active, activate it first. Then start the app:

### Windows PowerShell

```powershell
cd "c:\Users\Telsa\Documents\Google Alien\0 - SPRING 2026\COP 4751 Advanced Database\Course Project Job Application Tracker\mysql-app"
.\.venv\Scripts\Activate.ps1
python app.py
```

### macOS Terminal

```bash
cd /path/to/mysql-app
source .venv/bin/activate
python3 app.py
```

Then open:

`http://127.0.0.1:5000`

## Quick Start for Someone Cloning the Repo

If someone clones this project and wants to run it from scratch, these are the steps:

1. Install MySQL and MySQL Workbench
2. Clone the repository
3. Open a terminal in `mysql-app`
4. Create a virtual environment with `python -m venv .venv`
5. Activate the virtual environment
6. Install dependencies with `python -m pip install -r requirements.txt`
7. Copy `.env.example` to `.env`
8. Edit `.env` with the correct MySQL host, port, username, password, and database name
9. Open MySQL Workbench and run `schema.sql`
10. Optionally run `mock_data.sql`
11. Start the app with `python app.py`
12. Open `http://127.0.0.1:5000`

## How to Confirm the App Is Connected to MySQL

Use this quick test:

1. Start the Flask app
2. Open the website
3. Go to the `Users` page
4. Create a brand new user
5. Confirm the new user appears in the webpage table
6. Open MySQL Workbench
7. Expand the `job_application_tracker` schema
8. Expand `Tables`
9. Right-click `users`
10. Click `Select Rows - Limit 1000`
11. Confirm the same new user appears in MySQL Workbench

If you delete that same user from the webpage:

1. Delete the record in the Flask app
2. In MySQL Workbench, click the refresh icon in the `SCHEMAS` panel if needed
3. In the query tab, click the lightning bolt icon to rerun the `SELECT` query, or right-click `users` and click `Select Rows - Limit 1000` again
3. Confirm the user is gone

Important note: MySQL Workbench result grids are not live. You must rerun the query or reopen the table view to see the latest database state.

## Suggested Test Flow

This is a good order for checking the whole application:

1. Open the dashboard
2. Add a new user
3. Add a new company
4. Add a new job tied to that company
5. Add a new application tied to the user and job
6. Open the `Job Match` page and confirm the percentage is displayed
7. Edit one of the records
8. Delete one of the records
9. Click the refresh icon in the `SCHEMAS` panel if needed and click the lightning bolt icon to rerun the MySQL Workbench query to confirm the database changes

## Video Requirement

The course submission requires a 3 to 7 minute recorded demo video showing the client, server, and database working together.

- Video description suggestion: `This demo shows the Job Application Tracker project using Flask, MySQL, HTML, and CSS. It demonstrates CRUD operations for users, companies, jobs, and applications, along with the Job Match feature and proof of database updates in MySQL Workbench.`
- [`Demo video`](https://youtu.be/4im3ryqtzMc)

## GenAI Note

GenAI assistance for this project was only used for README wording and optional mock data support.
