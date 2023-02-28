# browser-chatgptapi

[中文简体](wiki/README_zh.md)  

By injecting js scripts into the browser OpenAI ChatGPT page, ChatGPT on the web page is turned into an API that supports multiple simultaneous connections and  supports hosting multiple ChatGPT accounts.

**How to use**: [How to use?](wiki/如何使用.md)


### Implementation idea.

Build a message forwarding server, and complete communication with the server by injecting scripts into the browser ChatGPT page. The message forwarding server allows multiple users to connect, and queries raised by the user are queued and processed in order and returned to the user.

### Demonstration.

**Demo video**: [YouTube](https://www.youtube.com/watch?v=dis8NDfT16I)

![image](imgs/api_test.png)



### Architecture diagram

![architecture-diagram.png](imgs/en_architecture-diagram.png)



### Finally

**The code is relatively rudimentary, there is much room for improvement, welcome to participate in the development together**





*These translations come from deepl*

