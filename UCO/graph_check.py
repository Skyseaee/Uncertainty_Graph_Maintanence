def has_cycle(adj_matrix, is_directed=False):
    """
    检测邻接矩阵表示的图是否存在环
    :param adj_matrix: 二维列表表示的邻接矩阵
    :param is_directed: 是否为有向图（默认无向）
    :return: True/False
    """
    n = len(adj_matrix)
    
    # 辅助函数：有向图的DFS环检测
    def _dfs_directed():
        visited = [False] * n
        rec_stack = [False] * n

        def dfs(node):
            if not visited[node]:
                visited[node] = True
                rec_stack[node] = True
                for neighbor in range(n):
                    if adj_matrix[node][neighbor]:
                        if not visited[neighbor]:
                            if dfs(neighbor):
                                return True
                        elif rec_stack[neighbor]:
                            return True
                rec_stack[node] = False
            return False

        for node in range(n):
            if dfs(node):
                return True
        return False

    # 辅助函数：无向图的并查集环检测
    def _union_find_undirected():
        # 检查自环
        for i in range(n):
            if adj_matrix[i][i]:
                return True

        parent = list(range(n))

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]  # 路径压缩
                u = parent[u]
            return u

        for i in range(n):
            for j in range(i+1, n):  # 避免重复处理无向边
                if adj_matrix[i][j]:
                    root_i = find(i)
                    root_j = find(j)
                    if root_i == root_j:
                        return True
                    parent[root_j] = root_i
        return False

    # 根据图类型选择检测方法
    if is_directed:
        return _dfs_directed()
    else:
        return _union_find_undirected()


# 测试用例
if __name__ == "__main__":
    # 无向图测试
    print("无向图测试:")
    # 有自环的无向图
    adj_self_loop = [
        [1, 0],
        [0, 0]
    ]
    print(has_cycle(adj_self_loop))  # True

    # 三角形环
    adj_triangle = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]
    print(has_cycle(adj_triangle))  # True

    # 树状无环
    adj_tree = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    print(has_cycle(adj_tree))  # False

    # 有向图测试
    print("\n有向图测试:")
    # 简单环
    adj_dir_cycle = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ]
    print(has_cycle(adj_dir_cycle, is_directed=True))  # True

    # 无环有向图
    adj_dag = [
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]
    print(has_cycle(adj_dag, is_directed=True))  # False

    # 自环有向图
    adj_dir_self_loop = [[1]]
    print(has_cycle(adj_dir_self_loop, is_directed=True))  # True