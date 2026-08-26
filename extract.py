"""Descarcă acatistele de pe doxologia.ro și le pune în acatiste.json.

Fiecare acatist devine o listă de secțiuni: {h: titlu, p: [paragrafe], r: [indicații]}.
Tăierea în pagini NU se face aici — o face pagina web, după cât încape pe ecran.

    python extract.py            # folosește ce e în raw/, descarcă ce lipsește
    python extract.py --refresh  # redescarcă tot
"""

import html
import json
import os
import re
import sys
import urllib.request

ACATISTE = [
    ("mihail-gavriil", "Acatistul Sfinților Arhangheli Mihail și Gavriil", "Sf. Arhangheli Mihail și Gavriil",
     "https://doxologia.ro/acatistul-sfintilor-arhangheli-mihail-gavriil"),
    ("ioan-rusul", "Acatistul Sfântului Ioan Rusul", "Sf. Ioan Rusul",
     "https://doxologia.ro/acatistul-sfantului-ioan-rusul"),
    ("buna-vestire", "Acatistul Bunei Vestiri", "Buna Vestire",
     "https://doxologia.ro/acatistul-bunei-vestiri"),
    ("ioachim-ana", "Acatistul Sfinților Părinți Ioachim și Ana", "Sf. Ioachim și Ana",
     "https://doxologia.ro/acatistul-sfintilor-parinti-ioachim-ana"),
    ("stelian", "Acatistul Sfântului Cuvios Stelian Paflagonul", "Sf. Stelian",
     "https://doxologia.ro/acatistul-sfantului-cuvios-stelian-paflagonul-ocrotitorul-pruncilor"),
    ("efrem", "Acatistul Sfântului Mucenic Efrem cel Nou", "Sf. Efrem cel Nou",
     "https://doxologia.ro/acatistul-sfantului-mucenic-efrem-cel-nou"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
RAW = "raw"

# titlurile din text: Condacul 1, Icosul al 2-lea, Rugăciune către...
TITLU = re.compile(r"^\s*(condac|icos|rug[ăa]ciun|otpust|troparul)", re.I)
INCEPUT = re.compile(r"^\s*condac(ul)?\s*1\s*$", re.I)


def descarca(slug, url, refresh=False):
    cale = os.path.join(RAW, slug + ".html")
    if os.path.exists(cale) and not refresh:
        return open(cale, encoding="utf-8", errors="replace").read()
    os.makedirs(RAW, exist_ok=True)
    cerere = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(cerere, timeout=30) as r:
        text = r.read().decode("utf-8", "replace")
    open(cale, "w", encoding="utf-8", newline="\n").write(text)
    print("  descărcat", url)
    return text


def corp(pagina):
    """Conținutul articolului, fără meniuri și bare laterale."""
    i = pagina.find("field--name-body field-type-text-with-summary")
    if i < 0:
        i = pagina.find("field--node-body")
    j = pagina.index('<div class="field-item">', i) + len('<div class="field-item">')
    adancime, k = 1, j
    while adancime > 0:
        m = re.compile(r"<div\b|</div>").search(pagina, k)
        if not m:
            break
        adancime += 1 if m.group(0).startswith("<div") else -1
        k = m.end()
    return pagina[j:k - len("</div>")]


def curata(s):
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace(" ", " ").replace("­", "").replace("​", "")
    s = s.translate(str.maketrans("şŞţŢ", "șȘțȚ"))   # cedilă -> virgulă dedesubt
    s = "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in s.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def sectiuni(pagina):
    blocuri = []
    for m in re.finditer(r"<p\b([^>]*)>(.*?)</p>", corp(pagina), flags=re.S | re.I):
        atribute, text = m.group(1), curata(m.group(2))
        if not text:
            continue
        centrat = "text-align-center" in atribute or "rtecenter" in atribute
        fel = "text"
        if centrat:
            fel = "titlu" if (TITLU.match(text) and len(text) < 90) else "indicatie"
        blocuri.append((fel, text))

    # sari peste linkuri audio și trimiteri, începe de la Condacul 1
    de_la = next((n for n, (f, t) in enumerate(blocuri) if INCEPUT.match(t)), 0)

    out, curenta = [], None
    for fel, text in blocuri[de_la:]:
        if fel == "titlu" or curenta is None:
            curenta = {"h": text if fel == "titlu" else "", "p": [], "r": []}
            out.append(curenta)
            if fel == "titlu":
                continue
        if fel == "indicatie":
            curenta["r"].append(text)
        else:
            curenta["p"].append(text)
    return [s for s in out if s["p"] or s["r"]]


def main():
    refresh = "--refresh" in sys.argv
    out = []
    for slug, titlu, scurt, url in ACATISTE:
        parti = sectiuni(descarca(slug, url, refresh))
        out.append({"slug": slug, "title": titlu, "short": scurt, "source": url, "sections": parti})
        semne = sum(len(p) for s in parti for p in s["p"])
        print("%-16s %2d secțiuni %6d semne | %s ... %s"
              % (slug, len(parti), semne, parti[0]["h"], parti[-1]["h"]))
    json.dump(out, open("acatiste.json", "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)
    print("-> acatiste.json")


if __name__ == "__main__":
    main()
