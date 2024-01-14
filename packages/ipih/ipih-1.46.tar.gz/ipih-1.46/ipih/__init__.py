import sys
import importlib.util
import platform

FACADE_NAME: str = "facade"
WINDOWS_SHARE_DOMAIN_NAME: str = "pih"
PIH_MODULE_NAME: str = "pih"
MODULE_NAME: str = "ipih"
MODULE_VERSION: str = "1.46"

def get_path(is_linux: bool) -> str:
    if is_linux:
        return f"//mnt/{FACADE_NAME}"
    return f"//{WINDOWS_SHARE_DOMAIN_NAME}/{FACADE_NAME}"

def import_pih() -> None:
    module_is_exists = importlib.util.find_spec(PIH_MODULE_NAME) is not None
    if not module_is_exists:
        sys.path.append(get_path(platform.system() == "Linux"))

import_pih()
