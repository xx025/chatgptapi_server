from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from message_forward.manger import server_manager

# from message_forward.public_param import server_manager

server = APIRouter()


@server.websocket("")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    server_manager["server"] = ws
    server_status = 1

    try:
        while True:
            data = await ws.receive_json()

            if data is None:
                await ws.send_json({'msg': '喜喜'})


    except WebSocketDisconnect:
        # await ws.close()
        pass
