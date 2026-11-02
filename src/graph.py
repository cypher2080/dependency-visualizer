from collections import deque


def build_graph(repository, root, max_depth, exclude=""):
    graph = {root: []}
    queue = deque([(root, 0)])
    while queue:
        name, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for child in repository.dependencies(name):
            if exclude and exclude in child:
                continue
            graph[name].append(child)
            if child not in graph:
                graph[child] = []
                queue.append((child, depth + 1))
    return graph


def find_cycles(graph):
    cycles = []
    for start in graph:
        stack = [(start, [start])]
        while stack:
            name, path = stack.pop()
            for child in graph.get(name, []):
                if child == start:
                    cycles.append(path + [start])
                elif child not in path and child > start:
                    stack.append((child, path + [child]))
    return cycles


def load_order(graph):
    waiting = {name: len(set(deps)) for name, deps in graph.items()}
    parents = {name: [] for name in graph}
    for name, deps in graph.items():
        for child in set(deps):
            parents[child].append(name)
    queue = deque(name for name, count in waiting.items() if count == 0)
    order = []
    while queue:
        name = queue.popleft()
        order.append(name)
        for parent in parents[name]:
            waiting[parent] -= 1
            if waiting[parent] == 0:
                queue.append(parent)
    rest = [name for name in graph if name not in order]
    return order, rest
