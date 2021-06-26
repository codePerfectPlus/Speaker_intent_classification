# Voice-Authentication-CNN

A simple Voice Authentication system using pre-trained Convolutional Neural Network.

```python
auth = {'username': 'username', password = 'password'}
```

## Enrollment

Enroll a new user using an audio file of his/her voice

- endpoint = `/api/v1/register`

```python
payload = {file: 'voice_file', username='unique_username'}
```

## Authenticate

Authenticate a user if it matches voice prints saved on the disk

- endpoint = `/api/v1/authenticate`

```python
payload = {file: 'voice_file'}
```

## Get Intent

Get Text intention

- endpoint = '/api/v1/getintent`

```python
payload = {"text": "Your text here"}
```
