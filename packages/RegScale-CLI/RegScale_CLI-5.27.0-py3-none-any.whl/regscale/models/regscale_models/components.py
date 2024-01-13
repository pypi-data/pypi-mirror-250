#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Component """
# standard python imports
from typing import Optional

from pydantic import BaseModel, ConfigDict
from .regscale_model import RegScaleModel
from regscale.core.app.api import Api
from regscale.core.app.application import Application


class Component(RegScaleModel):
    """Component Model"""

    _model_slug = "components"

    title: str
    description: str
    componentType: str
    componentOwnerId: str
    purpose: str = None
    securityPlansId: int = None
    cmmcAssetType: str = None
    createdBy: str = None
    createdById: str = None
    dateCreated: str = None
    lastUpdatedBy: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    status: str = "Active"
    uuid: str = None
    componentOwner: str = None
    cmmcExclusion: str = False
    id: int = None
    isPublic: str = True

    @staticmethod
    def _get_additional_endpoints():
        """
        Get additional endpoints for the Components model.

        :return: A dictionary of additional endpoints
        """
        return ConfigDict(
            get_list="/api/{model_slug}/getList",
            get_all_by_parent="/api/{model_slug}/getAllByParent/{intId}",
            get_count="/api/{model_slug}/getCount",
            graph="/api/{model_slug}/graph",
            graph_by_date="/api/{model_slug}/graphByDate/{strGroupBy}",
            report="/api/{model_slug}/report/{strReport}",
            filter_components="/api/{model_slug}/filterComponents",
            filter_component_dashboard="/api/{model_slug}/filterComponentDashboard",
            query_by_custom_field="/api/{model_slug}/queryByCustomField/{strFieldName}/{strValue}",
            insert="/api/{model_slug}",
            update="/api/{model_slug}/{id}",
            delete="/api/{model_slug}/{id}",
            get="/api/{model_slug}/find/{id}",
            evidence="/api/{model_slug}/evidence/{intID}",
            find_by_guid="/api/{model_slug}/findByGUID/{strGUID}",
            find_by_external_id="/api/{model_slug}/findByExternalId/{strID}",
            get_titles="/api/{model_slug}/getTitles",
            main_dashboard="/api/{model_slug}/mainDashboard/{intYear}",
            component_dashboard="/api/{model_slug}/componentDashboard/{intYear}",
            oscal="/api/{model_slug}/oscal/{intID}",
            statusboard="/api/{model_slug}/statusboard/{intID}/{strSearch}/{intPage}/{pageSize}",
            emass_export="/api/{model_slug}/emassExport/{intID}",
            mega_api="/api/{model_slug}/megaAPI/{intId}",
        )

    def __eq__(self, other):
        """
        Check if two Component objects are equal
        :param other: Component object to compare
        :return: True if equal, False if not
        :rtype: bool
        """
        return (
            self.title == other.title
            and self.description == other.description
            and self.componentType == other.componentType
        )

    def __hash__(self):
        """
        Hash a Component object
        :return: Hashed Component object
        :rtype: int
        """
        return hash((self.title, self.description, self.componentType))

    def __getitem__(self, key: any) -> any:
        """
        Get attribute from Pipeline
        :param any key:
        :return: value of provided key
        :rtype: any
        """
        if getattr(self, key) == "None":
            return None
        return getattr(self, key)

    def __setitem__(self, key: any, value: any) -> None:
        """
        Set attribute in Pipeline with provided key
        :param any key: Key to change to provided value
        :param any value: New value for provided Key
        :return: None
        """
        return setattr(self, key, value)

    @staticmethod
    def get_components_from_ssp(app: Application, ssp_id: int) -> list[dict]:
        """Get all components for a given SSP

        :param app: Application instance
        :param ssp_id: RegScale SSP
        :return: List of component dictionaries
        """
        api = Api(app)
        existing_res = api.get(
            app.config["domain"] + f"/api/components/getAllByParent/{ssp_id}"
        )
        if not existing_res.raise_for_status():
            return existing_res.json()
