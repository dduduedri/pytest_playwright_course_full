import json
from time import sleep

import pytest
from playwright.sync_api import Playwright, expect
from utils.api_base import APIUtils


PRODUCT_NAME = "ZARA COAT 3"
PRODUCT_ID = "6960eac0c941646b7a8b3e68"
CVV="922"


def get_credentials(user):
    with open('playwright_framework_1/data/credentials.json') as json_file:
        test_data = json.load(json_file)
        print(test_data)
        user_list = test_data[user]
    return user_list


# Hybrid E2E: create the order with the API, then find it in the UI order history.
# Raw Playwright locators (no page objects / base elements). user_a from playwright_framework_1/data/credentials.json; product id and country are hardcoded.
def test_e2e_full_hybrid_order_created_by_api(playwright: Playwright,context_setup) :

    user_list = get_credentials("user_a")

    api_utils = APIUtils()
    order_id=api_utils.create_order(playwright,user_list,PRODUCT_ID,"India")
    print("order_id:",order_id)

    my_page = context_setup
    my_page.goto("https://rahulshettyacademy.com/client/")
    #my_page.locator("#userEmail").fill("dudued@gmail.com") -> by css

    my_page.locator("//input[@id='userEmail']").fill(user_list["userEmail"]) #->xpath
    my_page.locator("//input[@id='userPassword']").fill(user_list["UserPassword"])
    my_page.get_by_role("button",name="Login").click()

    my_page.get_by_role("button",name="ORDERS").click()
    my_page.locator("//th").filter(has_text=order_id).locator("//following-sibling::td//button[text()='View']").click()
    expect(my_page.locator("//p[@class='tagline']")).to_contain_text("Thank you for Shopping With Us")
    sleep(5)
