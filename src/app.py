from flask import Flask
from flask import jsonify
from flask import render_template
from flask import abort

import pages

app = Flask(__name__)


@app.route("/pages/<int:page>")
def get_page(page):
    if page <= 0:
        abort(404)
    return jsonify(pages.get_page(page))


@app.route("/latest")
def get_latest():
    return jsonify(pages.get_page(1))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
