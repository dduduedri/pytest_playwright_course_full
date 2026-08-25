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


# Login once for every user returned by get_all_users() from data/ui_data/credentials.json.
# Parametrize feeds each user dict into the test; ids= uses userEmail as the pytest test id.
@pytest.mark.smoke
@pytest.mark.parametrize('user_credentials_params',get_all_users(),ids=lambda user: user["userEmail"])
def test_login_data_iteration(context_setup,user_credentials_params) :
    user_name=user_credentials_params["userEmail"]
    user_password = user_credentials_params["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)

# Login with a single user selected by parametrize.
# credentials_user_with_param is an indirect fixture: ["user_a"] is passed into the fixture,
# which loads that user from data/ui_data/credentials.json.
@pytest.mark.smoke
@pytest.mark.parametrize("credentials_user_with_param",["user_a"],indirect=True)
def test_login_data_fixture_with_param(context_setup,credentials_user_with_param) :
    user_name=credentials_user_with_param["userEmail"]
    user_password = credentials_user_with_param["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)

# Login with user_a from the full credentials dict.
# get_all_credentials is a fixture that returns data/ui_data/credentials.json (keys user_a, user_b).
@pytest.mark.smoke
def test_login_data_fixture(context_setup,get_all_credentials_file) :
    user_name=get_all_credentials_file["user_a"]["userEmail"]
    user_password = get_all_credentials_file["user_a"]["UserPassword"]

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_name,user_password)
    sleep(5)


# E2E: filter product cards, add to cart, checkout, and open the order in history.
# product_data is an indirect fixture: ["products"] loads data/ui_data/products.json.
@pytest.mark.smoke
@pytest.mark.parametrize("product_data",["products"],indirect=True)
def test_e2e_full_ui_filter_cards(context_setup,product_data) :

    CVV = "922"

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

# E2E: filter product cards, add to cart, checkout with payment data, and open the order in history.
# Two indirect fixtures: product_data loads data/ui_data/products.json, payment_data loads data/ui_data/payments.json.
@pytest.mark.smoke
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

# E2E: search for a product, add it to cart, checkout, and open the order in history.
# Uses hardcoded PRODUCT_NAME / PRODUCT_ID and user_b from data/ui_data/credentials.json via get_credentials().
@pytest.mark.smoke
def test_e2e_full_ui_search_card(context_setup) :

    PRODUCT_NAME = "ZARA COAT 3"
    PRODUCT_ID = "6960eac0c941646b7a8b3e68"
    CVV = "922"

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


# Hybrid E2E: create the order with the API, then find it in the UI order history.
# Uses user_a from data/ui_data/credentials.json via get_credentials(); product id and country are hardcoded.
@pytest.mark.smoke
def test_e2e_full_hybrid_order_created_by_api(playwright: Playwright,context_setup) :

    PRODUCT_ID = "6960eac0c941646b7a8b3e68"

    user_list = get_credentials("user_a")

    api_utils = APIUtils()
    order_id=api_utils.create_order(playwright,user_list,PRODUCT_ID,"India")
    print("order_id:",order_id)

    my_page = context_setup
    LoginPage(my_page).login_goto()
    LoginPage(my_page).login(user_list["userEmail"], user_list["UserPassword"])
    OrderHistory(my_page).search_order_history(order_id)
    sleep(5)