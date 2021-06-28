""" Main file to run server """
from src.app import app
import sys

if __name__ == '__main__':
    if sys.argv[1] == "local":
        app.run()
    app.run(host='0.0.0.0', port=5000)

#gunicorn main:app --bind 0.0.0.0:5000