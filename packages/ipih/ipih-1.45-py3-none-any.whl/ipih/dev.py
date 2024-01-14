import sys
from ipih import *

DEV_NAME: str = "dev"


def import_pih_dev() -> None:
    name: str = f"{FACADE_NAME}/{DEV_NAME}"
    if platform.system() == "Linux":
        pass
        #sys.path.append(f"//mnt/{name}")
    else:
        pass
        #sys.path.append(f"//{WINDOWS_SHARE_DOMAIN_NAME}/{name}")


import_pih_dev()
