from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def saveScreenshot(webElement):
    webElement.save_screenshot("test.png")
    print(webElement)


driver = webdriver.Chrome("./chromedriver")

driver.get("https://github.com/IvanGaray")
sleep(3)
urls = []
try:
    testEvidence = driver.find_elements(
        By.CSS_SELECTOR, "a.mr-1.text-bold.wb-break-word"
    )

    for url in testEvidence:
        urls.append(url.get_attribute("href"))

    print(urls)
    ##saveScreenshot(testEvidence)

except:
    print("Something went wrong")


driver.close()
