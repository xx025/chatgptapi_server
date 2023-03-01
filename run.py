from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from message_forward import user, server
from setting import user_path, server_path, port, host

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user, prefix=f"/{user_path}")
app.include_router(server, prefix=f"/{server_path}")

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static', app=StaticFiles(directory='./chat/static'), name='static')
# .mount()不要在分路由APIRouter().mount()调用，模板会报错


templates = Jinja2Templates(directory='./chat/templates')


@app.get("/")
def index(request: Request):
    ws_api = f"ws://{host}:{port}/{user_path}"
    page_params = {"request": request, "ws_api": ws_api}
    return templates.TemplateResponse("index.html", page_params)


if __name__ == "__main__":
    import uvicorn

    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
    uvicorn.run('run:app', host='0.0.0.0', port=port,
                reload=True,
                reload_delay=0.25,
                ws_ping_interval=99999,
                ws_ping_timeout=99999,
                timeout_keep_alive=99999
                )
    # linux 部署
    # #  部署 ：nohup uvicorn run:app --host=0.0.0.0 --port=8010 --ws-ping-interval=99999 --ws-ping-timeout=99999 --timeout-keep-alive=99999 > output.log 2>&1 &
