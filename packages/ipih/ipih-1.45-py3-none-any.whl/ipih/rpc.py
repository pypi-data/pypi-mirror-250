from enum import Enum
from ipih.rpc_collection import *
from ipih.tools import EnumTool

class ServiceRoleBase(Enum):
    
    @staticmethod
    def description(
        value: Enum | str | ServiceInformationBase, get_source_description: bool = False
    ) -> ServiceInformationBase | None:
        def isolated_name(value: ServiceInformationBase | None) -> str | None:
            if value is None:
                return None
            value.name = (
                ":".join(("isolated", value.name))
                if value.isolated and value.name.find("isolated") == -1
                else value.name
            )
            return value

        if isinstance(value, str):
            for service_role in ServiceRoleBase:
                if ServiceRoleBase.description(service_role).name == value:
                    return isolated_name(service_role.value)
            return None
        if isinstance(value, ServiceDescription):
            return isolated_name(
                ServiceRoleBase.description(value.name)
                if get_source_description
                else value
            )
        return isolated_name(EnumTool.get(value))