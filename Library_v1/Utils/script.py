import re;

from sys import (
    argv,
)

def get_start_script_name() -> str:
    name = re.sub(r".*(\\|\/)", '', argv[0])
    name = re.sub(r"\..*", '', name)
    return name