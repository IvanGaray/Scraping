from time import sleep
from turtle import title
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("headless")


driver = webdriver.Chrome("./chromedriver", options=options)

# We define a function that get an array and return a new one with the text attribute of each element of the first
def getElementsText(array):
    textList = []
    for element in array:
        textList.append(element.text)
    return textList


driver.get("https://github.com/IvanGaray")
sleep(3)
urls = []
titles = []

try:
    testEvidence = driver.find_elements(
        By.CSS_SELECTOR, "a.mr-1.text-bold.wb-break-word"
    )
    webTitle = driver.find_elements(By.CSS_SELECTOR, "span.repo")

    for url in testEvidence:
        urls.append(url.get_attribute("href"))
    for title in webTitle:
        titles.append(title.text)

    print(urls)
    print(titles)
    driver.save_screenshot("./evidence/main.png")

except:
    print("Something went wrong")
    driver.close()

# Now we have to use that list of links and go trought it to get the data we want.

js = []
ts = []
css = []
html = []


for url in urls:
    driver.get(url)
    sleep(3)
    try:
        txtjs = driver.find_elements(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(3)>a>span:nth-child(3)",
        )
        txtTs = driver.find_elements(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(3)>a>span:nth-child(3)",
        )
        txtCSS = driver.find_elements(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(3)>a>span:nth-child(3)",
        )
        txtHTML = driver.find_elements(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(3)>a>span:nth-child(3)",
        )
        js.append(getElementsText(txtjs))
        ts.append(getElementsText(txtTs))
        css.append(getElementsText(txtCSS))
        html.append(getElementsText(txtHTML))
        driver.save_screenshot("./evidence/" + url.split("IvanGaray/")[1] + ".png")
    except:
        print("Something went wrong")
        driver.close()
print("Finished!")

# Making the structure using the data
data_repositories = {
    "title": titles,
    "CSS": css,
    "HTML": html,
    "JavaScript": js,
    "TypeScript": ts,
}

df = pd.DataFrame(data_repositories)

# Save it into a CSV file
df.to_csv("./evidence/repositories.csv")

driver.close()
