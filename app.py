from flask import Flask, render_template, jsonify, abort, request
from search_backend.wiki_search import WikiSearch

app = Flask(__name__)


@app.route("/")
def root():
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    json = request.get_json()
    if not json or json.get('query') is None:
        abort(400)

    search_engine = WikiSearch.get_search_engine()

    query = str(json['query']).strip()

    return jsonify(
        # results=search_backend.search(query, type_of_search)
        results=search_engine.search(query)
    )


if __name__ == "__main__":
    app.run()
