""" Configuration file for flask """

from flask import Flask
from pathlib import Path
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)8s --- %(message)s ' +'(%(filename)s:%(lineno)s)',
					datefmt='%d/%m/%Y %I:%M:%S %p',
					level=logging.INFO,
					handlers=[
        				logging.FileHandler("debug.log", mode='a'),
        				logging.StreamHandler()])

base_dir = Path(__file__).parent.parent

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = False

    return app

app = create_app()
