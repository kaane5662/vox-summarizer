from selenium import webdriver
# from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document
from astrapy.db import AstraDBCollection    
from astrapy.db import AstraDB
from datasets import load_dataset
# from langchain.vectorstores import cassandra
# from langchain.vectorstores.cassandra import Cassandra
import os
from dotenv import load_dotenv
import json
load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
print(ASTRA_DB_API_ENDPOINT)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
import asyncio
# vstore = AstraDBVectorStore(
#     embedding=embedding,
#     token=ASTRA_DB_APPLICATION_TOKEN,
#     api_endpoint=ASTRA_DB_API_ENDPOINT,
#     namespace="vsearch"
# )

# print(ASTRA_DB_API_ENDPOINT)
# print(ASTRA_DB_APPLICATION_TOKEN)

# Initialize the client
# db = AstraDB(
#   token=ASTRA_DB_APPLICATION_TOKEN,
#   api_endpoint=ASTRA_DB_API_ENDPOINT,
#   namespace="vsearch",
# )
# db = db.collection("movie_reviews")
def test():
    dataset = load_dataset("datastax/philosopher-quotes")["train"]
    dataset = dataset[:15]
    # print(dataset)
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="test",
        namespace="vsearch",
        token=ASTRA_DB_APPLICATION_TOKEN,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
    )
    docs = []
    # print(dataset)
    # for i, entry in enumerate(dataset["author"]):
    #     # print(entry, "\n")
    #     metadata = {}
    #     metadata["author"] = dataset["author"][i]
    #     # 
    #     metadata["quote"] = dataset["quote"][i]
    #     # # Add a LangChain document with the quote and metadata tags
    #     doc = Document(page_content=dataset["quote"][i], metadata=metadata)
    #     docs.append(doc)

    # vstore.add_documents(docs)
    results = vstore.similarity_search("What is true happiness?", k=3)
    print(results)  
# 


test()

# driver = webdriver.Chrome()
#
