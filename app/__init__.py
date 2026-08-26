from flask import Flask

from app.config import config
from app.routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SUPABASE_BUCKET"] = config.SUPABASE_BUCKET

    from flask_cors import CORS

    CORS(app, origins=config.FRONTEND_ORIGIN)

    app.register_blueprint(api)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
