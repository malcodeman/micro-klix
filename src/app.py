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
    res = jsonify(pages.get_page(page))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route("/latest")
def get_latest():
    res = jsonify(pages.get_page(1))
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
