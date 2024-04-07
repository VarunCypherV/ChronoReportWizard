import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
from mailsender import sendEmail

def crawlerImage(reportName, search_url, name, email):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(search_url)

    # search_input = driver.find_element(By.ID, "twotabsearchtextbox")  # Locate the search input field on Amazon
    search_input = driver.find_element(By.NAME, "field-keywords")
    search_input.clear()
    search_input.send_keys(reportName)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    
    screenshot_path = "images/" + name + "_" + reportName + ".png"
    if not os.path.exists("images"):
        os.makedirs("images")
    
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # PIL saving the image
    img = Image.open(screenshot_path)
    img.save(screenshot_path)
    
    sendEmail(screenshot_path, email)

