import sys

from src.config import load_config
from src.errors import VisualizerError
from src.graph import build_graph, find_cycles
from src.local_repo import LocalRepository
from src.pypi import PypiRepository

DEFAULT_CONFIG = "config.yaml"
FAILURE_CODE = 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_CONFIG
    try:
        run(load_config(path))
    except VisualizerError as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return FAILURE_CODE
    return 0


def open_repository(config):
    if config.test_mode:
        return LocalRepository(config.repository)
    return PypiRepository(config.repository)


def run(config):
    repository = open_repository(config)
    graph = build_graph(
        repository, config.package, config.max_depth, config.exclude)
    print("Граф зависимостей %s:" % config.package)
    for name, deps in graph.items():
        print("  %s -> %s" % (name, ", ".join(deps) or "-"))
    for cycle in find_cycles(graph):
        print("Цикл: " + " -> ".join(cycle))


if __name__ == "__main__":
    sys.exit(main())
