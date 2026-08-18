from playwright.sync_api import Page

from ui.elements.button import Button
from ui.elements.expect_validation import ExpectValidation
from ui.elements.filter import Filter
from ui.elements.text import Text
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class OrderPaymentPage(BasePage):

        def place_order (self, cvv):
            # my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']").fill(CVV)
            TextBox(self.page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']"),
                    "Fill CVV Code").fill(cvv)

            # my_page.get_by_placeholder("Select Country").type("India")
            TextBox(self.page.get_by_placeholder("Select Country"), "Fill Country").type("India")

            # my_page.locator("//button[normalize-space()='India']").click() #my_page.get_by_role("button", name="India", exact=True).click()
            Button(self.page.locator("//button[normalize-space()='India']"), "click India option").click()

            # my_page.locator("//a[contains(text(),'Place Order')]").click()
            Button(self.page.locator("//a[contains(text(),'Place Order')]"), "click Place Order button").click()

            # expect(my_page.locator("//h1")).to_contain_text("Thankyou for the order.")
            ExpectValidation(self.page.locator("//h1"), "Check complete order message").to_contain_text("Thankyou for the order.")

            # order_id = my_page.locator("//label[@class='ng-star-inserted']").text_content().replace("| ","")
            order_id = Text(self.page.locator("//label[@class='ng-star-inserted']"), "Product Name").get_text().replace("| ", "")
            return order_id