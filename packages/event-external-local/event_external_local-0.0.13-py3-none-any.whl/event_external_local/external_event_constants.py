from logger_local.LoggerComponentEnum import LoggerComponentEnum


class ExternalEventLocalConstants:

    # TODO Please update your email
    DEVELOPER_EMAIL = 'gil.a@circ.zone'
    EXTERNAL_EVENT_LOCAL_COMPONENT_ID = 251
    EVENT_EXTERNAL_LOCAL_PYHTON_COMPONENT_NAME = 'event-external-local-python-package'
    EXTERNAL_EVENT_LOCAL_CODE_LOGGER_OBJECT = {
        'component_id': EXTERNAL_EVENT_LOCAL_COMPONENT_ID,
        'component_name': EVENT_EXTERNAL_LOCAL_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    EXTERNAL_EVENT_LOCAL_TEST_LOGGER_OBJECT = {
        'component_id': EXTERNAL_EVENT_LOCAL_COMPONENT_ID,
        'component_name': EVENT_EXTERNAL_LOCAL_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    # TODO Please replace <ENTITY> i.e. COUNTRY
    # UNKNOWN_<ENTITY>_ID = 0

    # TODO Please update if you need default values i.e. for testing
    # DEFAULT_XXX_NAME = None
    # DEFAULT_XXX_NAME = None

    # TODO In the case you use non-ML Table, please replace <entity> i.e. country
    EXTERNAL_EVENT_TABLE_NAME = 'event_external_table'

    EXTERNAL_EVENT_SCHEMA_NAME = 'event_external'

    EXTERNAL_EVENT_ID_COLUMN_NAME = 'event_external_id'

    EXTERNAL_EVENT_VIEW_NAME = 'event_external_view'
    # <ENTITY>_VIEW_NAME = '<entity>_ml_table'

    # TODO In the case you use ML Table, please replace <entity> i.e. country
    # <ENTITY>_TABLE_NAME = '<entity>_table'
    # <ENTITY>_ML_TABLE_NAME = '<entity>_ml_table'
    # <ENTITY>_ML_VIEW_NAME = '<entity>_ml_view'
