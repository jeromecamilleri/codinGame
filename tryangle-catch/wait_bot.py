#!/usr/bin/env python3
"""Minimal local opponent that reads every turn and answers WAIT."""

import sys


def line():
    return sys.stdin.buffer.readline()


first = line()
if first:
    house_count = int(first)
    for _ in range(house_count):
        line()

    while True:
        scores = line()
        if not scores:
            break
        for _ in range(house_count):
            line()
        path_count = int(line())
        for _ in range(path_count):
            line()
        triangle_count = int(line())
        for _ in range(triangle_count):
            line()
        linkable_count = int(line())
        for _ in range(linkable_count):
            line()
        print("WAIT", flush=True)
