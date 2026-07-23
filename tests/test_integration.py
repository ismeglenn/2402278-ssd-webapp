"""Integration tests against the running webapp + db containers."""
import os

import requests

BASE = os.environ.get("BASE_URL", "http://localhost:8000")
STRONG_PASSWORD = "Zq7-Trvmn82-Lk"


def test_home_page_loads():
    r = requests.get(BASE + "/")
    assert r.status_code == 200
    assert "Login" in r.text


def test_signup_rejects_common_password():
    r = requests.post(
        BASE + "/signup",
        data={"username": "ci_alice", "password": "123456789012"},
        allow_redirects=False,
    )
    assert r.status_code == 302
    assert r.headers["Location"].startswith("/?error")


def test_signup_accepts_strong_password_and_reaches_welcome():
    r = requests.post(
        BASE + "/signup",
        data={"username": "ci_bob", "password": STRONG_PASSWORD},
    )
    assert r.status_code == 200
    assert "Welcome, ci_bob" in r.text
    assert STRONG_PASSWORD in r.text


def test_login_rejects_unknown_user():
    r = requests.post(
        BASE + "/login",
        data={"username": "ci_no_such_user", "password": STRONG_PASSWORD},
        allow_redirects=False,
    )
    assert r.status_code == 302


def test_login_accepts_existing_user():
    # depends on test_signup_accepts_strong_password_and_reaches_welcome having run first
    r = requests.post(
        BASE + "/login",
        data={"username": "ci_bob", "password": STRONG_PASSWORD},
    )
    assert "Welcome, ci_bob" in r.text
