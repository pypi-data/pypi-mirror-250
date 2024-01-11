
import json


def readBinaryFromPath(path, chunk_size=4096):
    with open(path, 'rb') as f:
        while True:
            data = f.read(chunk_size)

            if not data:
                break

            yield data


def writeBinaryToPath(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def readJsonAtPath(path):
    with open(path) as f:
        return json.load(f)


def writeJsonToPath(path, data, indent=2):
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)
