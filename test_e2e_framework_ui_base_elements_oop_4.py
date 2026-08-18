import json
import time
from time import sleep

import pytest
from playwright.sync_api import Playwright, expect

from ui.elements.base_element import BaseElements
from ui.elements.button import Button
from ui.elements.filter import Filter
from ui.elements.text import Text
from ui.elements.text_box import TextBox
from ui.elements.expect_validation import ExpectValidation
from ui.pages.cart_page import CartPage

from ui.pages.login_page import LoginPage
from ui.pages.create_product_order_page import ProductPage
from ui.pages.order_history import OrderHistory
from ui.pages.order_payement_page import OrderPaymentPage
from utils.api_base import APIUtils

PRODUCT_NAME = "ZARA COAT 3"
PRODUCT_ID = "6960eac0c941646b7a8b3e68"
CVV="922"

def get_credentials(user):
    with open('data/ui_data/credentials.json') as json_file:
        test_data = json.load(json_file)
        print(test_data)
        user_list = test_data[user]
    return user_list



#filter from all product card and add to cart
def test_e2e_full_ui_no_filter_cards(context_setup) :
    user_list = get_credentials("user_a")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup

    # my_page.goto("https://rahulshettyacademy.com/client/")
    LoginPage(my_page).login_goto()

    #Login
    # TextBox(my_page.locator("//input[@id='userEmail']"),"Fill User Name").fill(user_name)
    # TextBox(my_page.locator("//input[@id='userPassword']"), "Fill User Name").fill(user_password)
    # Button(my_page.get_by_role("button",name="Login"),"click Login").click()
    LoginPage(my_page).login(user_name,user_password)


    #add_product_to_cart
    # product = Filter(my_page.locator("//div[@class='card']"),"Product Cards").has_text(PRODUCT_NAME)
    # Button(product.get_by_role("button", name="Add To Cart"),f"Add {PRODUCT_NAME} To Cart").click()
    ProductPage(my_page).add_product_to_cart(PRODUCT_NAME)

    #check_cart_count
    #cart_count = my_page.locator("//button[contains(@class,'btn-custom')]/label")
    #expect(cart_count).to_have_text("1")
    #ExpectValidation(cart_count, "Cart Count").to_have_text("1", timeout=10000)
    ProductPage(my_page).check_cart_count(1)


    # Button(my_page.locator("//button[@routerlink='/dashboard/cart']"), "click cart").click()
    # ExpectValidation(my_page.locator("//h1"), "My Cart Label").to_have_text("My Cart")
    # ExpectValidation(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']"), "Check product id Label").to_contain_text(PRODUCT_ID)
    # ExpectValidation(my_page.locator("//div[@class='cartSection']/h3"), "Check product name Label").to_contain_text(PRODUCT_NAME)
    # Button(my_page.get_by_role("button",name="Buy Now"), "click Buy Now").click()
    CartPage(my_page).check_ordered_product_in_cart(PRODUCT_NAME,PRODUCT_ID)

    # TextBox(my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']"), "Fill CVV Code").fill(CVV)
    # TextBox(my_page.get_by_placeholder("Select Country"),"Fill Country").type("India")
    # Button(my_page.locator("//button[normalize-space()='India']"), "click India option").click()
    # Button(my_page.locator("//a[contains(text(),'Place Order')]"), "click Place Order button").click()
    # ExpectValidation(my_page.locator("//h1"), "Check complete order message").to_contain_text("Thankyou for the order.")
    # order_id = Text(my_page.locator("//label[@class='ng-star-inserted']"),"Product Name").get_text().replace("| ", "")
    order_id=OrderPaymentPage(my_page).place_order(CVV)



    # Button(my_page.get_by_role("button",name="ORDERS"), "click ORDERS button").click()
    # order_row=Filter(my_page.locator("//th"), order_id).has_text(order_id)
    # Button(order_row.locator("//following-sibling::td//button[text()='View']"), "click View button in order row").click()
    # ExpectValidation(my_page.locator("//p[@class='tagline']"), "Check thanks message").to_contain_text("Thank you for Shopping With Us")
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)

#search and then add to cart
def test_e2e_full_ui_filter_card(context_setup) :

    user_list = get_credentials("user_b")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup
    my_page.goto("https://rahulshettyacademy.com/client/")
    #my_page.locator("#userEmail").fill("dudued@gmail.com") -> by css

    #my_page.locator("//input[@id='userEmail']").fill(user_name) #->xpath
    TextBox(my_page.locator("//input[@id='userEmail']"),"Fill User Name").fill(user_name)

    #my_page.locator("//input[@id='userPassword']").fill(user_password)
    TextBox(my_page.locator("//input[@id='userPassword']"), "Fill User Name").fill(user_password)

    #my_page.get_by_role("button",name="Login").click()
    Button(my_page.get_by_role("button",name="Login"),"click Login").click()

    #filter card
    #my_page.locator("//section//input[@name='search']").fill(PRODUCT_NAME)
    TextBox(my_page.locator("//section//input[@name='search']"), "Fill Product Search").fill(PRODUCT_NAME)

    #my_page.keyboard.press("Enter")
    TextBox(my_page.locator("//section//input[@name='search']"), "Press Enter on Product Search").press_key("Enter")

    #expect(my_page.locator("//div[@id='res']")).to_contain_text("Showing 1 results")
    ExpectValidation(my_page.locator("//div[@id='res']"), "Search Results").to_contain_text("Showing 1 results")

    #my_page.get_by_role("button",name="Add To Cart").click()
    Button(my_page.get_by_role("button",name="Add To Cart"), f"Add {PRODUCT_NAME} To Cart").click()

    cart_count = my_page.locator("//button[contains(@class,'btn-custom')]/label") #//button[contains(@class,'btn-custom')]/label[contains(text(),'1')]
    #expect(cart_count).to_have_text("1")
    ExpectValidation(cart_count, "Cart Count").to_have_text("1", timeout=10000)

    #my_page.locator("//button[@routerlink='/dashboard/cart']").click()
    Button(my_page.locator("//button[@routerlink='/dashboard/cart']"), "click cart").click()

    #expect(my_page.locator("//h1")).to_have_text("My Cart")
    ExpectValidation(my_page.locator("//h1"), "My Cart Label").to_have_text("My Cart")

    #expect(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']")).to_contain_text(PRODUCT_ID)
    ExpectValidation(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']"), "Check product id Label").to_contain_text(PRODUCT_ID)

    #expect(my_page.locator("//div[@class='cartSection']/h3")).to_contain_text(PRODUCT_NAME)
    ExpectValidation(my_page.locator("//div[@class='cartSection']/h3"), "Check product name Label").to_contain_text(PRODUCT_NAME)

    #my_page.get_by_role("button",name="Buy Now").click()
    Button(my_page.get_by_role("button",name="Buy Now"), "click Buy Now").click()

    #my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']").fill(CVV)
    TextBox(my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']"), "Fill CVV Code").fill(CVV)

    #my_page.get_by_placeholder("Select Country").type("India")
    TextBox(my_page.get_by_placeholder("Select Country"),"Fill Country").type("India")

    #my_page.locator("//button[normalize-space()='India']").click() #my_page.get_by_role("button", name="India", exact=True).click()
    Button(my_page.locator("//button[normalize-space()='India']"), "click India option").click()

    #my_page.locator("//a[contains(text(),'Place Order')]").click()
    Button(my_page.locator("//a[contains(text(),'Place Order')]"), "click Place Order button").click()

    #expect(my_page.locator("//h1")).to_contain_text("Thankyou for the order.")
    ExpectValidation(my_page.locator("//h1"), "Check complete order message").to_contain_text("Thankyou for the order.")

    #order_id = my_page.locator("//label[@class='ng-star-inserted']").text_content().replace("| ","")
    order_id = Text(my_page.locator("//label[@class='ng-star-inserted']"),"Product Name").get_text().replace("| ", "")
    print(order_id)

    #my_page.get_by_role("button",name="ORDERS").click()
    Button(my_page.get_by_role("button",name="ORDERS"), "click ORDERS button").click()

    #my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
    order_row=Filter(my_page.locator("//th"), order_id).has_text(order_id)
    Button(order_row.locator("//following-sibling::td//button[text()='View']"), "click View button in order row").click()

    #expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
    ExpectValidation(my_page.locator("//p[@class='tagline']"), "Check thanks message").to_contain_text("Thank you for Shopping With Us")
    sleep(5)


def test_e2e_full_hybrid_order_created_by_api(playwright: Playwright,context_setup) :

    user_list = get_credentials("user_a")

    api_utils = APIUtils()
    order_id=api_utils.create_order(playwright,user_list,PRODUCT_ID,"India")
    print("order_id:",order_id)

    my_page = context_setup
    my_page.goto("https://rahulshettyacademy.com/client/")
    #my_page.locator("#userEmail").fill("dudued@gmail.com") -> by css

    #my_page.locator("//input[@id='userEmail']").fill(user_list["userEmail"]) #->xpath
    TextBox(my_page.locator("//input[@id='userEmail']"),"Fill User Name").fill(user_list["userEmail"])

    #my_page.locator("//input[@id='userPassword']").fill(user_list["UserPassword"])
    TextBox(my_page.locator("//input[@id='userPassword']"), "Fill User Name").fill(user_list["UserPassword"])

    #my_page.get_by_role("button",name="Login").click()
    Button(my_page.get_by_role("button",name="Login"),"click Login").click()

    #my_page.get_by_role("button",name="ORDERS").click()
    Button(my_page.get_by_role("button",name="ORDERS"), "click ORDERS button").click()

    #my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
    order_row=Filter(my_page.locator("//th"), order_id).has_text(order_id)
    Button(order_row.locator("//following-sibling::td//button[text()='View']"), "click View button in order row").click()

    #expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
    ExpectValidation(my_page.locator("//p[@class='tagline']"), "Check thanks message").to_contain_text("Thank you for Shopping With Us")
    sleep(5)