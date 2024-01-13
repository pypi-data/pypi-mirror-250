from redrover_api.paths.api_v1_org_id_absence_identifier.get import ApiForget
from redrover_api.paths.api_v1_org_id_absence_identifier.put import ApiForput
from redrover_api.paths.api_v1_org_id_absence_identifier.delete import ApiFordelete


class ApiV1OrgIdAbsenceIdentifier(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
