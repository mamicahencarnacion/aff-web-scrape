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

    int_chapters = ""
    int_subscribers = ""
    int_views = ""
    int_comments = ""
    int_words = ""

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

    def get_eunhae_stories_metadata(
        self, content, titles, links, ids, authors, tags, views, chapters, subscribers, comments, words
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
            story_href = story_title.a.get("href")
            links.append(story_href[:story_href.rindex("/")])
            ids.append(story_href.split("/")[3])

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

            stats_metadata = story_views.span.text.split(",")
            self.get_story_statistics(stats_metadata=stats_metadata)
            chapters.append(self.int_chapters)
            subscribers.append(self.int_subscribers)
            views.append(self.int_views)
            comments.append(self.int_comments)
            words.append(self.int_words)

    def get_story_statistics(self, stats_metadata):
        for stat_desc in stats_metadata:
            stat_desc = stat_desc.strip()
            stat_desc = stat_desc.split(" ")
            if "chapters" in stat_desc:
                self.int_chapters = int(stat_desc[0])
            elif "subscribers" in stat_desc:
                self.int_subscribers = int(stat_desc[0])
            elif "views" in stat_desc:
                self.int_views = int(stat_desc[0])
            elif "comments" in stat_desc:
                self.int_comments = int(stat_desc[0])
            elif "words" in stat_desc:
                self.int_words = int(stat_desc[0])


if __name__ == "__main__":

    story_titles = []
    story_links = []
    story_ids = []
    story_authors = []
    story_tags_list = []
    story_chapters = []
    story_subscribers = []
    story_views_count = []
    story_comments = []
    story_words = []

    eh_stories = EunHaeStories()

    for page in range(0, 11461, 20):
        print(f"Scraping EunHae stories on page {page}...")
        page_contents = eh_stories.get_eunhae_page(page=page)
        eh_stories.get_eunhae_stories_metadata(
            content=page_contents,
            titles=story_titles,
            links=story_links,
            ids=story_ids,
            authors=story_authors,
            tags=story_tags_list,
            chapters=story_chapters,
            subscribers=story_subscribers,
            views=story_views_count,
            comments=story_comments,
            words=story_words
        )

    eh_stories.close_driver()

    csv_mapping = {
        "id": story_ids,
        "title": story_titles,
        "link": story_links,
        "author": story_authors,
        "tags": story_tags_list,
        "chapters": story_chapters,
        "subscribers": story_subscribers,
        "views": story_views_count,
        "comments": story_comments,
        "words": story_words,
    }

    write_to_csv(mapping=csv_mapping, file_name="stories.csv")
