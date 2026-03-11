from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import os
import base64
import tempfile
import datetime

# =============================== #
#          Color Logger           #
# =============================== #
import logging
import colorlog

handler = colorlog.StreamHandler()

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

handler.setFormatter(formatter)

log = colorlog.getLogger()
log.addHandler(handler)
log.setLevel(logging.INFO)

# =============================== #
#          Normal Logger          #
# =============================== #

# import logging as log
# log.basicConfig(level=log.INFO,format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d - %(name)s")
# log.info("Debug message")
# log.info("Program started")
# log.warning("Low disk space")
# log.error("File not found")
# log.critical("System crash")

def clipboard(value):
    pyperclip.copy(value)
    time.sleep(1)

def startup_india(data):
    log.info("Program started")
    error = ""
    data = data or {}
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # Selenium 4.6+ selenium-manager auto-downloads Chrome + ChromeDriver
        # Set cache dir to writable path on Render
        import os
        os.environ["SE_CACHE_PATH"] = "/tmp/selenium"
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get("https://www.nsws.gov.in/")        

        wait = WebDriverWait(driver, 15)
        log.info("Page opened")

        # Close popups
        wait.until(EC.element_to_be_clickable((By.ID, "close-popup"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "close1-popup"))).click()

        # =============================== #
        #       Login navigation          #
        # =============================== #      

        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button"))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Business User Login"))).click()

        # Credentials
        username_value = data.get("username")
        password_value = data.get("password")
        

        wait.until(EC.visibility_of_element_located((By.ID, "username"))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username_value)
        

        wait.until(EC.visibility_of_element_located((By.ID, "userPassword"))).clear()
        wait.until(EC.visibility_of_element_located((By.ID, "userPassword"))).send_keys(password_value)
        

        wait.until(EC.element_to_be_clickable((By.ID, "kc-login"))).click()
        log.info("Credentials fetched")

        # =============================== #
        #       Login validation          #
        # =============================== #       

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "input-error-email-login")))
            driver.quit()
            log.error("Login failed")
        except TimeoutException:
            log.info("Login successful")

            # =============================== #
            #       Dashboard navigation      #
            # =============================== #      

            # Bussiness Name to click  
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".content-list"))).click()
            # Apply Button to click this line
            #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.action-button"))).click()
            time.sleep(15)
            if driver.find_elements(By.CSS_SELECTOR, ".button.action-button"):
                log.info("Apply button show")
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.action-button"))).click()
                time.sleep(10)
            else:
                log.warning("Apply button not show")
                main_window = driver.current_window_handle
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.search-icon"))).click()
                search_box = wait.until(EC.presence_of_element_located((By.NAME, "global_search")))
                search_box.clear()
                for ch in "Registration as a Startup":
                    search_box.send_keys(ch)
                    time.sleep(0.2)
                wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Registration as a Startup')]"))).click()
                wait.until(EC.number_of_windows_to_be(2))
                for window in driver.window_handles:
                    if window != main_window:
                        driver.switch_to.window(window)
                        break
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add to Dashboard']"))).click()
                driver.close()
                driver.switch_to.window(main_window)
                driver.refresh()
                time.sleep(10)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.action-button"))).click()        
                log.info("Apply button clicked")    

            # =============================== #
            #       Start Page started        #
            # =============================== #    

            log.info("Start Page started")  

            # Click the visible selector area (NOT the input)
            selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.document-type-control .ant-select-selector")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", selector)
            selector.click()

            # Wait for dropdown options container
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown")))

            # Type text and press ENTER (most reliable for Ant Design)
            search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input.ant-select-selection-search-input")))
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys("Company Logo")
            search_input.send_keys(Keys.ENTER)

            #####################################
            # # Click Browse button (optional if modal not already open)
            # browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Browse File']]")))
            # browse_btn.click()

            # # Wait for modal file input
            # file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@type='file']")))
            # # Upload file directly (NO popup handling)
            # logo_file = data.get("lOGO_file")
            # if logo_file: file_input.send_keys(logo_file)
            #########################################
            # Click Browse button
            browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Browse File']]")))
            browse_btn.click()

            # Wait for file input
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@type='file']")))
            # Get base64 string
            logo_base64 = data.get("lOGO_file")
            if logo_base64:    
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, "logo.png")
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(logo_base64))
                file_input.send_keys(file_path)          
            time.sleep(3)
            os.remove(file_path)

            # Textarea using CLASS (dynamic name/id handled)
            #about_text = data.get("aboutcompany")

            #textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.ant-input.caf-textarea-control")))
            #textarea.clear()
            #textarea.send_keys(about_text)
            #about_text = data.get("aboutcompany")

            #textarea = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ant-input.caf-textarea-control")))
            #driver.execute_script("arguments[0].value = arguments[1];", textarea, about_text)
            # time.sleep(5)

            # website_value = data.get("website")
            # website_input = wait.until(EC.visibility_of_element_located((By.ID, "Website")))
            # website_input.clear()
            # website_input.send_keys(website_value)
            about_text = data.get("aboutcompany")
            clipboard(about_text)

            textarea = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.ant-input.caf-textarea-control")))
            textarea.click()
            textarea.send_keys(Keys.CONTROL, "v")

            website_value = data.get("website")
            clipboard(website_value)
            website_input = wait.until(EC.visibility_of_element_located((By.ID, "Website")))
            website_input.clear()
            website_input.send_keys(website_value)

            # Open the dropdown
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name^='you_are_interested_in'] .ant-select-selector"))).click()
            # Click all options one by one
            options = ["Investors", "Mentors", "Other Startups", "Incubators", "Accelerators"]
            for option in options:
                wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{option}']"))).click()
            # Wait until checkbox container is visible
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.nsws-field.form-declaration")))

            # Click using the LABEL (recommended for Ant Design checkboxes)
            terms_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ant-checkbox-wrapper")))
            driver.execute_script("arguments[0].click();", terms_label)

            # Click "Start Up Profile" collapse header
            element = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Start Up Profile']/ancestor::div[@class='ant-collapse-header']")))

            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            # Small wait (optional but safe)
            time.sleep(1)
            # Click
            element.click()
            time.sleep(2)

            log.info("Start Up Profile Complete")

            # =============================== #
            #       Entity Details            #
            # =============================== #

            log.info("Entity Details Started")

            # Click "Entity Details" collapse header

            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Entity Details']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            # Open Industry dropdown
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name^='industry_'] .ant-select-selector"))).click()

            # Type AI in search box
            search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[name^='industry_'] input.ant-select-selection-search-input")))
            search_box.send_keys(data.get("Industry"))

            # Select AI option
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{}']".format(data.get('Industry'))))).click()

            time.sleep(3)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='rc_select_5']/ancestor::div[contains(@class,'ant-select-selector')]"))).click()

            # Now send keys directly to active element
            driver.switch_to.active_element.send_keys(data.get("Sector"))

            # Select NLP option
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{}']".format(data.get('Sector'))))).click()

            # Open Categories dropdown (click selector, not input)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select') and starts-with(@name,'categories_')]//div[contains(@class,'ant-select-selector')]"))).click()

            # # Options from image
            # options_to_select = data.get("Catogries")

            # for option in options_to_select:
            #     wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[normalize-space()='{option}']"))).click()

            # # Close dropdown by clicking outside
            # driver.execute_script("document.body.click();")

            # options_to_select = data.get("Catogries")

            # for option in options_to_select:
            #     element = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class,'ant-select-dropdown')]//span[normalize-space()='{option}']")))

            #     # Scroll the option into view
            #     time.sleep(1)
            #     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

            #     # Click the option
            #     wait.until(EC.element_to_be_clickable(element)).click()

            options_to_select = data.get("Catogries")

            # 1️⃣ Open Categories dropdown
            dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[.//span[text()='Categories']]/following::div[contains(@class,'ant-select-selector')][1]")))
            driver.execute_script("arguments[0].click();", dropdown)

            time.sleep(1)

            # 2️⃣ Locate all search inputs and pick the 6th one
            search_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.ant-select-selection-search-input")))

            search_input = search_inputs[5]   # 6th search box

            # 3️⃣ Loop through categories
            for option in options_to_select:
                # Type category name
                search_input.send_keys(option)
                # Wait for filtered option
                option_xpath = f"//span[contains(@class,'ant-select-tree-title') and normalize-space()='{option}']"
                option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                # Click category
                driver.execute_script("arguments[0].click();", option_element)
                time.sleep(0.5)
                # Clear search box
                search_input.clear()

            # 4️⃣ Close dropdown
            driver.execute_script("document.body.click();")

            elements=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Entity Details']/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elements)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", elements)

            time.sleep(1)
            log.info("Entity Details Completed")

            # =============================== #
            #       Full Address(Office)      #
            # =============================== #

            log.info("Full Address(Office) Started")

            # Click "Full Address(Office)" collapse header

            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Full Address(Office)']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(1)
            element.click()
            time.sleep(1)

            # Open State dropdown
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@name,'state_')]//div[contains(@class,'ant-select-selector')]"))).click()

            # Type Tamil Nadu
            state=data.get("comp_address", {}).get("state")
            clipboard(state)
            driver.switch_to.active_element.send_keys(Keys.CONTROL, "v")

            # Select Tamil Nadu option
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{}']".format(state)))).click()

            time.sleep(2)
            # Open District dropdown
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@name,'district_')]//div[contains(@class,'ant-select-selector')]"))).click()

            # Type Chennai
            district=data.get("comp_address", {}).get("district")
            clipboard(district)
            driver.switch_to.active_element.send_keys(Keys.CONTROL, "v")

            # Select Chennai option
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{}']".format(district)))).click()
            time.sleep(2)
            # Enter City / Village

            city_value = data.get("comp_address", {}).get("city")
            clipboard(city_value)
            city_input = wait.until(EC.visibility_of_element_located((By.ID, "City/Village")))
            city_input.clear()
            city_input.send_keys(Keys.CONTROL, "v")

            # Enter Pin Code

            pin_value = data.get("comp_address", {}).get("pincode")
            clipboard(pin_value)
            pin_input = wait.until(EC.visibility_of_element_located((By.ID, "Pin Code")))
            pin_input.clear()
            pin_input.send_keys(Keys.CONTROL, "v")

            time.sleep(1)

            element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Full Address(Office)']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            log.info("Full Address(Office) Completed")

            # =========================================== #
            #       Authorized Representative Details     #
            # =========================================== #

            log.info("Authorized Representative Details Started")

            # Click "Authorized Representative Details" collapse header

            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Authorized Representative Details']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            wait = WebDriverWait(driver, 20)

            # Fill Name
            name_value = data.get("directors", [{}])[0].get("Name")
            clipboard(name_value)
            wait.until(EC.visibility_of_element_located((By.ID, "Name"))).clear()
            wait.until(EC.visibility_of_element_located((By.ID, "Name"))).send_keys(Keys.CONTROL, "v")

            # Fill Designation
            designation_value = data.get("directors", [{}])[0].get("Designation", "Director")
            clipboard(designation_value)
            wait.until(EC.visibility_of_element_located((By.ID, "Designation"))).clear()
            wait.until(EC.visibility_of_element_located((By.ID, "Designation"))).send_keys(Keys.CONTROL, "v")

            # Fill Mobile Number
            mobile_value = data.get("mobile_no")#data.get("directors", [{}])[0].get("Mobile_no")
            clipboard(mobile_value)
            wait.until(EC.visibility_of_element_located((By.ID, "Mobile Number"))).clear()
            wait.until(EC.visibility_of_element_located((By.ID, "Mobile Number"))).send_keys(Keys.CONTROL, "v")

            # Fill Email Address
            email_value = data.get("username") #data.get("directors", [{}])[0].get("Email")
            clipboard(email_value)
            wait.until(EC.visibility_of_element_located((By.ID, "Email Address"))).clear()
            wait.until(EC.visibility_of_element_located((By.ID, "Email Address"))).send_keys(Keys.CONTROL, "v")
            otp = data.get("otp")
            log.info(f"OTP: {otp}")
            if otp=="1":
                log.critical("Otp will be triggered")
                ##paste the code
                # Click Mobile Get OTP
                wait.until(EC.element_to_be_clickable((By.ID, "CheckMobileVerification"))).click()
                time.sleep(2)
                # Click Email Get OTP
                # Wait until Email OTP button is enabled
                wait.until(lambda d: d.find_element(By.ID, "CheckEmailVerification").is_enabled())
                email_btn = driver.find_element(By.ID, "CheckEmailVerification")
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", email_btn)
                # CLICK OUTSIDE (very important for Ant Design forms)
                driver.execute_script("document.body.click();")
                # Small wait for UI settle
                wait.until(lambda d: email_btn.is_displayed())
                # Now click Email Get OTP
                email_btn.click()
                # Enter Mobile OTP (without using dynamic name)
                # ── Wait for OTP from browser via queue ──
                otp_req_q  = data.get("_otp_request_queue")
                otp_resp_q = data.get("_otp_response_queue")
                if otp_req_q:
                    log.info("Sending OTP request signal to browser...")
                    otp_req_q.put({"event": "otp_needed", "message": "Enter Mobile OTP and Email OTP"})
                    log.info("Waiting for OTP from browser (up to 5 minutes)...")
                    otp_data = otp_resp_q.get(timeout=300)
                    mobile_otp = otp_data.get("mobile_otp", "")
                    email_otp  = otp_data.get("email_otp", "")
                else:
                    mobile_otp = input("Enter Mobile OTP: ")
                    email_otp  = input("Enter Email OTP: ")
                mobile_otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[.//span[text()='Mobile Number']]/following::input[@type='password'][1]")))
                driver.execute_script("arguments[0].removeAttribute('disabled')", mobile_otp_input)     
                mobile_otp_input.clear()
                mobile_otp_input.send_keys(mobile_otp)
                log.critical(f"Mobile OTP: {mobile_otp}")
                # Enter Email OTP (without using dynamic name)
                email_otp_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[.//span[text()='Email Address']]/following::input[@type='password'][1]")))
                driver.execute_script("arguments[0].removeAttribute('disabled')", email_otp_input)
                email_otp_input.clear()
                email_otp_input.send_keys(email_otp)
                log.critical(f"Email OTP: {email_otp}")
                # Click both Validate buttons
                validate_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[normalize-space()='Validate']")))
                for btn in validate_buttons:
                    time.sleep(2)
                    driver.execute_script("arguments[0].removeAttribute('disabled')", btn)
                    btn.click()
                ##paste the code 

            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Authorized Representative Details']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            # Click "Director(s) / Partner(s) Details" collapse header

            time.sleep(2)
            log.info("Director(s) / Partner(s) Details")

            # wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Director(s) / Partner(s) Details']/ancestor::div[contains(@class,'ant-collapse-header')]"))).click()

            # =========================================== #
            #       Director(s) / Partner(s) Details      #
            # =========================================== #
            log.info("Director(s) / Partner(s) Details Started")

            no_of_dir = len(data.get("directors"))
            wait = WebDriverWait(driver, 20)
            flag=True

            for i in range(no_of_dir):


                # ===============================
                # GET DIRECTOR SECTIONS ONLY
                # ===============================
                director_sections = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'ant-collapse-item')][.//span[contains(text(),'Director(s) / Partner(s) Details')]]")))

                section = director_sections[i]

                # ===============================
                # OPEN SECTION
                # ===============================
                header = section.find_element(By.XPATH,".//div[contains(@class,'ant-collapse-header')]")

                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", header)
                driver.execute_script("arguments[0].click();", header)

                # Wait until active
                wait.until(lambda d: "active" in section.find_element(By.XPATH,".//div[contains(@class,'ant-collapse-content')]").get_attribute("class"))

                content = section.find_element(By.XPATH,".//div[contains(@class,'ant-collapse-content-active')]")

                # ===============================
                # NAME
                # ===============================
                dir_name=data.get("directors", [{}])[i].get("Name", f"Director {i+1}")
                clipboard(dir_name)
                name_input = content.find_element(By.XPATH, ".//input[contains(@name,'name_')]")
                name_input.clear()
                name_input.send_keys(Keys.CONTROL, "v")

                # ===============================
                # GENDER
                # ===============================
                gender_box = content.find_element(By.XPATH, ".//div[starts-with(@name,'gender_')]")
                selector = gender_box.find_element(By.CLASS_NAME, "ant-select-selector")
                driver.execute_script("arguments[0].click();", selector)

                gender_input = gender_box.find_element(By.XPATH,".//input[contains(@class,'ant-select-selection-search-input')]")

                gender_input.send_keys(data.get("directors", [{}])[i].get("Gender", "Male"))
                gender_input.send_keys(Keys.RETURN)

                # ===============================
                # MOBILE
                # ===============================
                dir_mobile=data.get("directors", [{}])[i].get("Mobile_no")
                clipboard(dir_mobile)
                mobile_input = content.find_element(By.XPATH, ".//input[@name='phoneNumber']")
                mobile_input.clear()
                mobile_input.send_keys(Keys.CONTROL, "v")

                # ===============================
                # ADDRESS
                # ===============================
                dir_address=data.get("directors", [{}])[i].get("Address")
                clipboard(dir_address)
                postal_input = content.find_element(By.XPATH, ".//input[contains(@name,'postal_address')]")
                postal_input.clear()
                postal_input.send_keys(Keys.CONTROL, "v")

                # ===============================
                # EMAIL
                # ===============================
                dir_email=data.get("directors", [{}])[i].get("Email")
                clipboard(dir_email)
                email_input = content.find_element(By.XPATH, ".//input[contains(@name,'email_address')]")
                email_input.clear()
                email_input.send_keys(Keys.CONTROL, "v")


                # ===============================
                # ADD SECTION IF NEEDED
                # ===============================
                if flag==True:
                    flag=False
                    for j in range(no_of_dir-1):
                        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'+ Add Section')]")))
                        driver.execute_script("arguments[0].click();", add_button)
                        time.sleep(1)

                driver.execute_script("arguments[0].click();", header)
            
            log.info("Director(s) / Partner(s) Details Completed")


            # =========================================== #
            #       Information required                  #
            # =========================================== #
            log.info("Information required Started")

            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Information required']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            employees_value = data.get("no_of_emp") #input("Enter Current Number of Employees (including founders): ")

            employees_input = wait.until(EC.visibility_of_element_located((By.ID, "Current Number of Employees(including founders)")))
            employees_input.clear()
            employees_input.send_keys(employees_value)

            # Open dropdown (click parent selector)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='rc_select_11']/ancestor::div[contains(@class,'ant-select-selector')]"))).click()

            # Type Ideation
            stage=data.get("stage")
            driver.switch_to.active_element.send_keys(stage)

            # Select Ideation option
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='{}']".format(stage)))).click()

            # Click "No" radio button

            no_radio_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and @value='No']")))
            driver.execute_script("arguments[0].click();", no_radio_input)
            
            element=wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Information required']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(1)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)

            log.info("Information required Completed")

            # =========================================== #
            #       Nature of Startup                     #
            # =========================================== #

            log.info("Nature of Startup Started")

            nature_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Nature of Startup']/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", nature_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", nature_header)

            # Open "Nature of Startup" dropdown
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[starts-with(@name,'please_define_nature_of_your_startup_')]//div[contains(@class,'ant-select-selector')]"))).click()

            # Type Innovative
            driver.switch_to.active_element.send_keys("Innovative and Scalable")

            # Select "Innovative and Scalable"
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ant-select-item-option-content') and normalize-space()='Innovative and Scalable']"))).click()

            nature_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Nature of Startup']/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", nature_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", nature_header)

            log.info("Nature of Startup Completed")

            # ======================================================= #
            #       Is the startup creating an innovative product...  #
            # ======================================================= #

            log.info("Is the startup creating an innovative product Started")

            innovation_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Is the startup creating an innovative product')]/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", innovation_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", innovation_header)

            yes_radio_label = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Yes' and contains(@name,'is_the_startup_creating')]/ancestor::label")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", yes_radio_label)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", yes_radio_label)


            time.sleep(1)
            
            product_improvement = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'product_') and @value='Improvement']/ancestor::label")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", product_improvement)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", product_improvement)

            service_improvement = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'service_') and @value='Improvement']/ancestor::label")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", service_improvement)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", service_improvement)

            process_improvement = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'process_') and @value='Improvement']/ancestor::label")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", process_improvement)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", process_improvement)

            innovation_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Is the startup creating an innovative product')]/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", innovation_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", innovation_header)

            log.info("Is the startup creating an innovative product Completed")
            
            # =========================================================== #
            #       Is the startup creating a scalable business model...  #
            # =========================================================== #

            log.info("Is the startup creating a scalable business model Started")

            scalable_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Is the startup creating a scalable business model')]/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", scalable_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", scalable_header)

            # Select "Yes" for scalable business model question

            scalable_yes = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'is_the_startup_creating_a_scalable_business_model') and @value='Yes']/ancestor::label")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", scalable_yes)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", scalable_yes)
            
            time.sleep(1)

            # Check both checkboxes: Employment Generation & Wealth Creation

            checkbox_values = ["Employment Generation", "Wealth Creation"]

            for value in checkbox_values:
                checkbox_label = wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@type='checkbox' and @value='{value}']/ancestor::label")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_label)
                driver.execute_script("document.body.click();")
                driver.execute_script("arguments[0].click();", checkbox_label)
                
            scalable_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Is the startup creating a scalable business model')]/ancestor::div[contains(@class,'ant-collapse-header')]")))
            
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", scalable_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", scalable_header)

            log.info("Is the startup creating a scalable business model Completed")

            # ========================================= #
            #       Fill brief note textarea ....       #
            # ========================================= #

            log.info("Fill brief note textarea Started")

            note_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Please submit a brief note supporting')]/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", note_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", note_header)


            # Fill brief note textarea (min 500 characters required)

            brief_note = data.get("who_we_are")

            textarea = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@name,'please_submit_a_brief_note_supporting')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", textarea)
            pyperclip.copy(brief_note)
            textarea.click()
            textarea.send_keys(Keys.CONTROL, "v")



            note_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Please submit a brief note supporting')]/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", note_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", note_header)

            # Click "Has your startup received any funding" collapse header safely

            funding_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Has your startup received any funding']/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", funding_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", funding_header)

            # Click "No" for funding question safely (Ant Design radio)

            funding_no = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'has_your_startup_received_any_funding') and @value='No']/ancestor::label")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", funding_no)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", funding_no)

            # Click "Has your startup received any funding" collapse header safely

            funding_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Has your startup received any funding']/ancestor::div[contains(@class,'ant-collapse-header')]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", funding_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", funding_header)

            log.info("Has your startup received any funding Completed")

            # ==================================== #
            #       Startup Activities ....        #
            # ==================================== #

            log.info("Startup Activities Started")

            # Click "Startup Activities" collapse header safely

            activities_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Startup Activities']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", activities_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", activities_header)

            # Click "No" for recognition/awards question safely

            recognition_no = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'any_recognition_or_awards_received_by_the_startup') and @value='No']/ancestor::label")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", recognition_no)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", recognition_no)


            # Fill "What is the problem the startup is solving?" (min 500 characters)

            problem_text = data.get("problem_statement")
            problem_textarea = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@name,'what_is_the_problem_the_startup_is_solving')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", problem_textarea)
            clipboard(problem_text)
            problem_textarea.click()
            problem_textarea.send_keys(Keys.CONTROL, "v")

            # Fill "How does the startup propose to solve the problem?" (min 500 characters)

            solution_text = data.get("solution")
            solution_textarea = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@name,'how_does_the_startup_propose_to_solve_the_problem')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", solution_textarea)
            clipboard(solution_text)
            solution_textarea.click()
            solution_textarea.send_keys(Keys.CONTROL, "v")

            # Fill "What is the uniqueness of the solution?" (min 500 characters)

            uniqueness_text = data.get("uniqueness")
            uniqueness_textarea = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@name,'what_is_the_uniqueness_of_the_solution')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", uniqueness_textarea)
            clipboard(uniqueness_text)
            uniqueness_textarea.click()
            uniqueness_textarea.send_keys(Keys.CONTROL, "v")

            # Fill "How does the startup generate revenue?" (min 500 characters)

            revenue_text = data.get("revenue_growth")
            revenue_textarea = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@name,'how_does_the_startup_generate_revenue')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", revenue_textarea)
            clipboard(revenue_text)
            revenue_textarea.click()
            revenue_textarea.send_keys(Keys.CONTROL, "v")
                    
            activities_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Startup Activities']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", activities_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", activities_header)

            log.info("Startup Activities Completed")

            # ============================================ #
            #       Support Documents ....(pitch deck)     #
            # ============================================ #

            log.info("Support Documents Started")

            # Click collapse header:
            # "1. Please provide links or upload additional document..."
            time.sleep(1)
            support_doc_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Please provide links or upload additional document')]/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", support_doc_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", support_doc_header)
            time.sleep(2)

            # ===== SELECT TYPE : Pitch Deck =====
            # type_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[.//span[text()='Type']]/following::input[contains(@class,'ant-select-selection-search-input')][1])[1]")))

            # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", type_input)

            # type_input.click()
            # type_input.send_keys(Keys.CONTROL + "a")
            # type_input.send_keys(Keys.DELETE)
            # time.sleep(1)

            # type_input.send_keys("Pitch Desk")
            # time.sleep(2)
            # type_input.send_keys(Keys.ENTER)

            try:
                type_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[.//span[text()='Type']]/following::input[contains(@class,'ant-select-selection-search-input')][1])[1]")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", type_input)
                type_input.click()
                type_input.send_keys(Keys.CONTROL + "a")
                type_input.send_keys(Keys.DELETE)
                time.sleep(1)
                type_input.send_keys("Pitch Desk")
                time.sleep(2)
                type_input.send_keys(Keys.ENTER)
                # # open Type dropdown
                # wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[.//span[text()='Type']]/following::div[contains(@class,'ant-select-selector')][1])[1]"))).click()

                # # select Pitch desk
                # # wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'ant-select-tree-title') and normalize-space()='Pitch desk']")).click()
                # # type_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[last()-3]")))
                # # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", type_input)
                # # type_input.click()
                # # wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[14]"))).click()
                # # time.sleep(1)
                # # type_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[14]")))
                # # driver.execute_script("arguments[0].scrollIntoView({block:'center'});", type_input)
                # # type_input.click()
                # type_input.send_keys(Keys.CONTROL + "a")
                # type_input.send_keys(Keys.DELETE)
                # for ch in "Pitch desk":
                #     type_input.send_keys(ch)
                #     time.sleep(0.15)
                # # click checkbox for "Pitch desk"
                # time.sleep(1)
                # wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Pitch desk']/ancestor::div[contains(@class,'ant-select-tree-treenode')]//span[contains(@class,'ant-select-tree-checkbox')]"))).click()
                # time.sleep(2)
                # open Type dropdown
            except:
                wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[.//span[text()='Type']]/following::div[contains(@class,'ant-select-selector')][1])[1]"))).click()
                type_input = wait.until(EC.presence_of_element_located((By.XPATH, "//label[.//span[text()='Type']]/following::input[contains(@class,'ant-select-selection-search-input')][1]")))
                type_input.send_keys(Keys.CONTROL + "a")
                type_input.send_keys(Keys.DELETE)
                for ch in "Pitch desk":
                    type_input.send_keys(ch)
                    time.sleep(0.15)
                time.sleep(1)
                pitch_option = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'ant-select-tree-title') and normalize-space()='Pitch desk']")))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pitch_option)
                driver.execute_script("arguments[0].click();", pitch_option)
                time.sleep(2)
                type_input.send_keys(Keys.ESCAPE)
                time.sleep(2)

            # ===== SELECT SUBTYPE : Others =====
            subtype_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[last()-3]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", subtype_input)
            subtype_input.click()
            subtype_input.send_keys(Keys.CONTROL + "a")
            subtype_input.send_keys(Keys.DELETE)
            subtype_input.send_keys("Others")
            time.sleep(1)
            subtype_input.send_keys(Keys.ENTER)
            time.sleep(2)

            ################################$$$$$$$$$$$$$$$$$$$$$$
            # Click Browse button first 
            # browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='Browse File']])[2]"))) 
            # browse_btn.click() 
            # # Wait for modal 
            # #wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))) 
            # # Locate correct file input inside dialog 
            # #file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@type='file']"))) 
            # # Upload file 
            # pd_file = data.get("pitchdesk_file") 
            # if pd_file: file_input.send_keys(pd_file) 
            # # Wait for file input inside modal dialog 
            # file_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@role='dialog']//input[@type='file'])[2]"))) 
            # # Upload PDF file 
            # pd_file = data.get("pitchdesk_file") 
            # if pd_file: file_input.send_keys(pd_file)
            ################################################################
            browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[.//span[text()='Browse File']])[2]")))
            browse_btn.click()
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@role='dialog'])[2]")))
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@role='dialog']//input[@type='file'])[2]")))
            pd_base64 = data.get("pitchdesk_file")
            if pd_base64:
                if "," in pd_base64:
                    pd_base64 = pd_base64.split(",")[1]
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, "pitchdeck.pdf")
                print(file_path)
                time.sleep(2)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(pd_base64))
                time.sleep(5)
                file_input.send_keys(file_path)
                time.sleep(2)
                os.remove(file_path)   
            time.sleep(10)         
            support_doc_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(),'Please provide links or upload additional document')]/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", support_doc_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", support_doc_header)

            log.info("Support Documents Completed")

            # ==================================== #
            #       Self Certification ....        #
            # ==================================== #

            log.info("Self Certification Started")

            self_cert_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Self Certification']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", self_cert_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", self_cert_header)

            log.info("Self Certification Completed")

            # -------- SELECT CERTIFICATE OF INCORPORATION --------

            coi_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[last()-1]")))

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", coi_input)
            coi_input.click()

            coi_input.send_keys(Keys.CONTROL + "a")
            coi_input.send_keys(Keys.DELETE)
            coi_input.send_keys("Certificate of Incorporation")
            time.sleep(1)
            coi_input.send_keys(Keys.ENTER)

            #######################################################
            # # 1️⃣ CLICK 4th BROWSE BUTTON
            # browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'browse-btn')])[4]")))
            # browse_btn.click()

            # # 2️⃣ WAIT FOR THE LATEST VISIBLE MODAL
            # active_modal = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@role='dialog' and contains(@class,'ant-modal')])[last()]")))
            # # 3️⃣ FIND FILE INPUT INSIDE THAT MODAL
            # file_input = active_modal.find_element(By.XPATH, ".//input[@type='file']")

            # # 4️⃣ UPLOAD FILE
            # coi_file = data.get("COI_file")
            # if coi_file: file_input.send_keys(coi_file)
            ############################################################
            browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'browse-btn')])[4]")))
            browse_btn.click()
            active_modal = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@role='dialog' and contains(@class,'ant-modal')])[last()]")))
            file_input = active_modal.find_element(By.XPATH, ".//input[@type='file']")
            coi_base64 = data.get("COI_file")
            if coi_base64:
                if "," in coi_base64:
                    coi_base64 = coi_base64.split(",")[1]
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, "COI.pdf")
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(coi_base64))
                file_input.send_keys(file_path)
                time.sleep(2)
                os.remove(file_path)
            time.sleep(3)
            select_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@class,'ant-select-selection-search-input')])[last()]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_input)
            select_input.click()

            select_input.send_keys(Keys.CONTROL + "a")
            select_input.send_keys(Keys.DELETE)
            select_input.send_keys("Authorization Letter")
            time.sleep(1)
            select_input.send_keys(Keys.ENTER)
            #######################################################################
            # # 1️⃣ CLICK 5th BROWSE BUTTON
            # browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'browse-btn')])[5]")))
            # browse_btn.click()

            # # 2️⃣ WAIT FOR THE LATEST VISIBLE MODAL
            # active_modal = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@role='dialog' and contains(@class,'ant-modal')])[last()]")))
            # # 3️⃣ FIND FILE INPUT INSIDE THAT MODAL
            # file_input = active_modal.find_element(By.XPATH, ".//input[@type='file']")

            # # 4️⃣ UPLOAD FILE
            # loa_file = data.get("LOA_file")
            # if loa_file: file_input.send_keys(loa_file)
            ##########################################################################
            browse_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'browse-btn')])[5]")))
            browse_btn.click()
            active_modal = wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@role='dialog' and contains(@class,'ant-modal')])[last()]")))
            file_input = active_modal.find_element(By.XPATH, ".//input[@type='file']")
            loa_base64 = data.get("LOA_file")
            if loa_base64:
                if "," in loa_base64:
                    loa_base64 = loa_base64.split(",")[1]
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, "LOA.pdf")
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(loa_base64))
                file_input.send_keys(file_path)
                time.sleep(2)
                os.remove(file_path)
            time.sleep(2)
            cert_checkboxes = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'form-declaration')]//input[@type='checkbox']")))
            for checkbox in cert_checkboxes:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)            
                is_checked = driver.execute_script("return arguments[0].checked;", checkbox)            
                if not is_checked:
                    driver.execute_script("arguments[0].click();", checkbox)
            first_radio_label = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[contains(@name,'please_select_either_of_the_below_options_applicable_for_the_entity')]/ancestor::label)[1]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", first_radio_label)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", first_radio_label)
            self_cert_header = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Self Certification']/ancestor::div[contains(@class,'ant-collapse-header')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", self_cert_header)
            driver.execute_script("document.body.click();")
            driver.execute_script("arguments[0].click();", self_cert_header)
            
            log.info("Auto-proceeding: Save as Draft")            
            draft_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'caf-save-as-draft')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", draft_button)
            driver.execute_script("arguments[0].click();", draft_button)
            time.sleep(5)
            log.info("Auto-proceeding: First Submit")
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'caf-review-submit')]")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_button)
            driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(2)
            status = driver.find_element(By.XPATH, "//span[contains(@class,'form-status-title')]").text
            if "Incomplete data" in status:
                print("Form is incomplete")
                sections = driver.find_elements(By.XPATH,"//span[contains(text(),'Incomplete data')]/ancestor::div[contains(@class,'ant-collapse-header')]")
                print(len(sections))
                return {"status":200,"message":"Form is incomplete","data":status,"sections":sections,"length":len(sections)}
            time.sleep(2)
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'ant-checkbox-inner')]")))
            driver.execute_script("arguments[0].click();", checkbox)
            log.info("Auto-proceeding: Final Submit")
            submit_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Submit Application']")
            print(submit_btn.is_enabled())            
            submit_btn.click()
            time.sleep(5)
            log.info("Auto-proceeding: After Final Submit")
            driver.find_element(By.CLASS_NAME, "sumbit-ok").click()
            time.sleep(5)

            max_retry = 10
            retry = 0

            while retry < max_retry:

                try:
                    # Wait for Approved status
                    approved = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//span[normalize-space()='Approved']")))
                    print("Approved status visible")
                    # Check download button
                    download_buttons = driver.find_elements(By.XPATH,"//span[normalize-space()='Download']")
                    if download_buttons:
                        print("Download button visible")
                        # Click download button
                        download_buttons[0].click()
                        print("Download started")
                        break
                    else:
                        print("Download button not visible, refreshing page")
                except Exception as e:
                    print("Waiting for elements...", e)
                retry += 1
                driver.refresh()
                time.sleep(3)

            if retry == max_retry:
                raise Exception("Download button not visible after 10 retries")

            #driver.quit()
    except Exception as e:
        error = e
        return e
    finally:
        #driver.quit()
        return {"status":200,"message":f"Success completed {error}","timestamp":datetime.datetime.now().isoformat()}
if __name__=='__main__':
    startup_india()