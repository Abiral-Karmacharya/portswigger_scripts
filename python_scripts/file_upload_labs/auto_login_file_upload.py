from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def image_upload(url):
    print("Starting to get image placeholder")

    driver = webdriver.Chrome()
    driver.get(url)
    if driver:
        print("Successfully got the url")
        login(driver)
    else:
        print("Url could not be fetched")
    time.sleep(5)

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_btn = driver.find_element(By.XPATH, "//button[contains(., 'Upload')]")
    if file_input:
        file_loc = input("Enter the file location")
        file_input.send_keys(file_loc)
        file_btn.click()
        
    else: 
        print("File placeholder could not be fetched")
    time.sleep(2)

    driver.quit()

def login(driver):

    time.sleep(2)

    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")  
    username.send_keys("wiener")

    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")  
    password.send_keys("peter")

    login_btn = driver.find_element(By.XPATH, "//button[contains(.,'Log in')]")  
    login_btn.click()

    time.sleep(3)


