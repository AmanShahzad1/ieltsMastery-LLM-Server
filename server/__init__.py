from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

    from server.llama import lm
    
    app.register_blueprint(lm, url_prefix='/')

    return app