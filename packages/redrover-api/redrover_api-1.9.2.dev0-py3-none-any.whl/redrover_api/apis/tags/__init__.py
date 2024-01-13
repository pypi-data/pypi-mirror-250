# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from redrover_api.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ABSENCE = "Absence"
    ABSENCE_REASON_BALANCE = "AbsenceReasonBalance"
    ABSENCE_REASON = "AbsenceReason"
    ASSIGNMENT = "Assignment"
    CONNECTION = "Connection"
    REFERENCE_DATA = "ReferenceData"
    USER = "User"
    VACANCY = "Vacancy"
    ORGANIZATION = "Organization"
    WEBHOOKS = "Webhooks"
