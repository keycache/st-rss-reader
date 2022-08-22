from random import randint
from typing import Iterator, List
from urllib.parse import urlparse

import feedparser as fp
from bs4 import BeautifulSoup
from feedparser.util import FeedParserDict

FEED_IMG = "image"
FEED_IMG_URL = "href"

ID = "id"
TITLE = "title"
URL = "link"
IMG_URL = "img_url"
CONTENT = "content"
SUMMARY = "summary"
CREATED_TIME = "created_time"

CONTENT_TYPE = "type"
CONTENT_LANG = "language"
CONTENT_VALUE = "value"

CONTENT_TYPE_HTML = "text/html"
CONTENT_VALUE_CONDENSED_LEN = 500


class FeedContent:
    def __init__(
        self,
        raw_content=None,
        type=None,
        language=None,
        content=None,
        url=None,
    ) -> None:
        self.raw_content = raw_content
        self.type = type
        self.language = language
        self.content = content
        self.url = url
        self.condensed_text = None
        self.full_text = None

    def get_content(self):
        if not self.content:
            # try:
            #     self.content = self.raw_content[0][CONTENT_VALUE]
            # except Exception as e:
            #     print(
            #         "Exception in getting"
            #         f" content\n{type(self.raw_content)}\n{self.raw_content}"
            #     )
            if isinstance(self.raw_content, str):
                self.content = self.raw_content
            else:
                self.content = self.raw_content[0][CONTENT_VALUE]
        return self.content

    def get_condensed_content(self):
        if not self.condensed_text:
            content = self.get_content()
            if self.get_type() == CONTENT_TYPE_HTML:
                soup = BeautifulSoup(content, "html.parser")
                self.condensed_text = soup.get_text()[
                    :CONTENT_VALUE_CONDENSED_LEN
                ]
        return self.condensed_text

    def get_full_text(self):
        if not self.full_text:
            content = self.get_content()
            if self.get_type() == CONTENT_TYPE_HTML:
                soup = BeautifulSoup(content, "html.parser")
                self.full_text = soup.get_text()
        return self.full_text

    def get_language(self):
        if not self.language:
            self.language = self.raw_content[0][CONTENT_LANG]
        return self.language

    def get_type(self):
        if not self.type:
            try:
                self.type = self.raw_content[0][CONTENT_TYPE]
            except:
                # default is HTML
                self.type = CONTENT_TYPE_HTML
        return self.type

    def __str__(self) -> str:
        return str(
            {
                "type": self.get_type(),
                "language": self.get_language(),
                "content": self.get_condensed_content(),
            }
        )


class FeedItem:
    def __init__(
        self,
        feed,
        id=None,
        title=None,
        url=None,
        img_url=None,
        content=None,
        created_time=None,
        updated_tile=None,
    ) -> None:
        self.feed = feed
        self.id = id
        self.title = title
        self.url = url
        self.img_url = img_url
        self.content = content
        self.created_time = created_time
        self.updated_tile = updated_tile

    def get_id(self):
        if not self.id:
            self.id = self.feed[ID]
        return self.id

    def get_title(self):
        if not self.title:
            self.title = self.feed[TITLE]
        return self.title

    def get_url(self):
        if not self.url:
            self.url = self.feed[URL]
        return self.url

    def get_url(self):
        if not self.url:
            self.url = self.feed[URL]
        return self.url

    def get_content(self) -> FeedContent:
        if not self.content:
            for key in (CONTENT, SUMMARY):
                try:
                    self.content = FeedContent(raw_content=self.feed[key])
                except:
                    # print(
                    #     f"---------Exception---------\n{self.feed.keys()}\n{self.feed}"
                    # )
                    print(
                        f"---------Exception---------\n{self.feed.keys()}"
                    )
        return self.content

    def get_content_condensed(self) -> str:
        return self.get_content().get_condensed_content()

    def get_created_time(self):
        if not self.created_time:
            self.created_time = self.feed[CREATED_TIME]
        return self.created_time

    def get_updated_time(self):
        if not self.updated_time:
            self.updated_time = self.get_created_time()
        return self.updated_time

    def __str__(self) -> str:
        return str(
            {
                "id": self.get_id(),
                "title": self.get_title(),
                "url": self.get_url(),
                "content": str(self.get_content()),
            }
        )


class Feed:
    def __init__(
        self,
        url: str,
        name: str = None,
        img_url: str = None,
        feed_items: Iterator[FeedItem] = None,
    ) -> None:
        self.url = url
        self.name = name
        self.img_url = img_url
        self.feed_items = feed_items
        if not self.feed_items:
            self.get_feed_items()

    def get_feed_items(self, force=False) -> List[FeedItem]:
        if not force and self.feed_items:
            return self.feed_items
        else:
            print(
                f"id={id(self)}, force={force},"
                f" self.feed_items={self.feed_items}"
            )
        print("Fetching feed items...")
        feed: FeedParserDict = fp.parse(self.url)
        if not self.name:
            self.name = self.get_feed_name(feed)
        if not self.img_url:
            self.img_url = self.get_img_url(feed)
        self.feed_items = tuple(
            [FeedItem(feed=entry) for entry in feed["entries"]]
        )
        print(f"Fetched {len(self.feed_items)} items for {self.url}")
        return self.feed_items

    def get_img_url(self, feed: FeedParserDict) -> str:
        try:
            return feed["feed"][FEED_IMG][FEED_IMG_URL] or ""
        except KeyError:
            return ""

    def get_feed_name(self, feed: FeedParserDict) -> str:
        try:
            return feed["feed"][TITLE]
        except KeyError:
            print(f"Exception------->{feed['feed']}")
            return urlparse(feed["feed"][URL]).netloc

    @property
    def total_items(self):
        return len(self.feed_items)

    def __str__(self) -> str:
        return str(
            {
                "name": self.name,
                "total_items": self.total_items,
                "url": self.url,
                "image_url": self.img_url,
            }
        )

    def get_random_feed_item(self):
        index = randint(0, self.total_items - 1)
        return self.feed_items[index]


def get_feed_items(feed: Feed):
    feed_items = []
    if feed:
        for feed_item in feed.feed_items:
            feed_items.append(feed_item)
    return feed_items


if __name__ == "__main__":
    import feedparser as fp

    # feed = Feed('http://feeds.feedburner.com/AndroidPolice?format=xml')
    feed = Feed(url="https://waylonwalker.com/rss.xml", name=None)
    print(feed)
    print(feed.get_random_feed_item())
