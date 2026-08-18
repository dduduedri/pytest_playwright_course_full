from playwright.sync_api import Page

from ui.elements.button import Button
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class LoginPage(BasePage):

    def login(self, user_name, user_password):
        # my_page.locator("//input[@id='userEmail']").fill(user_name) #->xpath
        TextBox(self.page.locator("//input[@id='userEmail']"), "Fill User Name").fill(user_name)

        # my_page.locator("//input[@id='userPassword']").fill(user_password)
        TextBox(self.page.locator("//input[@id='userPassword']"), "Fill User Name").fill(user_password)

        # my_page.get_by_role("button",name="Login").click()
        Button(self.page.get_by_role("button", name="Login"), "click Login").click()

    def login_goto(self):
        self.page.goto("https://rahulshettyacademy.com/client/")
