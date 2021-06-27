""" Main file to run server """
from src.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#gunicorn main:app --bind 0.0.0.0:5000