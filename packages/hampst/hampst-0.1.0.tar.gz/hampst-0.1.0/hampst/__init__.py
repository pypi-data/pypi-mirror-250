import asyncio
import json

def batches(list_, n):
    return [
        list_[i:i + n]
        for i in range(0, len(list_), n)
    ]

def read_exact(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

def read(file_name):
    return read_exact(file_name).strip()

def read_json(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def write(file_name, string):
    with open(file_name, "w", encoding="utf-8") as f:
        return f.write(string)

def write_json(file_name, object_):
    with open(file_name, "w", encoding="utf-8") as f:
        return json.dump(object_, f, indent=4)

def ints(list_):
    return [int(item) for item in list_]

def main(function):
    asyncio.run(function)
