import os
from pathlib import Path
import shutil
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
    new_id = ids[-1] + 1 if len(ids) else 0

    return new_id


@faceDB_api.route('/', methods=['GET'])
def get_face_db():
    image_paths = list(map(os.path.basename, glob(f'face_db/images/*.jpg')))

    items = list()

    for p in image_paths:
        id, name = p.split('_')
        id = int(id)
        name, _ = os.path.splitext(name)
        url = f'{SERVER_URL}/faceDB/image?id={id}'

        items.append({'id':id, 'name':name, 'url':url})
    
    body = sorted(items, key=lambda item: item['id'])

    return make_response(SUCCESS, body)


@faceDB_api.route('/remove_all', methods=['GET'])
def remove_all_face_db():
    path = 'face_db/images'
    shutil.rmtree(path)
    Path(path).mkdir(exist_ok=True, parents=True)

    return make_response(SUCCESS, {})


@faceDB_api.route('/register', methods=['POST'])
def post_face_db():
    param = request.get_json()
    image = request.files['image']
    name = request.form.getlist('name')[0]

    # Todo crop face from uploaded image

    id = set_id()
    image.save(f'face_db/images/{id}_{name}.jpg')

    return make_status_response(SUCCESS)


@faceDB_api.route('/image', methods=['GET'])
def get_image():
    id = request.args['id']

    image_path = glob(f'face_db/images/{id}_*.jpg')[0]

    return send_file(image_path, mimetype='file')
