import requests

url = "http://34.141.241.48:5000/api/v1/authenticate"

payload={'username': 'deepak008'}

files=[
  ('file',('voice_login.wav',open('C:/Users/inspiron/Documents/GitHub/voice_auth_using_cnn/data/wav/Deepak11/voice_login.wav','rb'),'audio/wav'))
]

auth = ("username", "password")

response = requests.post(url, data=payload, files=files, auth=auth)

print(response.text)