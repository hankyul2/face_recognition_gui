import os
from glob import glob

from flask import Blueprint, request, send_file

from main import SUCCESS
from utils import make_status_response, make_response

faceDB_api = Blueprint("faceDB", __name__, url_prefix="/faceDB")
SERVER_URL = 'http://localhost:5000'


def set_id():
    image_paths = list(map(os.path.basename, glob(f'face_db/images/*.jpg')))
    ids = list()
    for p in image_paths:
        id, name = p.split('_')
        id = int(id)
        ids.append(id)

    ids = sorted(ids)
    new_id = ids[-1] + 1

    return new_id


@faceDB_api.route('/', methods=['GET'])
def get_face_db():
    image_paths = list(map(os.path.basename, glob(f'face_db/images/*.jpg')))

    ids = list()
    names = list()
    img_urls = list()

    for p in image_paths:
        id, name = p.split('_')
        id = int(id)
        name, _ = os.path.splitext(name)
        url = f'{SERVER_URL}/faceDB/image?id={id}'

        ids.append(id)
        names.append(name)
        img_urls.append(url)

    body = {'id': ids, 'name': names, 'img_url': img_urls}

    return make_response(SUCCESS, body)


@faceDB_api.route('/register', methods=['POST'])
def post_face_db():
    param = request.get_json()
    image = request.files['image']
    name = param['name']

    # Todo crop face from uploaded image

    id = set_id()
    image.save(f'face_db/images/{id}_{name}.jpg')

    return make_status_response(SUCCESS)


@faceDB_api.route('/image', methods=['GET'])
def get_image():
    id = request.args['id']

    image_path = glob(f'face_db/images/{id}_*.jpg')[0]

    return send_file(image_path, mimetype='file')
