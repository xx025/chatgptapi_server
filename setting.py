# this is a setting file that you can set some base parameters

host = 'localhost'  # 主机地址，如果在云端请填写云端ip地址
port = 8010  # 端口号

user_path = 'user'  # api路径 表现形式为`ws://localhost:port/user`
server_path = 'server'  # chatgpt对接的服务断开

server_tokens = ['r64XoPjdpVWPpSTrnin1', 'hkyH8Ldxf17l9N9FYBoa']  # 为chat服务连接设置验证机制

max_users = 3  # 最多支持用户连接数

# Redis 配置
redis_host = '127.0.0.1'  # 主机地址
redis_port = 6379  # 断开
redis_db = 0  # 数据库序号
