import json
import os

VERSION_LIST_FILE = "versions.json"
MIN_VERSION_LIST_FILE = "versions.json.min"

def load_version_list():
    if not os.path.exists(VERSION_LIST_FILE):
        return []
    with open(VERSION_LIST_FILE) as f:
        return json.load(f)

def save_version_list(data):
    with open(VERSION_LIST_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_minified(versions):
    data = []
    for v in versions:
        data.append([v["version_code"], v["version_name"]])
    with open(MIN_VERSION_LIST_FILE, 'w') as f:
        json.dump(data, f, separators=(',',':'))

def create_version(code, name, is_beta, protocol):
    code = int(code)
    versions = load_version_list()
    obj = {
        "version_code": code,
        "version_name": name,
        "protocol": protocol
    }
    if is_beta:
        obj["beta"] = True
    inserted = False
    for idx, val in enumerate(versions):
        if val["version_code"] == code:
            print("Warn: replacing existing")
            versions[idx] = val
            inserted = True
            break
        if val["version_code"] > code:
            versions.index(idx, obj)
            inserted = True
            break
    if not inserted:
        versions.append(obj)
    versions.sort(key=lambda x: x["version_code"])
    save_version_list(versions)
    create_minified(versions)
