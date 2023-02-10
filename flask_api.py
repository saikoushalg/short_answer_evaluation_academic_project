

def find_similarity(sentence1, sentence2):
    return 0


app = Flask(__name__)


@app.route('/similarity/<string:sentence1>/<string:sentence2>', methods=['GET', 'POST'])
def similarity(sentence1, sentence2):
    # Get the sentence1 and sentence2 from the request
    # data = request.get_json()
    # sentence1 = data['sentence1']
    # sentence2 = data['sentence2']

    similarity = find_similarity(sentence1, sentence2)

    # Return the similarity as a JSON response
    return jsonify(similarity)


if __name__ == '__main__':
    app.run(port=8000)
