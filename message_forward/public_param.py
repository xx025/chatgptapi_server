from queue import Queue

socket_manager = dict()

wait = False

current_wait_user = None  # 当前正在等待的用户

server_status = -1
query_queue = Queue(maxsize=0)

user_manager = {}

server_manager = {}


async def sendto_server(data, user_id):
    if server_status == 1:

        await server_manager["server"].send_json(data)
        current_wait_user = user_id

        query_queue.put((data, user_id))
        pass
    else:
        return 'No service available.'
