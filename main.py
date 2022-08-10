from logging import Logger, exception
from time import sleep
from turtle import title
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3


conn = sqlite3.connect("lunch.db")

c = conn.cursor()
# c.execute("""DROP TABLE repositories""")
c.execute("""CREATE TABLE repositories(title TEXT,language TEXT,precentage TEXT)""")


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


try:
    testEvidence = driver.find_elements(
        By.CSS_SELECTOR, "a.mr-1.text-bold.wb-break-word"
    )
    webTitle = driver.find_elements(By.CSS_SELECTOR, "span.repo")

    for url in testEvidence:
        urls.append(url.get_attribute("href"))

    print(urls)

    driver.save_screenshot("./evidence/main.png")

except:
    print("Something went wrong")
    driver.close()

# Now we have to use that list of links and go trought it to get the data we want.


mainLanguage = []
percentage = []


for url in urls:
    driver.get(url)
    sleep(3)
    try:
        repoTitle = driver.find_element(
            By.CSS_SELECTOR,
            "strong[itemprop=name]>a",
        ).text

        mainLanguage = driver.find_element(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(1)>a>span:nth-child(2)",
        ).text

        percentage = driver.find_element(
            By.CSS_SELECTOR,
            "div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div > div > div> div> ul>li:nth-child(1)>a>span:nth-child(3)",
        ).text
        # mainLanguage.append(getElementsText(txtLanguage))
        # percentage.append(getElementsText(txtPercentage))
        driver.save_screenshot("./evidence/" + url.split("IvanGaray/")[1] + ".png")
        c.execute(
            """INSERT INTO repositories VALUES(?,?,?)""",
            (repoTitle, mainLanguage, percentage),
        )
    except:
        print("something went so wrong")
        driver.close()
print("Finished!")
conn.commit()
# Making the structure using the data
# data_repositories = {
#    "title": title,
#    "main language": mainLanguage,
#    "percentage": percentage,
# }

# df = pd.DataFrame(data_repositories)

# Save it into a CSV file
df.to_csv("./evidence/repositories.csv")
# df.to_csv("./evidence/repositories.csv")

driver.close()
