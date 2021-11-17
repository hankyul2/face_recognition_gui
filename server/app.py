from flask import Flask

from config import config_by_name
from face_db import faceDB_api
from main import main_api
from recognition import recognition_api


def create_app(config_name, api_urls):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[config_name])

    # apply url
    for url in api_urls:
        app.register_blueprint(url)

    return app


API_URLS = [
    main_api,
    faceDB_api,
    recognition_api,
]

app = create_app("dev", API_URLS)
app.app_context().push()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
