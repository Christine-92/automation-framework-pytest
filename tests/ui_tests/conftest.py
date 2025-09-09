import pytest
from playwright.sync_api import sync_playwright

from src.config.settings import BASE_URL, USERNAME, PASSWORD

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def creds():
    return {"username": USERNAME, "password": PASSWORD}

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        viewport=None   # 👈 Maximizes to full available screen
    )
    page = context.new_page()
    yield page
    context.close()