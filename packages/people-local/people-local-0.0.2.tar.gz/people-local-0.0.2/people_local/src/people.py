from dotenv import load_dotenv
from group_remote.group_remote import GroupsRemote
from logger_local.Logger import Logger
from .people_constants import PeopleLocalConstants

load_dotenv()


logger = Logger.create_logger(
    object=PeopleLocalConstants.PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)


# TODO Shall we inherit from GroupsRemote?
class PeopleLocal(GroupsRemote):
    def __init__(self):
        super().__init__()

    def process_first_name(self, original_first_name: str, contact_id: int) -> str:
        logger.start(object={'original_first_name': original_first_name})
        try:

            first_name = ''.join(
                [i for i in original_first_name if not i.isdigit()])
            normilized_first_name = first_name.split()[0]
            logger.info("normilized_first_name", object={
                        'normilized_first_name': normilized_first_name})
            self.add_update_group_and_link_to_contact(
                # TODO MEPPING_INFO -> MAPPING_INFO
                entity_name=normilized_first_name, mapping_info=PeopleLocalConstants.MEPPING_INFO, contact_id=contact_id)
        except Exception as e:
            logger.error("error processing first name", object={
                         'original_first_name': original_first_name, 'error': e})
            raise e

        # TODO Please use GenericCrudMl to update person.first_name_table

        # TODO Create group to all people with the same first name and add this contact/profile to the group
        
        logger.end("success processing first name",
                   object={'normilized_first_name': normilized_first_name})
        return normilized_first_name

    def process_last_name(self, original_last_name: str, contact_id: int) -> str:
        logger.start(object={'original_last_name': original_last_name})
        try:
            last_name = ''.join(
                [i for i in original_last_name if not i.isdigit()])
            normilized_last_name = last_name.split()[0]
            logger.info("normilized_last_name", object={
                        'normilized_last_name': normilized_last_name})
            self.add_update_group_and_link_to_contact(
                entity_name=normilized_last_name, mapping_info=PeopleLocalConstants.MEPPING_INFO, contact_id=contact_id)
        except Exception as e:
            logger.error("error processing last name", object={
                         'original_last_name': original_last_name, 'error': e})
            raise e
        logger.end("success processing last name",
                   object={'normilized_last_name': normilized_last_name})

        # TODO Create group to the family and add this contact/profile to the group

        return normilized_last_name

    def process_organization(self, mapping_info: dict, organization_name: str, email_address: str, contact_id: int) -> str:
        logger.start(object={'organization_name': organization_name})
        try:
            if organization_name is None or organization_name == "":
                organization_name = self.extract_organization_from_email_address(
                    email_address=email_address)
            normalized_organization_name = self.add_update_group_and_link_to_contact(
                entity_name=organization_name, mapping_info=mapping_info, contact_id=contact_id)
        except Exception as e:
            logger.error("error processing organization", object={
                         'organization_name': organization_name, 'error': e})
            raise e
        logger.end("success processing organization",
                   object={'normalized_organization_name': normalized_organization_name})
        return normalized_organization_name

    def extract_organization_from_email_address(self, email_address: str) -> str:
        logger.start(object={'email_address': email_address})
        try:
            organization_name = email_address.split('@')[1].split('.')[0]
        except Exception as e:
            logger.error("error extracting organization from email address", object={
                         'email_address': email_address, 'error': e})
            raise e
        logger.end("success extracting organization from email address",
                   object={'organization_name': organization_name})
        return organization_name
