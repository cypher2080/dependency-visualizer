from src.errors import ConfigError

KEYS = ("package", "repository", "test_mode", "max_depth", "exclude")
TRUE_WORDS = ("true", "yes", "on")
FALSE_WORDS = ("false", "no", "off")
QUOTES = ("'", '"')
MIN_DEPTH = 1


class Config:
    def __init__(self, package, repository, test_mode, max_depth, exclude):
        self.package = package
        self.repository = repository
        self.test_mode = test_mode
        self.max_depth = max_depth
        self.exclude = exclude

    def items(self):
        return [(key, getattr(self, key)) for key in KEYS]


def load_config(path):
    try:
        with open(path, encoding="utf-8") as stream:
            text = stream.read()
    except OSError:
        raise ConfigError("не удалось открыть файл " + str(path))
    return build_config(parse_yaml(text))


def parse_yaml(text):
    data = {}
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ConfigError("строка %d: ожидается 'ключ: значение'" % number)
        key, value = line.split(":", 1)
        key = key.strip()
        if key in data:
            raise ConfigError("строка %d: повтор ключа %s" % (number, key))
        data[key] = _unquote(value.strip())
    return data


def _unquote(value):
    if len(value) > 1 and value[0] in QUOTES and value[-1] == value[0]:
        return value[1:-1]
    if " #" in value:
        return value.split(" #", 1)[0].strip()
    return value


def build_config(data):
    for key in data:
        if key not in KEYS:
            raise ConfigError("неизвестный параметр " + key)
    return Config(
        package=_package(data),
        repository=_required(data, "repository"),
        test_mode=_bool(data.get("test_mode", "false")),
        max_depth=_depth(data.get("max_depth", "")),
        exclude=data.get("exclude", ""),
    )


def _required(data, key):
    value = data.get(key, "")
    if not value:
        raise ConfigError("не задан параметр " + key)
    return value


def _package(data):
    name = _required(data, "package")
    if any(char.isspace() for char in name):
        raise ConfigError("имя пакета не должно содержать пробелов")
    return name


def _bool(value):
    if value.lower() in TRUE_WORDS:
        return True
    if value.lower() in FALSE_WORDS:
        return False
    raise ConfigError("test_mode должен быть true или false")


def _depth(value):
    try:
        depth = int(value)
    except ValueError:
        raise ConfigError("max_depth должен быть целым числом")
    if depth < MIN_DEPTH:
        raise ConfigError("max_depth должен быть не меньше 1")
    return depth
