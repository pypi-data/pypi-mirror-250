from .event_remote_util import EventRemoteUtil
from url_remote.url_circlez import OurUrl
from url_remote.action_name_enum import ActionName
from url_remote.entity_name_enum import EntityName
from url_remote.component_name_enum import ComponentName
from logger_local.Logger import Logger
from .event_constants import EventRemoteConstants
import copy
import requests
from dotenv import load_dotenv
load_dotenv()
from event_external_local.external_event_local_class import ExternalEventsLocal  # noqa402
from sdk.src.utilities import create_http_headers  # noqa402


class EventRemote:

    def __init__(self):
        self.event_external_local = ExternalEventsLocal()
        self.url_circlez = OurUrl()
        self.logger = Logger.create_logger(
            object=EventRemoteConstants.EVENT_REMOTE_CODE_LOGGER_OBJECT)
        self.brand_name = EventRemoteConstants.BRAND_NAME
        self.env_name = EventRemoteConstants.ENVIRONMENT_NAME
        self.user_jwt = self.logger.user_context.get_user_jwt()

    def get_url_by_action_name(self, action_name: ActionName,
                               api_version: int = 1, path_parameters: dict = None,
                               query_parameters: dict = None):
        # optional query_parameters can be added if needed
        return self.url_circlez.endpoint_url(
            brand_name=self.brand_name,
            environment_name=self.env_name,
            component_name=ComponentName.EVENT.value,
            entity_name=EntityName.EVENT.value,
            version=api_version,
            action_name=action_name.value,
            path_parameters=path_parameters if path_parameters else None,
            query_parameters=query_parameters if query_parameters else None
        )

    def create_event(self, event_json: dict):
        object_start = copy.copy(event_json)
        self.logger.start("Start create event", object=object_start)
        try:
            url = self.get_url_by_action_name(ActionName.CREATE_EVENT, api_version=EventRemoteConstants.EVENT_API_VERSION)
            url = "https://2iclscptqh.execute-api.us-east-1.amazonaws.com/play1/api/v1/event/createEvent"  # TODO delete

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            headers = create_http_headers(self.user_jwt)
            response = requests.post(
                url=url, json=event_json, headers=headers)

            response_json = EventRemoteUtil.handle_response(response=response)
            self.logger.end(
                f"End create event-remote, response: {response_json}")
            return response_json

        except requests.exceptions.HTTPError as e:
            self.logger.exception(
                    f"Http error - status code: {e.response.status_code}", object=e)
            self.logger.end("End create event-remote, HTTP error exception")
            raise e

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End create event-remote, connection error exception")
            raise e

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End create event-remote, timeout exception")
            raise e

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End create event-remote, request exception")
            raise e

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End create event-remote, general exception")
            raise e

    def create_external_event(self, external_event_details: dict):
        self.logger.start("Start create external event",
                          object={'external_event_details': external_event_details})
        try:
            event_response = self.create_event(event_json=external_event_details)
            event_id = event_response.get('event_id')

            # TODO send as a dict after event_external_local insert method gets a dict
            external_event_id = self.event_external_local.insert(
                system_id=external_event_details.get('system_id'),
                subsystem_id=external_event_details.get('subsystem_id'),
                url=external_event_details.get('url'),
                external_event_identifier=external_event_details.get('external_event_identifier'),
                environment_id=external_event_details.get('environment_id'))

            # TODO after creating event-event-external-local insert the mapping here

            event_ids = {
                'event_id': event_id,
                'event_external_id': external_event_id
            }
            object_end = copy.copy(event_ids)
            self.logger.end("End create external event-remote",
                            object=object_end)
            return event_ids

        except requests.exceptions.HTTPError as e:
            self.logger.exception(
                f"HTTP error status code: {e.response.status_code}", object=e)
            self.logger.end("End create external event-remote HTTP error exception")
            raise e

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End create external event-remote connection error exception")
            raise e

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End create external event-remote timeout exception")
            raise e

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End create external event-remote request exception")
            raise e

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End create external event-remote general exception")
            raise e

    def get_event_by_event_id(self, event_id: int):
        query_parameter = {
            'event_id': event_id
        }
        self.logger.start("Start get event-remote", object={'event_id': event_id})
        try:
            url = self.get_url_by_action_name(
                ActionName.GET_EVENT_BY_ID, api_version=EventRemoteConstants.EVENT_API_VERSION,
                query_parameters=query_parameter)
            url = f"https://2iclscptqh.execute-api.us-east-1.amazonaws.com/play1/api/v1/event/getEventById?eventId={event_id}"

            self.logger.info(
                "Endpoint event - getEventById action: " + url)

            headers = create_http_headers(self.user_jwt)

            response = requests.get(url=url, headers=headers)

            response_json = EventRemoteUtil.handle_response(response=response)
            self.logger.end(
                f"End get_event_by_event_id event-remote, response: {response_json}")
            return response_json

        except requests.exceptions.HTTPError as e:
            self.logger.exception(
                f"Http error - status code: {e.response.status_code}", object=e)
            self.logger.end("End get_event_by_event_id event-remote, HTTP error exception")
            raise e

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End get event-remote connection error exception")
            raise e

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End get event-remote timeout exception")
            raise e

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End get event-remote request exception")
            raise e

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End get event-remote general exception")
            raise e

    def delete_event_by_id(self, event_id: int):
        path_parameters = {
            'event_id': event_id
        }
        self.logger.start("Start delete event-remote", object=path_parameters)
        try:
            url = self.get_url_by_action_name(
                api_version=EventRemoteConstants.EVENT_API_VERSION,
                action_name=ActionName.DELETE_EVENT_BY_ID, path_parameters=path_parameters)

            url = f"https://2iclscptqh.execute-api.us-east-1.amazonaws.com/play1/api/v1/event/deleteEventById/{event_id}"  # TODO delete  # noqa501
            self.logger.info(
                "Endpoint event - deleteEventById action: " + url)

            headers = create_http_headers(self.user_jwt)

            response = requests.delete(url=url, headers=headers)
            response_json = EventRemoteUtil.handle_response(response=response)
            self.logger.end(
                f"End delete event-remote, response: {response_json}")
            return response_json

        except requests.exceptions.HTTPError as e:
            self.logger.exception(
                f"Http error - status code: {e.response.status_code}", object=e)
            self.logger.end("End delete_event_by_id event-remote, HTTP error exception")
            raise e

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End delete event-remote connection error exception")
            raise e

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End delete event-remote timeout exception")
            raise e

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End delete event-remote request exception")
            raise e

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End delete event-remote general exception")
            raise e

    def update_event_by_id(self, event_id: int, event_json: dict):

        self.logger.start("Start update event-remote", object={'event_json': copy.copy(event_json),
                                                               'event_id': event_id})
        try:
            path_parameters = {
                'event_id': event_id
            }
            url = self.get_url_by_action_name(
                action_name=ActionName.UPDATE_EVENT_BY_ID, path_parameters=path_parameters,
                api_version=EventRemoteConstants.EVENT_API_VERSION)

            url = f"https://2iclscptqh.execute-api.us-east-1.amazonaws.com/play1/api/v1/event/updateEventById/{event_id}"  # TODO delete  # noqa501

            self.logger.info(
                "Endpoint event - updateEventById action: " + url)

            headers = create_http_headers(self.user_jwt)

            response = requests.put(
                url=url, json=event_json, headers=headers)
            response_json = EventRemoteUtil.handle_response(response=response)
            self.logger.end(
                f"End update event-remote, response: {response_json}")
            return response_json

        except requests.exceptions.HTTPError as e:
            self.logger.exception(
                f"Http error - status code: {e.response.status_code}", object=e)
            self.logger.end("End update_event_by_id event-remote, HTTP error exception")
            raise e
        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            self.logger.end("End update event-remote connection error exception")
            raise e

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            self.logger.end("End update event-remote timeout exception")
            raise e

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            self.logger.end("End update event-remote request exception")
            raise e

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            self.logger.end("End update event-remote general exception")
            raise e

    def update_event_external_by_id(self, event_external_id: int, event_external_json: dict):
        self.logger.start("Start update_event_external_by_id", object={'event_json': copy.copy(event_external_json),
                                                                       'event_id': event_external_id})
        # TODO update when update_by_external_event_id method gets a dict
        self.event_external_local.update_by_external_event_id(
            external_event_id=event_external_id,
            system_id=event_external_json.get('system_id'),
            subsystem_id=event_external_json.get('sunsystem_id'),
            url=event_external_json.get('url'),
            external_event_identifier=event_external_json.get("external_event_identifier"),
            environment_id=event_external_json.get('environment_id'))

        self.logger.end("end update_event_external_by_id")

    def delete_event_external_by_id(self, event_external_id):
        self.logger.start("Start delete_event_external_by_id", object={'event_id': event_external_id})
        self.event_external_local.delete_by_external_event_id(external_event_id=event_external_id)
        self.logger.end("end delete_event_external_by_id")

    def get_event_by_event_external_id(self, event_external_id: int):
        self.logger.start("Start get_event_by_event_external_id", object={'event_external_id': event_external_id})
        event_external = self.event_external_local.select_by_external_event_id(external_event_id=event_external_id)
        self.logger.end(
            f"End get_event_by_event_id event-remote, response: {copy.copy(event_external)}")
        return event_external
