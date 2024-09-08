from langchain.prompts import PromptTemplate

PROMPT = PromptTemplate.from_template(
    "Create {total_count} quizzes for {context}. Write them in Korean. Difficulty should be {difficulty}"
)