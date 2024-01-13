#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Properties model."""
from typing import List, Union

from pydantic import ConfigDict
from .regscale_model import RegScaleModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime

logger = create_logger()
model_slug_id_url = "/api/{model_slug}/{id}"


class Properties(RegScaleModel):
    """Properties plan model"""

    _model_slug = "properties"
    id: int = 0
    createdById: str = ""  # this should be userID
    dateCreated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    lastUpdatedById: str = ""  # this should be userID
    isPublic: bool = True
    key: str = ""
    value: str = ""
    label: str = ""
    otherAttributes: str = ""
    parentId: int = 0
    parentModule: str = ""
    dateLastUpdated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def _get_additional_endpoints():
        """
        Get additional endpoints for the Properties model.

        :return: A dictionary of additional endpoints
        """
        return ConfigDict(
            get_all_by_parent="/api/{model_slug}/getAllByParent/{intParentID}/{strModule}",
            insert="/api/{model_slug}",
            batch_create_properties_post="/api/{model_slug}/batchCreate",
            batch_update_properties_put="/api/{model_slug}/batchUpdate",
            update=model_slug_id_url,
            delete=model_slug_id_url,
        )

    @classmethod
    def get_all_by_parent(cls, parent_id, parent_module):
        """
        Retrieves all properties for the given parent record.

        :param int parent_id: The ID of the parent record
        :param str parent_module: The module name
        :return: A list of properties or None
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_all_by_parent").format(
                model_slug=cls._model_slug,
                intParentID=parent_id,
                strModule=parent_module,
            )
        )
        if not response or response.status_code in [204, 404]:
            return []
        if response and response.ok:
            return [cls(**item) for item in response.json()]
        return []

    @staticmethod
    def from_dict(data: dict) -> "Properties":
        """Convert dict to Properties object
        :param data: dict to create object from
        :return: A Properties object
        """
        return Properties(**data)

    @staticmethod
    def create_properties_from_list(
        parent_id: Union[str, int],
        parent_module: str,
        properties_list: List[dict],
    ) -> List["Properties"]:
        """Create a list of Properties objects from a list of dicts
        :param parent_id: ID of the SSP to create the Properties objects for
        :param properties_list: List of dicts to create objects from
        :param parent_module: Parent module of the Properties objects
        :return: List of Properties objects
        """
        properties = [
            Properties(parentId=parent_id, parentModule=parent_module, **properties)
            for properties in properties_list
        ]
        return [
            property_.create_new_properties(return_object=True)
            for property_ in properties
        ]

    def create_new_properties(
        self, return_object: bool = False
    ) -> Union[bool, "Properties"]:
        """Create a new Properties object in RegScale
        :param return_object: Return the object if successful
        :return: True or the Properties created if successful, False otherwise
        """
        app = Application()
        api = Api(app=app)
        data = self.dict()
        data["id"] = None
        data["createdById"] = api.config["userId"]
        data["lastUpdatedById"] = api.config["userId"]
        properties_response = api.post(
            f'{api.config["domain"]}/api/properties/',
            json=data,
        )
        if properties_response.ok:
            logger.info(f'Created Properties: {properties_response.json()["id"]}')
            if return_object:
                return Properties.from_dict(properties_response.json())
            return True
        logger.error(f"Error creating Properties: {properties_response.text}")
        return False
