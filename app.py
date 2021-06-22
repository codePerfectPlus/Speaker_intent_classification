import os
from pathlib import Path
from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
from functools import wraps

from voice_auth import recognize_user, enroll_user

base_dir = Path(__file__).parent

app = Flask(__name__)

app.config["DEBUG"] = True

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    uname = "username"
    pswd = "password"

    return username == uname and password == pswd

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\nYou have to login with login',
        status=401,
        headers={'WWW-Authenticate': 'Basic realm="Login Required'})

@app.route('/')
def home():
    return jsonify({
        "status": "200"
    })

@app.route('/api/v1/register', methods=['POST'])
def register_new_user():
    """ 
    Function for registering new user on server
    """
    audio_file = request.files["file"]
    username = request.form['username']

    audio_directory = os.path.join(base_dir, "data/wav")
    file_name = secure_filename(audio_file.filename)

    full_file_name = os.path.join(audio_directory, username + "wav")

    audio_file.save(full_file_name)

    response = enroll_user(username, full_file_name)

    return jsonify({
        'status': True,
        'response': response })

@app.route("/api/v1/authenticate", methods=['POST'])
def authenticate_user():

    audio_file = request.files["file"]
    #email = request.get_json(force=True).decode("utf-8")

    audio_directory = os.path.join(base_dir, "data/wav")
    file_name = secure_filename(audio_file.filename)

    full_file_name = os.path.join(audio_directory, f"{file_name}")

    audio_file.save(full_file_name)

    response = recognize_user(full_file_name)
    print(response)

    return jsonify({
        'status': True,
        'response': response })
