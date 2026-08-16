import json
import time
from time import sleep

import pytest
from playwright.sync_api import Playwright, expect

from ui.elements.base_element import BaseElements
from utils.api_base import APIUtils

PRODUCT_NAME = "ZARA COAT 3"
PRODUCT_ID = "6960eac0c941646b7a8b3e68"
CVV="922"

def get_credentials(user):
    with open('data/credentials.json') as json_file:
        test_data = json.load(json_file)
        print(test_data)
        user_list = test_data[user]
    return user_list



#filter from all product card and add to cart
def test_e2e_full_ui_no_filter_cards_base_elements(context_setup) :

    user_list = get_credentials("user_a")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup
    base_element = BaseElements(my_page)

    my_page.goto("https://rahulshettyacademy.com/client/")
    #my_page.locator("#userEmail").fill("dudued@gmail.com") -> by css

    #my_page.locator("//input[@id='userEmail']").fill(user_name) #->xpath
    base_element.fill_by_locator("//input[@id='userEmail']",user_name,"fill user name")

    #my_page.locator("//input[@id='userPassword']").fill(user_password)
    base_element.fill_by_locator("//input[@id='userPassword']", user_password,"fill user password")

    #my_page.get_by_role("button",name="Login").click()
    base_element.click_by_role("button","Login","click login button")

    product_element=my_page.locator("//div[@class='container']//div[@class='row']//div[@class='card']").filter(has_text=PRODUCT_NAME)
    product_element.get_by_role("button",name="Add To Cart").click()

    cart_count = my_page.locator("//button[contains(@class,'btn-custom')]/label") #//button[contains(@class,'btn-custom')]/label[contains(text(),'1')]
    expect(cart_count).to_have_text("1")

    my_page.locator("//button[@routerlink='/dashboard/cart']").click()
    expect(my_page.locator("//h1")).to_have_text("My Cart")

    expect(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']")).to_contain_text(PRODUCT_ID)
    expect(my_page.locator("//div[@class='cartSection']/h3")).to_contain_text(PRODUCT_NAME)
    my_page.get_by_role("button",name="Buy Now").click()
    my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']").fill(CVV)
    my_page.get_by_placeholder("Select Country").type("India")
    my_page.locator("//button[normalize-space()='India']").click() #my_page.get_by_role("button", name="India", exact=True).click()
    my_page.locator("//a[contains(text(),'Place Order')]").click()
    expect(my_page.locator("//h1")).to_contain_text("Thankyou for the order.")
    order_id = my_page.locator("//label[@class='ng-star-inserted']").text_content().replace("| ","")
    print(order_id)
    my_page.get_by_role("button",name="ORDERS").click()
    my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
    expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
    sleep(5)

#search and then add to cart
def test_e2e_full_ui_filter_card(context_setup) :

    user_list = get_credentials("user_b")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup
    my_page.goto("https://rahulshettyacademy.com/client/")
    #my_page.locator("#userEmail").fill("dudued@gmail.com") -> by css
    my_page.locator("//input[@id='userEmail']").fill(user_name) #->xpath
    my_page.locator("//input[@id='userPassword']").fill(user_password)
    my_page.get_by_role("button",name="Login").click()

    #filter card
    my_page.locator("//section//input[@name='search']").fill(PRODUCT_NAME)
    my_page.keyboard.press("Enter")

    expect(my_page.locator("//div[@id='res']")).to_contain_text("Showing 1 results")
    my_page.get_by_role("button",name="Add To Cart").click()

    cart_count = my_page.locator("//button[contains(@class,'btn-custom')]/label") #//button[contains(@class,'btn-custom')]/label[contains(text(),'1')]
    expect(cart_count).to_have_text("1")

    my_page.locator("//button[@routerlink='/dashboard/cart']").click()
    expect(my_page.locator("//h1")).to_have_text("My Cart")

    expect(my_page.locator("//div[@class='cartSection']/p[@class='itemNumber']")).to_contain_text(PRODUCT_ID)
    expect(my_page.locator("//div[@class='cartSection']/h3")).to_contain_text(PRODUCT_NAME)
    my_page.get_by_role("button",name="Buy Now").click()
    my_page.locator("//div[contains(text(),'CVV Code')]/following-sibling::input[@type='text']").fill(CVV)
    my_page.get_by_placeholder("Select Country").type("India")
    my_page.locator("//button[normalize-space()='India']").click() #my_page.get_by_role("button", name="India", exact=True).click()
    my_page.locator("//a[contains(text(),'Place Order')]").click()
    expect(my_page.locator("//h1")).to_contain_text("Thankyou for the order.")
    order_id = my_page.locator("//label[@class='ng-star-inserted']").text_content().replace("| ","")
    print(order_id)
    my_page.get_by_role("button",name="ORDERS").click()
    my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
    expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
    sleep(5)


