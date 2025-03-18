from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from pages.cart_page import CartPage
import logging
import random
import pytest
import time
import re


random_wait = random.randrange(2, 6)

@pytest.mark.usefixtures("driver")
class TestCartPage:
    TARGET_PROD_XPATH = '//td[.//img[contains(@alt, "마우스")]]'
    DISABLED_PLUS_BTN_XPATH = './/div[contains(@class, "plus") and contains(@class, "disabled")]'
    DISABLED_MINUS_BTN_XPATH = './/div[contains(@class, "minus") and contains(@class, "disabled")]'
    CART_CNT_XPATH = '//td[contains(@class, "cart-deal-item__image")]'
    DELETE_BTN_XPATH = '//a[contains(text(), "삭제")]'
    CHECKED_INPUT_XPATH = '//input[@type="checkbox"]'

    # 기준 상품 탐색
    def standard_prod(self, driver:WebDriver):
        target_prod = driver.find_element(By.XPATH, self.TARGET_PROD_XPATH)
        return target_prod

    # 수량 체크
    def check_quantity(self):
        target_prod = self.standard_prod(self)
        quantity_input = target_prod.find_element(By.TAG_NAME, "input")
        current_quantity = int(quantity_input.get_attribute("value"))
        quantity_limit = int(quantity_input.get_attribute("data-max-quantity"))
        
        if current_quantity == 0:
            raise ValueError
        
        if current_quantity > quantity_limit:
            raise ValueError

        if current_quantity == quantity_limit:
            return f"최대 구매 수량 도달: {current_quantity}"
        
        return current_quantity, quantity_limit
    
    # 체크항목 가격 표시
    # 일반회원, 판매자배송상품, 여러 상품 등록 기준으로 작성
    # 검증은 1개 상품 기준으로 진행
    order_amount_param = [()]

    @pytest.mark.parametrize
    def test_cart_price(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)
            
    # 주문 예상 금액 계산
            checked_prod = driver.find_elements(By.XPATH, self.CHECKED_INPUT_XPATH)
            amount_list = []
            delivery_charges = []

            for prod in checked_prod:
                price_element = prod.find_element(By.CLASS_NAME, "unit-total-sale-price")
                price = price_element.text.strip().replace(",", "").replace("원", "")
                
                quantity_element = prod.find_element(By.TAG_NAME, "input")
                quantity = quantity_element.get_attribute("value")
                
                expenditure = int(price) * int(quantity)
                amount_list.append(expenditure)

                delivery_charge_elem = prod.find_element(By.XPATH, '//strong[contains(text(), "원")]')
                delivery_charge = delivery_charge_elem.text.strip().replace(",", "").replace("원", "")
                if delivery_charge == "무료":
                    delivery_charges.append(0)
                    return
                delivery_charges.append(delivery_charge)




        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_수량1 증가_실패__NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('검색결과페이지_범위필터_증가_실패_TimeoutException.png')
            assert False

    # 상품 삭제
    @pytest.mark.skip(reason="이유 없음")
    def test_delete_prod(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("cartView"))
            
            cart_cnt_before = driver.find_elements(By.XPATH, self.CART_CNT_XPATH)
            cart_page.click_by_xpath(self.DELETE_BTN_XPATH)
            cart_cnt_after = driver.find_elements(By.XPATH, self.CART_CNT_XPATH)

            assert len(cart_cnt_after) == len(cart_cnt_before)-1
            time.sleep(2)

        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_수량1 증가_실패__NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('검색결과페이지_범위필터_증가_실패_TimeoutException.png')
            assert False

    # 장바구니페이지에서 수량 1 증가
    @pytest.mark.skip(reason="테스트 실행 못함")
    def test_quantity_plus_1(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("cartView"))

            quantity_before = self.check_quantity(self) # 수량 확인
            cart_page.quantity_change_by_btn("plus")    # 수량 1 증가
            quantity_after = self.check_quantity(self)  # 수량 확인

            assert quantity_after[0] == quantity_before[0] + 1
            assert quantity_after[1] == quantity_before[1]
            driver.save_screenshot("장바구니페이지_수량_1증가_성공.png")
            logging.info("장바구니페이지 수량 1증가 성공")
            time.sleep(random_wait)

        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_수량1 증가_실패__NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('검색결과페이지_범위필터_증가_실패_TimeoutException.png')
            assert False

    # 장바구니페이지에서 수량 1 감소
    @pytest.mark.skip(reason="테스트 실행 못함")
    def test_quantity_mius_1(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("cartView"))

            quantity_before = self.check_quantity(self) # 수량 확인
            cart_page.quantity_change_by_btn("minus")   # 수량 1 감소
            quantity_after = self.check_quantity(self)  # 수량 확인

            assert quantity_after[0] == quantity_before[0] - 1
            assert quantity_after[1] == quantity_before[1]
            driver.save_screenshot("장바구니페이지_수량_1감소_성공.png")
            logging.info("장바구니페이지 수량 1감소 성공")
            time.sleep(random_wait)

        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_수량1 감소_실패_NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_수량1 감소_실패_TimeoutException.png')
            assert False

    # 장바구니페이지에서 최대 수량으로 변경
    @pytest.mark.skip(reason="테스트 실행 못함")
    def test_quantity_max(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("cartView"))

            # 수량 변경 확인
            quantity_after = cart_page.quantity_change_by_keys("max")    # 수량 변경값 return
            quantity_before = self.check_quantity(self)

            assert quantity_after == quantity_before[1]
            driver.save_screenshot("장바구니페이지_최대_수량_적용_성공.png")
            logging.info("장바구니페이지 최대 수량 적용 성공")
            time.sleep(random_wait)

            # + 버튼 비활성화 확인
            cart_page.quantity_change_by_btn("plus")
            target_prod = self.standard_prod(self)
            plus_btns = target_prod.find_elements(By.XPATH, self.DISABLED_PLUS_BTN_XPATH)

            assert len(plus_btns) > 0
            driver.save_screenshot("장바구니페이지_최대_수량_초과_불가_성공.png")
            logging.info("장바구니페이지 최대 수량 초과 불가 성공")

        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_최대_수량_적용_실패_NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_최대_수량_적용_실패_TimeoutException.png')
            assert False

    
    # 장바구니페이지에서 최소 수량으로 변경
    @pytest.mark.skip(reason="테스트 실행 못함")
    def test_quantity_min(self, driver: WebDriver):
        try:
            time.sleep(2)
            cart_page = CartPage(driver)
            cart_page.open()
            time.sleep(random_wait)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("cartView"))

            quantity_after = cart_page.quantity_change_by_keys("min")    # 수량 변경값 return

            assert quantity_after == 1
            driver.save_screenshot("장바구니페이지_최소_수량_적용_성공.png")
            logging.info("장바구니페이지 최대 수량 적용 성공")
            time.sleep(random_wait)

            # - 버튼 비활성화 확인
            cart_page.quantity_change_by_btn("minus")
            target_prod = self.standard_prod(self)
            minus_btns = target_prod.find_elements(By.XPATH, self.DISABLED_MINUS_BTN_XPATH)

            assert len(minus_btns) > 0
            driver.save_screenshot("장바구니페이지_최소_수량_미만_불가_성공.png")
            logging.info("장바구니페이지 최소 수량 미만 불가 성공")

        except NoSuchElementException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_최소_수량_적용_실패_NoSuchElementException.png')
            assert False

        except TimeoutException as e:
            logging.exception(f"error:{e}")
            driver.save_screenshot('장바구니페이지_최소_수량_적용_실패_TimeoutException.png')
            assert False