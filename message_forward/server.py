import json
from typing import Union

from fastapi import APIRouter, Query, Depends
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

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
                    # 暂时不知道问什么会取出None
                    data = json.loads(d1.decode('utf-8'))

                    user_id = data['user_id']
                    user_msg = json.loads(data['query_msg'])
                    print(user_id, user_msg)
                    await ws.send_json(user_msg)
                    ans1 = await ws.receive_json()
                    if user_manager.get(user_id):
                        print(user_id, ans1)
                        await user_manager[user_id].send_json(ans1)
                    else:
                        print("User not found")

        except WebSocketDisconnect:
            print(f'{server_id} disconnected')
            server_manger.pop(server_id)
