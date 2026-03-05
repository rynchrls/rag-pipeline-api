import socketio

# async_mode="asgi" is what we want for FastAPI
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(
    sio, socketio_path=""
)  # socketio_path="" = handle paths relative to mount point
