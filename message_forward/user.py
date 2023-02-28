import json

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from message_forward.manger import user_manager, max_users, server_manger, r
from message_forward.models import Message

user = APIRouter()

index = 0


def get_user_id():
    global index
    index += 1
    return f'user{index}'


async def sendto_server(data: Message, user_id: str):
    """

    :param data: Message 对象，需要先转换成json对象再进行json dumps存储
    :param user_id:
    :return:
    """
    if len(server_manger) > 0:

        await r.lpush('msgs', json.dumps({'user_id': user_id,
                                          'query_msg': data.json()}))
    else:
        return 'No service available.'


async def receive_query_data(user_id):
    try:
        data = await user_manager[user_id].receive_json()
        return Message(**data)
    except ValidationError:
        await user_manager[user_id].send_json(
            {'msg': 'Data format error or query parameter too '
                    'long. The query parameter is limited to '
                    '300 characters or less.'})
    except WebSocketDisconnect:
        raise WebSocketDisconnect


@user.websocket("")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    if not len(user_manager) < max_users:
        await ws.send_json({'msg': 'User overload, please try again later.'})
        await ws.close()
    else:

        user_id = get_user_id()
        user_manager[user_id] = ws

        wait_status = False
        await ws.send_json({'msg': f'Connection successful, your ID is {user_id}.'})

        try:
            while True:
                data = await receive_query_data(user_id)
                if data:
                    if wait_status:
                        await ws.send_json({'msg': 'Please wait for the previous message to return.'})
                    else:
                        await sendto_server(data, user_id)

        except WebSocketDisconnect:

            print(f'{user_id}user disconnected')
            user_manager.pop(user_id)
