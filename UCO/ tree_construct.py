# UCF Construct
import sys
import copy
from functools import cmp_to_key

import UCO
import heap
from maintanence import delete_edges

class TreeNode:
    nodes: []
    threshold: float
    children: []
    k: int
    upper_threshold: float
    lower_threshold: float

    def __init__(self, nodes, k, threshold):
        self.nodes = nodes
        self.k = k
        self.upper_threshold = threshold
        self.lower_threshold = threshold

    def get_threshold(self) -> float:
        return max(self.upper_threshold, self.lower_threshold)


def construct_tree(graph: [[]], k_probs: [[]], edge: [], threshold=0.1):
    assert threshold <= 0.1, "threshold is too big"
    # compare core
    core = cal_core(graph)
    cores = [[i, c] for i, c in enumerate(core)]
    sorted(cores, key=cmp_to_key(lambda x, y: y[1] - x[1]))
    k_max = cores[0][1]
    for k in range(k_max, 0, -1):        
        temp_graph, vertex = extract_graph(graph, k)
        probs = [UCO.cal_prob(temp_graph, index, k) for index in vertex]
        cur_thres = 0
        S = list() # S is a stack
        eta_threshold = [0 for _ in range(len(vertex))]
        probs_index = [[prob, i] for i, prob in enumerate(probs)]
        heaps = heap.Heap(probs_index, compare=lambda a, b: a[0] > b[0])
        heaps.heapify()

        while UCO.graph_is_empty(temp_graph):
            u = heaps.heap_pop()
            cur_thres = max(cur_thres, u[0])
            eta_threshold[u[1]] = cur_thres
            S.append(u[1])

            # remove v from vertex set
            vertex.remove(u[1])
            for i, neighbor in enumerate(temp_graph[u[1]]):
                if neighbor != 0:
                    # remove neighbor edge from map
                    UCO.remove_edge_from_graph(temp_graph, u[1], i)

                    # update k probs

                    probs = [UCO.cal_prob(temp_graph, index, k) for index in vertex]
                    probs_index = [[prob, i] for i, prob in zip(vertex, probs)]
                    heaps = heap.Heap(probs_index, compare=lambda a, b: a[0] > b[0])
                    heaps.heapify()

        construct_eta_k_tree(graph, k, S, eta_threshold)
    


def cal_core(graph: [[]]):
    n = len(graph)
    core = list(range(n))
    vertex = set(list(range(n)))
    while len(vertex) != 0:
        degree = degree_certain_graph(graph)
        index = find_min(degree)
        k = degree[index]
        temp_vertex = []
        while degree[index] <= k:
            core[index] = k
            # remove edge
            for i in range(n):
                if graph[index][i] != 0:
                    degree[i] -= 1
            
            vertex.remove(index)
            # update index
            index = find_min(degree)


    return core


def find_min(degree):
    index, k = -1, sys.maxsize
    for i, d in enumerate(degree):
        if d < k:
            k = d
            index = i

    return index


def degree_certain_graph(graph: [[]]):
    n = len(graph)
    vertex = list(range(n))
    for i, g in enumerate(graph):
        for p in g:
            if p != 0:
                vertex[i] += 1
    
    return vertex


def extract_graph(graph, k, cores):
    vertex = []
    for core in cores:
        if core[1] >= k:
            vertex.append(core[0])
    
    temp_graph = copy.deepcopy(graph)
    delete_edges(temp_graph, vertex)
    return temp_graph, set(vertex)


def find_connected_component(graph, vertexes) -> [[]]:
    if len(vertexes) <= 1:
        return [vertexes]
    
    node_index, n, group = 0, len(vertexes), 0

    res = [-1 for _ in range(n)]
    res[node_index] = group

    while node_index < n:
        find_more = True
        neighbor = set([i for i, v in enumerate(graph[vertexes[node_index]]) if v != 0])

        while find_more:
            find_more = False
            for v in vertexes:
                if res[v] == -1 and v in neighbor:
                    res[v] = res[node_index]
                    find_more = True
                    neighbor = neighbor | set([i for i, v in enumerate(graph[v]) if v != 0])
        
        i = 0
        while i < n and res[i] != -1:
            i += 1
        node_index = i
        group += 1
    
    ans = [[] for _ in range(group)]
    for i, r in enumerate(res):
        ans[r].append(i)  
    return ans  


def find_neighbors(graph, vertexes):
    neighbor = set()
    for v in vertexes:
        neighbor = neighbor | set([i for i, v in enumerate(graph[v]) if v != 0])
    
    return neighbor

        
def construct_eta_k_tree(graph: [[]], k: int, stack: [], eta_threshold: []):
    while len(stack) != 0:
        node = stack[-1]
        stack = stack[:-1]
        ct = eta_threshold[node]
        H = []
        while len(stack) != 0 and eta_threshold[stack[-1]] == ct:
            H.append(stack[-1])
            stack = stack[:-1]
        
        for connected in find_connected_component(graph, H):
            X_treeNode = TreeNode(connected, k, ct)
            for v in find_neighbors(graph, connected):
                if eta_threshold[v] < ct:
                    continue
                # 1. get the node containing v (Y)
                # 2. get the root of Y (Z)
                
                pass
