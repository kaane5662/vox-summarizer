from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

import time


driver = webdriver.Chrome()
# time.sleep(3)
url ="https://www.indeed.com/jobs?q=software+engineer+intern"


page = 10
while(page < 100):
    driver.get(f"{url}&start={page}")
    time.sleep(.5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all('li', class_='eu4oa1w0')
    for job in jobs:
        title = job.find("span", id=lambda x: x and x.startswith("jobTitle"))
        anchor = job.find("a")
        recruiter = job.find("span", class_="css-92r8pb")
        link = anchor.get("href") if anchor else None
        recruiter = recruiter.text.strip() if recruiter else None
        pay = job.find("div", class_="css-1cvo3fd")
        pay = pay.text.strip() if pay else None
        if title:
            print(title.text.strip(),"\n", link, "\n",pay, "\n", recruiter, "\n")
            # print(job.prettify(),"\n\n")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    page += 10
    

driver.quit()