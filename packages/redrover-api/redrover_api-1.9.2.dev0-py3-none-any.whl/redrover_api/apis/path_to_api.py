import typing_extensions

from redrover_api.paths import PathValues
from redrover_api.apis.paths.api_v1_org_id_absence_identifier import ApiV1OrgIdAbsenceIdentifier
from redrover_api.apis.paths.api_v1_org_id_absence import ApiV1OrgIdAbsence
from redrover_api.apis.paths.api_v1_org_id_absence_reason_identifier import ApiV1OrgIdAbsenceReasonIdentifier
from redrover_api.apis.paths.api_v1_org_id_absence_reason import ApiV1OrgIdAbsenceReason
from redrover_api.apis.paths.api_v1_org_id_employee_employee_identifier_absence_reason_balances_id import ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalancesId
from redrover_api.apis.paths.api_v1_org_id_employee_employee_identifier_absence_reason_balances import ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalances
from redrover_api.apis.paths.api_v1_org_id_assignment_identifier import ApiV1OrgIdAssignmentIdentifier
from redrover_api.apis.paths.api_v1_org_id_connection_id_download import ApiV1OrgIdConnectionIdDownload
from redrover_api.apis.paths.api_v1_org_id_connection_id_data import ApiV1OrgIdConnectionIdData
from redrover_api.apis.paths.api_v1_org_id_connection_id_run import ApiV1OrgIdConnectionIdRun
from redrover_api.apis.paths.api_v1_organization import ApiV1Organization
from redrover_api.apis.paths.api_v1_organization_id import ApiV1OrganizationId
from redrover_api.apis.paths.api_v1_organization_id_school_year import ApiV1OrganizationIdSchoolYear
from redrover_api.apis.paths.api_v1_organization_id_school_year_current import ApiV1OrganizationIdSchoolYearCurrent
from redrover_api.apis.paths.api_v1_org_id_reference_data_attribute import ApiV1OrgIdReferenceDataAttribute
from redrover_api.apis.paths.api_v1_org_id_user_identifier import ApiV1OrgIdUserIdentifier
from redrover_api.apis.paths.api_v1_org_id_user_identifier_role import ApiV1OrgIdUserIdentifierRole
from redrover_api.apis.paths.api_v1_org_id_user_substitute import ApiV1OrgIdUserSubstitute
from redrover_api.apis.paths.api_v1_org_id_user_substitute_identifier import ApiV1OrgIdUserSubstituteIdentifier
from redrover_api.apis.paths.api_v1_org_id_user_employee_identifier import ApiV1OrgIdUserEmployeeIdentifier
from redrover_api.apis.paths.api_v1_org_id_user_administrator_identifier import ApiV1OrgIdUserAdministratorIdentifier
from redrover_api.apis.paths.api_v1_org_id_user_employee import ApiV1OrgIdUserEmployee
from redrover_api.apis.paths.api_v1_org_id_user_administrator import ApiV1OrgIdUserAdministrator
from redrover_api.apis.paths.api_v1_org_id_vacancy_identifier import ApiV1OrgIdVacancyIdentifier
from redrover_api.apis.paths.api_v1_org_id_vacancy_vacancy_details import ApiV1OrgIdVacancyVacancyDetails
from redrover_api.apis.paths.api_v1_org_id_vacancy import ApiV1OrgIdVacancy
from redrover_api.apis.paths.api_v1_webhooks_id import ApiV1WebhooksId
from redrover_api.apis.paths.api_v1_webhooks import ApiV1Webhooks
from redrover_api.apis.paths.api_v1_webhooks_identifier import ApiV1WebhooksIdentifier

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_ORG_ID_ABSENCE_IDENTIFIER: ApiV1OrgIdAbsenceIdentifier,
        PathValues.API_V1_ORG_ID_ABSENCE: ApiV1OrgIdAbsence,
        PathValues.API_V1_ORG_ID_ABSENCE_REASON_IDENTIFIER: ApiV1OrgIdAbsenceReasonIdentifier,
        PathValues.API_V1_ORG_ID_ABSENCE_REASON: ApiV1OrgIdAbsenceReason,
        PathValues.API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES_ID: ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalancesId,
        PathValues.API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES: ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalances,
        PathValues.API_V1_ORG_ID_ASSIGNMENT_IDENTIFIER: ApiV1OrgIdAssignmentIdentifier,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_DOWNLOAD: ApiV1OrgIdConnectionIdDownload,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_DATA: ApiV1OrgIdConnectionIdData,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_RUN: ApiV1OrgIdConnectionIdRun,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATION_ID: ApiV1OrganizationId,
        PathValues.API_V1_ORGANIZATION_ID_SCHOOL_YEAR: ApiV1OrganizationIdSchoolYear,
        PathValues.API_V1_ORGANIZATION_ID_SCHOOL_YEAR_CURRENT: ApiV1OrganizationIdSchoolYearCurrent,
        PathValues.API_V1_ORG_ID_REFERENCE_DATA_ATTRIBUTE: ApiV1OrgIdReferenceDataAttribute,
        PathValues.API_V1_ORG_ID_USER_IDENTIFIER: ApiV1OrgIdUserIdentifier,
        PathValues.API_V1_ORG_ID_USER_IDENTIFIER_ROLE: ApiV1OrgIdUserIdentifierRole,
        PathValues.API_V1_ORG_ID_USER_SUBSTITUTE: ApiV1OrgIdUserSubstitute,
        PathValues.API_V1_ORG_ID_USER_SUBSTITUTE_IDENTIFIER: ApiV1OrgIdUserSubstituteIdentifier,
        PathValues.API_V1_ORG_ID_USER_EMPLOYEE_IDENTIFIER: ApiV1OrgIdUserEmployeeIdentifier,
        PathValues.API_V1_ORG_ID_USER_ADMINISTRATOR_IDENTIFIER: ApiV1OrgIdUserAdministratorIdentifier,
        PathValues.API_V1_ORG_ID_USER_EMPLOYEE: ApiV1OrgIdUserEmployee,
        PathValues.API_V1_ORG_ID_USER_ADMINISTRATOR: ApiV1OrgIdUserAdministrator,
        PathValues.API_V1_ORG_ID_VACANCY_IDENTIFIER: ApiV1OrgIdVacancyIdentifier,
        PathValues.API_V1_ORG_ID_VACANCY_VACANCY_DETAILS: ApiV1OrgIdVacancyVacancyDetails,
        PathValues.API_V1_ORG_ID_VACANCY: ApiV1OrgIdVacancy,
        PathValues.API_V1_WEBHOOKS_ID: ApiV1WebhooksId,
        PathValues.API_V1_WEBHOOKS: ApiV1Webhooks,
        PathValues.API_V1_WEBHOOKS_IDENTIFIER: ApiV1WebhooksIdentifier,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_ORG_ID_ABSENCE_IDENTIFIER: ApiV1OrgIdAbsenceIdentifier,
        PathValues.API_V1_ORG_ID_ABSENCE: ApiV1OrgIdAbsence,
        PathValues.API_V1_ORG_ID_ABSENCE_REASON_IDENTIFIER: ApiV1OrgIdAbsenceReasonIdentifier,
        PathValues.API_V1_ORG_ID_ABSENCE_REASON: ApiV1OrgIdAbsenceReason,
        PathValues.API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES_ID: ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalancesId,
        PathValues.API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES: ApiV1OrgIdEmployeeEmployeeIdentifierAbsenceReasonBalances,
        PathValues.API_V1_ORG_ID_ASSIGNMENT_IDENTIFIER: ApiV1OrgIdAssignmentIdentifier,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_DOWNLOAD: ApiV1OrgIdConnectionIdDownload,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_DATA: ApiV1OrgIdConnectionIdData,
        PathValues.API_V1_ORG_ID_CONNECTION_ID_RUN: ApiV1OrgIdConnectionIdRun,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATION_ID: ApiV1OrganizationId,
        PathValues.API_V1_ORGANIZATION_ID_SCHOOL_YEAR: ApiV1OrganizationIdSchoolYear,
        PathValues.API_V1_ORGANIZATION_ID_SCHOOL_YEAR_CURRENT: ApiV1OrganizationIdSchoolYearCurrent,
        PathValues.API_V1_ORG_ID_REFERENCE_DATA_ATTRIBUTE: ApiV1OrgIdReferenceDataAttribute,
        PathValues.API_V1_ORG_ID_USER_IDENTIFIER: ApiV1OrgIdUserIdentifier,
        PathValues.API_V1_ORG_ID_USER_IDENTIFIER_ROLE: ApiV1OrgIdUserIdentifierRole,
        PathValues.API_V1_ORG_ID_USER_SUBSTITUTE: ApiV1OrgIdUserSubstitute,
        PathValues.API_V1_ORG_ID_USER_SUBSTITUTE_IDENTIFIER: ApiV1OrgIdUserSubstituteIdentifier,
        PathValues.API_V1_ORG_ID_USER_EMPLOYEE_IDENTIFIER: ApiV1OrgIdUserEmployeeIdentifier,
        PathValues.API_V1_ORG_ID_USER_ADMINISTRATOR_IDENTIFIER: ApiV1OrgIdUserAdministratorIdentifier,
        PathValues.API_V1_ORG_ID_USER_EMPLOYEE: ApiV1OrgIdUserEmployee,
        PathValues.API_V1_ORG_ID_USER_ADMINISTRATOR: ApiV1OrgIdUserAdministrator,
        PathValues.API_V1_ORG_ID_VACANCY_IDENTIFIER: ApiV1OrgIdVacancyIdentifier,
        PathValues.API_V1_ORG_ID_VACANCY_VACANCY_DETAILS: ApiV1OrgIdVacancyVacancyDetails,
        PathValues.API_V1_ORG_ID_VACANCY: ApiV1OrgIdVacancy,
        PathValues.API_V1_WEBHOOKS_ID: ApiV1WebhooksId,
        PathValues.API_V1_WEBHOOKS: ApiV1Webhooks,
        PathValues.API_V1_WEBHOOKS_IDENTIFIER: ApiV1WebhooksIdentifier,
    }
)
