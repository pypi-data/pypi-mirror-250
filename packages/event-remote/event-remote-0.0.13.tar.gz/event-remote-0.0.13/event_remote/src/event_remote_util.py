from .event_constants import EventRemoteConstants
from requests import Response
import requests
from httpstatus import HTTPStatus
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger  # noqa 402

logger = Logger.create_logger(object=EventRemoteConstants.EVENT_REMOTE_CODE_LOGGER_OBJECT)


class EventRemoteUtil:

    @staticmethod
    def handle_response(response: Response):
        response_json = response.json()
        if response.status_code == HTTPStatus.OK or response.status_code == HTTPStatus.CREATED:
            return response_json
        else:
            raise requests.exceptions.HTTPError(response=response, request=None)
