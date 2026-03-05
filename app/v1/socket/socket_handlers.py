from app.socketio_app import sio


@sio.event
async def connect(sid, environ, auth):
    # auth is whatever the client passes, e.g. { token: "..." }
    print("connect", sid, auth)
    await sio.emit("server:hello", {"msg": "connected"}, to=sid)


@sio.event
async def disconnect(sid):
    print("disconnect", sid)


@sio.event
async def join_pipeline(sid, data):
    # data: { "pipeline_id": 123 }
    room = f"pipeline:{data['pipeline_id']}"
    await sio.enter_room(sid, room)
    await sio.emit("server:joined", {"room": room}, to=sid)


@sio.event
async def client_message(sid, data):
    # data: { pipeline_id: 123, text: "hi" }
    room = f"pipeline:{data['pipeline_id']}"
    await sio.emit("pipeline:message", data, room=room)
