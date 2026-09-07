# Rânduiala acatistelor

Un cititor de acatiste pentru două persoane care citesc în rotație, luni / miercuri / vineri.
Deschizi pagina, apeși pe numele tău și începe acatistul care îți revine astăzi. Fără meniuri,
fără derulare: textul curge continuu și se taie în pagini exact cât încape pe ecran.

Gândit pentru tabletă în landscape și telefon.

## Rânduiala

O săptămână se citește în ordinea de bază, următoarea se schimbă între cele două persoane,
apoi tot așa. Ancora este **luni, 24 august 2026** = săptămână de bază.

| Ziua     | Seria întâi                  | Seria a doua        |
|----------|------------------------------|---------------------|
| Luni     | Sf. Arhangheli Mihail și Gavriil | Sf. Ioachim și Ana |
| Miercuri | Sf. Ioan Rusul               | Sf. Stelian         |
| Vineri   | Buna Vestire                 | Sf. Efrem cel Nou   |

În săptămâna de bază Daniela citește seria întâi și Alexandru seria a doua; în săptămâna
următoare invers. Dacă ziua curentă nu e zi de acatist, pagina arată următoarea zi de citit,
iar rândul *Luni · Miercuri · Vineri* lasă alegerea manuală.

## Ce face pagina

- **Rugăciunile începătoare** înaintea fiecărui acatist.
- **Paginare după ecran** — textul e tăiat în bucăți mici (frază, punct și virgulă, rând de
  „Bucură-te"), iar pagina se umple până jos; bucățile ajunse pe aceeași pagină se lipesc la
  loc, deci textul arată neschimbat. Se recalculează la rotirea tabletei și la schimbarea
  mărimii textului, păstrând locul din text.
- Un rând „Bucură-te…" nu se rupe niciodată în două pagini, iar un titlu nu rămâne singur jos.
- Săgeți mari jos, glisare stânga/dreapta, săgeți de la tastatură.
- Ține ecranul aprins cât citești (`wakeLock`) și reia de unde ai rămas în aceeași zi.
- Temă deschisă și întunecată, după setarea aparatului.

## Folosire

`index.html` e site-ul complet, un singur fișier, fără dependențe. Îl deschizi direct
în browser sau îl pui pe orice găzduire statică (inclusiv GitHub Pages, din ramura `main`,
directorul rădăcină).

## Dezvoltare

```
python extract.py     # descarcă acatistele de pe doxologia.ro -> acatiste.json
python build.py       # coase acatiste.json în template.html -> index.html
```

`python extract.py --refresh` redescarcă paginile chiar dacă există în `raw/`
(directorul `raw/` nu e urmărit de git).

Modifică `template.html`, nu `index.html` — al doilea e generat.

## Texte

Textele acatistelor sunt preluate de pe [doxologia.ro](https://doxologia.ro), cu diacriticele
normalizate la ș/ț cu virgulă dedesubt. Link-ul sursă pentru fiecare acatist e păstrat în
câmpul `source` din `acatiste.json`.
