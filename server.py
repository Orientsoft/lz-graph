from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import os

import pandas as pd

# consts
root_path = '/home/voyager/project/lz-graph/data/'

node_df = pd.read_csv(os.path.join(root_path, 'nodes.csv'))
type_list = node_df['CUSTOMTYPE']

link_df = pd.read_csv(os.path.join(root_path, 'stat_links.csv'))
source_list = link_df['source']
target_list = link_df['target']

# init data
init_dict = {
    'node_count': len(type_list),
    'source_list': source_list,
    'target_list': target_list
}

task_queue = Queue()
result_queue = Queue()

class QueueManager(BaseManager): pass
QueueManager.register('get_task_queue', callable=lambda:task_queue)
QueueManager.register('get_result_queue', callable=lambda:result_queue)
QueueManager.register('get_init_dict', callable=lambda:init_dict)

manager = QueueManager(address=('0.0.0.0', 50000), authkey=b'asdfjkl;')

server = manager.get_server()
server.serve_forever()

print('listening')
