from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/latest')
def get_latest():
    result = requests.get("https://www.klix.ba/najnovije/str1")
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    articles = soup.find_all("article")
    articles_array = []
    for article in articles:
        articles_array.append({
            "headline": str(article.find("h1").get_text()),
            "comments": int(article.find("span", class_="comments").get_text()),
            "shares": int(article.find("span", class_="shareovi").get_text()),
        })
    return jsonify(articles_array)
@app.route('/')
def home():
    return "Klix microservice"

if __name__ == '__main__':
    app.run()
