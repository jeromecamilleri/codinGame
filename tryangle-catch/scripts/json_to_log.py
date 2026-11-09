#!/usr/bin/env python3
"""Wrapper: le convertisseur partagé vit dans common/json_to_log.py (lancer depuis tryangle-catch/)."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parents[2] / "common" / "json_to_log.py"), run_name="__main__")
