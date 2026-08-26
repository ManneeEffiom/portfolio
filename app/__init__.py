import os

from flask import Flask
from flask_cors import CORS

from app.config import config
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.abspath(config.UPLOAD_FOLDER)

    CORS(app, origins=config.FRONTEND_ORIGIN)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from app.routes import api

    app.register_blueprint(api)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
