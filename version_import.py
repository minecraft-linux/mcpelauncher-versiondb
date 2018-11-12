import mcpeinfocheck
import axmlparserpy.apk as apk
import os
import sys
import shutil
import zipfile
import json
import versiondb

def do_add(apkfile):
    ap = apk.APK(apkfile)
    pkg_name = ap.get_package()
    version_name = ap.get_androidversion_name()
    version_code = ap.get_androidversion_code()
    mcpe_path = None

    with zipfile.ZipFile(apkfile, 'r') as z:
        for name in z.namelist():
            if name.startswith("lib/") and name.endswith("/libminecraftpe.so"):
                arch = name[4:-18]
                mcpe_path = os.getcwd() + "/libminecraftpe.so"
                src = z.open(name)
                dest = open(mcpe_path, "wb")
                with src, dest:
                    shutil.copyfileobj(src, dest)
    if mcpe_path == None:
        raise Exception("Invalid .apk specified")
        return

    so_info = mcpeinfocheck.get_so_info(mcpe_path)
    print(apkfile, so_info)

    versions = versiondb.VersionList(".")
    versions.add_version(version_code, version_name, so_info["is_beta"], so_info["protocol_ver"])
    versions.save()

    os.remove(mcpe_path)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        do_add(arg)
