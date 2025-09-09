from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page:Page):
        self.page = page

        # Locators of login page
        self.email = page.get_by_test_id("email_input")
        self.password = page.get_by_test_id("password_input")
        self.login_btn = page.get_by_test_id("submit_button")
        self.reset_submit = page.get_by_test_id("reset_submit")
        self.inline_error = page.get_by_test_id("Invalid lgoin credentalis")
       # Links (exact routes you shared)
        self.forgot = page.locator('a[href="/app/auth/reset/password"]')
        self.signup = page.locator('a[href="/app/auth/signup"]')
        self.reset_email = page.get_by_test_id("email_input")

        #positive prof after login that user is on dashboard
        self.sidebar = page.get_by_test_id("sidebar-conversations")

    def login(self, username:str, password:str):
        self.email.fill(username)
        self.password.fill(password)
        self.login_btn.click()

    def fill_creds(self, username: str, password: str):
        self.email.fill(username)
        self.password.fill(password)

    def click_login(self):
        self.login_btn.click()

    def go_to_forgot_password(self):
        self.forgot.click()

    def click_reset_submit(self):
        self.reset_submit.click()

    def go_to_sign_up(self):
        self.signup.click()
