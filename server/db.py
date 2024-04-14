from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_astradb import AstraDBVectorStore
from astrapy.db import AstraDB
from dotenv import load_dotenv
import os


load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

vstore = AstraDBVectorStore(
    embedding=OpenAIEmbeddings(api_key=OPENAI_API_KEY),
    collection_name="articlestore1",
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace="vsearch"
)

db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace="vsearch"
)

collection = db.collection("test")
vox_articles = db.collection("articles1")
vox_vstores = db.collection("articlestore1")


