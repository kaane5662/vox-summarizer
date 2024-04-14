from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

import time

url = "https://www.vox.com/culture/2024/3/22/24107807/caitlin-clark-basketball-iowa-march-madness-stats"


def scrape_vox(url):

    try:
        source = requests.get(url)
        soup = BeautifulSoup(source.content,"html.parser")
        queries = str.split(url, "/")
        article_content = soup.find("div",class_="c-entry-content")
        children = article_content.children
        for child in children:
            if child.name != "p":
                continue
            text:str = child.text.strip()
            print(text,"\n")
        article_header = soup.find("div", class_="c-entry-hero")
        article_title = article_header.find("h1", class_="c-page-title").text.strip()
        article_category = [ label.find("span").text.strip() for label in article_header.find_all("li", class_="c-entry-group-labels__item") ]
        article_author = article_header.find("span", class_="c-byline__author-name").text.strip()
        print(article_title, "\n")
        print(article_category, "\n")
        print(article_author, "\n")
        
    except Exception as e:
        print("An unexpected error has occured:",e)

        
scrape_vox(url)
    
