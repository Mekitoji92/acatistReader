"""Coase acatiste.json în template.html și scrie index.html (site-ul gata de folosit)."""

import json

date = json.load(open("acatiste.json", encoding="utf-8"))
sablon = open("template.html", encoding="utf-8").read()
pagina = sablon.replace("__DATA__", json.dumps(date, ensure_ascii=False, separators=(",", ":")))
open("index.html", "w", encoding="utf-8", newline="\n").write(pagina)

print("index.html  %d KB  |  %d acatiste, %d secțiuni"
      % (len(pagina.encode("utf-8")) // 1024, len(date), sum(len(a["sections"]) for a in date)))
