// ==UserScript==
// @name         ChatGPT-link-to-PythonWeb
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  关注：https://github.com/xx025/browser-chatgptapi
// @author       You
// @match        https://chat.openai.com/chat*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=openai.com
// @require      https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/reconnecting-websocket/1.0.0/reconnecting-websocket.js
// @grant        none
// ==/UserScript==


(function () {
    'use strict';


    console.log(`// @name         ChatGPT-link-to-PythonWeb
// @description  关注：https://github.com/xx025/browser-chatgptapi`)

    let server_url = "ws://localhost:8010/server/server"
    // 如果只是本机测试，请勿做改变，当然注意端口号
    //  如果web服务器与脚本运行的客户端不在一个机器上，需要在chrome
    //  中关闭安全检查允许Https+ws这种允许方式
    // 可参考：https://blog.csdn.net/qq_36657291/article/details/111947175


    var ws = new ReconnectingWebSocket(server_url);

    // ReconnectingWebSocket 这是一个websocket断开自动重连的库, https://github.com/joewalnes/reconnecting-websocket
    // 使用字节跳动的CDN https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/reconnecting-websocket/1.0.0/reconnecting-websocket.js


    let input_eara = document.querySelector('textarea')  // 文本框
    let btn = input_eara.nextSibling;//发送按钮

    let k = 0;
    let listener = false;
    ws.onmessage = function (event) {
        let lt = JSON.parse(event.data)
        console.log(lt.msg)
        input_eara = document.querySelector('textarea')
        btn = input_eara.nextSibling
        // 向chatgpt发送消息
        input_eara.value = lt.msg;
        input_eara.nextSibling.click();
        k = 0;

        if (!listener) {
            listener = true;
            btn.addEventListener('DOMSubtreeModified', function () {
                // 对发送按钮进行监听，可获取一个轮回完成事件
                k += 1
                if (k === 6) {
                    let selectorAll = document.querySelectorAll('.markdown');
                    let result = selectorAll[selectorAll.length - 1].innerText
                    console.log(result)
                    ws.send(JSON.stringify({msg: result}))
                }
            }, false);
        }
    };
})();




