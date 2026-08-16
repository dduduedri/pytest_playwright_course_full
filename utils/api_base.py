from playwright.sync_api import Playwright, expect

BASE_URL = "https://rahulshettyacademy.com"

class APIUtils:
    def get_token(self,playwright: Playwright,user_cred):

        login_payload = {"userEmail": user_cred["userEmail"], "userPassword": user_cred["UserPassword"]}
        api_request_context = playwright.request.new_context(base_url=BASE_URL,ignore_https_errors=True)
        response = api_request_context.post("/api/ecom/auth/login",
                                            data=login_payload ,
                                            headers={"Content-Type": "application/json"})
        assert response.ok, \
            f"Login failed: {response.status} - {response.text()}"
        response_body = response.json()
        return response_body["token"]


    def create_order(self,playwright: Playwright,user_cred,product_id,country):
        create_order_payload = {"orders": [{"country": country, "productOrderedId": product_id}]}
        api_request_context = playwright.request.new_context(base_url=BASE_URL,ignore_https_errors=True)
        token=self.get_token(playwright,user_cred)
        response = api_request_context.post("/api/ecom/order/create-order",
                                            data=create_order_payload,
                                            headers={"Content-Type": "application/json",
                                                     "Authorization": token})
        assert response.ok, \
            f"Login failed: {response.status} - {response.text()}"

        response_body = response.json()
        assert "Order Placed Successfully" in response_body["message"]
        return response_body["orders"][0]
