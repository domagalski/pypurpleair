import pathlib

_ROOT = pathlib.Path(__file__).parent


def Settings(**kwargs):
    return {"interpreter_path": _ROOT / ".venv/purpleair/bin/python3"}
