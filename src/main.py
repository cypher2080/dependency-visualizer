import sys

from src.config import load_config
from src.d2 import render, to_d2
from src.errors import VisualizerError
from src.graph import build_graph, find_cycles, load_order
from src.local_repo import LocalRepository
from src.pypi import PypiRepository

DEFAULT_CONFIG = "config.yaml"
DEFAULT_MODE = "all"
FAILURE_CODE = 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_CONFIG
    mode = argv[1] if len(argv) > 1 else DEFAULT_MODE
    try:
        if mode not in MODES:
            raise VisualizerError("неизвестный режим " + mode)
        MODES[mode](load_config(path))
    except VisualizerError as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return FAILURE_CODE
    return 0


def open_repository(config):
    if config.test_mode:
        return LocalRepository(config.repository)
    return PypiRepository(config.repository)


def make_graph(config):
    return build_graph(
        open_repository(config), config.package,
        config.max_depth, config.exclude)


def show_params(config):
    for key, value in config.items():
        print("%s = %s" % (key, value))


def show_deps(config):
    names = open_repository(config).dependencies(config.package)
    print("Прямые зависимости %s:" % config.package)
    for name in names:
        print("  " + name)


def show_graph(config, graph=None):
    graph = graph or make_graph(config)
    print("Граф зависимостей %s:" % config.package)
    for name, deps in graph.items():
        print("  %s -> %s" % (name, ", ".join(deps) or "-"))
    for cycle in find_cycles(graph):
        print("Цикл: " + " -> ".join(cycle))


def show_order(config, graph=None):
    order, rest = load_order(graph or make_graph(config))
    print("Порядок загрузки: " + " ".join(order))
    if rest:
        print("Не загружены из-за цикла: " + " ".join(rest))


def show_d2(config, graph=None):
    text = to_d2(graph or make_graph(config))
    print("D2:")
    print(text, end="")
    image = render(text)
    if image:
        print("Изображение: " + image)


def show_all(config):
    graph = make_graph(config)
    show_graph(config, graph)
    show_order(config, graph)
    show_d2(config, graph)


MODES = {
    "params": show_params,
    "deps": show_deps,
    "graph": show_graph,
    "order": show_order,
    "d2": show_d2,
    "all": show_all,
}


if __name__ == "__main__":
    sys.exit(main())
