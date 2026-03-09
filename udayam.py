from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def udayam():

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://udyamregistration.gov.in/Government-India/Ministry-MSME-registration.htm")

    wait = WebDriverWait(driver, 15)

    # Login menu
    login_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Login']")))

    # Hover on Login
    ActionChains(driver).move_to_element(login_menu).perform()

    # Udyami Login option
    udyami_login = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Udyami Login')]")))

    # Click using JS
    driver.execute_script("arguments[0].click();", udyami_login)