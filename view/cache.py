import re
import streamlit as st

from gpt.split import split_file
from gpt.chain import run_quiz_chain
from gpt.retrievers import wiki_search

from datetime import timedelta

@st.cache_data(show_spinner="Loading file...", ttl=timedelta(hours=1))
def get_cached_split_file(file):
    return split_file(file)

@st.cache_data(show_spinner="Making Quiz...", ttl=timedelta(hours=1))
def get_cached_run_quiz_chain(_llm, _docs, topic, difficulty, quiz_count):
    return run_quiz_chain(_llm, _docs, topic, difficulty, quiz_count)

@st.cache_data(show_spinner="Making Quiz...", ttl=timedelta(hours=1))
def get_cached_wiki_search(topic):
    return wiki_search(topic)