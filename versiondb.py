import json
import os
import re

class VersionList:
    def __init__(self, directory):
        self.main_file = os.path.join(directory, "versions.json")
        self.versions = []
        self.load()

    def load(self):
        if not os.path.exists(self.main_file):
            return
        with open(self.main_file) as f:
            self.versions = json.load(f)

    def save(self):
        with open(self.main_file, 'w') as f:
            json.dump(self.versions, f, indent=4)

    def save_minified(self, arch):
        data = []
        for v in self.versions:
            if arch in v["codes"]:
                data.append([v["codes"][arch], v["version_name"], 1 if ("beta" in v and v["beta"]) else 0])
        with open(os.path.join(os.path.dirname(self.main_file), "versions." + arch + ".json.min"), 'w') as f:
            json.dump(data, f, separators=(',',':'))

    def add_version(self, code, name, is_beta, arch):
        code = int(code)
        obj = { 
            "version_name": name,
            "codes": {}
        }
        obj["codes"][arch] = code
        if is_beta:
            obj["beta"] = True
        inserted = False
        for idx, val in enumerate(self.versions):
            if val["version_name"] == name:
                self.versions[idx]["codes"][arch] = code
                inserted = True
                break
        if not inserted:
            self.versions.append(obj)
        self.sort()
        
    def sort(self):
        b = re.compile(r"^([0-9])\.")
        m = re.compile(r"\.([0-9])\.")
        e = re.compile(r"\.b?([0-9])$")
        self.versions.sort(key=lambda x: e.sub(r".0\1", m.sub(r".0\1.", m.sub(r".0\1.", b.sub(r"0\1.", x["version_name"])))))

    def importLegacy(self, path, arch):
        if not os.path.exists(self.main_file):
            return
        with open(path) as f:
            versions = json.load(f)
            for idx, val in enumerate(versions):
                self.add_version(val["version_code"], val["version_name"], "beta" in val and val["beta"], arch)