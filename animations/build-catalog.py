#!/usr/bin/env python3
"""Пересобирает animations/catalog.json по содержимому папок.

Темы могут быть вложенными: animations/<тема>/<подтема>/.../<явление>/.
Папка считается явлением, если в ней есть index.html (интерактивная версия)
или хотя бы один gif; всё, что лежит выше, — темы. Внутрь папки явления скрипт
не заходит. Папки _template и shared пропускаются.

Запуск из любого каталога: python3 animations/build-catalog.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = {"_template", "shared"}


def subdirs(path):
    return sorted(
        d for d in path.iterdir()
        if d.is_dir() and d.name not in SKIP and not d.name.startswith(".")
    )


def readme_title(folder):
    """Первый заголовок '# ' из README.md папки или None."""
    readme = folder / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return None


def phenomenon_title(folder):
    """Заголовок: из README.md, иначе <title> из index.html, иначе имя папки."""
    title = readme_title(folder)
    if title:
        return title
    page = folder / "index.html"
    if page.is_file():
        match = re.search(r"<title>(.*?)</title>", page.read_text(encoding="utf-8"), re.I | re.S)
        if match:
            return match.group(1).strip()
    return folder.name


def gifs_of(folder):
    # Основной gif (с именем явления) идёт первым.
    return sorted(
        (f.name for f in folder.glob("*.gif") if f.name != "preview.gif"),
        key=lambda name: (name != folder.name + ".gif", name),
    )


def preview_of(folder, gifs):
    for name in ("preview.gif", "preview.png"):
        if (folder / name).is_file():
            return name
    return gifs[0] if gifs else None


def walk(folder, topics, items):
    """topics — цепочка названий тем от корня каталога до folder."""
    for child in subdirs(folder):
        interactive = (child / "index.html").is_file()
        gifs = gifs_of(child)
        if interactive or gifs:
            if not topics:
                continue  # явление должно лежать внутри темы
            items.append({
                "topics": topics,
                "title": phenomenon_title(child),
                "path": child.relative_to(ROOT).as_posix(),
                "interactive": interactive,
                "gifs": gifs,
                "preview": preview_of(child, gifs),
            })
        else:
            walk(child, topics + [readme_title(child) or child.name], items)


def main():
    items = []
    walk(ROOT, [], items)
    target = ROOT / "catalog.json"
    target.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("catalog.json: явлений — %d" % len(items))


if __name__ == "__main__":
    main()
