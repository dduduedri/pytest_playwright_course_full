from playwright.sync_api import Page

from ui.elements.button import Button
from ui.elements.expect_validation import ExpectValidation
from ui.elements.filter import Filter
from ui.elements.text import Text
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class OrderHistory(BasePage):

        def search_order_history (self, order_id):
            # my_page.get_by_role("button",name="ORDERS").click()
            Button(self.page.get_by_role("button", name="ORDERS"), "click ORDERS button").click()

            # my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
            order_row = Filter(self.page.locator("//th"), order_id).has_text(order_id)
            Button(order_row.locator("//following-sibling::td//button[text()='View']"),
                   "click View button in order row").click()

            # expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
            ExpectValidation(self.page.locator("//p[@class='tagline']"), "Check thanks message").to_contain_text(
                "Thank you for Shopping With Us")