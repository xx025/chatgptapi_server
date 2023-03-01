# browser-chatgptapi
![Snipaste_2023-03-01_22-59-42.png](imgs%2FSnipaste_2023-03-01_22-59-42.png)
这是一个，ChatGPT3.5 API 服务（即在OpenAI网页使用的模型），它允许连接多个ChatGPT账户协同工作，并构建一个对外的API接口服务。

## 快速开始

在此之前你需要有一个redis数据库，在`example.setting.cfg`一些基础的配置选项，包含主机地址、端口号、redis数据库等。

1. 运行web服务

    
    
    ```shell
    git clone -b master https://github.com/xx025/browser-chatgptapi.git
    cd browser-chatgptapi
    pip install virtualenv
    virtualenv venv
    venv\Scripts\activate.bat  
    pip install -r requirements.txt
   python run.py
   ```

   此时web服务正在允许，他有两个重要的接口
   
    - `ws://localhost:8010/user` 供用户连接
    - `ws://localhost:8010/server` 供chatgpt服务连接
   
   数据格式示例：
   
      ```json
      {
         "msg": "hello, i am user1"
      }   
      ```
   
   
      ```json
   {
       "msg": "hello user1, i am  server1"
   }   
      ```



2. 连接chatgpt服务
   
   - 下面是工作在revChatGPT[完整代码](etc/revChatGPT2.py)
   ```python
    import json
    from revChatGPT.V1 import Chatbot
    from ws4py.client.threadedclient import WebSocketClient
    from ws4py.messaging import TextMessage
     
    class CG_Client(WebSocketClient):    
        def received_message(self, resp:TextMessage):
            prompt = json.loads(str(resp)).get('msg', 'hello')
            print(prompt)
            access_token = "you_access_token"
            chatbot = Chatbot(config={"access_token": access_token})
            response = ""
            for data in chatbot.ask(prompt):
                response = data["message"]
            data = json.dumps({'msg': response})
            self.send(data)    
    
    if __name__ == '__main__':
        ws = None
        try:
            ws = CG_Client('ws://127.0.0.1:8010/server?token=r64XoPjdpVWPpSTrnin1')
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()
   ```
   
   [其他](etc/etc.md)
   
3. 进行测试

   我写了一个简单的测速页面你可以打开一个或多个`http://localhost:8010/` 进行测试，你可以用postman打开一个WebSocket
   API测速页面进行测式

### 演示：

**演示视频**：[YouTube](https://www.youtube.com/watch?v=dis8NDfT16I)

![image](imgs/api_test.png)

### 架构图

![架构图.png](imgs/en_architecture-diagram.png)

### 最后

**代码比较简陋，可完善之处多多，欢迎参与一起开发**


```shell

git checkout --orphan latest_branch
git add -A
git commit -am "Initial commit"
git branch -D main
git branch -m main
```
