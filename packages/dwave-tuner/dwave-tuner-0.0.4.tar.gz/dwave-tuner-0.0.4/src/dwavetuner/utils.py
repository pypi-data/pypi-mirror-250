import json
import pathlib


def exists(path):
    if type(path) == str:
        path = pathlib.Path(path)

    return path.exists()


def ls(path):
    if type(path) == str:
        path = pathlib.Path(path)

    return path.iterdir()


def load_json(path):
    if type(path) == str:
        path = pathlib.Path(path)

    if not path.exists():
        raise Exception(f'File {path} does not exist.')

    with open(path, 'r') as f:
        return json.load(f)


def dump_json(obj, path):
    if type(path) == str:
        path = pathlib.Path(path)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, 'w') as f:
        json.dump(obj, f)

    return True
