from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from message_forward import user, app1
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
app.include_router(app1, prefix=f"/{server_path}")

templates = Jinja2Templates(directory='./')


@app.get("/")
def index(request: Request):
    ws_api = f"ws://{host}:{port}/{user_path}"
    page_params = {"request": request, "ws_api": ws_api}
    return templates.TemplateResponse("index2.html", page_params)


if __name__ == "__main__":
    import uvicorn

    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
    # 如果是linux服务器并且附带python37+环境则直接运行 pip install fastapi jinja2 uvicorn[standard]
    uvicorn.run('run:app', host='0.0.0.0', port=port, reload=True, reload_delay=0.25)
