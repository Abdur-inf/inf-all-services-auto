from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time


def IEcode():

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.dgft.gov.in/CP/")

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)

    captcha = input("Enter Captcha: ")
    wait.until(EC.presence_of_element_located((By.ID, "txt_Captcha"))).send_keys(captcha)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='fn_JLoginSubmit()']"))).click()

    time.sleep(4)

    if driver.find_elements(By.ID, "exmsg"):
        print("Login failed")

    elif driver.find_elements(By.XPATH, "//h6[normalize-space()='Change Password']"):

        current_pwd = input("Enter Current Password: ")
        new_pwd = input("Enter New Password: ")

        wait.until(EC.presence_of_element_located((By.ID, "txtCurrentPassword"))).send_keys(current_pwd)
        wait.until(EC.presence_of_element_located((By.ID, "txtNewPassword"))).send_keys(new_pwd)
        wait.until(EC.presence_of_element_located((By.ID, "txtConfirmPassword"))).send_keys(new_pwd)

        wait.until(EC.element_to_be_clickable((By.ID, "back"))).click()

    time.sleep(5)

    if driver.find_elements(By.XPATH, "//h3[normalize-space()='Valid']"):
        print("Its already success")

    elif driver.find_elements(By.XPATH, "//a[contains(@class,'apply-iec-info')]"):
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'apply-iec-info')]"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "modifyIEC"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "btnNewApp"))).click()

    # ---------------- USER INPUT SECTION ----------------

    nature = input("Nature of concern (Proprietorship/Partnership/etc): ")
    Select(wait.until(EC.presence_of_element_located((By.ID, "constitutionType")))).select_by_visible_text(nature)

    firm_name = input("Enter Firm Name: ")
    driver.find_element(By.ID, "entityName").clear()
    driver.find_element(By.ID, "entityName").send_keys(firm_name)

    pan = input("Enter PAN Number: ")
    driver.execute_script("document.getElementById('panNumber').removeAttribute('disabled')")
    driver.find_element(By.ID, "panNumber").clear()
    driver.find_element(By.ID, "panNumber").send_keys(pan)

    pan_name = input("Enter Name as per PAN: ")
    driver.find_element(By.ID, "nameAsPan").clear()
    driver.find_element(By.ID, "nameAsPan").send_keys(pan_name)

    dob = input("Enter DOB (DD/MM/YYYY): ")
    birth = driver.find_element(By.ID, "birthdate")
    birth.clear()
    for ch in dob:
        birth.send_keys(ch)
        time.sleep(0.1)

    category = input("Category of Exporters: ")
    Select(driver.find_element(By.ID, "preferred")).select_by_visible_text(category)

    sez = input("Is firm in SEZ? (YES/NO): ").upper()
    if sez == "YES":
        driver.find_element(By.ID, "SEZ1").click()
    else:
        driver.find_element(By.ID, "SEZ2").click()

    eou = input("Is firm in EOU? (YES/NO): ").upper()
    if eou == "YES":
        driver.find_element(By.ID, "EOU1").click()
    else:
        driver.find_element(By.ID, "EOU2").click()

    cin = input("Enter CIN / LLPIN: ")
    driver.execute_script("document.getElementById('cin').removeAttribute('disabled')")
    driver.find_element(By.ID, "cin").send_keys(cin)

    gst = input("Enter GSTIN: ")
    driver.find_element(By.ID, "gstin").send_keys(gst)

    mobile = input("Enter Firm Mobile: ")
    driver.find_element(By.ID, "addMobileid").clear()
    driver.find_element(By.ID, "addMobileid").send_keys(mobile)

    email = input("Enter Firm Email: ")
    driver.find_element(By.ID, "addEmail").clear()
    driver.find_element(By.ID, "addEmail").send_keys(email)

    # ---------------- FILE UPLOAD ----------------

    pdf_path = input("Enter PDF file path: ")
    driver.find_element(By.ID, "importFilegeneralAttach2490181").send_keys(pdf_path)

    input("Press Enter to exit...")
    driver.quit()