from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename

from main import SUCCESS
from utils import make_response, make_status_response

recognition_api = Blueprint("recognition", __name__, url_prefix="/recognition")


@recognition_api.route('/', methods=['GET'])
def main():
    return render_template('upload.html')


# Register image to recognition folder like 'upload.jpg'
@recognition_api.route('/register', methods=['POST'])
def register():
    image = request.files['image']
    image.save(secure_filename('upload.jpg'))
    return make_status_response(SUCCESS)


@recognition_api.route('/identification', methods=['GET'])
def identification():
    # Todo identification with all face bank
    body = {'name': 'Seungmin', 'score': 99.9}
    return make_response(SUCCESS, body)


@recognition_api.route('/verification', methods=['GET'])
def verification():
    name = request.args["name"]
    # Todo verification with name.jpg
    body = {'result': 'MATCH', 'score': 99.9}
    return make_response(SUCCESS, body)
