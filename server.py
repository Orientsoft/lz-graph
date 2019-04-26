from multiprocessing.managers import BaseManager
import Queue

task_queue = Queue.Queue()
result_queue = Queue.Queue()

class QueueManager(BaseManager): pass
QueueManager.register('get_task_queue', callable=lambda:task_queue)
QueueManager.register('get_result_queue', callable=lambda:result_queue)

manager = QueueManager(address=('', 50000), authkey='python_queue_server')

server = manager.get_server()
server.serve_forever()
