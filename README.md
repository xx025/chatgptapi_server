# browser-chatgptapi

将网页版ChatGPT做成API，

**如何使用**：[如何使用？](wiki/如何使用.md)

**真逆向ChatAPI**： [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT)

**推荐魔法网络**：[点此链接有月1元优惠套餐](https://xx025.github.io/773ycd9u.html)


### 实现思路：




一个web服务器，chatgpt网页利用注入脚本与服务器通信，接收查询语句并返回,利用sowebscoekt 协议与服务器进行通信。






- ./ChatGptPagesScripts.js :导入浏览器脚本管理器
- ./run.py web服务
- ./index.html 一个简单的测试页面



### 演示：
![image](https://user-images.githubusercontent.com/71559822/220007238-2b040e5e-1be7-404e-9cc6-3605f862660d.png)



### 架构图

暂时只能单用户，单个ChatGPT,未来看后期发展
![未命名绘图](https://user-images.githubusercontent.com/71559822/220315748-b6bb2d29-0243-4ac8-aab4-0296424689cb.png)



**代码比较简陋，可完善之处多多，欢迎参与一起开发**
