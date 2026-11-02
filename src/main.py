import sys

from src.config import load_config
from src.errors import VisualizerError

DEFAULT_CONFIG = "config.yaml"
FAILURE_CODE = 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_CONFIG
    try:
        config = load_config(path)
    except VisualizerError as error:
        print("Ошибка: " + str(error), file=sys.stderr)
        return FAILURE_CODE
    for key, value in config.items():
        print("%s = %s" % (key, value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
