import os
from flask import Flask
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).parent.parent

print(base_dir)
def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True

    return app

app = create_app()
