from feeder.feed import Feed
from feeder.user import User
from opml.opml_parser import parse


def handle_opml(content: str) -> User:
    feeds = []
    if content:
        print(f"Parsing opml file")
        rss = parse(content)
        for feed in rss["feeds"]:
            user_feed = Feed(url=feed["url"], name=feed["title"])
            feeds.append(user_feed)
        print(f"Found {len(feeds)} feeds in opml file")
    user = User(feeds=feeds)
    return user
