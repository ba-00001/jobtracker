import json
import os
from collections import Counter
from contextlib import contextmanager
from typing import Any, Iterable

import psycopg


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "job_application_tracker"),
}


@contextmanager
def get_connection():
    connection = psycopg.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dbname=DB_CONFIG["database"],
        row_factory=psycopg.rows.dict_row,
    )
    try:
        yield connection
    finally:
        connection.close()


def deserialize_row(row: dict[str, Any]) -> dict[str, Any]:
    parsed = dict(row)
    for key in ("skills", "required_skills"):
        if key in parsed and parsed[key]:
            parsed[key] = json.loads(parsed[key]) if isinstance(parsed[key], str) else parsed[key]
        elif key in parsed:
            parsed[key] = []
    return parsed


def fetch_all(query: str, params: Iterable[Any] | None = None) -> list[dict[str, Any]]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        cursor.close()
    return [deserialize_row(row) for row in rows]


def fetch_one(query: str, params: Iterable[Any] | None = None) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        cursor.close()
    return deserialize_row(row) if row else None


def execute_query(query: str, params: Iterable[Any] | None = None) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        row = cursor.fetchone() if cursor.description else None
        cursor.close()
    return row["id"] if row and "id" in row else 0


def get_all_users() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM users ORDER BY created_at DESC, user_id DESC")


def get_user(user_id: int) -> dict[str, Any] | None:
    return fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))


def create_user(data: dict[str, Any]) -> int:
    return execute_query(
        """
        INSERT INTO users (full_name, email, phone, location, skills, experience_level)
        VALUES (%s, %s, %s, %s, %s::jsonb, %s)
        RETURNING user_id AS id
        """,
        (
            data["full_name"],
            data["email"],
            data["phone"],
            data["location"],
            json.dumps(data["skills"]),
            data["experience_level"],
        ),
    )


def update_user(user_id: int, data: dict[str, Any]) -> None:
    execute_query(
        """
        UPDATE users
        SET full_name = %s, email = %s, phone = %s, location = %s, skills = %s, experience_level = %s
        WHERE user_id = %s
        """,
        (
            data["full_name"],
            data["email"],
            data["phone"],
            data["location"],
            json.dumps(data["skills"]),
            data["experience_level"],
            user_id,
        ),
    )


def delete_user(user_id: int) -> None:
    execute_query("DELETE FROM users WHERE user_id = %s", (user_id,))


def get_all_companies() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM companies ORDER BY created_at DESC, company_id DESC")


def get_company(company_id: int) -> dict[str, Any] | None:
    return fetch_one("SELECT * FROM companies WHERE company_id = %s", (company_id,))


def create_company(data: dict[str, Any]) -> int:
    return execute_query(
        """
        INSERT INTO companies (name, industry, location, website, recruiter_name, recruiter_email, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING company_id AS id
        """,
        (
            data["name"],
            data["industry"],
            data["location"],
            data["website"],
            data["recruiter_name"],
            data["recruiter_email"],
            data["notes"],
        ),
    )


def update_company(company_id: int, data: dict[str, Any]) -> None:
    execute_query(
        """
        UPDATE companies
        SET name = %s, industry = %s, location = %s, website = %s,
            recruiter_name = %s, recruiter_email = %s, notes = %s
        WHERE company_id = %s
        """,
        (
            data["name"],
            data["industry"],
            data["location"],
            data["website"],
            data["recruiter_name"],
            data["recruiter_email"],
            data["notes"],
            company_id,
        ),
    )


def delete_company(company_id: int) -> None:
    execute_query("DELETE FROM companies WHERE company_id = %s", (company_id,))


def get_all_jobs() -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies ON companies.company_id = jobs.company_id
        ORDER BY jobs.posted_date DESC, jobs.job_id DESC
        """
    )


def get_job(job_id: int) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies ON companies.company_id = jobs.company_id
        WHERE jobs.job_id = %s
        """,
        (job_id,),
    )


def create_job(data: dict[str, Any]) -> int:
    return execute_query(
        """
        INSERT INTO jobs (
            company_id, title, location, employment_type, salary_min, salary_max,
            status, required_skills, description, posted_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)
        RETURNING job_id AS id
        """,
        (
            data["company_id"],
            data["title"],
            data["location"],
            data["employment_type"],
            data["salary_min"],
            data["salary_max"],
            data["status"],
            json.dumps(data["required_skills"]),
            data["description"],
            data["posted_date"],
        ),
    )


def update_job(job_id: int, data: dict[str, Any]) -> None:
    execute_query(
        """
        UPDATE jobs
        SET company_id = %s, title = %s, location = %s, employment_type = %s,
            salary_min = %s, salary_max = %s, status = %s, required_skills = %s,
            description = %s, posted_date = %s
        WHERE job_id = %s
        """,
        (
            data["company_id"],
            data["title"],
            data["location"],
            data["employment_type"],
            data["salary_min"],
            data["salary_max"],
            data["status"],
            json.dumps(data["required_skills"]),
            data["description"],
            data["posted_date"],
            job_id,
        ),
    )


def delete_job(job_id: int) -> None:
    execute_query("DELETE FROM jobs WHERE job_id = %s", (job_id,))


def get_all_applications() -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT applications.*, users.full_name, jobs.title AS job_title, companies.name AS company_name
        FROM applications
        JOIN users ON users.user_id = applications.user_id
        JOIN jobs ON jobs.job_id = applications.job_id
        JOIN companies ON companies.company_id = jobs.company_id
        ORDER BY applications.applied_date DESC, applications.application_id DESC
        """
    )


def get_application(application_id: int) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT applications.*, users.full_name, jobs.title AS job_title, companies.name AS company_name
        FROM applications
        JOIN users ON users.user_id = applications.user_id
        JOIN jobs ON jobs.job_id = applications.job_id
        JOIN companies ON companies.company_id = jobs.company_id
        WHERE applications.application_id = %s
        """,
        (application_id,),
    )


def create_application(data: dict[str, Any]) -> int:
    return execute_query(
        """
        INSERT INTO applications (
            user_id, job_id, applied_date, stage, source, resume_version,
            cover_letter_sent, notes, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING application_id AS id
        """,
        (
            data["user_id"],
            data["job_id"],
            data["applied_date"],
            data["stage"],
            data["source"],
            data["resume_version"],
            data["cover_letter_sent"],
            data["notes"],
            data["status"],
        ),
    )


def update_application(application_id: int, data: dict[str, Any]) -> None:
    execute_query(
        """
        UPDATE applications
        SET user_id = %s, job_id = %s, applied_date = %s, stage = %s, source = %s,
            resume_version = %s, cover_letter_sent = %s, notes = %s, status = %s
        WHERE application_id = %s
        """,
        (
            data["user_id"],
            data["job_id"],
            data["applied_date"],
            data["stage"],
            data["source"],
            data["resume_version"],
            data["cover_letter_sent"],
            data["notes"],
            data["status"],
            application_id,
        ),
    )


def delete_application(application_id: int) -> None:
    execute_query("DELETE FROM applications WHERE application_id = %s", (application_id,))


def get_user_options() -> list[dict[str, Any]]:
    return fetch_all("SELECT user_id, full_name FROM users ORDER BY full_name")


def get_company_options() -> list[dict[str, Any]]:
    return fetch_all("SELECT company_id, name FROM companies ORDER BY name")


def get_job_options() -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT jobs.job_id, jobs.title, companies.name AS company_name
        FROM jobs
        JOIN companies ON companies.company_id = jobs.company_id
        ORDER BY companies.name, jobs.title
        """
    )


def compute_match(skills: list[str], required_skills: list[str]) -> int:
    if not required_skills:
        return 0
    normalized_user = {skill.lower() for skill in skills}
    normalized_required = {skill.lower() for skill in required_skills}
    overlap = normalized_user.intersection(normalized_required)
    return round((len(overlap) / len(normalized_required)) * 100)


def get_job_matches() -> list[dict[str, Any]]:
    rows = fetch_all(
        """
        SELECT applications.application_id, applications.stage, applications.status,
               users.full_name, users.skills, jobs.title AS job_title,
               jobs.required_skills, companies.name AS company_name
        FROM applications
        JOIN users ON users.user_id = applications.user_id
        JOIN jobs ON jobs.job_id = applications.job_id
        JOIN companies ON companies.company_id = jobs.company_id
        ORDER BY applications.application_id DESC
        """
    )

    matches = []
    for row in rows:
        user_skills = row.get("skills", [])
        required_skills = row.get("required_skills", [])
        normalized_user = {skill.lower() for skill in user_skills}
        matched_skills = sorted(skill for skill in required_skills if skill.lower() in normalized_user)
        missing_skills = sorted(skill for skill in required_skills if skill.lower() not in normalized_user)
        matches.append(
            {
                **row,
                "match_percentage": compute_match(user_skills, required_skills),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            }
        )
    return matches


def get_dashboard_summary() -> dict[str, Any]:
    applications = get_all_applications()
    jobs = get_all_jobs()
    users = get_all_users()
    companies = get_all_companies()
    matches = get_job_matches()
    stage_counts = Counter(application["stage"] for application in applications)
    average_match = round(sum(item["match_percentage"] for item in matches) / len(matches), 1) if matches else 0

    return {
        "total_users": len(users),
        "total_companies": len(companies),
        "total_jobs": len(jobs),
        "total_applications": len(applications),
        "recent_applications": applications[:5],
        "stage_counts": dict(stage_counts),
        "average_match": average_match,
        "match_results": matches[:5],
    }
