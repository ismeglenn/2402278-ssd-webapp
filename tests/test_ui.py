"""Browser-driven UI tests over HTTP against the running webapp."""
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE = os.environ.get("BASE_URL", "http://localhost:8000")
SELENIUM_REMOTE_URL = os.environ.get("SELENIUM_REMOTE_URL")


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    if SELENIUM_REMOTE_URL:
        return webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=opts)
    return webdriver.Chrome(options=opts)


def test_home_page_has_login_form():
    driver = make_driver()
    try:
        driver.get(BASE + "/")
        assert driver.find_element(By.NAME, "username")
        assert driver.find_element(By.NAME, "password")
    finally:
        driver.quit()


def test_signup_with_strong_password_reaches_welcome_page():
    driver = make_driver()
    try:
        driver.get(BASE + "/signup")
        driver.find_element(By.NAME, "username").send_keys("ui_dave")
        driver.find_element(By.NAME, "password").send_keys("Trqm4-Zxpl92-Bv")
        driver.find_element(By.TAG_NAME, "button").click()
        assert "Welcome, ui_dave" in driver.page_source
    finally:
        driver.quit()


def test_frontend_blocks_submission_for_short_password():
    driver = make_driver()
    try:
        driver.get(BASE + "/signup")
        driver.find_element(By.NAME, "username").send_keys("ui_eve")
        driver.find_element(By.NAME, "password").send_keys("short")
        driver.find_element(By.TAG_NAME, "button").click()
        assert driver.current_url.endswith("/signup")
    finally:
        driver.quit()
