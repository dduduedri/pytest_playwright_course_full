from playwright.sync_api import Page

from ui.elements.button import Button
from ui.elements.expect_validation import ExpectValidation
from ui.elements.filter import Filter
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class CartPage(BasePage):

        def check_and_buy_ordered_product_in_cart (self, product_name, product_id):
            # my_page.locator("//button[@routerlink='/dashboard/cart']").click()
            Button(self.page.locator("//button[@routerlink='/dashboard/cart']"), "click cart").click()

            # expect(my_page.locator("//h1")).to_have_text("My Cart")
            ExpectValidation(self.page.locator("//h1"), "My Cart Label").to_have_text("My Cart")

            # expect(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']")).to_contain_text(product_id)
            ExpectValidation(self.page.locator("//div[@class='cartSection']/p[@class='itemNumber']"),
                             "Check product id Label").to_contain_text(product_id)
            # expect(my_page.locator("//div[@class='cartSection']/h3")).to_contain_text(product_name)
            ExpectValidation(self.page.locator("//div[@class='cartSection']/h3"),
                             "Check product name Label").to_contain_text(product_name)
            # my_page.get_by_role("button",name="Buy Now").click()
            Button(self.page.get_by_role("button", name="Buy Now"), "click Buy Now").click()