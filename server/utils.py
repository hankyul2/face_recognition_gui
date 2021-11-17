import io
import json
from base64 import encodebytes

from PIL import Image


def make_response(status, body):
    res = json.dumps({"status": status, "body": body})
    return res


def make_status_response(status):
    res = json.dumps({"status": status})
    return res


def encode_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img
