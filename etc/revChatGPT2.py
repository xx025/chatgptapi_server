import json

from revChatGPT.V1 import Chatbot
from ws4py.client.threadedclient import WebSocketClient
from ws4py.messaging import TextMessage

accessToken = "account of chatgpt accesstoken"


class CG_Client(WebSocketClient):

    def received_message(self, resp: TextMessage):
        prompt = json.loads(str(resp)).get('msg', 'hello')
        print(prompt)

        chatbot = Chatbot(config={"access_token": accessToken })
        response = ""
        for data in chatbot.ask(prompt):
            response = data["message"]
        data = json.dumps({'msg': response})
        self.send(data)


if __name__ == '__main__':
    ws = None
    try:
        ws = CG_Client('ws://localhost:8010/server?token=r64XoPjdpVWPpSTrnin1')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
