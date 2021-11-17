from flask import Blueprint

from utils import make_response

main_api = Blueprint("main", __name__, url_prefix="/")
SUCCESS = "success"
FAILURE = "failure"


@main_api.route("/", methods=["GET"])
def main():
    body = {"answer": "Face Recognition Server"}
    return make_response(SUCCESS, body)
