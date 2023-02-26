import json
from time import sleep

from fastapi import APIRouter
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from message_forward.manger import query_queue, manger_app, r, user_manager

app1 = APIRouter()


@app1.websocket("")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    manger_app['app1_status'] = 1

    for user_ws in user_manager.values():
        await user_ws.send_json({'msg': 'The server is now available'})
    while True:
        try:
            queue_length = await r.llen('msgs')
            if queue_length > 0:
                d1 = await r.rpop('msgs')

                data = json.loads(d1.decode('utf-8'))

                user_id = data['user_id']
                user_msg = json.loads(data['query_msg'])
                print(user_id, user_msg)
                await ws.send_json(user_msg)
                ans1 = await ws.receive_json()
                if user_manager.get(user_id):
                    await user_manager[user_id].send_json(ans1)
                else:
                    print("User not found")


        except WebSocketDisconnect:
            print(f'app1 disconnected')
            manger_app['app1_status'] = 0
