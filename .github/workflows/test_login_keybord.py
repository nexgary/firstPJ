import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 引入設定檔
import config

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver

def test_login(driver):
    driver.get(config.LOGIN_URL)
    wait = WebDriverWait(driver, 30)

    try:
        customer_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='客戶代號']")))
        customer_input.click()
        customer_input.clear()
        time.sleep(0.5)
        customer_input.send_keys(config.CUSTOMER_ID)
        customer_input.send_keys(Keys.TAB)

        account_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='帳號']")))
        account_input.click()
        account_input.clear()
        time.sleep(0.5)
        account_input.send_keys(config.ACCOUNT)
        account_input.send_keys(Keys.TAB)

        password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='密碼']")))
        password_input.click()
        password_input.clear()
        time.sleep(0.5)
        password_input.send_keys(config.PASSWORD)
        password_input.send_keys(Keys.ENTER)

        wait.until(EC.url_contains("WebPos"))
        assert "WebPos" in driver.current_url or "首頁" in driver.page_source

        try:
            confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wui-button.wui-item.wui-mr-2.wui-color-blue-pos[title='確定']")))
            confirm_button.click()
        except:
            print("⚠️ 未找到或不需點擊『確定』按鈕")

        hr_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wui-left-menu-item-text wui-left-menu-item-root' and @data-ww-key='人事管理']")))
        hr_menu.click()

        employee_info = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wui-left-menu-item-text' and @data-ww-key='WEMM0070']")))
        employee_info.click()

        salary_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wui-left-menu-item-text wui-left-menu-item-root' and @data-ww-key='薪資管理']")))
        salary_menu.click()
        time.sleep(0.5)

        salary_calc = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wui-left-menu-item-text' and @data-ww-key='WPAU3020']")))
        salary_calc.click()
        time.sleep(0.5)

        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.wui-button.wui-color-primary[title='下一步']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.wui-button.wui-color-primary[title='下一步']")))
        next_button.click()
        time.sleep(0.5)
        # 點擊「發放日期預設」按鈕
        release_date_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='wui-button' and @title='發放日期預設' and contains(., '發放日期預設')]"
        )))
        release_date_button.click()
        time.sleep(0.5)
        # 點擊 dateOption 按鈕
        date_option_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[data-ww-key='dateOption']"
        )))
        date_option_button.click()
        time.sleep(0.5)
        #點擊當月末日
        month_end_link = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//a[@class='wui-link' and text()='當月末日']"
        )))
        month_end_link.click()
        time.sleep(0.5)
        #確定
        confirm_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='wui-button wui-color-primary' and @title='確定' and contains(., '確定')]"
        )))
        confirm_button.click()
        time.sleep(0.5)

        # 點擊「執行」按鈕（下一步）
        execute_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='wui-button wui-color-primary' and @title='下一步' and contains(., '執行')]"
        )))
        execute_button.click()
        time.sleep(0.5)

        confirm_button_2 = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='wui-button wui-color-primary' and @title='確定' and contains(., '確定')]"
        )))
        confirm_button_2.click()
        time.sleep(0.5)

        input("✅ 測試完成，請按 Enter 關閉瀏覽器...")

    except Exception as e:
        import traceback
        print(f"❌ 測試失敗：{e}")
        print(traceback.format_exc())

    finally:
        driver.quit()
