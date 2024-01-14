from ipih.rpc_collection import ServiceInformationBase, ServiceDescription
from ipih.rpc import ServiceRoleBase
from ipih.const import SERVICE
from ipih.tools import NetworkTool, OSTool, e, ne


class ServiceTool:
    @staticmethod
    def is_service_as_listener(information: ServiceInformationBase) -> bool:
        return information.name.find(SERVICE.EVENT_LISTENER_NAME_PREFIX) == 0

    @staticmethod
    def is_service_as_support(information: ServiceInformationBase) -> bool:
        return information.name.find(SERVICE.SUPPORT_NAME_PREFIX) == 0

    @staticmethod
    def create_port(
        role_or_information: ServiceRoleBase | ServiceInformationBase,
    ) -> int:
        return (
            ServiceRoleBase.description(role_or_information).port
            or NetworkTool.next_free_port()
        )

    @staticmethod
    def create_host(
        role_or_information: ServiceRoleBase | ServiceInformationBase,
    ) -> int:
        description: ServiceDescription = ServiceRoleBase.description(
            role_or_information
        )
        return (
            OSTool.host()
            if description.isolated or e(description.host)
            else description.host
        )
        
    @staticmethod
    def get_host(role_or_information: ServiceRoles | ServiceInformationBase) -> str:
        information: ServiceInformationBase | None = ServiceRoles.description(
            role_or_information
        )
        if isinstance(information, ServiceDescription):
            if ne(information.port):
                return PIH.DATA.FORMAT.donain(information.host)
        return PIH.DATA.FORMAT.donain(
            (
                ServiceTool.get_information(role_or_information)
                or ServiceInformationBase()
            ).host
            or information.host
        )

    @staticmethod
    def get_port(
        role_or_information: ServiceRoleBase | ServiceInformationBase,
    ) -> int | None:
        information: ServiceInformationBase | None = ServiceRoleBase.description(
            role_or_information
        )
        if isinstance(information, ServiceDescription):
            if ne(information.port):
                return information.port
        return (
            PIH.SERVICE.get_information(role_or_information)
            or ServiceInformationBase()
        ).port or information.port
        
    @staticmethod
    def get_information(
        role_or_information: ServiceRoles | ServiceInformationBase,
        cached: bool = True,
    ) -> ServiceInformation | None:
        service_information: ServiceInformationBase | None = (
            ServiceRoles.description(role_or_information)
        )
        # if PIH.SERVICE.is_service_as_listener(service_information):
        #    return RPC.ping(service_information)
        if e(PIH.SERVICE.ADMIN.SERVICE_INFORMATION_MAP):
            PIH.SERVICE.ADMIN.request_for_service_information_list()
        service_information = PIH.SERVICE.get_information_from_cache(
            service_information
        )
        if cached:
            return service_information
        if e(service_information):
            return None
        return RPC.ping(service_information)
