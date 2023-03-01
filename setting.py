# this is a setting file that you can set some base parameters

from configobj import ConfigObj

import os

#  将配置信息写在setting.cfg或example.setting.cfg中
if os.path.exists('setting.cfg'):
    setting_path = 'setting.cfg'
else:
    setting_path = 'example.setting.cfg'

config = ConfigObj(setting_path, encoding='UTF-8')

wbs = config.get('webserver', {})

host = wbs.get('host') or 'localhost'
# 主机地址，如果在云端请填写云端ip地址
port = wbs.get('port') or 8010
# 端口号
port = int(port)

user_path = wbs.get('user_path') or 'user'
# api路径 表现形式为`ws://localhost:port/user`
server_path = wbs.get('server_path') or 'server'
# chatgpt对接的服务端口

server_tokens = wbs.get('server_tokens') or ['r64XoPjdpVWPpSTrnin1', 'hkyH8Ldxf17l9N9FYBoa']
# 为chat服务连接设置验证机制

max_users = wbs.get('max_users') or 3  # 最多支持用户连接数
max_users = int(max_users)

# Redis 配置

reds = config.get('redis', {})
redis_host = reds.get('host') or '127.0.0.1'
# redis数据库地址
redis_port = reds.get('port') or 6379  # 断开
redis_port = int(redis_port)

redis_db = reds.get('db') or 0
# 数据库序号
redis_db = int(redis_db)
