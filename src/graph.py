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
