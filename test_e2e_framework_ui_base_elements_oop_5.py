import json
from time import sleep

import pytest
from playwright.sync_api import Playwright, expect
from ui.pages.cart_page import CartPage

from ui.pages.login_page import LoginPage
from ui.pages.create_product_order_page import ProductPage
from ui.pages.order_history import OrderHistory
from ui.pages.order_payement_page import OrderPaymentPage
from utils.api_base import APIUtils
from utils.data_reader import get_all_users, get_credentials, get_data

PRODUCT_NAME = "ZARA COAT 3"
PRODUCT_ID = "6960eac0c941646b7a8b3e68"
CVV="922"


#use data reader method ad parameter
@pytest.mark.parametrize('user_credentials_params',get_all_users(),ids=lambda user: user["userEmail"]) #ids its just give id name to the parameters
def test_login_data_iteration(context_setup,user_credentials_params) :
    user_name=user_credentials_params["userEmail"]
    user_password = user_credentials_params["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)

#use credentials_user_with_param fixture to run credential user with the user param
@pytest.mark.parametrize("credentials_user_with_param",["user_a"],indirect=True)
def test_login_data_fixture_with_param(context_setup,credentials_user_with_param) :
    user_name=credentials_user_with_param["userEmail"]
    user_password = credentials_user_with_param["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)

#use credentials_user fixture to get all the users
def test_login_data_fixture(context_setup,credentials_user) :
    user_name=credentials_user("user_a")["userEmail"]
    user_password = credentials_user("user_a")["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)


#filter from all product card and add to cart , use generic_data fixure to get data from \data\ui_data\products.json
@pytest.mark.parametrize("product_data",["products"],indirect=True)
def test_e2e_full_ui_filter_cards(context_setup,product_data) :
    user_list = get_credentials("user_a") #from utils.data_reader import  get_credentials
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    products = product_data["zara_coat"]
    product_name=products["productName"]
    product_id=products["productID"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    ProductPage(my_page).add_product_to_cart(product_name)
    ProductPage(my_page).check_cart_count(1)
    CartPage(my_page).check_and_buy_ordered_product_in_cart(product_name, product_id)
    order_id=OrderPaymentPage(my_page).place_order(CVV,"India")
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)

#filter from all product card and add to cart , use multiple  generic_data fixure to get data from \data\ui_data\products.json
@pytest.mark.parametrize("product_data", ["products"], indirect=True)
@pytest.mark.parametrize("payment_data", ["payments"], indirect=True)
def test_e2e_full_ui_filter_cards(context_setup,product_data,payment_data) :
    user_list = get_credentials("user_a") #from utils.data_reader import  get_credentials
    user_name=user_list["userEmail"]
    user_password = user_list["UserPassword"]

    products = product_data["zara_coat"]
    product_name=products["productName"]
    product_id=products["productID"]

    payment = payment_data["credit"]
    payment_cvv=payment["cvv"]
    payment_country=payment["country"]


    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    ProductPage(my_page).add_product_to_cart(product_name)
    ProductPage(my_page).check_cart_count(1)
    CartPage(my_page).check_and_buy_ordered_product_in_cart(product_name, product_id)
    order_id=OrderPaymentPage(my_page).place_order(payment_cvv,payment_country)
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
    order_id = OrderPaymentPage(my_page).place_order(CVV,"India")
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