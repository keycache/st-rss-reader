from typing import Iterator, List

from config.constants import SETTINGS
from feeder.feed import Feed


class User:
    def __init__(self, feeds: List[Feed] = None) -> None:
        self.feeds = feeds or self.get_feeds()
        print(f"Set the feeds: {len(self.feeds)}")

    def get_feed_names(self) -> Iterator[str]:
        # todo abstract `.name`
        for feed in self.feeds:
            print(f"Fetching feed names -> {feed}")
        return [feed.name for feed in self.feeds]

    def get_feed_icon_urls(self) -> Iterator[str]:
        # todo abstract `.img_url`
        return tuple([feed.img_url for feed in self.feeds])

    def get_feeds(self) -> List[Feed]:
        if not (hasattr(self, "feeds") and self.feeds):
            print("Evaluating feeds...Will take long")
            urls = [
                # ("https://waylonwalker.com/rss.xml", None),
                # ("http://feeds.feedburner.com/AndroidPolice?format=xml", "AP"),
            ]
            self.feeds = []
            for url, name in urls:
                print(f"Processing {url}.")
                feed = Feed(url=url, name=name)
                self.feeds.append(feed)
        return self.feeds

    def get_feed(self, feed_name: str) -> Feed | None:
        if not feed_name:
            return None
        for feed in self.feeds:
            if feed.name == feed_name:
                return feed
        return None


def get_feed(feed_name: str, user: User) -> Feed:
    return user.get_feed(feed_name=feed_name)


def get_feed_names(user: User) -> Iterator["str"]:
    user_feed_names = user.get_feed_names()
    if user_feed_names:
        return tuple(user_feed_names + ["---", SETTINGS])
    return (SETTINGS,)


if __name__ == "__main__":
    feed = Feed(url="http://feeds.macrumors.com/MacRumors-All", name="MacR")
    print(feed.get_feed_items()[0].get_content_condensed())
