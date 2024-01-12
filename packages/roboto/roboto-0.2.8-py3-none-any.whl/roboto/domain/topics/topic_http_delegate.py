import collections.abc
import typing
import urllib.parse

from ...association import Association
from ...exceptions import RobotoHttpExceptionParse
from ...http import HttpClient, roboto_headers
from .topic_delegate import TopicDelegate
from .topic_record import (
    MessagePathRecord,
    RepresentationRecord,
    TopicRecord,
)
from .topic_requests import (
    AddMessagePathRepresentationRequest,
    AddMessagePathRequest,
    CreateTopicRequest,
    SetDefaultRepresentationRequest,
    UpdateTopicRequest,
)


class TopicHttpDelegate(TopicDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient):
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

    def add_message_path(
        self, topic_record: TopicRecord, request: AddMessagePathRequest
    ) -> MessagePathRecord:
        raise NotImplementedError("add_message_path is an admin-only operation")

    def add_message_path_representation(
        self, topic_record: TopicRecord, request: AddMessagePathRepresentationRequest
    ) -> RepresentationRecord:
        raise NotImplementedError(
            "add_message_path_representation is an admin-only operation"
        )

    def create_topic(self, request: CreateTopicRequest) -> TopicRecord:
        raise NotImplementedError("create_topic is an admin-only operation")

    def get_message_paths(
        self, topic_record: TopicRecord
    ) -> collections.abc.Sequence[MessagePathRecord]:
        quoted_topic_name = urllib.parse.quote_plus(topic_record.topic_name)
        encoded_association = topic_record.association.url_encode()
        url = "/".join(
            [
                self.__roboto_service_base_url,
                "v1/topics",
                f"association/{encoded_association}/name/{quoted_topic_name}/message-path",
            ]
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(resource_owner_id=topic_record.org_id),
            )
        return [
            MessagePathRecord.model_validate(record)
            for record in response.from_json(json_path=["data"])
        ]

    def get_topic_by_name_and_association(
        self,
        topic_name: str,
        association: Association,
        org_id: typing.Optional[str] = None,
    ) -> TopicRecord:
        quoted_topic_name = urllib.parse.quote_plus(topic_name)
        encoded_association = association.url_encode()
        url = "/".join(
            [
                self.__roboto_service_base_url,
                "v1/topics",
                f"association/{encoded_association}/name/{quoted_topic_name}",
            ]
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(resource_owner_id=org_id),
            )
        return TopicRecord.model_validate(response.from_json(json_path=["data"]))

    def hard_delete_topic(
        self,
        topic_record: TopicRecord,
    ) -> None:
        raise NotImplementedError("hard_delete_topic is an admin-only operation")

    def set_default_representation(
        self, topic_record: TopicRecord, request: SetDefaultRepresentationRequest
    ) -> RepresentationRecord:
        raise NotImplementedError(
            "set_default_representation is an admin-only operation"
        )

    def soft_delete_topic(
        self,
        topic_record: TopicRecord,
    ) -> None:
        raise NotImplementedError("soft_delete_topic is an admin-only operation")

    def update_topic(
        self, topic_record: TopicRecord, request: UpdateTopicRequest
    ) -> TopicRecord:
        raise NotImplementedError("update_topic is an admin-only operation")
