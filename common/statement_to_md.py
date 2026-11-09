#!/usr/bin/env python3
"""Convertit un énoncé HTML de referee CodinGame (config/.../statement_*.html[.tpl]) en Markdown.

  statement_to_md.py FICHIER.html [--level level5] [--title "Titre"] > OBJECTIF.md

Les blocs <!-- BEGIN levelX ... --> / <!-- END --> ne sont gardés que s'ils contiennent --level
(ligue affichée) ; le texte hors bloc est toujours gardé. Bibliothèque standard uniquement.
"""
import argparse
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "section", "ul", "ol", "table", "tr", "br", "pre", "details", "summary"}


class Conv(HTMLParser):
    def __init__(self, level):
        super().__init__(convert_charrefs=True)
        self.level, self.stack, self.out = level, [], []
        self.skip = 0
        self.pre = False
        self.lists = []
        self.cells = 0

    @property
    def on(self):
        return all(self.stack) and not self.skip

    def w(self, s):
        if self.on:
            self.out.append(s)

    def handle_comment(self, c):
        c = c.strip()
        if c.startswith("BEGIN"):
            self.stack.append(self.level in c.split()[1:])
        elif c == "END" and self.stack:
            self.stack.pop()

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg"):
            self.skip += 1
        elif tag in ("h1", "h2", "h3", "h4"):
            self.w("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("b", "strong"):
            self.w("**")
        elif tag in ("i", "em"):
            self.w("*")
        elif tag in ("const", "var", "action", "code", "tt"):
            self.w("`")
        elif tag == "pre":
            self.pre = True
            self.w("\n\n```\n")
        elif tag in ("ul", "ol"):
            self.lists.append(tag)
            self.w("\n")
        elif tag == "li":
            self.w("\n" + "  " * (len(self.lists) - 1) + ("- " if not self.lists or self.lists[-1] == "ul" else "1. "))
        elif tag == "tr":
            self.cells = 0
            self.w("\n| ")
        elif tag in ("td", "th"):
            self.w("")
        elif tag == "br":
            self.w("\n")
        elif tag in BLOCK:
            self.w("\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip = max(0, self.skip - 1)
        elif tag in ("b", "strong"):
            self.w("**")
        elif tag in ("i", "em"):
            self.w("*")
        elif tag in ("const", "var", "action", "code", "tt"):
            self.w("`")
        elif tag == "pre":
            self.pre = False
            self.w("\n```\n\n")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.w("\n")
        elif tag in ("td", "th"):
            self.w(" | ")
        elif tag in ("h1", "h2", "h3", "h4", "p", "div", "table", "details"):
            self.w("\n\n")

    def handle_data(self, data):
        if not self.on:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


def convert(text, level):
    p = Conv(level)
    p.feed(text)
    md = "".join(p.out).replace("\xa0", " ")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"\*\*\s*\*\*", "", md)
    md = re.sub(r"(?m)^(#+)\s+", r"\1 ", md)
    md = re.sub(r"(?m)^[ \t]+(?=\S)", "", md)
    return md.strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--level", default="level5")
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    md = convert(open(a.file, encoding="utf-8").read(), a.level)
    sys.stdout.write((f"# {a.title}\n\n" if a.title else "") + md)


if __name__ == "__main__":
    main()
