import json

# from circles_local_database_python.generic_crud import GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from message_local.Recipient import Recipient
from queue_worker_local.queue_worker import QueueWorker
from user_context_remote.user_context import UserContext

from .utils import generate_random_string

# from email_address_local.email_address import EmailAddressesLocal


SMARTLINK_COMPONENT_ID = 258
SMARTLINK_COMPONENT_NAME = "smartlink"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
logger_object = {
    'component_id': SMARTLINK_COMPONENT_ID,
    'component_name': SMARTLINK_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=logger_object)

SMARTLINK_LENGTH = 20  # (26*2 + 10) ^ 20 = 62^20 possibilities (number with 36 digits)
# If adding more actions, make sure to update action_to_parameters and requirements.txt
VERIFY_EMAIL_ADDRESS_ACTION_ID = 17
SMARTLINK_ENTITY_TYPE_ID = 18


class SmartLinkLocal(QueueWorker):
    def __init__(self) -> None:
        # QueueWorker is a subclass of GenericCRUD.
        QueueWorker.__init__(self, schema_name="smartlink", table_name="smartlink_table",
                             id_column_name="smartlink_id", view_name="smartlink_view",
                             action_boolean_column="is_smartlink_action")
        self.user = UserContext()

    # We use primitive types for parameters and return value because we want to be able to call this function from srvls
    def insert(self, smartlink_type_id: int, campaign_id: int,
               from_recipient: dict = None, to_recipient: dict = None) -> dict:
        """Returns the inserted row as a dict"""
        # TODO should have an expiration parameter with a default of 7 days in case of email invitation,
        #  a few hours for sending pin code
        # TODO add support of multiple criteria per campaign
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "from_recipient": from_recipient,
                             "to_recipient": to_recipient,
                             "campaign_id": campaign_id,
                             "smartlink_type_id": smartlink_type_id})
        smartlink_data = super().select_one_dict_by_id(view_table_name="smartlink_type_view",
                                                       id_column_name="smartlink_type_id",
                                                       id_column_value=smartlink_type_id)

        smartlink_identifier = generate_random_string(length=SMARTLINK_LENGTH)
        # smartlink = f"www.circ.zone?a={smartlink_identifier}"
        smartlink_details = {
            "smartlink_identifier": smartlink_identifier,
            "campaign_id": campaign_id,
            "action_id": smartlink_data["action_id"],
            "dialog_workflow_script_id": smartlink_data["dialog_workflow_script_id"],
            "smartlink_type_id": smartlink_type_id,
            # TODO: get to_group_id and effective user id
        }
        if from_recipient:
            from_recipient_object = Recipient.from_json(from_recipient)
            smartlink_details["from_email"] = from_recipient_object.get_email_address()
            smartlink_details["from_normalized_phone"] = from_recipient_object.get_canonical_telephone()
            # contact_id, user_id, person_id, profile_id
            smartlink_details.update(
                {"from_" + key: value for key, value in from_recipient.items() if key.endswith("_id")})

        if to_recipient:
            to_recipient_object = Recipient.from_json(to_recipient)
            smartlink_details["to_email"] = to_recipient_object.get_email_address()
            smartlink_details["to_normalized_phone"] = to_recipient_object.get_canonical_telephone()
            smartlink_details["lang_code"] = to_recipient_object.get_preferred_language()
            smartlink_details.update({"to_" + key: value for key, value in to_recipient.items() if key.endswith("_id")})

        super().switch_db(new_database="identifier")
        super().insert(table_name="identifier_table",
                       data_json={"identifier": smartlink_identifier, "entity_type_id": SMARTLINK_ENTITY_TYPE_ID})

        super().switch_db(new_database="smartlink")
        smartlink_id = super().insert(data_json=smartlink_details)

        smartlink_details["smartlink_id"] = smartlink_id
        smartlink_details["session_id"] = session_id  # we can't add it before the insert because it's not in the table

        logger.end(object={"smartlink_details": smartlink_details})
        return smartlink_details

    # REST API GET request with GET parameter id=GsMgEP7rQJWRZUNWV4ES which executes a function based on action_id
    # from action_table with all fields that are not null in starlink_table (similar to queue worker but sync)
    # and get back from the action json with return-code, redirection url, stdout, stderr...
    # call api_management.incoming_api() which will call api_call.insert()

    def execute(self, smartlink_identifier: str) -> dict:
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "smartlink_identifier": smartlink_identifier})
        smartlink_details = self.select_one_dict_by_id(id_column_name="smartlink_identifier",
                                                       id_column_value=smartlink_identifier)
        if not smartlink_details:
            logger.error(message=f"smartlink_identifier {smartlink_identifier} not found",
                         object={"session_id": session_id})
            return {}

        action_to_parameters = {
            VERIFY_EMAIL_ADDRESS_ACTION_ID: {
                "function_parameters_json": {"email_address": smartlink_details["to_email"]},
                "class_parameters_json": {}},
            # If adding more actions, make sure to update requirements.txt
            # ...
        }
        if smartlink_details["action_id"] not in action_to_parameters:
            logger.error(message=f"action_id {smartlink_details['action_id']} not found",
                         object={"session_id": session_id})
            return {}
        execution_details = {
            "action_id": smartlink_details["action_id"],
            "smartlink_id": smartlink_identifier,
            "function_parameters_json": json.dumps(
                action_to_parameters[smartlink_details["action_id"]]["function_parameters_json"]),
            "class_parameters_json": json.dumps(
                action_to_parameters[smartlink_details["action_id"]]["class_parameters_json"]),
            "session_id": session_id,
            # "user_jwt": self.user.get_user_jwt(),
        }
        # TODO: save redirection url (how?)
        # AWS Lambda environment is read-only, so we can't install packages.
        super().execute(execution_details=execution_details, install_packages=False)

        smartlink_details["session_id"] = session_id
        logger.end(object={"execution_details": execution_details})
        return smartlink_details

    # 2. REST API POST gets json with all the details of a specific identifier for Dialog Workflow Remote
    def get_smartlink_by_identifier(self, smartlink_identifier: str) -> dict:
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "smartlink_identifier": smartlink_identifier})

        smartlink_details = super().select_one_dict_by_id(id_column_name="smartlink_identifier",
                                                          id_column_value=smartlink_identifier)
        if not smartlink_details:
            logger.error(message=f"smartlink_id {smartlink_identifier} not found",
                         object={"session_id": session_id})
            return {}
        smartlink_details["session_id"] = session_id

        logger.end(object={"smartlink_details": smartlink_details})
        return smartlink_details

    def get_smartlink_by_id(self, smartlink_id: int) -> dict:
        session_id = generate_random_string(length=32)
        logger.start(object={"session_id": session_id,
                             "smartlink_id": smartlink_id})

        smartlink_details = super().select_one_dict_by_id(id_column_name="smartlink_id",
                                                          id_column_value=smartlink_id)
        if not smartlink_details:
            logger.error(message=f"smartlink_id {smartlink_id} not found",
                         object={"session_id": session_id})
            return {}

        smartlink_details["session_id"] = session_id
        logger.end(object={"smartlink_details": smartlink_details})
        return smartlink_details
