import os
import multiprocessing
from multiprocessing.managers import BaseManager

from tqdm import tqdm
import networkx as nx

cpu_count = os.cpu_count()

class QueueManager(BaseManager): pass
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
QueueManager.register('get_init_dict')

manager = QueueManager(address=('192.168.0.46', 50000), authkey=b'asdfjkl;')

manager.connect()
task_queue = manager.get_task_queue()
# result_queue = manager.get_result_queue()

# init
init_data = manager.get_init_dict()
node_count = init_data.get('node_count')
source_list = init_data.get('source_list')
target_list = init_data.get('target_list')

G = nx.DiGraph()
G.add_nodes_from(range(node_count))
for i in tqdm(range(len(source_list))):
    G.add_edges_from([(source_list[i], target_list[i])])

# G.add_edges_from([(source_list[i], target_list[i]) for i in range(2000)])

print('networkX G - nodes: {}, edges: {}'.format(
    G.number_of_nodes(),
    G.number_of_edges()
))

task_buffer = []

def worker_func(task):
    node = task['node']
    depth = task['bfs_depth']
        
    edges = list(nx.bfs_edges(G, node, depth_limit=depth))
    nodes = [node] + [v for u, v in edges]

    result = {
        'edges': edges,
        'nodes': nodes
    }
    
    print('subG {} depth {} - nodes: {}, edges: {}'.format(
        node,
        depth,
        len(nodes),
        len(edges)
    ))
    
    #result_queue = manager.get_result_queue()
    #result_queue.put(result)

def callback(result):
    result_queue = manager.get_result_queue()
    result_queue.put(result)

pool = multiprocessing.Pool(cpu_count)

while True:
    task = task_queue.get()
    pool.apply_async(worker_func, (task, ))
