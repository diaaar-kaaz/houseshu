#!/usr/bin/env python3
"""Пересобрать index.html из template.html и data.json.

Добавить кадр: положить файл в img/rooms/ (полный) и thumb/rooms/ (превью),
дописать имя в нужную комнату в data.json, запустить `python3 build.py`.
Превью делается так:  python3 build.py --thumbs   (пересоздаст все превью из img/)
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent

if "--thumbs" in sys.argv:
    from PIL import Image
    n = 0
    for src in sorted(ROOT.glob("img/**/*.jpg")) + sorted(ROOT.glob("img/**/*.png")):
        rel = src.relative_to(ROOT/"img")
        dst = ROOT/"thumb"/rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(src).convert("RGB")
        w = min(1800 if src.stem == "plan" else 1200, im.width)
        im.resize((w, round(im.height*w/im.width)), Image.LANCZOS)\
          .save(dst, "JPEG", quality=80, optimize=True, progressive=True)
        n += 1
    print(f"превью: {n}")

data = json.load(open(ROOT/"data.json"))
tpl = (ROOT/"template.html").read_text()
(ROOT/"index.html").write_text(tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
print("index.html пересобран:", len(data["rooms"]), "комнат,",
      sum(len(r["files"]) for r in data["rooms"]), "кадров интерьера,", len(data["ext"]), "снаружи")
