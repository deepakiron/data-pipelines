-- Create the db_pipelines database
CREATE DATABASE db_pipelines;

-- Create users
CREATE USER readonly_user WITH PASSWORD 'readonly_password';
CREATE USER editor_user WITH PASSWORD 'editor_password';

-- Grant privileges to readonly_user (read-only)
GRANT CONNECT ON DATABASE db_pipelines TO readonly_user;

\c db_pipelines  -- Switch to the airflow1 database

GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- Grant privileges to editor_user (read-write)
GRANT CONNECT ON DATABASE db_pipelines TO editor_user;

GRANT USAGE ON SCHEMA public TO editor_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO editor_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO editor_user;

\c airflow

GRANT CONNECT ON DATABASE db_pipelines TO editor_user;

GRANT USAGE ON SCHEMA public TO editor_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO editor_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT ON TABLES TO editor_user;
