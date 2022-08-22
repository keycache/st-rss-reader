MAX_DISPLAY_VALUES = (10, 20, 50)
MAX_DISPLAY_SIZE = "max-display-size"
TEMP_MAX_DISPLAY_SIZE = "temp-max-display-size"
OPML_CONTENT = "opml-content"
SETTINGS = "Settings"
SELECTED_FEED = "selected_feed"

SAMPLE_OPML_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>Demo title</title>
    </head>
    <body>
        <outline text="Technology" title="Technology">
            <outline type="rss" text="MacRumors" title="MacRumors" xmlUrl="http://feeds.macrumors.com/MacRumors-All" htmlUrl="https://www.macrumors.com"/>
            <outline type="rss" text="AnPol" title="AnPol" xmlUrl="http://feeds.feedburner.com/AndroidPolice?format=xml" htmlUrl="https://www.androidpolice.com"/>
        </outline>
    </body>
</opml>
"""
