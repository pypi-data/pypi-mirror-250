from logger_local.LoggerComponentEnum import LoggerComponentEnum
import os


class EventRemoteConstants:
    DEVELOPER_EMAIL = 'gil.a@circ.zone'
    EVENT_REMOTE_COMPONENT_ID = 248
    EVENT_REMOTE_PYHTON_COMPONENT_NAME = 'event-remote-restapi-python-package'
    EVENT_REMOTE_CODE_LOGGER_OBJECT = {
        'component_id': EVENT_REMOTE_COMPONENT_ID,
        'component_name': EVENT_REMOTE_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    EVENT_REMOTE_TEST_LOGGER_OBJECT = {
        'component_id': EVENT_REMOTE_COMPONENT_ID,
        'component_name': EVENT_REMOTE_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'developer_email': DEVELOPER_EMAIL
    }

    BRAND_NAME = os.getenv("BRAND_NAME")
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME")
    EVENT_API_VERSION = 1

    TEST_LOCATION_ID_1 = 1
    TEST_ORGANIZERS_PROFILE_ID_1 = 4
    TEST_URL_1 = 'http://testt.com/1'
    TEST_LOCATION_ID_2 = 2
    TEST_ORGANIZERS_PROFILE_ID_2 = 2
    TEST_URL_2 = 'http://testt.com/2'
    TEST_INVALID_URL = "not_a_url"
    SYSTEM_ID = 10
    EXTERNAL_EVENT_IDENTIFIER = 'external_event_identifier'
    TEST_URL_EXTERNAL_1 = 'http://externalTe.com/1'
    INVALID_EVENT_ID = -1

    EVENT_TEST_JSON_1 = {"location_id": TEST_LOCATION_ID_1,
                         "organizers_profile_id": TEST_ORGANIZERS_PROFILE_ID_1,
                         "website_url": TEST_URL_1,
                         "facebook_event_url": TEST_URL_1,
                         "meetup_event_url": TEST_URL_1,
                         "registration_url": TEST_URL_1
                         }

    EVENT_TEST_JSON_2 = {
        'location_id': TEST_LOCATION_ID_2,
        'organizers_profile_id': TEST_ORGANIZERS_PROFILE_ID_2,
        'website_url': TEST_URL_2,
        "facebook_event_url": TEST_URL_2,
        "meetup_event_url": TEST_URL_2,
        "registration_url": TEST_URL_2
    }

    EXTERNAL_EVENT_TEST_JSON_1 = {
        'location_id': TEST_LOCATION_ID_1,
        'organizers_profile_id': TEST_ORGANIZERS_PROFILE_ID_1,
        'website_url': TEST_URL_1,
        "facebook_event_url": TEST_URL_1,
        "meetup_event_url": TEST_URL_1,
        "registration_url": TEST_URL_1,
        'system_id': SYSTEM_ID,
        'is_approved': None,
        'url':  None,  # cannot have duplicate url in the table
        'external_event_identifier': EXTERNAL_EVENT_IDENTIFIER,
        'subsystem_id': None,
        'environment_id': None
    }

    EXTERNAL_EVENT_TEST_JSON_2 = {
        'location_id': TEST_LOCATION_ID_2,
        'organizers_profile_id': TEST_ORGANIZERS_PROFILE_ID_2,
        'website_url': TEST_URL_2,
        "facebook_event_url": TEST_URL_2,
        "meetup_event_url": TEST_URL_2,
        "registration_url": TEST_URL_2,
        'system_id': SYSTEM_ID,
        'is_approved': None,
        'url':  None,
        'external_event_identifier': EXTERNAL_EVENT_IDENTIFIER,
        'subsystem_id': None,
        'environment_id': None
    }
    EVENT_TEST_INVALID_JSON = {
        'location_id': TEST_LOCATION_ID_1,
        'organizers_profile_id': TEST_ORGANIZERS_PROFILE_ID_1,
        'website_url': TEST_INVALID_URL,
        "facebook_event_url": TEST_INVALID_URL,
        "meetup_event_url": TEST_INVALID_URL,
        "registration_url": TEST_INVALID_URL
    }

    EXTERNAL_EVENT_TABLE_NAME = 'event_external_table'

    EXTERNAL_EVENT_SCHEMA_NAME = 'event_external'

    EXTERNAL_EVENT_ID_COLUMN_NAME = 'event_external_id'

    EXTERNAL_EVENT_VIEW_NAME = 'event_external_view'
