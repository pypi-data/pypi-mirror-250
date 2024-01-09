# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901

from .software_source_summary import SoftwareSourceSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CustomSoftwareSourceSummary(SoftwareSourceSummary):
    """
    A custom software source contains a custom collection of packages.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CustomSoftwareSourceSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.os_management_hub.models.CustomSoftwareSourceSummary.software_source_type` attribute
        of this class is ``CUSTOM`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this CustomSoftwareSourceSummary.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CustomSoftwareSourceSummary.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CustomSoftwareSourceSummary.
        :type display_name: str

        :param repo_id:
            The value to assign to the repo_id property of this CustomSoftwareSourceSummary.
        :type repo_id: str

        :param url:
            The value to assign to the url property of this CustomSoftwareSourceSummary.
        :type url: str

        :param time_created:
            The value to assign to the time_created property of this CustomSoftwareSourceSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this CustomSoftwareSourceSummary.
        :type time_updated: datetime

        :param description:
            The value to assign to the description property of this CustomSoftwareSourceSummary.
        :type description: str

        :param software_source_type:
            The value to assign to the software_source_type property of this CustomSoftwareSourceSummary.
            Allowed values for this property are: "VENDOR", "CUSTOM", "VERSIONED"
        :type software_source_type: str

        :param availability:
            The value to assign to the availability property of this CustomSoftwareSourceSummary.
            Allowed values for this property are: "AVAILABLE", "SELECTED", "RESTRICTED"
        :type availability: str

        :param os_family:
            The value to assign to the os_family property of this CustomSoftwareSourceSummary.
            Allowed values for this property are: "ORACLE_LINUX_9", "ORACLE_LINUX_8", "ORACLE_LINUX_7"
        :type os_family: str

        :param arch_type:
            The value to assign to the arch_type property of this CustomSoftwareSourceSummary.
            Allowed values for this property are: "X86_64", "AARCH64", "I686", "NOARCH", "SRC"
        :type arch_type: str

        :param package_count:
            The value to assign to the package_count property of this CustomSoftwareSourceSummary.
        :type package_count: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this CustomSoftwareSourceSummary.
        :type lifecycle_state: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CustomSoftwareSourceSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CustomSoftwareSourceSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this CustomSoftwareSourceSummary.
        :type system_tags: dict(str, dict(str, object))

        :param vendor_software_sources:
            The value to assign to the vendor_software_sources property of this CustomSoftwareSourceSummary.
        :type vendor_software_sources: list[oci.os_management_hub.models.Id]

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'repo_id': 'str',
            'url': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'description': 'str',
            'software_source_type': 'str',
            'availability': 'str',
            'os_family': 'str',
            'arch_type': 'str',
            'package_count': 'int',
            'lifecycle_state': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'vendor_software_sources': 'list[Id]'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'repo_id': 'repoId',
            'url': 'url',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'description': 'description',
            'software_source_type': 'softwareSourceType',
            'availability': 'availability',
            'os_family': 'osFamily',
            'arch_type': 'archType',
            'package_count': 'packageCount',
            'lifecycle_state': 'lifecycleState',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'vendor_software_sources': 'vendorSoftwareSources'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._repo_id = None
        self._url = None
        self._time_created = None
        self._time_updated = None
        self._description = None
        self._software_source_type = None
        self._availability = None
        self._os_family = None
        self._arch_type = None
        self._package_count = None
        self._lifecycle_state = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._vendor_software_sources = None
        self._software_source_type = 'CUSTOM'

    @property
    def vendor_software_sources(self):
        """
        **[Required]** Gets the vendor_software_sources of this CustomSoftwareSourceSummary.
        List of vendor software sources.


        :return: The vendor_software_sources of this CustomSoftwareSourceSummary.
        :rtype: list[oci.os_management_hub.models.Id]
        """
        return self._vendor_software_sources

    @vendor_software_sources.setter
    def vendor_software_sources(self, vendor_software_sources):
        """
        Sets the vendor_software_sources of this CustomSoftwareSourceSummary.
        List of vendor software sources.


        :param vendor_software_sources: The vendor_software_sources of this CustomSoftwareSourceSummary.
        :type: list[oci.os_management_hub.models.Id]
        """
        self._vendor_software_sources = vendor_software_sources

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
