from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium import webdriver
import logging
import pytest
import random
import os

# ✅ 기존 핸들러 제거 (중복 설정 방지)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 로그 파일 저장 위치 설정 (conftest.py가 있는 폴더 기준)
# log_filename = f"{date.today().strftime('%Y%m%d')}_coupang_test_result.log"
log_filename = os.path.join(os.path.dirname(__file__), "coupang_test_result.log")

# 로그 설정
logging.basicConfig(
    filename=log_filename,
    encoding="utf-8",
    errors="replace",  # 인코딩 문제 방지
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info("pytest 실행 시 로그 설정 완료")
user_agents = [
    # Add your list of user agents here
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/91.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

@pytest.fixture(scope="function")

def driver():
    # proxy : 크롤링 중 ip가 차단되었을 때 vpn을 사용해서 ip 우회하는 것
    user_agent = random.choice(user_agents)

    # 크롬 옵션 설정
    chrome_options = Options()  # 쿠팡에서 자동화를 막아서 옵션 수정 필요
    
    # 1) User-Agent 변경
    chrome_options.add_argument(f"user-agent{user_agent}")    # 사용자 접근 환경 강제 입력

    # 2) SSL 인증서 에러 무시
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")

    # 4) Selenium이 automation된 브라우저임을 숨기는 몇 가지 설정 (js가 인식하지 못하도록 함)
    #    - (disable-blink-features=AutomationControlled) 제거
    #    - excludeSwitches, useAutomationExtension
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 혹은 다음 방식으로 Blink 특징을 비활성화할 수도 있으나
    # "AutomationControlled" 자체가 표기되지 않도록 한다.
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 5) 디버그 로깅 줄이기 (선택)
    # chrome_options.add_argument("--log-level=3") 

    # 6) Sandbox나 DevShm 사이즈 문제 우회 (리눅스 환경에서 발생 가능)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-popup-blocking')

    # 드라이버 객체 생성
    driver = webdriver.Chrome(service=Service(), options=chrome_options)   
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"Referer": "https://www.coupang.com/"}})
    driver.execute_cdp_cmd("Network.clearBrowserCache", {})

    # Step 4: Scrape using Stealth
    #enable stealth mode
    stealth(driver,
        languages=["ko-KR", "ko"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    driver.delete_all_cookies()
    #  대기시간 설정
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver 

    # 테스트가 끝나면 드라이버 종료
    driver.quit()
