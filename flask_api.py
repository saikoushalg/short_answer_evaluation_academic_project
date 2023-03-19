from flask import Flask, request
from flask import jsonify
from sentence_transformers import SentenceTransformer
from transformers import BertTokenizer, BertModel
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('bert-base-nli-mean-tokens')


def find_similarity(sentence1, sentence2, outof_score):
    ans_embed = []
    ans_embed.append(sentence1)
    ans_embed.append(sentence2)
    ans_embed = model.encode(ans_embed)
    result = cosine_similarity([ans_embed[0]], ans_embed[1:])
    similarity_score = result[0][0].astype('float')
    result = round(result[0][0]*outof_score, 2)
    percentage = round(((similarity_score*outof_score)/outof_score)*100, 2)
    res = {
        'percentage': percentage, 'score': result, 'similarity': similarity_score,'Status':"OK" }
    return res


app = Flask(__name__)


@app.route('/similarity/<string:sentence1>/<string:sentence2>/<int:outof_score>', methods=['GET', 'POST'])
def similarity(sentence1, sentence2, outof_score):

    similarity = find_similarity(sentence1, sentence2, outof_score)

    return jsonify(similarity)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
