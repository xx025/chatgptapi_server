from pydantic import BaseModel, Field


class Message(BaseModel):
    msg: str = Field(...,
                     max_length=300,
                     description='This is the request body format for sending messages'
                     )


class SendServerMessage(Message):
    """
    要在服务端区分哪一个user发送的请求，绑定对于的对话框
    """
    user_id: str = Field(..., description='user_id')
