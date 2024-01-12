class AD:
    DOMAIN_NAME: str = "fmv"
    DOMAIN_ALIAS: str = "pih"
    DOMAIN_SUFFIX: str = "lan"
    DOMAIN_DNS: str = ".".join([DOMAIN_NAME, DOMAIN_SUFFIX])
    DOMAIN_MAIN: str = DOMAIN_DNS
    PATH_ROOT: str = j(("//", DOMAIN_MAIN))

    ROOT_CONTAINER_DN: str = f"{OU}Unit,DC={DOMAIN_NAME},DC={DOMAIN_SUFFIX}"
    WORKSTATIONS_CONTAINER_DN: str = f"{OU}Workstations,{ROOT_CONTAINER_DN}"
    SERVERS_CONTAINER_DN: str = f"{OU}Servers,{ROOT_CONTAINER_DN}"
    USERS_CONTAINER_DN_SUFFIX: str = f"Users,{ROOT_CONTAINER_DN}"
    ACTIVE_USERS_CONTAINER_DN: str = f"{OU}{USERS_CONTAINER_DN_SUFFIX}"
    INACTIVE_USERS_CONTAINER_DN: str = f"{OU}dead{USERS_CONTAINER_DN_SUFFIX}"
    GROUP_CONTAINER_DN: str = f"{OU}Groups,{ROOT_CONTAINER_DN}"
    PROPERTY_ROOT_DN: str = f"{OU}Property,{GROUP_CONTAINER_DN}"
    PROPERTY_WS_DN: str = f"{OU}WS,{PROPERTY_ROOT_DN}"
    PROPERTY_USER_DN: str = f"{OU}User,{PROPERTY_ROOT_DN}"
    JOB_POSITION_CONTAINER_DN: str = f"{OU}Job positions,{GROUP_CONTAINER_DN}"

    WORKSTATION_PREFIX_LIST: list[str] = ["ws-", "nb-", "fmvulianna"]

    class USER:
        MARKETER_ADMINISTRATOR: str = "marketer_admin"
        CALL_CENTRE_ADMINISTRATOR: str = "callCentreAdmin"
        REGISTRATION_AND_CALL: str = "reg_and_call"
        CONTROL_SERVICE: str = "cctv"
        INDICATIONS_ALL: str = "indications_all"
        ADMINISTRATOR: str = "Administrator"

    class JobPositions(Enum):
        HR: int = auto()
        IT: int = auto()
        CALL_CENTRE: int = auto()
        REGISTRATOR: int = auto()
        RD: int = auto()
        MARKETER: int = auto()

    class Groups(Enum):
        TimeTrackingReport: int = auto()
        Inventory: int = auto()
        Polibase: int = auto()
        Admin: int = auto()
        ServiceAdmin: int = auto()
        CardRegistry: int = auto()
        PolibaseUsers: int = auto()
        RD: int = auto()
        IndicationWatcher: int = auto()
        FunctionalDiagnostics: int = auto()

    class WSProperies(Enum):
        Watchable: int = 1
        Shutdownable: int = 2
        Rebootable: int = 4
        DiskReportable: int = 8