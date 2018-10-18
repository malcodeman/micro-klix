from flask import Flask
from flask import jsonify
from flask import render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def scrap_page(page):
    result = requests.get(page)
    return result.content


def get_articles(soup):
    base_url = "https://www.klix.ba"
    articles = soup.find_all("article")
    articles_array = []
    for article in articles:
        articles_array.append({
            "url": base_url + str(article.find("a").get("href")),
            "lead": str(article.find("h1").get_text()),
            "headline": str(article.find("span", class_="kategorija").get_text()),
            "comments": int(article.find("span", class_="comments").get_text()),
            "shares": int(article.find("span", class_="shareovi").get_text())
        })
    return articles_array


def get_page(page):
    content = scrap_page("https://www.klix.ba/najnovije/str" + str(page))
    soup = BeautifulSoup(content, "html.parser")
    return get_articles(soup)


@app.route('/pages/<page>')
def pages(page):
    return jsonify(get_page(page))


@app.route('/latest')
def get_latest():
    return jsonify(get_page(1))


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
