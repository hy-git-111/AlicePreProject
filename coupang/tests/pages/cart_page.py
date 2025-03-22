from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import user_data


class CartPage:
    url = "https://cart.coupang.com/cartView.pang"
    TARGET_PROD_XPATH = '//td[.//img[contains(@alt, "마우스")]]'
    QUANTITY_XPATH = {"plus": './/div[contains(@class, "plus")]', "minus": './/div[contains(@class, "minus")]'}
    PADDING_AREA_XPATH = './/div/div/div[contains(@class, "info-padding")]'
    # QUANTITY_PLUS_XPATH = './/div[contains(@class, "plus")]'
    # QUANTITY_MINUS_XPATH = './/div[contains(@class, "minus")]'
    # DISABLED_QTY_BTN_CLASS_NAME = 'disabled'

    # 객체 인스턴스화를 위한 세팅, 파이테스트의 'driver'를 받아 driver 객체에 넣는다.
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # 상품 상세 페이지 열기
    def open(self):
        self.driver.get(self.url)
        self.driver.add_cookie(user_data.cookies)

    # 기준 상품 탐색
    def standard_prod(self, driver:WebDriver):
        target_prod = driver.find_element(By.XPATH, self.TARGET_PROD_XPATH)
        return target_prod

    # 수량 증감
    def quantity_change_by_btn(self, quantity_change):
        target_prod = self.standard_prod(self)
        quantity_change_btn = target_prod.find_element(By.XPATH, self.QUANTITY_XPATH[quantity_change])

        quantity_change_btn.click()

    # 최대/최소 수량 입력
    def quantity_change_by_keys(self, quantity_change_to):
        target_prod = self.standard_prod(self)
        quantity_input = target_prod.find_element(By.TAG_NAME, "input")
        padding_area = target_prod.find_element(By.XPATH, self.PADDING_AREA_XPATH)

        current_quantity = int(quantity_input.get_attribute("value"))
        quantity_limit = int(quantity_input.get_attribute("data-max-quantity"))

        quantity_input.clear()
        
        if quantity_change_to == "max":
            quantity_input.send_keys(quantity_limit)
            padding_area.click()

            current_quantity = int(quantity_input.get_attribute("value"))
            return current_quantity
        
        if quantity_change_to == "min":
            quantity_input.send_keys(1)
            padding_area.click()

            current_quantity = int(quantity_input.get_attribute("value"))
            return current_quantity
        
    # 상품 클릭
    def click_by_xpath(self, element_xpath):
        target_prod = self.standard_prod(self)
        delete_btn = target_prod.find_element(By.XPATH, element_xpath)
        delete_btn.click()

