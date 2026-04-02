import os
from datetime import date, datetime
from typing import Any

from flask import Flask, flash, redirect, render_template, request, url_for

import database


"""mysql-app/app.py
Flask web application for the Job Application Tracker.
Defines routes, request handling, form parsing, and page rendering for users, companies, jobs, applications, and matches.
"""

# This file handles the Flask side of the project.
# I kept the routes grouped by feature so each page is easier to find and explain.
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "job-tracker-dev-secret")

STAGE_OPTIONS = [
    "Wishlist",
    "Applied",
    "Phone Screen",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
]
JOB_STATUS_OPTIONS = ["Open", "Paused", "Closed"]
EXPERIENCE_LEVELS = ["Intern", "Entry", "Mid", "Senior", "Lead"]
EMPLOYMENT_TYPES = ["Internship", "Part-time", "Contract", "Full-time", "Hybrid", "Remote"]


def normalize_skills(raw_value: str) -> list[str]:
    # I store skills as a simple comma-separated input in the forms,
    # then split them into a clean list before sending them to the database layer.
    return [skill.strip() for skill in raw_value.split(",") if skill.strip()]


def parse_date(value: str | None):
    # Dates come in from the HTML form as strings, so I convert them here once.
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_int(value: str | None):
    # Empty number inputs should stay empty instead of crashing the app.
    if value in (None, ""):
        return None
    return int(value)


def parse_bool(value: str | None) -> bool:
    # Checkboxes submit "on" when checked, so I convert that into True/False here.
    return value == "on"


def serialize_form_values(form: dict[str, Any]) -> dict[str, Any]:
    # When validation fails, this keeps the form filled in with readable text
    # instead of raw Python lists or missing checkbox values.
    serialized = dict(form)
    if isinstance(serialized.get("skills"), list):
        serialized["skills"] = ", ".join(serialized["skills"])
    if isinstance(serialized.get("required_skills"), list):
        serialized["required_skills"] = ", ".join(serialized["required_skills"])
    serialized["cover_letter_sent"] = bool(serialized.get("cover_letter_sent"))
    return serialized


@app.context_processor
def inject_today() -> dict[str, Any]:
    # This lets me use today's date in templates without repeating the same logic in each route.
    return {"today": date.today()}


@app.route("/")
def dashboard():
    # The dashboard pulls together the summary data I want to show on the home page.
    return render_template("dashboard.html", summary=database.get_dashboard_summary())


@app.route("/users")
def users():
    # This page shows the user list and the create form on the same screen.
    return render_template("users.html", users=database.get_all_users(), form_data={}, experience_levels=EXPERIENCE_LEVELS)


@app.post("/users/create")
def create_user():
    # I build a clean dictionary first so validation and saving use the same values.
    form_data = {
        "full_name": request.form.get("full_name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "location": request.form.get("location", "").strip(),
        "skills": normalize_skills(request.form.get("skills", "")),
        "experience_level": request.form.get("experience_level", "").strip(),
    }
    if not form_data["full_name"] or not form_data["email"]:
        flash("Full name and email are required for each user.", "error")
        return render_template("users.html", users=database.get_all_users(), form_data=serialize_form_values(form_data), experience_levels=EXPERIENCE_LEVELS), 400

    # After validation passes, I send the cleaned form data to the database helper.
    database.create_user(form_data)
    flash("User profile created.", "success")
    return redirect(url_for("users"))


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id: int):
    # Edit routes use GET to load the form and POST to save the changes.
    user = database.get_user(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("users"))

    if request.method == "POST":
        form_data = {
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "location": request.form.get("location", "").strip(),
            "skills": normalize_skills(request.form.get("skills", "")),
            "experience_level": request.form.get("experience_level", "").strip(),
        }
        if not form_data["full_name"] or not form_data["email"]:
            flash("Full name and email are required for each user.", "error")
            return render_template("user_form.html", form_data=serialize_form_values(form_data), experience_levels=EXPERIENCE_LEVELS), 400

        # Update uses the same cleaned values, but sends the current user id too.
        database.update_user(user_id, form_data)
        flash("User profile updated.", "success")
        return redirect(url_for("users"))

    return render_template("user_form.html", form_data=user, experience_levels=EXPERIENCE_LEVELS)


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id: int):
    """Delete an existing user and redirect back to the users page."""
    database.delete_user(user_id)
    flash("User deleted.", "success")
    return redirect(url_for("users"))


@app.route("/companies")
def companies():
    # Same layout idea as users: table on one side, create form on the other.
    return render_template("companies.html", companies=database.get_all_companies(), form_data={})


@app.post("/companies/create")
def create_company():
    form_data = {
        "name": request.form.get("name", "").strip(),
        "industry": request.form.get("industry", "").strip(),
        "location": request.form.get("location", "").strip(),
        "website": request.form.get("website", "").strip(),
        "recruiter_name": request.form.get("recruiter_name", "").strip(),
        "recruiter_email": request.form.get("recruiter_email", "").strip(),
        "notes": request.form.get("notes", "").strip(),
    }
    if not form_data["name"]:
        flash("Company name is required.", "error")
        return render_template("companies.html", companies=database.get_all_companies(), form_data=form_data), 400

    # Company records are simpler, so I can save the form data directly after validation.
    database.create_company(form_data)
    flash("Company created.", "success")
    return redirect(url_for("companies"))


@app.route("/companies/<int:company_id>/edit", methods=["GET", "POST"])
def edit_company(company_id: int):
    """Load and save the edit form for a single company record."""
    company = database.get_company(company_id)
    if not company:
        flash("Company not found.", "error")
        return redirect(url_for("companies"))

    if request.method == "POST":
        form_data = {
            "name": request.form.get("name", "").strip(),
            "industry": request.form.get("industry", "").strip(),
            "location": request.form.get("location", "").strip(),
            "website": request.form.get("website", "").strip(),
            "recruiter_name": request.form.get("recruiter_name", "").strip(),
            "recruiter_email": request.form.get("recruiter_email", "").strip(),
            "notes": request.form.get("notes", "").strip(),
        }
        if not form_data["name"]:
            flash("Company name is required.", "error")
            return render_template("company_form.html", form_data=form_data), 400

        database.update_company(company_id, form_data)
        flash("Company updated.", "success")
        return redirect(url_for("companies"))

    return render_template("company_form.html", form_data=company)


@app.post("/companies/<int:company_id>/delete")
def delete_company(company_id: int):
    """Delete a company record and return to the companies page."""
    database.delete_company(company_id)
    flash("Company deleted.", "success")
    return redirect(url_for("companies"))


@app.route("/jobs")
def jobs():
    # Jobs need company data too because each job belongs to a company.
    return render_template(
        "jobs.html",
        jobs=database.get_all_jobs(),
        companies=database.get_company_options(),
        form_data={},
        job_status_options=JOB_STATUS_OPTIONS,
        employment_types=EMPLOYMENT_TYPES,
    )


@app.post("/jobs/create")
def create_job():
    form_data = {
        "company_id": request.form.get("company_id", "").strip(),
        "title": request.form.get("title", "").strip(),
        "location": request.form.get("location", "").strip(),
        "employment_type": request.form.get("employment_type", "").strip(),
        "salary_min": request.form.get("salary_min", "").strip(),
        "salary_max": request.form.get("salary_max", "").strip(),
        "status": request.form.get("status", "").strip(),
        "required_skills": normalize_skills(request.form.get("required_skills", "")),
        "description": request.form.get("description", "").strip(),
        "posted_date": request.form.get("posted_date", "").strip(),
    }
    if not form_data["company_id"] or not form_data["title"]:
        flash("Company and job title are required.", "error")
        return render_template(
            "jobs.html",
            jobs=database.get_all_jobs(),
            companies=database.get_company_options(),
            form_data=serialize_form_values(form_data),
            job_status_options=JOB_STATUS_OPTIONS,
            employment_types=EMPLOYMENT_TYPES,
        ), 400

    # I convert the raw form strings into the types the database expects before saving.
    payload = {
        "company_id": int(form_data["company_id"]),
        "title": form_data["title"],
        "location": form_data["location"],
        "employment_type": form_data["employment_type"],
        "salary_min": parse_int(form_data["salary_min"]),
        "salary_max": parse_int(form_data["salary_max"]),
        "status": form_data["status"] or "Open",
        "required_skills": form_data["required_skills"],
        "description": form_data["description"],
        "posted_date": parse_date(form_data["posted_date"]),
    }
    database.create_job(payload)
    flash("Job posting created.", "success")
    return redirect(url_for("jobs"))


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id: int):
    """Load and save the edit form for a single job posting."""
    job = database.get_job(job_id)
    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs"))

    if request.method == "POST":
        form_data = {
            "company_id": request.form.get("company_id", "").strip(),
            "title": request.form.get("title", "").strip(),
            "location": request.form.get("location", "").strip(),
            "employment_type": request.form.get("employment_type", "").strip(),
            "salary_min": request.form.get("salary_min", "").strip(),
            "salary_max": request.form.get("salary_max", "").strip(),
            "status": request.form.get("status", "").strip(),
            "required_skills": normalize_skills(request.form.get("required_skills", "")),
            "description": request.form.get("description", "").strip(),
            "posted_date": request.form.get("posted_date", "").strip(),
        }
        if not form_data["company_id"] or not form_data["title"]:
            flash("Company and job title are required.", "error")
            return render_template(
                "job_form.html",
                companies=database.get_company_options(),
                form_data=serialize_form_values(form_data),
                job_status_options=JOB_STATUS_OPTIONS,
                employment_types=EMPLOYMENT_TYPES,
            ), 400

        payload = {
            "company_id": int(form_data["company_id"]),
            "title": form_data["title"],
            "location": form_data["location"],
            "employment_type": form_data["employment_type"],
            "salary_min": parse_int(form_data["salary_min"]),
            "salary_max": parse_int(form_data["salary_max"]),
            "status": form_data["status"] or "Open",
            "required_skills": form_data["required_skills"],
            "description": form_data["description"],
            "posted_date": parse_date(form_data["posted_date"]),
        }
        # Jobs are saved as a separate payload because some fields need type conversion first.
        database.update_job(job_id, payload)
        flash("Job posting updated.", "success")
        return redirect(url_for("jobs"))

    return render_template(
        "job_form.html",
        companies=database.get_company_options(),
        form_data=job,
        job_status_options=JOB_STATUS_OPTIONS,
        employment_types=EMPLOYMENT_TYPES,
    )


@app.post("/jobs/<int:job_id>/delete")
def delete_job(job_id: int):
    """Delete a job posting and redirect to the jobs list."""
    database.delete_job(job_id)
    flash("Job deleted.", "success")
    return redirect(url_for("jobs"))


@app.route("/applications")
def applications():
    # Applications connect users and jobs, so this page needs both dropdown lists ready.
    return render_template(
        "applications.html",
        applications=database.get_all_applications(),
        users=database.get_user_options(),
        jobs=database.get_job_options(),
        form_data={},
        stage_options=STAGE_OPTIONS,
    )


@app.post("/applications/create")
def create_application():
    form_data = {
        "user_id": request.form.get("user_id", "").strip(),
        "job_id": request.form.get("job_id", "").strip(),
        "applied_date": request.form.get("applied_date", "").strip(),
        "stage": request.form.get("stage", "").strip(),
        "source": request.form.get("source", "").strip(),
        "resume_version": request.form.get("resume_version", "").strip(),
        "cover_letter_sent": request.form.get("cover_letter_sent"),
        "notes": request.form.get("notes", "").strip(),
        "status": request.form.get("status", "").strip(),
    }
    if not form_data["user_id"] or not form_data["job_id"]:
        flash("User and job are required for each application.", "error")
        return render_template(
            "applications.html",
            applications=database.get_all_applications(),
            users=database.get_user_options(),
            jobs=database.get_job_options(),
            form_data=serialize_form_values(form_data),
            stage_options=STAGE_OPTIONS,
        ), 400

    # The form sends everything as text, so I clean up dates, ids, and checkbox values here.
    payload = {
        "user_id": int(form_data["user_id"]),
        "job_id": int(form_data["job_id"]),
        "applied_date": parse_date(form_data["applied_date"]),
        "stage": form_data["stage"] or "Applied",
        "source": form_data["source"],
        "resume_version": form_data["resume_version"],
        "cover_letter_sent": parse_bool(form_data["cover_letter_sent"]),
        "notes": form_data["notes"],
        "status": form_data["status"] or form_data["stage"] or "Applied",
    }
    # Once the user and job ids are cleaned up, this creates the linked application record.
    database.create_application(payload)
    flash("Application created.", "success")
    return redirect(url_for("applications"))


@app.route("/applications/<int:application_id>/edit", methods=["GET", "POST"])
def edit_application(application_id: int):
    """Load and save the edit form for an application record."""
    application = database.get_application(application_id)
    if not application:
        flash("Application not found.", "error")
        return redirect(url_for("applications"))

    if request.method == "POST":
        form_data = {
            "user_id": request.form.get("user_id", "").strip(),
            "job_id": request.form.get("job_id", "").strip(),
            "applied_date": request.form.get("applied_date", "").strip(),
            "stage": request.form.get("stage", "").strip(),
            "source": request.form.get("source", "").strip(),
            "resume_version": request.form.get("resume_version", "").strip(),
            "cover_letter_sent": request.form.get("cover_letter_sent"),
            "notes": request.form.get("notes", "").strip(),
            "status": request.form.get("status", "").strip(),
        }
        if not form_data["user_id"] or not form_data["job_id"]:
            flash("User and job are required for each application.", "error")
            return render_template(
                "application_form.html",
                users=database.get_user_options(),
                jobs=database.get_job_options(),
                form_data=serialize_form_values(form_data),
                stage_options=STAGE_OPTIONS,
            ), 400

        payload = {
            "user_id": int(form_data["user_id"]),
            "job_id": int(form_data["job_id"]),
            "applied_date": parse_date(form_data["applied_date"]),
            "stage": form_data["stage"] or "Applied",
            "source": form_data["source"],
            "resume_version": form_data["resume_version"],
            "cover_letter_sent": parse_bool(form_data["cover_letter_sent"]),
            "notes": form_data["notes"],
            "status": form_data["status"] or form_data["stage"] or "Applied",
        }
        # This keeps the application stage and notes easy to update from the edit page.
        database.update_application(application_id, payload)
        flash("Application updated.", "success")
        return redirect(url_for("applications"))

    return render_template(
        "application_form.html",
        users=database.get_user_options(),
        jobs=database.get_job_options(),
        form_data=application,
        stage_options=STAGE_OPTIONS,
    )


@app.post("/applications/<int:application_id>/delete")
def delete_application(application_id: int):
    """Delete an application record and redirect to the applications page."""
    database.delete_application(application_id)
    flash("Application deleted.", "success")
    return redirect(url_for("applications"))


@app.route("/matches")
def matches():
    # This page just focuses on the job match feature and the percentage results.
    return render_template("matches.html", matches=database.get_job_matches())


if __name__ == "__main__":
    app.run(debug=True)
