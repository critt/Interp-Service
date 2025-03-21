from socketio import AsyncServer, ASGIApp
from fastapi import FastAPI
from auth import verify_token
from gcp_service import GCPService

sio = AsyncServer(async_mode="asgi")
app = FastAPI()
socket_app = ASGIApp(sio)

gcp_service = GCPService()


@sio.on("connect")
async def connect(sid, environ):
    token = environ.get("HTTP_AUTHORIZATION")
    if not verify_token(token):
        raise ConnectionRefusedError("Unauthorized")
    print(f"Client connected: {sid}")


@sio.on("disconnect")
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.on("start_stream")
async def start_stream(sid, config):
    await gcp_service.start_stream(sio, sid, config, "/")


@sio.on("end_stream")
async def end_stream(sid):
    await gcp_service.stop_stream(sid)
