from typing import Iterator

import streamlit as st
from streamlit_option_menu import option_menu

from config.constants import MAX_DISPLAY_SIZE, MAX_DISPLAY_VALUES, SETTINGS
from config.settings import (
    get_max_display_index,
    get_selected_feed,
    get_setting_max_display,
    get_setting_user_opml,
    get_user_data,
    init_settings,
    set_selected_feed,
    set_setting_temp_max_display,
    set_setting_user_opml,
    set_settings_max_display,
    set_user,
)
from feeder.feed import Feed, FeedItem, get_feed_items
from feeder.user import User, get_feed, get_feed_names
from opml.factory import handle_opml

user_id = "uid-1"


def render_feed_item(feed_item: FeedItem, i: int):
    # st.title(title)
    st.markdown(
        f"""<h1><a href="{feed_item.get_url()}" target="_blank" rel="noopener noreferrer">{i}. {feed_item.get_title()}</a></h1>""",
        unsafe_allow_html=True,
    )
    img, feed_actions = st.columns([1, 4])
    with img:
        st.image(feed_item.img_url or "http://placekitten.com/200/300")
    feed_actions.write(feed_item.get_content_condensed())
    st.markdown("---")


def render_side_bar(feed_names: Iterator[str]) -> None:
    with st.sidebar:
        selected_feed = option_menu("FEEDS", feed_names, default_index=0)
        set_selected_feed(feed_name=selected_feed)


def handle_save_settings(max_display_size: int or str, opml_content: str):
    print(f"Saving settings: {max_display_size}, {len(opml_content)}")
    set_settings_max_display(value=max_display_size)
    user = handle_opml(content=opml_content)
    set_user(user_id=user_id, user=user)
    set_selected_feed(user.feeds[0].name)
    set_setting_user_opml(content=opml_content)


def render_settings():
    max_display_size = st.selectbox(
        "Max display initial render",
        MAX_DISPLAY_VALUES,
        key=MAX_DISPLAY_SIZE,
        index=get_max_display_index(),
    )
    opml_contents = st.text_area(
        "Paste OPML contents to import feeds",
        height=40,
        value=get_setting_user_opml(),
    )
    st.button(
        "Save Settings",
        on_click=handle_save_settings,
        args=(max_display_size, opml_contents),
    )


def render_title_row(feed: Feed) -> None:
    ##todo user getter funcs
    st.title(f"{feed.name} ({(feed.total_items)})")


def render_feed_items(feed_items: Iterator[FeedItem]) -> None:
    max_display_size = get_setting_max_display()
    load_more = False
    for i, feed_item in enumerate(feed_items):
        if i + 1 > max_display_size:
            load_more = True
            break
        render_feed_item(feed_item=feed_item, i=i + 1)
    if load_more:
        print(f"Displaying {max_display_size} of {len(feed_items)}")
        render_load_more()


def handle_load_more(*args, **kwargs):
    max_display_value = get_setting_max_display()
    print(f"Curr max display value -> {max_display_value}")
    max_display_value = max_display_value + MAX_DISPLAY_VALUES[0]
    set_setting_temp_max_display(value=max_display_value)
    print(f"Updated max display value: {get_setting_max_display()}")


def render_load_more() -> None:
    st.markdown(
        """<style>div.stButton > button:first-child {background-color: rgb(255, 75, 75);}</style>""",
        unsafe_allow_html=True,
    )
    _, col, _ = st.columns([1, 1, 1])
    col.button("Load More", on_click=handle_load_more)


def render_main(user: User) -> None:
    selected_feed = get_selected_feed()

    if selected_feed == SETTINGS:
        render_settings()
        return
    if selected_feed:
        feed = get_feed(feed_name=selected_feed, user=user)
        render_title_row(feed=feed)
        feed_items = get_feed_items(feed=feed)
        render_feed_items(feed_items=feed_items)


def init_user_settings():
    if SETTINGS not in st.session_state:
        init_settings()
        set_selected_feed(SETTINGS)
    if user_id not in st.session_state:
        set_user(user_id=user_id, user=User(feeds=[]))


def run():
    if user_id:
        init_user_settings()
        if st.session_state[user_id]:
            user_state: User = get_user_data(user_id=user_id)
            render_side_bar(feed_names=get_feed_names(user=user_state))
            render_main(user=user_state)


if __name__ == "__main__":
    run()
