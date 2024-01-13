# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from redrover_api.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_ORG_ID_ABSENCE_IDENTIFIER = "/api/v1/{orgId}/Absence/{identifier}"
    API_V1_ORG_ID_ABSENCE = "/api/v1/{orgId}/Absence"
    API_V1_ORG_ID_ABSENCE_REASON_IDENTIFIER = "/api/v1/{orgId}/AbsenceReason/{identifier}"
    API_V1_ORG_ID_ABSENCE_REASON = "/api/v1/{orgId}/AbsenceReason"
    API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES_ID = "/api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances/{id}"
    API_V1_ORG_ID_EMPLOYEE_EMPLOYEE_IDENTIFIER_ABSENCE_REASON_BALANCES = "/api/v1/{orgId}/Employee/{employeeIdentifier}/absenceReasonBalances"
    API_V1_ORG_ID_ASSIGNMENT_IDENTIFIER = "/api/v1/{orgId}/Assignment/{identifier}"
    API_V1_ORG_ID_CONNECTION_ID_DOWNLOAD = "/api/v1/{orgId}/Connection/{id}/download"
    API_V1_ORG_ID_CONNECTION_ID_DATA = "/api/v1/{orgId}/Connection/{id}/data"
    API_V1_ORG_ID_CONNECTION_ID_RUN = "/api/v1/{orgId}/Connection/{id}/run"
    API_V1_ORGANIZATION = "/api/v1/Organization"
    API_V1_ORGANIZATION_ID = "/api/v1/Organization/{id}"
    API_V1_ORGANIZATION_ID_SCHOOL_YEAR = "/api/v1/Organization/{id}/schoolYear"
    API_V1_ORGANIZATION_ID_SCHOOL_YEAR_CURRENT = "/api/v1/Organization/{id}/schoolYear/current"
    API_V1_ORG_ID_REFERENCE_DATA_ATTRIBUTE = "/api/v1/{orgId}/ReferenceData/attribute"
    API_V1_ORG_ID_USER_IDENTIFIER = "/api/v1/{orgId}/User/{identifier}"
    API_V1_ORG_ID_USER_IDENTIFIER_ROLE = "/api/v1/{orgId}/User/{identifier}/{role}"
    API_V1_ORG_ID_USER_SUBSTITUTE = "/api/v1/{orgId}/User/substitute"
    API_V1_ORG_ID_USER_SUBSTITUTE_IDENTIFIER = "/api/v1/{orgId}/User/substitute/{identifier}"
    API_V1_ORG_ID_USER_EMPLOYEE_IDENTIFIER = "/api/v1/{orgId}/User/employee/{identifier}"
    API_V1_ORG_ID_USER_ADMINISTRATOR_IDENTIFIER = "/api/v1/{orgId}/User/administrator/{identifier}"
    API_V1_ORG_ID_USER_EMPLOYEE = "/api/v1/{orgId}/User/employee"
    API_V1_ORG_ID_USER_ADMINISTRATOR = "/api/v1/{orgId}/User/administrator"
    API_V1_ORG_ID_VACANCY_IDENTIFIER = "/api/v1/{orgId}/Vacancy/{identifier}"
    API_V1_ORG_ID_VACANCY_VACANCY_DETAILS = "/api/v1/{orgId}/Vacancy/vacancyDetails"
    API_V1_ORG_ID_VACANCY = "/api/v1/{orgId}/Vacancy"
    API_V1_WEBHOOKS_ID = "/api/v1/Webhooks/{id}"
    API_V1_WEBHOOKS = "/api/v1/Webhooks"
    API_V1_WEBHOOKS_IDENTIFIER = "/api/v1/Webhooks/{identifier}"
