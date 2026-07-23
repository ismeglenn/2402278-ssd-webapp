-- Common/breached passwords, used for the server-side OWASP C7 password check.
CREATE TABLE common_passwords (
    password TEXT PRIMARY KEY
);
\copy common_passwords(password) FROM '/docker-entrypoint-initdb.d/100k-most-used-passwords-NCSC.txt'

-- Created-user log (username + creation time only, no password stored).
CREATE TABLE "2402278" (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
