import typing_extensions

from redrover_api.apis.tags import TagValues
from redrover_api.apis.tags.absence_api import AbsenceApi
from redrover_api.apis.tags.absence_reason_balance_api import AbsenceReasonBalanceApi
from redrover_api.apis.tags.absence_reason_api import AbsenceReasonApi
from redrover_api.apis.tags.assignment_api import AssignmentApi
from redrover_api.apis.tags.connection_api import ConnectionApi
from redrover_api.apis.tags.reference_data_api import ReferenceDataApi
from redrover_api.apis.tags.user_api import UserApi
from redrover_api.apis.tags.vacancy_api import VacancyApi
from redrover_api.apis.tags.organization_api import OrganizationApi
from redrover_api.apis.tags.webhooks_api import WebhooksApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ABSENCE: AbsenceApi,
        TagValues.ABSENCE_REASON_BALANCE: AbsenceReasonBalanceApi,
        TagValues.ABSENCE_REASON: AbsenceReasonApi,
        TagValues.ASSIGNMENT: AssignmentApi,
        TagValues.CONNECTION: ConnectionApi,
        TagValues.REFERENCE_DATA: ReferenceDataApi,
        TagValues.USER: UserApi,
        TagValues.VACANCY: VacancyApi,
        TagValues.ORGANIZATION: OrganizationApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ABSENCE: AbsenceApi,
        TagValues.ABSENCE_REASON_BALANCE: AbsenceReasonBalanceApi,
        TagValues.ABSENCE_REASON: AbsenceReasonApi,
        TagValues.ASSIGNMENT: AssignmentApi,
        TagValues.CONNECTION: ConnectionApi,
        TagValues.REFERENCE_DATA: ReferenceDataApi,
        TagValues.USER: UserApi,
        TagValues.VACANCY: VacancyApi,
        TagValues.ORGANIZATION: OrganizationApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)
