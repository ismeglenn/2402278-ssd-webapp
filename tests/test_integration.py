"""Integration tests against the running webapp + db containers."""
import os
import re

import requests

BASE = os.environ.get("BASE_URL", "http://localhost:8000")
STRONG_PASSWORD = "Zq7-Trvmn82-Lk"


def get_csrf_token(session, path):
    """Forms are CSRF-protected, so fetch the page's token before posting to it."""
    r = session.get(BASE + path)
    return re.search(r'name="csrf_token" value="([^"]+)"', r.text).group(1)


def test_home_page_loads():
    r = requests.get(BASE + "/")
    assert r.status_code == 200
    assert "Login" in r.text


def test_signup_rejects_common_password():
    session = requests.Session()
    token = get_csrf_token(session, "/signup")
    r = session.post(
        BASE + "/signup",
        data={"username": "ci_alice", "password": "123456789012", "csrf_token": token},
        allow_redirects=False,
    )
    assert r.status_code == 302
    assert r.headers["Location"].startswith("/?error")


def test_signup_accepts_strong_password_and_reaches_welcome():
    session = requests.Session()
    token = get_csrf_token(session, "/signup")
    r = session.post(
        BASE + "/signup",
        data={"username": "ci_bob", "password": STRONG_PASSWORD, "csrf_token": token},
    )
    assert r.status_code == 200
    assert "Welcome, ci_bob" in r.text
    assert STRONG_PASSWORD in r.text


def test_login_rejects_unknown_user():
    session = requests.Session()
    token = get_csrf_token(session, "/")
    r = session.post(
        BASE + "/login",
        data={"username": "ci_no_such_user", "password": STRONG_PASSWORD, "csrf_token": token},
        allow_redirects=False,
    )
    assert r.status_code == 302


def test_login_accepts_existing_user():
    # depends on test_signup_accepts_strong_password_and_reaches_welcome having run first
    session = requests.Session()
    token = get_csrf_token(session, "/")
    r = session.post(
        BASE + "/login",
        data={"username": "ci_bob", "password": STRONG_PASSWORD, "csrf_token": token},
    )
    assert "Welcome, ci_bob" in r.text
