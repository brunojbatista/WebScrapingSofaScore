import os
import sys
import re;
import urllib.request;
from pathlib import Path
import shutil
...
# Download the file from `url` and save it locally under `file_name`:

def create_path(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def separator(path):
    return os.sep.join(re.split(r"[\/\\]", path))    

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_custom_path(relative_path: str):
    folders = re.split(r"[\/\\]", re.sub(r"(^\s*\\+|^\s*\/+)", '', relative_path))
    return re.sub(r"(\\+\s*$|\/+\s*$)", '', os.path.join(get_script_path(), *folders))

def download(url: str, filename: str, relative_path: str = ''):
    download_folder = get_custom_path(relative_path);
    create_path(download_folder)
    fullpath = separator(f"{download_folder}/{filename}");
    print(f"path: {fullpath}")
    with urllib.request.urlopen(url) as response, open(fullpath, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return fullpath;

def delete_folder(path: str):
    return shutil.rmtree(path)

def delete_file(path: str):
    return os.remove(path)

def move_file(current_path: str, new_path: str):
    return Path(current_path).rename(new_path)

def get_relative_full_path(relativepath: str, is_create: bool = False) -> dict:
    _relativepath = separator(relativepath)
    _fullpath = get_custom_path(_relativepath)
    if is_create: create_path(_fullpath)
    return {
        "relativepath": _relativepath,
        "fullpath": _fullpath,
    }

def is_file(fullpath: str) -> bool:
    return Path(fullpath).is_file();

def edit_chromedriver(driver_path: str):
    import io, re, string, os;
    print(f"driver_path: {driver_path}")
    # path = os.path.abspath(driver_path)
    replacement = "akl_YTGFRtDgbvpoqxgSdtYska".encode()
    with io.open(driver_path, "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"cdc_" in line:
                fh.seek(-len(line), 1)
                newLine = re.sub(b"cdc_.{22}", replacement, line)
                fh.write(newLine)
                print(">> Linha encontrada e alterada com sucesso <<")