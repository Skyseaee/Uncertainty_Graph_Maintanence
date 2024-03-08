# UCF Construct
import sys
import copy
import UCO
import heap
from maintenance import delete_edges

class TreeNode:
    nodes: []
    threshold: float
    children: []
    k: int
    upper_threshold: float
    down_threshold: float


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

        construct_eta_k_tree()
    


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