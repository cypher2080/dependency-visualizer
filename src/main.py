import sys

from src.config import load_config
from src.errors import VisualizerError
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


def run(config):
    repository = PypiRepository(config.repository)
    names = repository.dependencies(config.package)
    print("Прямые зависимости %s:" % config.package)
    for name in names:
        print("  " + name)


if __name__ == "__main__":
    sys.exit(main())
