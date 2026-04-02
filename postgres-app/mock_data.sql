INSERT INTO users (full_name, email, phone, location, skills, experience_level) VALUES
('Avery Johnson', 'avery@example.com', '555-0101', 'Orlando, FL', '["Python", "SQL", "Flask", "Git"]'::jsonb, 'Entry'),
('Jordan Lee', 'jordan@example.com', '555-0102', 'Tampa, FL', '["Java", "PostgreSQL", "HTML", "CSS"]'::jsonb, 'Intern');

INSERT INTO companies (name, industry, location, website, recruiter_name, recruiter_email, notes) VALUES
('Sunrise Analytics', 'Data Analytics', 'Miami, FL', 'https://example.com', 'Dana Perez', 'dana@example.com', 'Interested in entry-level analysts'),
('Cloud Harbor Tech', 'Software', 'Remote', 'https://example.org', 'Chris Patel', 'chris@example.org', 'Strong onboarding program');

INSERT INTO jobs (company_id, title, location, employment_type, salary_min, salary_max, status, required_skills, description, posted_date) VALUES
(1, 'Data Analyst Intern', 'Miami, FL', 'Internship', 18000, 24000, 'Open', '["SQL", "Excel", "Python"]'::jsonb, 'Support reporting and dashboard work.', '2026-03-20'),
(2, 'Junior Backend Developer', 'Remote', 'Full-time', 60000, 72000, 'Open', '["Python", "Flask", "PostgreSQL", "Git"]'::jsonb, 'Build and maintain web APIs.', '2026-03-24');

INSERT INTO applications (user_id, job_id, applied_date, stage, source, resume_version, cover_letter_sent, notes, status) VALUES
(1, 2, '2026-03-25', 'Interview', 'LinkedIn', 'v3', TRUE, 'Technical interview scheduled.', 'Interview'),
(2, 1, '2026-03-26', 'Applied', 'Handshake', 'v1', FALSE, 'Waiting for recruiter response.', 'Applied');
