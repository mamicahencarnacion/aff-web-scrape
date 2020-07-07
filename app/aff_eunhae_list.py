"""
    Created by Ma. Micah Encarnacion on 07/07/2020
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("/home/micahencarnacion/Downloads/chromedriver", options=chrome_options)

titles = []
links = []
authors = []
tags = []
views = []

for page in range(0, 2001, 20):
    print(f"Scraping Asianfanfics Eunhae Page {page}...")

    if not page:
        driver.get("https://www.asianfanfics.com/browse/tag/eunhae/S")
    else:
        driver.get(f"https://www.asianfanfics.com/browse/tag/eunhae/S/{page}")

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for section in soup.find_all("section", attrs={"class": "excerpt"}):
        this_story_tags = []
        if len(section["class"]) != 1:
            continue

        story_title = section.find("h1", attrs={"class": "excerpt__title"})
        story_author = section.find("div", attrs={"class": "excerpt__meta__name"})
        story_tags = section.find("div", attrs={"class": "excerpt__meta__tags"})
        story_views = section.find("div", attrs={"class": "excerpt__meta__views"})

        if not (story_title and story_tags and story_views):
            continue

        titles.append(story_title.text)
        links.append(story_title.a.get("href"))

        try:
            authors.append(story_author.a.text.strip())
        except AttributeError as ae:
            authors.append("")

        for tag in story_tags.children:
            try:
                this_story_tags.append(tag.text)
            except AttributeError as ae:
                continue
        tags.append(",".join(this_story_tags))

        views.append(story_views.span.text)

df = pd.DataFrame(
    {
        "title": titles,
        "link": links,
        "author": authors,
        "tag": tags,
        "views": views,
    }
)
df.to_csv("stories.csv", index=False, encoding="utf-8")

driver.close()