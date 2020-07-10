"""
    Created by Ma. Micah Encarnacion on 08/07/2020
"""
import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    "/home/micahencarnacion/Downloads/chromedriver", options=chrome_options
)

id_subscribers = []

with open('stories.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    index = 0

    with open('subscriptions.csv', mode='w') as subscriptions_file:
        fieldnames = ['story_id', 'username']
        writer = csv.DictWriter(subscriptions_file, fieldnames=fieldnames)

        writer.writeheader()

    for row in csv_reader:
        if index > 500:
            break

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        if row["subscribers"]:
            index += 1
            print(f"Getting subscribers for story # {index} {row['title']}...")
            for page in range(0, 228, 12):
                print(f"Reading {row['title']} subscribers page {page}...")
                if not page:
                    driver.get(f"https://www.asianfanfics.com/favorite/story_subscribers/{row['id']}/L")
                else:
                    driver.get(f"https://www.asianfanfics.com/favorite/story_subscribers/{row['id']}/L/{page}")
                content = driver.page_source
                soup = BeautifulSoup(content, features="html.parser")

                for li in soup.find_all("li", attrs={"class": "text-center"}):
                    if len(li["class"]) != 1:
                        continue

                    hrefs = li.find_all("a")
                    for href in hrefs:
                        if href.text.isalnum():
                            with open('subscriptions.csv', mode='a') as subscriptions_file:
                                fieldnames = ['story_id', 'username']
                                writer = csv.DictWriter(subscriptions_file,fieldnames=fieldnames)
                                writer.writerow({"story_id": row["id"], "username": href.text})

        line_count += 1
    print(f'Processed {line_count} lines.')
