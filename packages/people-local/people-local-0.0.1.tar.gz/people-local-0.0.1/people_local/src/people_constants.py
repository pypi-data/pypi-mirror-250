from logger_local.LoggerComponentEnum import LoggerComponentEnum

class PeopleLocalConstants:

    # ask your team leader for this integer
    PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 265
    PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "Enter you repository name"
    DEVELOPER_EMAIL = "sahar.g@circ.zone"

    PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
        'component_id': PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    PEOPLE_LOCAL_PYTHON_PACKAGE_TEST_OGGER_OBJECT = {
        'component_id': PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': PEOPLE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        # TODO Please add the framework you use
        'developer_email': DEVELOPER_EMAIL
    }

    MEPPING_INFO = {
        'default_schema_name': 'contact_group',
        'default_id_column_name': None,
        'default_table_name': None,
        'default_view_table_name': None,
        'default_entity_name1': 'contact',
        'default_entity_name2': 'group'

    }
