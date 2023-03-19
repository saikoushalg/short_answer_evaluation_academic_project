from flask import Flask, render_template, request
from google.cloud import vision
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from google.protobuf import any_pb2
from google.cloud.vision_v1.types import Image

app = Flask(
    __name__, template_folder='C:/Users/saiko/Desktop/major_project/academic_project_E07/templates')


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/saiko/Desktop/major_project/academic_project_E07/autograder-378705-9750926382f4.json"

client = vision.ImageAnnotatorClient()


model = SentenceTransformer('bert-base-nli-mean-tokens')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():

    image_bytes = request.files['answer'].read()
    reference_text = request.files['reference_answer'].read()

    image = Image(content=image_bytes)

    ref_text = Image(content=reference_text)

    max_marks = int(request.form['max_marks'])

# for answer image
    response_ans = client.text_detection(image=image)
    texts = response_ans.text_annotations
    extracted_text = ''

    for text in texts:
        extracted_text += text.description

    extracted_text = extracted_text.strip().lower()

# for reference text
    response_ref = client.text_detection(image=ref_text)
    text_ref = response_ref.text_annotations
    reference_text_q = ''

    for t in text_ref:
        reference_text_q += t.description

    reference_text_q = reference_text_q.strip().lower()


# converting to vectors and computing the similarity

    ans_embed = []
    ans_embed.append(reference_text_q)
    ans_embed.append(extracted_text)
    ans_embed = model.encode(ans_embed)
    similarity = cosine_similarity([ans_embed[0]], ans_embed[1:])
    similarity_score = similarity[0][0].astype('float')
    disp_similarity = round(similarity_score, 4)
    result = round(similarity[0][0]*max_marks, 2)
    percentage = round(((similarity[0][0]*max_marks)/max_marks)*100, 2)

    return render_template('result.html', extracted_text=extracted_text, reference_text=reference_text_q, similarity_score=disp_similarity, result=result, percentage=percentage)


if __name__ == '__main__':
    app.run(debug=True)
