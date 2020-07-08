"""
    Created by Ma. Micah Encarnacion on 07/07/2020
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import write_to_csv


class EunHaeStories:
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        "/home/micahencarnacion/Downloads/chromedriver", options=chrome_options
    )

    def get_eunhae_page(self, page=None):
        if not page:
            self.driver.get("https://www.asianfanfics.com/browse/tag/eunhae/S")
        else:
            self.driver.get(
                f"https://www.asianfanfics.com/browse/tag/eunhae/S/{page}"
            )

        page_content = self.driver.page_source

        return page_content

    def close_driver(self):
        self.driver.close()

    @staticmethod
    def get_eunhae_stories_metadata(
        content, titles, links, authors, tags, views
    ):
        soup = BeautifulSoup(content, features="html.parser")

        for section in soup.find_all("section", attrs={"class": "excerpt"}):
            this_story_tags = []
            if len(section["class"]) != 1:
                continue

            story_title = section.find("h1", attrs={"class": "excerpt__title"})
            story_author = section.find(
                "div", attrs={"class": "excerpt__meta__name"}
            )
            story_tags = section.find(
                "div", attrs={"class": "excerpt__meta__tags"}
            )
            story_views = section.find(
                "div", attrs={"class": "excerpt__meta__views"}
            )

            if not (story_title and story_tags and story_views):
                continue

            titles.append(story_title.text)
            links.append(story_title.a.get("href"))

            try:
                authors.append(story_author.a.text.strip())
            except AttributeError:
                authors.append("")

            for tag in story_tags.children:
                try:
                    this_story_tags.append(tag.text)
                except AttributeError:
                    continue
            tags.append(",".join(this_story_tags))

            views.append(story_views.span.text)


if __name__ == "__main__":

    story_titles = []
    story_links = []
    story_authors = []
    story_tags_list = []
    story_views_list = []

    eh_stories = EunHaeStories()

    for page in range(0, 11461, 20):
        print(f"Scraping EunHae stories on page {page}...")
        page_contents = eh_stories.get_eunhae_page(page=page)
        EunHaeStories.get_eunhae_stories_metadata(
            content=page_contents,
            titles=story_titles,
            links=story_links,
            authors=story_authors,
            tags=story_tags_list,
            views=story_views_list,
        )

    eh_stories.close_driver()

    csv_mapping = {
        "title": story_titles,
        "link": story_links,
        "author": story_authors,
        "tag": story_tags_list,
        "views": story_views_list,
    }

    write_to_csv(mapping=csv_mapping, file_name="stories.csv")
