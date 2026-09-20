#!/usr/bin/env python3
"""Builds the wordication-legal static site from per-language body fragments.

Output (relative to REPO):
  privacy.html, terms.html                     English, current version
  <lang>/privacy.html, <lang>/terms.html       six translations
  privacy/<v>/index.html + <lang>/index.html   frozen snapshots
  terms/<v>/index.html  + <lang>/index.html
"""
import json, os, pathlib, shutil

HERE = pathlib.Path(__file__).parent
REPO = HERE.parent
VERSION = "1.0.0"
LANGS = ["en", "fr", "de", "es", "it", "hr", "sr"]

STYLE = """        *, *::before, *::after { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.7; color: #333; max-width: 760px; margin: 0 auto; padding: 40px 24px 60px; }
        a { color: #5B3FE0; }
        h1 { font-size: 2rem; color: #1B1146; border-bottom: 2px solid #eee; padding-bottom: 12px; margin-bottom: 4px; }
        .meta { color: #888; font-size: 0.9rem; margin-bottom: 32px; }
        h2 { font-size: 1.15rem; color: #1B1146; margin-top: 36px; margin-bottom: 8px; }
        ul, ol { padding-left: 20px; }
        li { margin-bottom: 6px; }
        .contact-box { background: #F3F0FE; padding: 16px 20px; border-left: 4px solid #5B3FE0; border-radius: 0 8px 8px 0; margin: 32px 0 0; }
        .back { display: inline-block; margin-bottom: 28px; font-size: 0.9rem; color: #5B3FE0; text-decoration: none; }
        .back:hover { text-decoration: underline; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 0.92rem; }
        th { background: #F3F0FE; text-align: left; padding: 8px 12px; color: #1B1146; border: 1px solid #E4DEF5; }
        td { padding: 8px 12px; border: 1px solid #E4DEF5; vertical-align: top; }
        tr:nth-child(even) td { background: #FAF8FF; }
        .lang-switch { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; font-size: 0.88rem; }
        .lang-switch a { color: #5B3FE0; text-decoration: none; padding: 4px 12px; border-radius: 20px; border: 1px solid #D5CBFA; }
        .lang-switch a:hover { background: #EFEBFE; }
        .lang-switch a.active { background: #5B3FE0; color: #fff; border-color: #5B3FE0; }
        .deletion-box { background: #f0faf4; border-left: 4px solid #27ae60; border-radius: 0 8px 8px 0; padding: 14px 20px; margin: 16px 0; }"""

VERSION_STYLE = """
        .version-notice { background: #fff8e1; border-left: 4px solid #f6b93b; border-radius: 0 8px 8px 0; padding: 10px 16px; font-size: 0.9rem; margin-bottom: 24px; }
        .version-notice a { color: #5B3FE0; }"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Wordication: Word Guess Party</title>
    <link rel="icon" type="image/png" href="{up}public/icons/wordication-icon.png">
    <link rel="apple-touch-icon" href="{up}public/icons/wordication-icon.png">
    <style>
{style}
    </style>
</head>
<body>
    <a href="{home}" class="back">&#8592; {back}</a>
{notice}    <div class="lang-switch">
{switch}
    </div>
{body}
</body>
</html>
"""


def strings(lang):
    return json.loads((HERE / "content" / lang / "strings.json").read_text())


def body(lang, doc):
    return (HERE / "content" / lang / f"{doc}.html").read_text().rstrip("\n")


def switch_links(current, hrefs):
    out = []
    for lang in LANGS:
        cls = ' class="active"' if lang == current else ""
        out.append(f'        <a href="{hrefs[lang]}"{cls}>{lang.upper()}</a>')
    return "\n".join(out)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print("wrote", path.relative_to(REPO))


def build():
    st = {lang: strings(lang) for lang in LANGS}

    for doc in ("privacy", "terms"):
        # --- current version -------------------------------------------------
        for lang in LANGS:
            if lang == "en":
                home, up = "index.html", ""
                hrefs = {l: (f"{doc}.html" if l == "en" else f"{l}/{doc}.html") for l in LANGS}
                out = REPO / f"{doc}.html"
            else:
                home, up = "../index.html", "../"
                hrefs = {l: (f"../{doc}.html" if l == "en" else
                             (f"{doc}.html" if l == lang else f"../{l}/{doc}.html")) for l in LANGS}
                out = REPO / lang / f"{doc}.html"
            write(out, PAGE.format(
                lang=lang, title=st[lang][f"{doc}Title"], style=STYLE, home=home,
                up=up, back=st[lang]["home"], notice="", switch=switch_links(lang, hrefs),
                body=body(lang, doc)))

        # --- frozen snapshot -------------------------------------------------
        for lang in LANGS:
            if lang == "en":
                home, up = "../../index.html", "../../"
                latest = f"../../{doc}.html"
                hrefs = {l: ("index.html" if l == "en" else f"{l}/index.html") for l in LANGS}
                out = REPO / doc / VERSION / "index.html"
            else:
                home, up = "../../../index.html", "../../../"
                latest = f"../../../{lang}/{doc}.html"
                hrefs = {l: ("../index.html" if l == "en" else
                             ("index.html" if l == lang else f"../{l}/index.html")) for l in LANGS}
                out = REPO / doc / VERSION / lang / "index.html"
            notice = ('    <div class="version-notice">'
                      + st[lang][f"{doc}Notice"].format(v=VERSION, href=latest)
                      + "</div>\n")
            write(out, PAGE.format(
                lang=lang, title=st[lang][f"{doc}Title"], style=STYLE + VERSION_STYLE,
                home=home, up=up, back=st[lang]["home"], notice=notice,
                switch=switch_links(lang, hrefs), body=body(lang, doc)))


if __name__ == "__main__":
    build()
