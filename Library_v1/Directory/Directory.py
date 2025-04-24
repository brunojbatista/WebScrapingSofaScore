import os
import sys
import re;
import urllib.request;
from pathlib import Path
import shutil
import time;
from Library_v1.Utils.string import (
    clear_accents,
    default_lower,
)

"""
    Implementar uma função para buscar os arquivos dentro do diretório através de regex
"""

class Directory():

    def __init__(self, path: str = "."):
        self.path = Directory.set_default_path(path);
        self.relativepath = None;
        self.fullpath = None;
        self.set_path();

    def set_default_path(path):
        return Directory.separator(re.sub(r"(^[\\\/]*|[\\\/]*$)", '', path))

    def get_script_path():
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def set_path(self, ):
        if self.is_dir(): self.fullpath = os.path.realpath(self.path);

    def get_path(self, ):
        return self.fullpath;

    def get_relativepath(self, ):
        return self.path

    def separator(path):
        return os.sep.join(re.split(r"[\/\\]+", path));

    def create(self, ):
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.set_path();

    def delete(self, ) -> bool:
        shutil.rmtree(self.fullpath)
        self.fullpath = None;
        return True;

    def delete_files(self, ) -> bool:
        filepaths = self.find_files(r".*");
        for filepath in filepaths: os.remove(filepath);
        return True;

    def is_dir(self, ) -> bool:
        return Path(self.path).is_dir();

    def has_path(self, ) -> bool:
        return not self.get_path() is None;

    def move_file(self, filepath: str):
        if filepath is None: raise NameError("Não identificado o caminho do arquivo")
        name = re.sub(r".*(\\|\/)", '', filepath)
        new_filepath = f"{self.get_path()}/{name}"
        Path(filepath).rename(new_filepath)
        return new_filepath;
    
    def find_file(self, searched_name, path = None):
        if not self.is_dir(): return None;
        if path is None: path = self.path
        else: path = Directory.set_default_path(f"{self.path}/{path}")
        file_target = None
        for root, dirs, files in os.walk(self.path):
            if path != root: continue;
            for file in files:
                if re.search(searched_name, file, flags=re.I):
                    file_target = os.path.realpath(Directory.separator(f"{path}/{file}"))
                if not file_target is None: break;
            if not file_target is None: break;
        return file_target

    def find_dir(self, path):
        if not self.is_dir(): return None;
        if path == '.':  return self.get_path();
        if path is None: path = self.path
        else: path = Directory.set_default_path(f"{self.path}/{path}")
        dir_target = None;
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                relative_dir = Directory.separator(f"{root}/{dir}")
                if relative_dir == path:
                    dir_target = os.path.realpath(relative_dir)
                if not dir_target is None: break;
            if not dir_target is None: break;
        return dir_target;

    def find_files(self, search_regex, path = None) -> list:
        if not self.is_dir(): return None;
        if path is None: path = self.path
        else: path = Directory.set_default_path(f"{self.path}/{path}")
        filepaths = []
        for root, dirs, files in os.walk(self.path):
            if path != root: continue;
            for file in files:
                if re.search(search_regex, file, flags=re.I):
                    filepaths.append(os.path.realpath(Directory.separator(f"{path}/{file}")))
        return filepaths;

    def find_filenames(self, search_regex, path = None):
        filepaths = self.find_files(search_regex, path)
        filenames = [re.sub(r".*(\\|\/)", '', x) for x in filepaths]
        return filenames
    
    def wait_filename(self, waiting_function: callable, path = None, attempts: int = 60):
        print("="*80)
        print(">> wait_filename:")
        while True:
            time.sleep(1)
            filenames_splitted = [re.split(r"\.", x) for x in self.find_filenames(r".*", path)] 
            filenames_splitted = [ splitted[0:(len(splitted)-1)] for splitted in filenames_splitted ]
            filenames = [ default_lower(clear_accents(".".join(splitted))) for splitted in filenames_splitted ]
            print(f"\tfilenames: {filenames}")
            for name in filenames:
                if waiting_function(name): return True;
            attempts -= 1
            if attempts <= 0: raise ValueError(f"O tempo de espera esgotou do arquivo")

    def create_dir(self, relative_path):
        Path(os.path.realpath(Directory.separator(f"{self.path}/{relative_path}"))).mkdir(parents=True, exist_ok=True)

    def get_realpath(path):
        return os.path.realpath(Directory.separator(path))
    
