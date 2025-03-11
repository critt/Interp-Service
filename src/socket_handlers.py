import json
from socketio import AsyncServer
from interfaces import IStreamingService
from auth import verify_token
from constants import (
    NAMESPACE_SUBJECT,
    NAMESPACE_OBJECT,
    EVENT_CONNECT,
    EVENT_DISCONNECT,
    EVENT_START_STREAM,
    EVENT_BINARY_AUDIO,
    EVENT_END_STREAM,
)


def register_socket_handlers(sio: AsyncServer, streaming_service: IStreamingService):
    def register_namespace_handlers(namespace: str):
        @sio.on(EVENT_CONNECT, namespace=namespace)
        async def connect(sid, environ, tokenMap):
            if not verify_token(tokenMap.get("token")):
                raise ConnectionRefusedError("authentication failed")
            print(f"Client connected to {namespace}: {sid}", flush=True)

        @sio.on(EVENT_DISCONNECT, namespace=namespace)
        async def disconnect(sid):
            print(f"Client disconnected from {namespace}: {sid}", flush=True)

        @sio.on(EVENT_START_STREAM, namespace=namespace)
        async def start_google_stream(sid, config):
            print(
                f"Starting streaming audio data from client {sid} on {namespace}",
                flush=True,
            )
            await streaming_service.start_stream(
                sio, sid, json.loads(config), namespace
            )

        @sio.on(EVENT_BINARY_AUDIO, namespace=namespace)
        async def receive_binary_audio_data(sid, message):
            streaming_service.add_audio_data(sid, message)

        @sio.on(EVENT_END_STREAM, namespace=namespace)
        async def close_google_stream(sid):
            print(
                f"Closing streaming data from client {sid} on {namespace}", flush=True
            )
            await streaming_service.stop_stream(sid)

    register_namespace_handlers(NAMESPACE_SUBJECT)
    register_namespace_handlers(NAMESPACE_OBJECT)
