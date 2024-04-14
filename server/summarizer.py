from db import vox_articles, vstore, OPENAI_API_KEY
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import requests


class Summarizer:
    def __init__(self, url) -> None:
        self.documents = []
        self.article_author = None
        self.article_title = None
        self.article_author = None
        self.categories = None
        self.url = url     
        self.article_id = None
    
    def vox_summary_exists(article_id):
        content = vox_articles.find_one({"article_id": article_id})
        print(content)
        return False if content["data"]["document"] is None else True
    
    def scrape_vox(self):
        source = requests.get(self.url)
        #extract html page from url
        soup = BeautifulSoup(source.content,"html.parser")
        
        #extract header information
        article_header = soup.find("div", class_="c-entry-hero")
        self.article_title = article_header.find("h1", class_="c-page-title").text.strip()
        self.article_categories = [ label.find("span").text.strip() for label in article_header.find_all("li", class_="c-entry-group-labels__item") ]
        self.article_author = article_header.find("span", class_="c-byline__author-name").text.strip()
        article_content = soup.find("div",class_="c-entry-content")
        children = article_content.children
        # store documents for vectorstore
        documents = []
        #iterate through paragraph blocks
        for child in children:
            if child.name != "p":
                continue
            #grab the paragraph text for each child
            text:str = child.text.strip()
            document = Document(page_content=text, metadata={"article_id":self.article_id})
            documents.append(document)
        self.documents = documents
        vstore.add_documents(documents=documents)

    def create_ai_summary(self):
        retriever = vstore.as_retriever(search_kwargs= {"filter":{"article_id":self.article_id}} )
        summary_template = """
        You are an english professor that helps students summarize articles. You will write one full summary of the article and try to identify important subsections and summarize those as well. It is required to include any quantitative data analysis if there are any statistics mentioned. Use the provided context as the basis
        for your answers and do not make up new reasoning paths and MUST follow the following
        GUIDELINES:
        -Write a one-sentence summary of each paragraph.
        -Formulate a single sentence that summarizes the whole text.
        -Write a paragraph (or more): begin with the overall summary sentence and follow it with the paragraph summary sentences.
        -Rearrange and rewrite the paragraph to make it clear and concise, to eliminate repetition and relatively minor points, and to provide transitions. The final version should be a complete, unified, and coherent.

        FORMATTING:
        -At the top write the main summary using /s to start and \s to end
        -Write the subsections using /h to start and \h to end
        -Write the summary of the subsections using /hs to start and \hs to end

        Your answers must be concise and to the point, and refrain from inserting your own implicit bias or making opinions.

        CONTEXT:
        {context}


        YOUR ANSWER:"""
        summary_prompt = ChatPromptTemplate.from_template(summary_template)
        llm = ChatOpenAI(api_key=OPENAI_API_KEY)
        chain = (
            {"context": retriever,}
            | summary_prompt
            | llm
            | StrOutputParser()
        )
        answer = chain.invoke("Follow the instructions")
        # similar = vstore.similarity_search(prompt, k=3, filter={"metadata.article_id":self.article_id})
        # response = {}
        # response["similar"] = []
        # for doc in similar:
        #     docdata = {}
        #     docdata["content"] = doc.page_content
        #     docdata["metadata"] = doc.metadata
        #     response["similar"].append(docdata)
        # response["result"] = answer
        vox_articles.insert_one({
            "author": self.article_author,
            "categories": self.article_categories,
            "article_id": self.article_id,
            "title": self.article_title,
            "summary": answer
        })

        return self.article_id
    def answer_question(article_id, question):
        retriever = vstore.as_retriever(search_kwargs= {"filter":{"article_id":article_id}} )
        summary_template = """
        You are an helpful assistant that answers a QUESTION based on the specific CONTEXT. It is required to include any quantitative data analysis if there are any statistics related to the QUESTION. Try to keep your answers at max 3 sentences.
        

        Your answers must be concise and to the point, and refrain from inserting your own implicit bias or making opinions.

        CONTEXT:
        {context}

        QUESTION:
        {question}

        YOUR ANSWER:"""
        summary_prompt = ChatPromptTemplate.from_template(summary_template)
        llm = ChatOpenAI(api_key=OPENAI_API_KEY)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | summary_prompt
            | llm
            | StrOutputParser()
        )
        answer = chain.invoke(question)
        return answer