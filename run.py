from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

app = FastAPI(
    docs_url='/doc'
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

socket_manager = dict()

wait = False


async def sendto_server(data):
    # global wait
    # if not wait:
    #     wait = True
    #     await socket_manager['server'].send_json(data)
    # else:
    #     return True

    await socket_manager['server'].send_json(data)


async def sendto_user(data):
    global wait
    await socket_manager['user'].send_json(data)
    wait = False


@app.websocket("/server/{server}")
async def websocket_endpoint(websocket: WebSocket, server: str):
    ws = websocket
    await ws.accept()

    socket_manager['server'] = ws
    # if not websocket.headers.get('x-user-type') == 'server':
    #     await ws.send_json({"message": "这个接口只供服务端连接"})
    #     await ws.close(code=882)

    if socket_manager.get('user'):
        await sendto_user({'msg': '服务端加入成功'})

    try:
        while True:
            data = await websocket.receive_json()

            print(data)
            if not socket_manager.get('user'):
                await ws.send_json({'msg': '客户端未加入'})
            else:
                await sendto_user(data)

    except WebSocketDisconnect:
        # await ws.close()
        socket_manager.pop('server')


@app.websocket("/user/{user}")
async def websocket_endpoint(ws: WebSocket, user: str):

    await ws.accept()
    socket_manager['user'] = ws
    await ws.send_json({'msg': '连接成功'})

    try:
        while True:
            data = await ws.receive_json()
            print(data)
            if not socket_manager.get('server'):
                await ws.send_json({'msg': '服务端未加入'})
            else:
                result = await sendto_server(data)
                if result:
                    await ws.send_json({'msg': '请等待上一条消息返回'})

    except WebSocketDisconnect:

        print('user disconnected')
        socket_manager.pop('user')


templates = Jinja2Templates(directory='./')


@app.get("/")
def index(request: Request):
    api_url = 'ws://localhost:8010/user/user1'
    return templates.TemplateResponse("index2.html",
                                      {"request": request, 'api_url': api_url})


if __name__ == "__main__":
    import uvicorn

    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
    # 如果是linux服务器并且附带python37+环境则直接运行 pip install fastapi jinja2 uvicorn[standard]
    uvicorn.run('run:app', host='0.0.0.0', port=8010)
