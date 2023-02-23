from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.endpoints import WebSocketEndpoint
from fastapi.responses import HTMLResponse
from enum import Enum
from typing import Any, Dict, List, Optional
import asyncio

app = FastAPI()


import redis
import aioredis
import os

class ConnectionManager:
    def __init__(self):
        # 保存当前所有的链接的websocket对象
        # self.active_connections: List[WebSocket] = []
        self.active_connections = []

    async def connect(self, websocket: WebSocket):


        client = str(websocket)[1:-1].split(' ')[3]
        print("是后端还是兑换",client)
        await websocket.accept()
        # 添加到当前已链接成功的队列中进行管理
        self.active_connections.append(websocket)

    async def close(self, websocket: WebSocket):
        # 主动的断开的客户端的链接，不是抛出异常的方式断开
        await websocket.close()
        self.active_connections.remove(websocket)

    async def disconnect(self, websocket: WebSocket):
        # 从队列里面删除我们的已经断开链接的websocket对象
        self.active_connections.remove(websocket)
        # await websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # 发现消息
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        # 循环变量给所有在线激活的链接发送消息-全局广播
        print("当前的用户链接数，",len(self.active_connections))
        for connection in self.active_connections:
            await connection.send_text(message)




@app.get("/test")
async def get34545():
    print("全局广播！！！PID", os.getpid())
    app.state.pubmessage.publish('message_channel_http', "我要全局广播！！！！！！！！！！")
    return '我要全局广播！'





@app.websocket_route("/ws/{user_id}", name="ws")
class EchoSever(WebSocketEndpoint):
    encoding: str = "text"
    session_name: str = ""
    count: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 从args中提取对应的输入的参数信息
        print(args[0]['endpoint'])
        print(args[0]['path_params'])
        self.user_id: Optional[str] = args[0]['path_params'].get('user_id')

    # 开始有链接上来的时候对应的处理
    async def on_connect(self, websocket):
        await  app.state.manager.connect(websocket)
        print("进入房间的时候的pid",  os.getpid())
        await  app.state.manager.broadcast(f"游客： {self.user_id}进入了房间！")
        # await self.daojishi(websocket)

    # 客户端开始有数据发送过来的时候的处理
    async def on_receive(self, websocket, data):
        # timeout_count = getattr(websocket, 'timeout_count')
        # setattr(websocket, 'timeout_count', 0)
        print("说话时候的PID", os.getpid())
        await  app.state.manager.broadcast(f"游客：{self.user_id} 说》{data}")

    # 客户端断开链接的时候
    async def on_disconnect(self, websocket, close_code):
        # 进行全局的广播所有的在线链接的所有用户消息
        try:
            await  app.state.manager.disconnect(websocket)
            # 广播给其他所有在线的websocket
            await  app.state.manager.broadcast(f"游客： {self.user_id} 离开了聊天室")
        except ValueError:
            # 倒计时自动结束的之后，客户端再点击一次断开的时候异常处理！
            pass



@app.on_event('startup')
async def on_startup():

    # 异步redis消息的队列的处理机制
    # https://aioredis.readthedocs.io/en/v1.2.0/start.html
    pubmessage = await aioredis.create_redis( 'redis://localhost')
    await pubmessage.set("ceshi","我是测试数据")
    sadsa = await pubmessage.get("ceshi")
    print('读取测试数据，验证redis链接情况：',sadsa)
    print("读取测试数据，验证redis链接情况！！！PID", os.getpid())

    app.state.pubmessage = pubmessage

    # 执行消息订阅机制
    loop = asyncio.get_event_loop()
    loop.create_task(register_pubsub())



async def register_pubsub():
    pool = await aioredis.create_pool( 'redis://localhost',minsize=5, maxsize=10)
    async def reader(channel):
        # 进行消息的消费
        while await channel.wait_message():
            msg = await channel.get(encoding='utf-8')
            print("========================================>")
            print("全局的广播信息！！！essage in {}: {}".format(channel.name, msg))
            # 执行全局的消息广播
            await app.state.manager.broadcast(f"HTTP游客：接收到全局的广播信息！")

    with await pool as conn:
        # 执行消息注册
        await conn.execute_pubsub('subscribe', 'message_channel_http')
        channel = conn.pubsub_channels['message_channel_http']
        await reader(channel)  # wait for reader to complete
        await conn.execute_pubsub('unsubscribe', 'message_channel_http')

    # 加下面的的话就会容易断开！傻叉了！
    # pool.close()
    # await pool.wait_closed()



@app.on_event('startup')
async def on_startup():

    manager = ConnectionManager()
    # 设置发布者属性对象
    app.state.manager = manager
    # 设置任务渠道消费者


if __name__ == '__main__':
    import uvicorn
    # import threading
    # kkl =threading.Thread(target=doresubscribe)
    # kkl.start()


    uvicorn.run('wstest:app', host='0.0.0.0', port=9082, access_log=False, workers=2, use_colors=True)
    # uvicorn.run(app='wstest:app', host="127.0.0.1", port=8000, workers =5, reload=True, debug=True)