import shutil
import subprocess
import sys

from src.errors import VisualizerError

D2_FILE = "graph.d2"
IMAGE_FILE = "graph.svg"


def to_d2(graph):
    lines = ["direction: down"]
    for name, deps in graph.items():
        lines.append('"%s"' % name)
        for child in deps:
            lines.append('"%s" -> "%s"' % (name, child))
    return "\n".join(lines) + "\n"


def render(text):
    with open(D2_FILE, "w", encoding="utf-8") as stream:
        stream.write(text)
    if not shutil.which("d2"):
        print("d2 не установлен, изображение не построено")
        return None
    result = subprocess.run(
        ["d2", D2_FILE, IMAGE_FILE], capture_output=True, text=True)
    if result.returncode != 0:
        raise VisualizerError("d2: " + result.stderr.strip())
    _show(IMAGE_FILE)
    return IMAGE_FILE


def _show(path):
    command = "open" if sys.platform == "darwin" else "xdg-open"
    if shutil.which(command):
        subprocess.Popen([command, path])
