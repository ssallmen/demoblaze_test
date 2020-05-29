#!/usr/bin/env python

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

main_page_url = "https://www.demoblaze.com"
cart_url = "https://www.demoblaze.com/cart.html"
catalog_product_xpath = "//div[@id='tbodyid']//a[@class='hrefch' and @href='prod.html?idp_={id}']"
cart_product_xpath = "//div[@class='table-responsive']//tbody/tr[@class='success']"
cart_product_delete_xpath = f"{cart_product_xpath}/td[4]/a"
cart_product_name_xpath = f"{cart_product_xpath}/td[2]"
product_add_to_cart_btn_xpath = "//div[@id='tbodyid']//a[contains(@class, 'btn-success')]"

class demoblaze:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(8)
        self.open_main_page()

    def open_main_page(self):
        self.driver.get(main_page_url)

    def open_cart(self):
        self.driver.get("https://www.demoblaze.com/cart.html")

    def filter_phones(self):
        pass

    def open_product(self, id=None, name=None):
        if id is not None:
            self.find_catalog_product_by_id(id).click()
        elif name is not None:
            self.find_catalog_product_by_name(name).click()
        else:
            raise Exception("Give product id or name!")

    def find_catalog_product_by_id(self, id):
        return self.driver.find_element_by_xpath(catalog_product_xpath.format(id=id)) # //a[@class='hrefch' and @href='prod.html?idp_={id}']

    def find_catalog_product_by_name(self, name):
        pass

    def add_current_product_to_cart(self):
        self.driver.find_element_by_xpath(product_add_to_cart_btn_xpath).click()
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(), 'Timed out waiting for product added popup to appear')
            alert = self.driver.switch_to.alert
            alertMessage = alert.text
            if alertMessage != "Product added":
                raise AssertionError(f"Right alert message was not shown! (was '{alertMessage}')")
            alert.accept()
        except TimeoutException:
            print("No popup")
            raise
        print("Added product to cart")

    def verify_product_in_cart(self, name='', count=None):
        products = self.driver.find_elements_by_xpath(f"{cart_product_name_xpath}[contains(text(), '{name}')]")
        if len(products):
            if count is None or len(products) == int(count):
                return True
            else:
                raise AssertionError(f"{len(products)} required products in cart but expected {count}")
        else:
            raise AssertionError(f"No required products in cart")
        print(f"{len(products)} pieces of product '{name}' was in cart")

    def get_number_of_products_in_cart(self):
        return len(self.driver.find_elements_by_xpath(cart_product_xpath))

    def delete_product_from_cart(self, name=''):
        if name == '':
            name=self.driver.find_element_by_xpath(cart_product_name_xpath).text
        print("Deleting product {name} from cart".format(name=name))
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"{cart_product_name_xpath}[contains(text(), '{name}')]/../td[4]/a")), "Deleting product did not come possible in 3 seconds").click()
        except TimeoutException:
            print("The 'Delete' link did not activate")
            raise
        try:
            WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, cart_product_xpath)), "Cart did not update in 5 seconds")
        except TimeoutException:
            print("Cart was not updating when deleting product")
            raise

    def clear_cart(self):
        self.open_cart()
        products = self.driver.find_elements_by_xpath(cart_product_xpath)
        while len(products) > 0:
            print(f"{len(products)} products in cart")
            self.delete_product_from_cart()
            products = self.driver.find_elements_by_xpath(cart_product_xpath)
            print(products)
        print("Cart is empty")

    def close(self):
        self.driver.close()

# db = demoblaze()
# db.clear_cart()
# db.open_main_page()
# db.open_product(id='1')
# db.add_current_product_to_cart()
# db.open_cart()
# db.verify_product_in_cart(count=1)
# time.sleep(2)
# db.clear_cart()