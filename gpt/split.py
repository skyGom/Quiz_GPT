import os

from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader

def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs