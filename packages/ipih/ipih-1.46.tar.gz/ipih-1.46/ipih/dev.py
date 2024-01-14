import sys
from ipih import *

DEV_NAME: str = "dev"


def import_pih_dev() -> None:
    name: str = f"{FACADE_NAME}/{DEV_NAME}"
    path: str = get_path(platform.system() == "Linux")
    if path in sys.path:
        sys.path.remove(path)
    if platform.system() == "Linux":
        sys.path.append(f"//mnt/{name}")
    else:
        sys.path.append(f"//{WINDOWS_SHARE_DOMAIN_NAME}/{name}")


import_pih_dev()
