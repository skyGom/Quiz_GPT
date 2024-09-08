from gpt.prompt import PROMPT

def run_quiz_chain(llm, _docs, topic, difficulty, quiz_count):
    chain = _create_chain(llm)
    return chain.invoke({"total_count":quiz_count, "context":_docs, "difficulty":difficulty})

def _create_chain(llm):
    return PROMPT | llm

def _format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)