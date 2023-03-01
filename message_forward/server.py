import json
from typing import Union

from fastapi import APIRouter, Query, Depends
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState

from message_forward.manger import server_manger, r, user_manager
from setting import server_tokens

server = APIRouter()

index = 0


def get_server_id():
    global index
    index += 1
    return f'server{index}'


async def get_cookie_or_token(
        websocket: WebSocket,
        token: Union[str, None] = Query(default=None),
):
    return token


@server.websocket("")
async def websocket_endpoint(ws: WebSocket, token: str = Depends(get_cookie_or_token)):
    await ws.accept()
    if token not in server_tokens:
        await ws.send_text('Require the correct token.!.')
        await ws.close()
        return

    server_id = get_server_id()  # 当然可以用token作为id 或某种id-token的一对一映射
    server_manger[server_id] = ws

    print(f"{server_id} connected")

    while True:
        try:
            queue_length = await r.llen('msgs')
            if queue_length > 0:
                d1 = await r.rpop('msgs')

                if d1:
                    # 心跳机制传入None
                    data = json.loads(d1.decode('utf-8'))
                    user_id = data['user_id']
                    user_query = json.loads(data['query_msg'])
                    print(server_id, '<---', user_id, ':', user_query)
                    try:
                        await ws.send_json(user_query)
                        server_answer = await ws.receive_json()
                        if user_manager.get(user_id):
                            print(server_id, '-->', user_id, server_answer)
                            await user_manager[user_id].send_json(server_answer)
                        else:
                            print("User not found")
                    except WebSocketDisconnect:
                        raise WebSocketDisconnect

        except WebSocketDisconnect:
            print(f'{server_id} disconnected')
            server_manger.pop(server_id)
