import re
import pytest
from playwright.sync_api import expect
from ui_pages.login_page import LoginPage

PATH = "/app/login"
FORGOT_PATH = "/app/auth/reset/password"
SIGNUP_PATH = "/app/auth/signup"
INVALID_CREDS_TEXT = "Invalid login credentials. Please try again."
RESET_GENERIC_TEXT = "If an account with this email exists, you will receive password reset instructions."
INVALID_EMAIL = "invalidemail"
INVALID_PASSWORD = "invalidpassword"

def test_login_success_to_dashboard(page, base_url, creds):
    page.goto(f"{base_url}{PATH}")
    lp = LoginPage(page)
    lp.login(creds["username"], creds["password"])

    # Assertions
    expect(lp.sidebar).to_be_visible()
    expect(page).not_to_have_url(re.compile(r"/app/login$"))

def test_login_shows_error_on_incorrect_credentials(page, base_url, creds):
    page.goto(f"{base_url}{PATH}")
    lp = LoginPage(page)

    lp.login(creds["username"], INVALID_PASSWORD)

    expect(page).to_have_url(re.compile(r"/app/login$"))
    expect(page.get_by_text(INVALID_CREDS_TEXT)).to_be_visible()


def test_login_invalid_email_disables_submit(page, base_url):
    page.goto(f"{base_url}{PATH}")
    lp = LoginPage(page)
    lp.fill_creds(INVALID_EMAIL,INVALID_PASSWORD)

    page.keyboard.press("Tab")  # trigger client-side validation


    expect(lp.login_btn).to_be_disabled()


def test_nav_forgot_password_opens_reset(page, base_url, creds):
    page.goto(f"{base_url}{PATH}")
    lp = LoginPage(page)
    lp.go_to_forgot_password()
    expect(page).to_have_url(re.compile(re.escape(FORGOT_PATH) + r"$"))

    expect(lp.reset_email).to_be_visible()

    expect(lp.reset_submit).to_be_disabled()
    lp.fill_creds(creds["username"],None)
    expect(lp.reset_submit().to_be_enabled())
    lp.click_reset_submit()

    expect(page.get_by_text(re.compile(re.escape(RESET_GENERIC_TEXT)))).to_be_visible()

def test_nav_signup_opens_signup(page, base_url):
    page.goto(f"{base_url}{PATH}")
    lp = LoginPage(page)

    lp.go_to_sign_up()
    expect(page).to_have_url(re.compile(re.escape(SIGNUP_PATH) + r"$"))
