import os
import uuid
import shutil
from flask import Flask, request, jsonify, Response
from werkzeug.utils import secure_filename
from functools import wraps

from src.utils.voice_auth import recognize_user, enroll_user
from src.config import app, base_dir


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
        "status": True,
        'response': 200
    })

@app.route('/api/v1/register', methods=['POST'])
@requires_auth
def register_new_user():
    """ 
    Function for registering new user on server
    """
    audio_file = request.files["file"]
    username = request.form['username'].lower()

    audio_directory = os.path.join(base_dir, "data/wav")
    file_name = secure_filename(audio_file.filename)

    full_file_name = os.path.join(audio_directory, username + ".wav")

    audio_file.save(full_file_name)
    response = enroll_user(username, full_file_name)

    os.remove(full_file_name)
    return jsonify({
        'status': True,
        'response': response })

    
@app.route("/api/v1/authenticate", methods=['POST'])
@requires_auth
def authenticate_user():
    """ function for authentication user on server """

    audio_file = request.files["file"]
    
    audio_directory = os.path.join(base_dir, "data/wav")
    file_name = secure_filename(audio_file.filename)

    full_file_name = os.path.join(audio_directory, str(uuid.uuid1()) + ".wav")

    audio_file.save(full_file_name)

    status, response = recognize_user(full_file_name)
    
   
    return jsonify({
        'status': status,
        'response': response 
    })
