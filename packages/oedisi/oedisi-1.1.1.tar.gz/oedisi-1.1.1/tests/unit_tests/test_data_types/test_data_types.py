import os
import json
import pytest
import importlib
from pathlib import Path

DATADIR = Path(__file__).parent / "data"

INPUT_FILES = [p for p in DATADIR.glob("*.json")]


@pytest.mark.parametrize("filepath", INPUT_FILES)
def test_all_formats(filepath):
    name = filepath.name.split(".")[0]
    with open(filepath) as f_in:
        json_data = json.load(f_in)
        class_name = getattr(importlib.import_module("oedisi.types.data_types"), name)
        class_name.parse_obj(json_data)
