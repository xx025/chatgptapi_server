from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from message_forward import user, server

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user, prefix='/user', )
app.include_router(server, prefix='/server')

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
    uvicorn.run('run:app', host='0.0.0.0', port=8010, reload=True, reload_delay=0.25)
