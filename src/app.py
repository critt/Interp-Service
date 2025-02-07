import asyncio
import socketio
from aiohttp import web
import json
from config import BACKEND_PORT
from config import GOOGLE_SERVICE_JSON_FILE
from gcp_service import GCPService
import firebase_admin
from firebase_admin import credentials, auth, exceptions as firebase_exceptions

# Initialize Firebase Admin SDK
cred = credentials.Certificate(GOOGLE_SERVICE_JSON_FILE)
firebase_admin.initialize_app(cred)

# TODO: add firebase sdk and validate tokens for each request

app = web.Application()
routes = web.RouteTableDef()

@routes.get('/getSupportedLanguages')
async def get_supported_languages(request):
    print('Getting supported languages')
    return web.json_response(GCPService.get_supported_languages())

@routes.get('/detectLanguage')
async def detect_language(request):
    print('Detecting language')
    text = request.query['text']
    return web.json_response(GCPService.detect_language(text))

app.add_routes(routes)

# Bind our Socket.IO server to our web app instance
sio = socketio.AsyncServer(cors_allowed_origins=[])  # * is bad
sio.attach(app)

# Define the SubjectNamespace
@sio.on('connect', namespace='/subject')
async def connect_subject(sid, environ, tokenMap):
    try:
        auth.verify_id_token(tokenMap['token'])
    except firebase_exceptions.FirebaseError as fbe:
        print(f"Unauthorized: Invalid token for client {sid}: {fbe}")
        raise ConnectionRefusedError('authentication failed')
    except (KeyError, TypeError) as e:
        print(f"Unauthorized: missing token for client {sid}: {e}")
        raise ConnectionRefusedError('authentication failed')
    print(f'Client connected to /subject: {sid}')

@sio.on('disconnect', namespace='/subject')
async def disconnect_subject(sid):
    print(f'Client disconnected from /subject: {sid}')

@sio.on('startGoogleCloudStream', namespace='/subject')
async def start_google_stream_subject(sid, config):
    print(f'Starting streaming audio data from client {sid} on /subject')
    await GCPService.start_stream(sio, sid, json.loads(config), '/subject')

@sio.on('binaryAudioData', namespace='/subject')
async def receive_binary_audio_data_subject(sid, message):
    GCPService.add_audio_data(sid, message)

@sio.on('endGoogleCloudStream', namespace='/subject')
async def close_google_stream_subject(sid):
    print(f'Closing streaming data from client {sid} on /subject')
    await GCPService.stop_stream(sid)

# Define the ObjectNamespace
@sio.on('connect', namespace='/object')
async def connect_object(sid, environ, tokenMap):
    try:
        auth.verify_id_token(tokenMap['token'])
    except firebase_exceptions.FirebaseError as fbe:
        print(f"Unauthorized: Invalid token for client {sid}: {fbe}")
        raise ConnectionRefusedError('authentication failed')
    except (KeyError, TypeError) as e:
        print(f"Unauthorized: missing token for client {sid}: {e}")
        raise ConnectionRefusedError('authentication failed')
    print(f'Client connected to /object: {sid}')

@sio.on('disconnect', namespace='/object')
async def disconnect_object(sid):
    print(f'Client disconnected from /object: {sid}')

@sio.on('startGoogleCloudStream', namespace='/object')
async def start_google_stream_object(sid, config):
    print(f'Starting streaming audio data from client {sid} on /object')
    await GCPService.start_stream(sio, sid, json.loads(config), '/object')

@sio.on('binaryAudioData', namespace='/object')
async def receive_binary_audio_data_object(sid, message):
    GCPService.add_audio_data(sid, message)

@sio.on('endGoogleCloudStream', namespace='/object')
async def close_google_stream_object(sid):
    print(f'Closing streaming data from client {sid} on /object')
    await GCPService.stop_stream(sid)

print(f'Backend running on port {BACKEND_PORT}')
web.run_app(app, port=BACKEND_PORT)