from flask import Flask, render_template, jsonify, abort, request
import search_backend
app = Flask(__name__)


@app.route("/")
def root():
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    json = request.get_json()
    if not json or json.get('query') is None:
        abort(400)

    query = str(json['query']).strip()
    type_of_search = str(json['type_of_search'])

    return jsonify(
        results=search_backend.search(query, type_of_search)
    )


if __name__ == "__main__":
    app.run()
