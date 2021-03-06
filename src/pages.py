from flask import request
from bs4 import BeautifulSoup
import requests


def check_for_k(string):
    return "k" in string


def remove_k(string):
    return string.replace("k", "")


def convert_to_int(string):
    return float(string) * 1000


def clean_int(string):
    if(check_for_k(string)):
        return convert_to_int(remove_k(string))
    else:
        return int(string)


def scrap_page(page):
    result = requests.get(page)
    return result.content


def get_previous_page(page):
    if page == 1:
        return request.host + "/latest"
    else:
        return request.host + "/pages/" + str(page - 1)


def get_next_page(page):
    return request.host + "/pages/" + str(page + 1)


def get_articles(soup):
    base_url = "https://www.klix.ba"
    articles = soup.find_all("article")
    articles_array = []
    for article in articles:
        articles_array.append({
            "url": base_url + str(article.find("a").get("href")),
            "lead": str(article.find("h1").get_text()),
            "headline": str(article.find("span", class_="kategorija").get_text()),
            "comments": clean_int(article.find("span", class_="comments").get_text()),
            "shares": clean_int(article.find("span", class_="shareovi").get_text())
        })
    return articles_array


def get_page(page):
    content = scrap_page("https://www.klix.ba/najnovije/str" + str(page))
    soup = BeautifulSoup(content, "html.parser")
    response = {
        "articles": get_articles(soup),
        "previous": get_previous_page(page),
        "next": get_next_page(page)
    }
    return response
