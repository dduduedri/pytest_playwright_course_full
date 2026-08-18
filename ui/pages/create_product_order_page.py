from playwright.sync_api import Page

from ui.elements.button import Button
from ui.elements.expect_validation import ExpectValidation
from ui.elements.filter import Filter
from ui.elements.text_box import TextBox
from ui.pages.base_page import BasePage


class ProductPage(BasePage):

    def filter_product_element (self, product_name):
        # product_element=my_page.locator("//div[@class='container']//div[@class='row']//div[@class='card']").filter(has_text=PRODUCT_NAME)
        product_element = Filter(self.page.locator("//div[@class='card']"), "Product Cards").has_text(product_name)
        return product_element

    def search_product (self, product_name):
        # my_page.locator("//section//input[@name='search']").fill(PRODUCT_NAME)
        TextBox(self.page.locator("//section//input[@name='search']"), "Fill Product Search").fill(product_name)

        # my_page.keyboard.press("Enter")
        TextBox(self.page.locator("//section//input[@name='search']"), "Press Enter on Product Search").press_key("Enter")

        # expect(my_page.locator("//div[@id='res']")).to_contain_text("Showing 1 results")
        ExpectValidation(self.page.locator("//div[@id='res']"), "Search Results").to_contain_text("Showing 1 results")

    def add_product_to_cart(self, product_name):
        product_element = self.filter_product_element(product_name)
        # product_element.get_by_role("button",name="Add To Cart").click()
        Button(product_element.get_by_role("button", name="Add To Cart"), f"Add {product_name} To Cart").click()

    def check_cart_count(self,count):
        cart_count = self.page.locator("//button[contains(@class,'btn-custom')]/label")
        # expect(cart_count).to_have_text("1")
        ExpectValidation(cart_count, "Cart Count").to_have_text(str(count), timeout=10000)