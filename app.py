import json

import streamlit as st

from gpt.model import create_llm, is_valid_openai_key

from view.cache import get_cached_run_quiz_chain, get_cached_split_file, get_cached_wiki_search, run_quiz_chain, split_file

st.set_page_config(
    page_title="Quiz GPT", page_icon="❓"
    )

st.title("Quiz GPT")

import streamlit as st

# 한 번만 키를 확인하도록 session_state를 사용합니다.
if "api_key" not in st.session_state:
    st.session_state.api_key = None
    st.session_state.valid_key = False

with st.sidebar:
    if not st.session_state.api_key:
        api_key = st.text_input("OpenAI API key를 입력해주세요.", type="password")
        
        if api_key:
            with st.spinner("API 키 확인 중..."):
                valid_key = is_valid_openai_key(api_key)
                if valid_key:
                    st.session_state.api_key = api_key
                    st.session_state.valid_key = True
                else:
                    st.warning("API 키가 유효하지 않습니다. 다시 시도해주세요.")
    
    # 유효한 API 키가 확인된 경우
    if st.session_state.valid_key:
        llm = create_llm(st.session_state.api_key)            

    docs = None
    topic = None
    difficulty = None
    quiz_count = 0
    correct_count = 0
    
    choice = st.selectbox("Choose What you want to use.",(
        "File",
        "Wikipedia Article",
    ))

    if choice == "File":
        file = st.file_uploader("Upload a .docx, .txt or .pdf file", type=["txt", "docx", "pdf"])
        if file:
            docs = get_cached_split_file(file)
    else:
        topic = st.text_input("Search Wikipedia...")
        if topic:
            docs = get_cached_wiki_search(topic)

    difficulty = st.selectbox("Select the difficulty level.", ("Easy", "Medium", "Hard"))
    quiz_count = st.number_input("Number of questions", min_value=1, max_value=10, value=5)
    
    st.write("https://github.com/skyGom/Quiz_GPT")
    
if not docs:
    st.markdown(
        """
    Welcome to QuizGPT.
                
    I will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.
                
    Get started by uploading a file or searching on Wikipedia in the sidebar.
    """
    )
else:
    response = get_cached_run_quiz_chain(llm, docs, topic if topic else (file.name if file else ""), difficulty, quiz_count)
    response = response.additional_kwargs["function_call"]["arguments"]
    with st.form("questions_form"):
        for question in json.loads(response)["questions"]:
            st.write(question["question"])
            value = st.radio(
                "Select an option.",
                [answer["answer"] for answer in question["answers"]],
                index=None,
            )
            if {"answer": value, "correct": True} in question["answers"]:
                st.success("Correct!")
                correct_count += 1
            elif value is not None:
                st.error("Wrong!")
        button = st.form_submit_button()
    
        if button:
            if correct_count == quiz_count:
                st.info("Great!", icon="✅")
                st.balloons()
            else:
                st.warning(f"Correct : {correct_count} / {quiz_count}", icon="❌")