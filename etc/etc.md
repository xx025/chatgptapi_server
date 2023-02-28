你也可以通过向网页注入js脚本完成连接

将脚本[ChatGptPagesScripts.js](ChatGptPagesScripts.js),导入如脚本管理器如`Tampermonkey`

打开OpenAI [ChatGPT官网](https://chat.openai.com/chat) 登录账号

正常登陆后通过注入的脚本，将会连接到web服务，当然你有的话，可以在浏览器中创建多个窗口登录多个账号

考虑到web服务与登录chatgpt账号的浏览器不在一个机器上，会出现`MixedContent`
错误，请查看[StackFlow](https://stackoverflow.com/questions/18321032)对此问题的解决方案