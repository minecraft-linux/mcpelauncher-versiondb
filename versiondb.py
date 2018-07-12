import json
import os

class VersionList:
    def __init__(self, directory):
        self.main_file = os.path.join(directory, "versions.json")
        self.min_file = os.path.join(directory, "versions.json.min")
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
        self.save_minified()

    def save_minified(self):
        data = []
        for v in self.versions:
            data.append([v["version_code"], v["version_name"], 1 if "beta" in v else 0])
        with open(self.min_file, 'w') as f:
            json.dump(data, f, separators=(',',':'))

    def add_version(self, code, name, is_beta, protocol):
        code = int(code)
        obj = {
            "version_code": code,
            "version_name": name,
            "protocol": protocol
        }
        if is_beta:
            obj["beta"] = True
        inserted = False
        for idx, val in enumerate(self.versions):
            if val["version_code"] == code:
                print("Warn: replacing existing")
                self.versions[idx] = val
                inserted = True
                break
            if val["version_code"] > code:
                self.versions.insert(idx, obj)
                inserted = True
                break
        if not inserted:
            self.versions.append(obj)
        self.versions.sort(key=lambda x: x["version_code"])
