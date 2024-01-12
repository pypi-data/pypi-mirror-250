from inspect import currentframe, getframeinfo
from typing import Any, Dict, Tuple
import datetime

# ANSI color codes
RESET_COLOR = "\u001b[0m"
YELLOW = "\u001b[33m"
CYAN = "\u001b[36m"


def print_pos(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
    cf = currentframe()
    frameinfo = getframeinfo(cf.f_back)
    print(f"{YELLOW}@ {frameinfo.filename}:{frameinfo.lineno}{RESET_COLOR}")
    print(*args, **kwargs)


def print_pos_time(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
    cf = currentframe()
    current_time = datetime.datetime.now().isoformat(timespec="milliseconds")
    frameinfo = getframeinfo(cf.f_back)
    print(
        f"{CYAN}{current_time}{RESET_COLOR}: {YELLOW}@ {frameinfo.filename}:{frameinfo.lineno}{RESET_COLOR}"
    )
    print(*args, **kwargs)
