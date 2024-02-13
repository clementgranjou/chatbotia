from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
import pandas as pd
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
import json

llm = Ollama(model="llama2")

loader = CSVLoader(file_path="./cryptocurrency_data.csv")

data = loader.load()


embeddings = OllamaEmbeddings()


text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(data)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context in data which contain fiancial data:
<context>
{context}
</context>
Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)
print("vectoriasation success")

def bot_answer(user_input):
    call_llm = document_chain.invoke({
        "input": user_input,
        "context": [Document(page_content="All financial data bout crypto currency")]
    })

    return  {"client_answer": call_llm}
    # output_parser = StrOutputParser()


    