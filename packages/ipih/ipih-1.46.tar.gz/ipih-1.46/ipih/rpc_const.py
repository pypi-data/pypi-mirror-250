from ipih.rpc_collection import IServiceCommand
from enum import auto

class ServiceCommands(IServiceCommand):
    ping: int = auto()
    subscribe: int = auto()
    unsubscribe: int = auto()
    create_subscribtions: int = auto()
    stop_service: int = auto()
    on_service_starts: int = auto()
    on_service_stops: int = auto()
    update_service_information: int = auto()
    # HeatBeat
    heart_beat: int = auto()
