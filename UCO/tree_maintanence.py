import copy
import math

import maintanence
import UCO
import change_graph
import tree_construct
import decorate

@decorate.wrapper
def tree_maintenance(k_core, heaps, index_of_changed_points, graph, threshold, origin_tree):
    final_index = maintanence.core_maintenance(k_core, heaps, index_of_changed_points, copy.deepcopy(graph))
    changed = find_changed(maintanence.transpose_matrix(heaps, k_core), final_index, k_core)

    for i in range(k_core):
        change = changed[i]
        need_split = []
        for k, c in enumerate(change):
            if c != 0 and find_changed(heaps[k][i], final_index[i][k], threshold):
                continue
            # find the node
            node = tree_construct.find_node_from_up_to_down(origin_tree[i], k)
            bottom = find_bottom(origin_tree[i])
            # split node
            node.split_node(k, final_index[i][k], graph, threshold, bottom)

def find_changed(old_heap, new_heap, k_core):
    changed = [[] for _ in range(k_core)]
    for i, (old, new) in enumerate(zip(old_heap, new_heap)):
        length = max(len(old), len(new))
        changed[i] = list(range(length))
        for j in range(length):
            if j < len(old) and j < len(new):
                if new[j] == old[j]:
                    continue
                changed[i][j] = 1 if new[j] - old[j] > 0 else -1
            elif j < len(old):
                changed[i][j] = -1
            else:
                changed[i][j] = 1

    return changed


def whether_in_same_interval(old, new, threshold):
    ceil = math.ceil(old / threshold) * threshold
    floor = ceil - threshold
    if floor <= new <= ceil:
        return True
    else:
        return False


def find_bottom(root):
    if isinstance(root, tree_construct.BottomTreeNode):
        return root
    return find_bottom(root.children[0])


if __name__ == '__main__':
    graph = [
        [.0, .5, .2, .0, .0, .0, .0, .0, .0, .0],
        [.5, .0, .8, .2, .6, .0, .0, .0, .0, .0],
        [.2, .8, .0, .5, .8, .0, .0, .0, .0, .0],
        [.0, .2, .5, .0, .4, .0, .0, .0, .0, .0],
        [.0, .6, .8, .4, .0, .2, .0, .0, .0, .0],
        [.0, .0, .0, .0, .2, .0, .5, .0, .0, .0],
        [.0, .0, .0, .0, .0, .5, .0, .8, .5, .8],
        [.0, .0, .0, .0, .0, .0, .8, .0, .0, .0],
        [.0, .0, .0, .0, .0, .0, .5, .0, .0, .8],
        [.0, .0, .0, .0, .0, .0, .8, .0, .8, .0],
    ]

    heaps = UCO.UCO_Index(graph)
    origin_tree = tree_construct.construct_tree(graph, 0.01)
    k_core = len(heaps[0])
    for h in heaps:
        k_core = max(k_core, len(h))
    indexes_of_changed_points = change_graph.pipeline_change_map(graph, True)
    print(tree_maintenance(k_core, heaps, indexes_of_changed_points, graph, origin_tree))
