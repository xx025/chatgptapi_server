from aioredis import Redis

from setting import max_users

"""
this explains form chatgpt

aioredis 和 redis 都是用于 Python 编程语言的 Redis 客户端库。两者之间的主要区别在于它们的实现方式和所支持的异步编程模型。

redis 是一个同步客户端，它使用阻塞 I/O 操作与 Redis 服务器进行通信。当您向 Redis 发送命令时，它会一直等待 Redis 响应才会返回结果。这意味着您需要为每个 Redis 连接创建一个新的线程，以确保您的应用程序不会被阻塞。

相比之下，aioredis 是一个异步客户端，它使用非阻塞 I/O 操作与 Redis 服务器进行通信。这意味着您可以使用协程和异步函数来编写代码，而无需为每个 Redis 连接创建一个新的线程。这使得它在异步应用程序中具有更好的性能和可伸缩性，并且在处理高并发请求时更加稳定。

因此，如果您正在使用 Python 的异步编程模型（例如 asyncio），则应该使用 aioredis。如果您使用的是传统的同步编程模型，那么可以使用 redis。
"""

r = Redis(host='127.0.0.1', port=6379, db=0)
# 连接Redis数据库

manger_app = {'app1_status': 0}

user_manager = {}  # 用户管理

max_users = max_users  # 最大用户数量
