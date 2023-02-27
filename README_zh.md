# browser-chatgptapi



**购买ChatGPT账号**: [价格实惠，1元起，去购买](https://xx025.github.io/z9c3c4)

**推荐魔法网络>支持ChatGPT**：[点此链接有月1元优惠套餐](https://xx025.github.io/773ycd9u) 



通过向浏览器OpenAI ChatGPT页面注入js脚本的方式，将网页上的ChatGPT变成一个API，支持多人同时连接

**如何使用**：[如何使用？](wiki/如何使用.md)


### 实现思路：

构建一个消息转发服务器，通过向浏览器ChatGPT页面注入脚本完成与服务器的通信，消息转发服务器允许多个用户进行连接，并且用户提出的查询进行排队依次处理并返回给用户。

### 演示：

**演示视频**：[YouTube](https://www.youtube.com/embed/o4SETVDbaEY)

![image](imgs/api_test.png)



### 架构图

![架构图.png](imgs/zh_architecture-diagram.png)



### 最后

**代码比较简陋，可完善之处多多，欢迎参与一起开发**