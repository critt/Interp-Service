import json
from socketio import AsyncServer
from gcp_service import GCPService
from auth import verify_token

def register_socket_handlers(sio: AsyncServer):
    @sio.on('connect', namespace='/subject')
    async def connect_subject(sid, environ, tokenMap):
        if not verify_token(tokenMap.get('token')):
            raise ConnectionRefusedError('authentication failed')
        print(f'Client connected to /subject: {sid}', flush=True)

    @sio.on('disconnect', namespace='/subject')
    async def disconnect_subject(sid):
        print(f'Client disconnected from /subject: {sid}', flush=True)

    @sio.on('startGoogleCloudStream', namespace='/subject')
    async def start_google_stream_subject(sid, config):
        print(f'Starting streaming audio data from client {sid} on /subject', flush=True)
        await GCPService.start_stream(sio, sid, json.loads(config), '/subject')

    @sio.on('binaryAudioData', namespace='/subject')
    async def receive_binary_audio_data_subject(sid, message):
        GCPService.add_audio_data(sid, message)

    @sio.on('endGoogleCloudStream', namespace='/subject')
    async def close_google_stream_subject(sid):
        print(f'Closing streaming data from client {sid} on /subject', flush=True)
        await GCPService.stop_stream(sid)

    @sio.on('connect', namespace='/object')
    async def connect_object(sid, environ, tokenMap):
        if not verify_token(tokenMap.get('token')):
            raise ConnectionRefusedError('authentication failed')
        print(f'Client connected to /object: {sid}', flush=True)

    @sio.on('disconnect', namespace='/object')
    async def disconnect_object(sid):
        print(f'Client disconnected from /object: {sid}', flush=True)

    @sio.on('startGoogleCloudStream', namespace='/object')
    async def start_google_stream_object(sid, config):
        print(f'Starting streaming audio data from client {sid} on /object', flush=True)
        await GCPService.start_stream(sio, sid, json.loads(config), '/object')

    @sio.on('binaryAudioData', namespace='/object')
    async def receive_binary_audio_data_object(sid, message):
        GCPService.add_audio_data(sid, message)

    @sio.on('endGoogleCloudStream', namespace='/object')
    async def close_google_stream_object(sid):
        print(f'Closing streaming data from client {sid} on /object', flush=True)
        await GCPService.stop_stream(sid)
