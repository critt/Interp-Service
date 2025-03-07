from fastapi import FastAPI
import socketio
from config import settings
from routes import router as api_router

app = FastAPI()

# Initialize Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[])
sio_app = socketio.ASGIApp(sio)

# Include API routes
app.include_router(api_router)

# Mount Socket.IO app
app.mount("/", sio_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.backend_port)
