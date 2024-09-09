from langchain.retrievers import WikipediaRetriever

def wiki_search(topic):
    retriever = WikipediaRetriever(top_k_results=5) # type: ignore
    docs = retriever.get_relevant_documents(topic)
    return docs