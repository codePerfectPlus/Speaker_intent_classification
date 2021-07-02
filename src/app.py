""" Flask app.py """
import os
import uuid
from flask import Flask, request, jsonify, Response, send_file
from functools import wraps
from pathlib import Path
import logging

#from src.voiceauth1.voice_auth import recognize_user_v1, enroll_user_v1
from src.voiceauth2.voice_registration import enroll_user_v2
from src.voiceauth2.voice_recognizer import recognize_user_v2

base_dir = Path(__file__).parent.parent
app = Flask(__name__)
app.config['DEBUG'] = False

logging.basicConfig(format='[%(asctime)s] %(levelname)8s --- %(message)s ' +'(%(filename)s:%(lineno)s)',
					datefmt='%d/%m/%Y %I:%M:%S %p',
					level=logging.INFO,
					handlers=[
        				logging.FileHandler("debug.log", mode='a'),
        				logging.StreamHandler()])

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
    return jsonify({"status": True, 'response': 200})

'''
@app.route('/api/v1/register', methods=['GET', 'POST'])
@requires_auth
def register_new_user_v1():
    """ post api for registering new user on server """

    if request.method == 'POST':
        audio_file = request.files["file"]
        username = request.form['username'].lower()

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(audio_directory, username + ".wav")

        audio_file.save(full_file_name)
        status, response = enroll_user_v1(username, full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})


@app.route("/api/v1/authenticate", methods=['GET', 'POST'])
@requires_auth
def authenticate_user_v1():
    """ post api for authentication user on server """

    if request.method == "POST":
        audio_file = request.files["file"]

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(
            audio_directory, str(uuid.uuid1()) + ".wav")

        audio_file.save(full_file_name)

        status, response = recognize_user_v1(full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})
'''

@app.route('/api/v2/register', methods=['GET', 'POST'])
@requires_auth
def register_new_user_v2():
    """ post api for registering new user on server using v2"""

    if request.method == 'POST':
        audio_file = request.files["file"]
        username = request.form['username'].lower()

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(audio_directory, username + ".wav")

        audio_file.save(full_file_name)
        status, response = enroll_user_v2(username, full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})


@app.route("/api/v2/authenticate", methods=['GET', 'POST'])
@requires_auth
def authenticate_user_v2():
    """ post api for authentication user on server using v2"""

    if request.method == "POST":
        audio_file = request.files["file"]

        audio_directory = os.path.join(base_dir, "data/wav")

        full_file_name = os.path.join(
            audio_directory, str(uuid.uuid1()) + ".wav")

        audio_file.save(full_file_name)

        status, response = recognize_user_v2(full_file_name)

        os.remove(full_file_name)
        return jsonify({'status': status, 'response': response})

    return jsonify({'status': True, 'response': 200})

@app.route('/api/v2/getintent', methods=['POST'])
@requires_auth
def get_text_intent_v2():
    req = request.get_json(silent=True, force=True)

    query_result = req.get('queryResult')
    query_text = query_result["queryText"]

    query_intent = query_result.get('intent')['displayName']

    response = {
        "response": query_intent,
        "text": query_text,
        "status": 200
    }
    return jsonify({
        'fulfillmentText': str(response),
        'source': 'webhook'})
    