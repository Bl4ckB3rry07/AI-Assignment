from collections import deque

def bfs(start):
    print("\n=== Breadth-First Search (BFS) ===")
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print(" Goal found using BFS!")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print_path(path)
            print(f" Total steps: {len(path) - 1}")
            return path
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = OPEN + new_pairs
    print(" Goal not found.")
    return []

def dfs(start):
    print("\n=== Depth-First Search (DFS) ===")
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print(" Goal found using DFS!")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            print_path(path)
            print(f" Total steps: {len(path) - 1}")
            return path
        else:
            CLOSED.append(node_pair)
            children = N.moveGen()
            new_nodes = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(node, N) for node in new_nodes]
            OPEN = new_pairs + OPEN
    print(" Goal not found.")
    return []

def reconstructPath(goal_node_pair, CLOSED):
    parent_map = {}
    for node, parent in CLOSED:
        parent_map[node] = parent

    path = []
    goal_node, parent = goal_node_pair
    path.append(goal_node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]
    return path

def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
    closed_nodes = [node for node, parent in CLOSED]
    new_nodes = [c for c in children if c not in open_nodes and c not in closed_nodes]
    return new_nodes

def print_path(path):
    print(" Path:")
    for i, node in enumerate(path):
        end = " " if i == len(path) - 1 else " ->"
        print(f"  {node}{end}")
        
        

from rab import RabbitState
from bridge import BridgeState

# Modified Rabbit Problem
start_rabbit = RabbitState("LLL_RRR")
bfs(start_rabbit)
dfs(start_rabbit)

# Modified Bridge Problem
start_bridge = BridgeState({'Amogh', 'Ameya', 'Grandmother', 'Grandfather'}, set(), 0, 'L')
bfs(start_bridge)
dfs(start_bridge)

