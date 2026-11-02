# Визуализатор графа зависимостей

CLI-инструмент строит граф зависимостей Python-пакетов (pip) и выводит его
на языке диаграмм [D2](https://d2lang.com). Зависимости берутся напрямую из
JSON API репозитория PyPI, без pip и сторонних библиотек.

Вариант №2, практическая работа №2 по дисциплине «Конфигурационное
управление».

## Возможности

- чтение настроек из YAML-файла с проверкой всех параметров;
- получение прямых зависимостей пакета с PyPI (`requires_dist`);
- построение транзитивного графа обходом в ширину (BFS) без рекурсии;
- ограничение глубины анализа и исключение пакетов по подстроке;
- корректная обработка циклических зависимостей и их вывод;
- тестовый режим: граф читается из файла, пакеты — большие латинские буквы;
- порядок загрузки зависимостей (топологическая сортировка);
- генерация описания графа на D2 и показ изображения `graph.svg`.

## Настройки

Конфигурация задаётся YAML-файлом (по умолчанию `config.yaml`):

```yaml
package: requests
repository: https://pypi.org/pypi
test_mode: false
max_depth: 3
exclude: ""
```

| Параметр     | Описание                                                  |
|--------------|-----------------------------------------------------------|
| `package`    | имя анализируемого пакета (обязательный)                  |
| `repository` | URL репозитория или путь к файлу тестового репозитория    |
| `test_mode`  | `true` — читать граф из файла, `false` — из PyPI          |
| `max_depth`  | максимальная глубина анализа, целое число ≥ 1             |
| `exclude`    | подстрока: пакеты, содержащие её, не учитываются          |

При ошибке (нет файла, неизвестный или повторный ключ, пустое имя пакета,
неверный `test_mode`, нечисловая или нулевая глубина, пакет не найден)
выводится сообщение `Ошибка: ...` и программа завершается с кодом 1.

Формат файла тестового репозитория:

```
A: B C
B: D
C: D E
D:
E:
```

## Модули

| Файл                | Назначение                                        |
|---------------------|---------------------------------------------------|
| `src/config.py`     | разбор YAML и проверка параметров                 |
| `src/pypi.py`       | запрос к PyPI и разбор строк требований           |
| `src/local_repo.py` | тестовый репозиторий из файла                     |
| `src/graph.py`      | BFS, поиск циклов, порядок загрузки               |
| `src/d2.py`         | генерация D2 и построение изображения             |
| `src/main.py`       | точка входа                                       |

## Запуск и тесты

Нужен Python 3.9+. Для изображения — утилита `d2` (`brew install d2`),
без неё выводится только текст D2.

Linux / macOS:

```sh
./run.sh                      # config.yaml
./run.sh configs/cycle.yaml   # другой файл настроек
python3 -m unittest -v        # тесты
```

Windows:

```bat
run.bat
run.bat configs\cycle.yaml
```

Вторым аргументом можно задать режим: `params`, `deps`, `graph`, `order`,
`d2` или `all` (по умолчанию):

```sh
./run.sh configs/flask.yaml order
```

Через Makefile:

```sh
make run                          # config.yaml
make run CONFIG=configs/flask.yaml
make test                         # тесты
make demo                         # три тестовых графа
```

## Скрипты этапов

В папке `scripts` на каждую задачу этапа — отдельный скрипт:

| Скрипт                    | Что показывает                                |
|---------------------------|-----------------------------------------------|
| `stage1_params.sh`        | вывод параметров в формате ключ-значение      |
| `stage1_errors.sh`        | обработка ошибок всех параметров              |
| `stage2_deps.sh`          | прямые зависимости requests с PyPI            |
| `stage3_simple.sh`        | граф BFS на простом тестовом репозитории      |
| `stage3_cycle.sh`         | граф с циклической зависимостью               |
| `stage3_depth_exclude.sh` | ограничение глубины и фильтр по подстроке     |
| `stage3_errors.sh`        | несуществующий пакет и файл репозитория       |
| `stage4_order_test.sh`    | порядок загрузки на тестовых репозиториях     |
| `stage4_order_pip.sh`     | порядок загрузки flask в сравнении с pip      |
| `stage5_requests.sh`      | D2 и изображение графа requests               |
| `stage5_flask.sh`         | D2 и изображение графа flask                  |
| `stage5_httpx.sh`         | D2 и изображение графа httpx                  |

## Примеры

Тестовый репозиторий с циклом (`configs/cycle.yaml`):

```
$ ./run.sh configs/cycle.yaml
Граф зависимостей A:
  A -> B
  B -> C
  C -> A, D
  D -> -
Цикл: A -> B -> C -> A
Порядок загрузки: D
Не загружены из-за цикла: A B C
D2:
direction: down
"A"
"A" -> "B"
...
```

Глубина и фильтр (`configs/deep.yaml`, `max_depth: 2`, `exclude: X`):

```
Граф зависимостей A:
  A -> B
  B -> C
  C -> -
Порядок загрузки: C B A
```

Реальные пакеты (`configs/requests.yaml`, `flask.yaml`, `httpx.yaml`):

```
requests -> charset-normalizer, idna, urllib3, certifi
Порядок загрузки: charset-normalizer idna urllib3 certifi requests

flask -> blinker, click, importlib-metadata, itsdangerous, jinja2,
         markupsafe, werkzeug
importlib-metadata -> zipp
jinja2 -> markupsafe
werkzeug -> markupsafe
Порядок загрузки: blinker click itsdangerous markupsafe zipp jinja2
                  werkzeug importlib-metadata flask

httpx -> anyio, certifi, httpcore, idna
anyio -> exceptiongroup, idna, typing-extensions
httpcore -> certifi, h11
exceptiongroup -> typing-extensions
Порядок загрузки: certifi idna typing-extensions h11 exceptiongroup
                  httpcore anyio httpx
```

## Сравнение с pip и pipdeptree

`pipdeptree -p flask` показывает то же дерево: blinker, click,
importlib_metadata → zipp, itsdangerous, Jinja2 → MarkupSafe, MarkupSafe,
Werkzeug → MarkupSafe.

`pip install flask` устанавливает в порядке: zipp, markupsafe, itsdangerous,
click, blinker, werkzeug, jinja2, importlib-metadata, flask.

Расхождения и их причины:

- порядок «соседних» пакетов отличается: любая топологическая сортировка
  корректна, если зависимости идут раньше зависимых, а pip упорядочивает
  их по-своему;
- инструмент учитывает зависимости с маркерами окружения
  (`python_version < "3.10"` и т. п.), а pip ставит их только когда маркер
  выполняется. Поэтому на новом Python pip не установит, например,
  `importlib-metadata` для flask или `exceptiongroup` для anyio;
- необязательные зависимости (`extra == "..."`) пропускаются, как и в pip
  без указания extras;
- инструмент берёт метаданные последней версии пакета, а pip выбирает
  версии с учётом ограничений и уже установленных пакетов;
- pipdeptree показывает только установленные пакеты, а инструмент — все
  зависимости из репозитория с ограничением по глубине.
