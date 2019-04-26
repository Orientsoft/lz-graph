from multiprocessing.managers import BaseManager

import networkx as nx

class QueueManager(BaseManager): pass
QueueManager.register('get_task_queue', callable=lambda:task_queue)
QueueManager.register('get_result_queue', callable=lambda:result_queue)

manager = QueueManager(address=('', 50000), authkey='python_queue_server')

manager.connect()
task_queue = manager.get_task_queue()
result_queue = manager.get_result_queue()

# init
G = nx.DiGraph()
G.add_nodes_from(range(task['node_count']))
G.add_edges_from([(task['source_list'][i], task['target_list'][i]) for i in range(len(task['source_list']))])

while True:
    task = task_queue.get()
    
    if (task['type'] == 'init'):
        
        
        result = {
            'edge_count': G.number_of_edges(),
            'node_count': G.number_of_nodes()
        }
        
    elif (task['type'] == 'subgraph'):
        edges = list(nx.bfs_edges(G, task['node'], depth_limit=task['bfs_depth']))
        nodes = [node] + [v for u, v in edges]
        
        result = {
            'edges': edges,
            'nodes': nodes
        }
        
        result_queue.put(result)

    