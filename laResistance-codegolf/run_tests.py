#!/usr/bin/env python3
"""Tests locaux : exemple du sujet, comparaison à une force brute sur des cas aléatoires, cas de grande taille.

Usage: python3 run_tests.py [solution.py ...]   (défaut: golf.py ref.py)
"""
import random
import subprocess
import sys
import time
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
M = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()
EXAMPLE = "......-...-..---.-----.-..-..-..\n5\nHELL\nHELLO\nOWORLD\nWORLD\nTEST\n", 2


def morse(w):
    return "".join(M[ord(c) - 65] for c in w)


def brute(seq, words):
    codes = [morse(w) for w in words]

    @lru_cache(None)
    def go(i):
        if i == len(seq):
            return 1
        return sum(go(i + len(c)) for c in codes if seq.startswith(c, i))
    return go(0)


def suffix_count(seq, words):
    """Comptage itératif depuis la fin (indépendant de golf.py, sans récursion)."""
    codes = [morse(w) for w in words]
    g = [0] * (len(seq) + 1)
    g[len(seq)] = 1
    for i in range(len(seq) - 1, -1, -1):
        g[i] = sum(g[i + len(c)] for c in codes if seq.startswith(c, i))
    return g[0]


def make(seq, words):
    return f"{seq}\n{len(words)}\n" + "\n".join(words) + "\n"


def random_case(rng):
    words = list({"".join(rng.choice("ETIA") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 8))})
    seq = "".join(morse(rng.choice(words)) for _ in range(rng.randint(1, 12)))
    return make(seq, words), brute(seq, words)


def big_case(rng):
    # 30 "A" (= ".-" = E+T, donc 2^30 façons) noyés dans des "T" ; R reste < 2^63 comme dans le sujet
    words = ["E", "T", "A"]
    toks = ["A"] * 30 + ["T"] * 33300
    rng.shuffle(toks)
    seq = "".join(morse(t) for t in toks)
    return make(seq, words), suffix_count(seq, words)


def run(sol, data):
    t = time.time()
    out = subprocess.run([sys.executable, str(HERE / sol)], input=data, capture_output=True, text=True, timeout=60)
    return out.stdout.strip(), time.time() - t, out.stderr.strip()


def main():
    sols = sys.argv[1:] or ["golf.py", "ref.py"]
    rng = random.Random(1)
    cases = [("exemple", *EXAMPLE)]
    cases += [(f"alea{i}", *random_case(rng)) for i in range(200)]
    cases.append(("grand", *big_case(rng)))
    ok = True
    for sol in sols:
        bad = 0
        slow = 0.0
        for name, data, expected in cases:
            out, dt, err = run(sol, data)
            slow = max(slow, dt)
            if out != str(expected):
                bad += 1
                ok = False
                print(f"  {sol} {name}: attendu {expected}, obtenu {out!r} {err[:200]}")
        print(f"{sol}: {len(cases) - bad}/{len(cases)} OK, plus lent {slow:.2f}s, {(HERE / sol).stat().st_size} octets")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
