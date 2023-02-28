from pydantic import BaseModel, Field


class Message(BaseModel):
    msg: str = Field(...,
                     max_length=300,
                     description='This is the request body format for sending messages'
                     )


