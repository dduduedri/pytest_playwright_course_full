import json
from time import sleep

from playwright.sync_api import Playwright, expect
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
def test_e2e_full_ui_filter_cards(context_setup) :
    user_list = get_credentials("user_a")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    ProductPage(my_page).add_product_to_cart(PRODUCT_NAME)
    ProductPage(my_page).check_cart_count(1)
    CartPage(my_page).check_and_buy_ordered_product_in_cart(PRODUCT_NAME, PRODUCT_ID)
    order_id=OrderPaymentPage(my_page).place_order(CVV)
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)

#search and then add to cart
def test_e2e_full_ui_search_card(context_setup) :
    user_list = get_credentials("user_b")
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name, user_password)
    ProductPage(my_page).search_product(PRODUCT_NAME)
    ProductPage(my_page).add_product_to_cart(PRODUCT_NAME)
    ProductPage(my_page).check_cart_count(1)
    CartPage(my_page).check_and_buy_ordered_product_in_cart(PRODUCT_NAME, PRODUCT_ID)
    order_id = OrderPaymentPage(my_page).place_order(CVV)
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)


def test_e2e_full_hybrid_order_created_by_api(playwright: Playwright,context_setup) :
    user_list = get_credentials("user_a")

    api_utils = APIUtils()
    order_id=api_utils.create_order(playwright,user_list,PRODUCT_ID,"India")
    print("order_id:",order_id)

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_list["userEmail"], user_list["UserPassword"])
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)