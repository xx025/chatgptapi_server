# browser-chatgptapi

通过向浏览器OpenAI ChatGPT页面注入js脚本的方式，将网页上的ChatGPT变成一个API，支持多人同时连接,支持托管多个ChatGPT账户

**如何使用**：[如何使用？](如何使用.md)

### 实现思路：

构建一个消息转发服务器，通过向浏览器ChatGPT页面注入脚本完成与服务器的通信，消息转发服务器允许多个用户进行连接，并且用户提出的查询进行排队依次处理并返回给用户。

### 演示：

**演示视频**：[YouTube](https://www.youtube.com/watch?v=dis8NDfT16I)

![image](../imgs/api_test.png)

### 架构图

![架构图.png](../imgs/en_architecture-diagram.png)

### 最后

**代码比较简陋，可完善之处多多，欢迎参与一起开发**