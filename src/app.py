import os
import uuid
from flask import Flask, request, jsonify, Response
from functools import wraps

from src.utils.voice_auth import recognize_user, enroll_user
from src.utils.intent_classification import get_intent
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


@app.route('/api/v1/register', methods=['GET', 'POST'])
@requires_auth
def register_new_user():
    """ post api for registering new user on server """

    if request.method == 'POST':
        audio_file = request.files["file"]
        username = request.form['username'].lower()

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(audio_directory, username + ".wav")

        audio_file.save(full_file_name)
        status, response = enroll_user(username, full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})


@app.route("/api/v1/authenticate", methods=['GET', 'POST'])
@requires_auth
def authenticate_user():
    """ post api for authentication user on server """

    if request.method == "POST":
        audio_file = request.files["file"]

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(
            audio_directory, str(uuid.uuid1()) + ".wav")

        audio_file.save(full_file_name)

        status, response = recognize_user(full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})


@app.route('/api/v1/getintent', methods=['GET', 'POST'])
@requires_auth
def get_text_intent():
    """ Post api for intent classification """

    if request.method == 'POST':
        text = request.form["text"]

        intent = get_intent(text)

        return jsonify({'status': True, 'response': intent})

    return jsonify({'status': True, 'response': 200})
