from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db import vox_articles, vstore, vox_vstores
from summarizer import Summarizer
import requests
load_dotenv()


app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'], methods=['GET', 'POST'])

@app.route('/')
def index():
    return 'Welcome to my Flask app!'


@app.route('/summaries', methods=['GET'])
def get_summaries():
    try:
        content  = vox_articles.find()
        # print(content)
        return jsonify(content["data"]["documents"]), 200
    except Exception as e:
        return jsonify({"message":f"Unexpected error has occured: {e}"}), 500
    
@app.route("/summary/<int:id>", methods = ["GET"])
def get_summary(id):
    try:
        content = vox_articles.find_one({"article_id": id})
        print(content)
        return jsonify(content["data"]["document"]), 200
    except Exception as e:
        return jsonify({"message":f"Unexpected error has occured: {e}"}), 500

@app.route("/generate", methods = ["POST"])
def generate_summary():
    data = request.json
    try:
        if not data["url"].startswith("https://www.vox.com/"):
            return jsonify({"message": "Not a vox article"}), 400
        # extract article id
        queries = str.split(data["url"], "/")
        article_id = int(queries[len(queries)-2])   
        summarizer = Summarizer(data["url"])
        if Summarizer.vox_summary_exists(article_id):
            return jsonify({"message": "Summary has aready been generated for this article"}), 400
        summarizer.article_id = article_id
        summarizer.scrape_vox()
        summary_article_id = summarizer.create_ai_summary()
        return jsonify({"message":f"Summary successfully created for: {summary_article_id}", "article_id": summary_article_id}), 201
    except Exception as e:
        print(e)
        return jsonify({"message":f"Unexpected error has occured: {e}"}), 500

@app.route("/ask/<int:id>", methods = ["POST"])  
def answer_question(id):
    data = request.json
    try:
        answer = Summarizer.answer_question(id, data["question"])
        return jsonify(answer), 201
    except Exception as e:
        return jsonify({"message":f"Unexpected error has occured: {e}"}), 500

@app.route("/regenerate/<int:id>", methods = ["PUT"])
def regenerate_summary(id):
    pass
    # try:
    #     if not Summarizer.vox_summary_exists():
    #         return jsonify({"message": "There is no data for this specific article"}), 400
    #     return jsonify({"message":f"Summary successfully regenerated for: {summary_article_id}", "article_id": summary_article_id}), 201
    # except Exception as e:
    #     return jsonify({"message":f"Unexpected error has occured: {e}"}), 500
    
@app.route("/delete/<int:id>", methods = ["PUT"])
def delete_summary(id):
    try:
        vox_vstores.delete_many(filter={"metadata.article_id": id})
        print("Vectors deleted")
        vox_articles.delete_many(filter={"article_id": id})
        return jsonify({"message":f"Article successfully deleted: {id}"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message":f"Unexpected error has occured: {e}"}), 500
# @app.route("/filter", methods = ["POST"])
# def filter_by_name():
#     data = request.json
#     quote = data["quote"]

#     # O(N^2)
#     content = collection.find(filter={"metadata.quote": quote})
#     # if content["data"]["document"] == None:
#     #     return jsonify({"message":"No matching documents"}), 401
#     return jsonify(content), 200

# @app.route("/books", methods = ["POST"])
# def create_book():
#     data = request.json
#     docs = []
#     content  = data["content"]
#     doc = Document(page_content=content, metadata = data)
#     docs.append(doc)
#     vstore.add_documents(doc)
#     return jsonify({"message": "Document added successfully"}), 201

# @app.route("/books/similar", methods = ["POST"])
# def find_similar():
#     data = request.json
#     prompt = data["prompt"]
#     retriever = vstore.as_retriever(search_kwargs={"k": 3})
#     philo_template = """
#     You are a philosopher that draws inspiration from great thinkers of the past
#     to craft well-thought answers to user questions. Use the provided context as the basis
#     for your answers and do not make up new reasoning paths - just mix-and-match what you are given.
#     Your answers must be concise and to the point, and refrain from answering about other topics than philosophy.

#     CONTEXT:
#     {context}

#     QUESTION: {question}

#     YOUR ANSWER:"""
#     philo_prompt = ChatPromptTemplate.from_template(philo_template)
#     llm = ChatOpenAI(api_key=OPENAI_API_KEY)
#     chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | philo_prompt
#         | llm
#         | StrOutputParser()
#     )
#     answer = chain.invoke(prompt)
#     similar = vstore.similarity_search(prompt, k=3)
#     response = {}
#     response["similar"] = []
#     for doc in similar:
#         docdata = {}
#         docdata["content"] = doc.page_content
#         docdata["metadata"] = doc.metadata
#         response["similar"].append(docdata)
#     response["result"] = answer
#     return  jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
