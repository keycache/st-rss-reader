from typing import Any, Dict

import streamlit as st

from config.constants import (
    MAX_DISPLAY_SIZE,
    MAX_DISPLAY_VALUES,
    OPML_CONTENT,
    SAMPLE_OPML_CONTENT,
    SELECTED_FEED,
    SETTINGS,
    TEMP_MAX_DISPLAY_SIZE,
)
from feeder.user import User


def set_user(user_id: str, user: User):
    print(f"Updating user state with new feeds")
    st.session_state[user_id] = user


def get_user_data(user_id) -> User:
    if user_id not in st.session_state:
        user = User()
        set_user(user_id=user_id, user=user)
    return st.session_state[user_id]


def get_selected_feed():
    return st.session_state[SELECTED_FEED]


def set_selected_feed(feed_name):
    st.session_state[SELECTED_FEED] = feed_name
    print(
        f"Set selected feed({feed_name}) to"
        f" {get_selected_feed()}/{st.session_state[SELECTED_FEED]}"
    )


def init_settings(
    max_display_size: int = None,
    temp_max_display_size: int = None,
    opml_content: str = None,
) -> Dict[str, Any]:
    if SETTINGS not in st.session_state:
        st.session_state[SETTINGS] = {
            MAX_DISPLAY_SIZE: max_display_size or MAX_DISPLAY_VALUES[0],
            TEMP_MAX_DISPLAY_SIZE: temp_max_display_size
            or MAX_DISPLAY_VALUES[0],
            OPML_CONTENT: opml_content or SAMPLE_OPML_CONTENT,
        }


def get_max_display_index():
    max_display_value = get_setting_max_display()
    try:
        return MAX_DISPLAY_VALUES.index(max_display_value)
    except ValueError:
        return 0


def get_setting_max_display() -> int:
    init_settings()
    if MAX_DISPLAY_SIZE not in st.session_state[SETTINGS]:
        set_settings_max_display(MAX_DISPLAY_VALUES[0])
    return max(
        st.session_state[SETTINGS][MAX_DISPLAY_SIZE],
        st.session_state[SETTINGS][TEMP_MAX_DISPLAY_SIZE],
    )


def set_settings_max_display(value) -> None:
    init_settings(max_display_size=value)
    st.session_state[SETTINGS][MAX_DISPLAY_SIZE] = int(value)


def get_setting_temp_max_display():
    init_settings()
    if TEMP_MAX_DISPLAY_SIZE not in st.session_state[SETTINGS]:
        max_display_value = get_setting_max_display()
        set_setting_temp_max_display(max_display_value + MAX_DISPLAY_VALUES[0])
    return st.session_state[SETTINGS][TEMP_MAX_DISPLAY_SIZE]


def set_setting_temp_max_display(value: int):
    init_settings(temp_max_display_size=value)
    st.session_state[SETTINGS][TEMP_MAX_DISPLAY_SIZE] = value


def set_setting_user_opml(content) -> None:
    init_settings()
    st.session_state[SETTINGS][OPML_CONTENT] = content


def get_setting_user_opml() -> None:
    init_settings()
    return st.session_state[SETTINGS][OPML_CONTENT]
