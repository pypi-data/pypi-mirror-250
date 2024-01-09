# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901

from .package_summary import PackageSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdatablePackageSummary(PackageSummary):
    """
    A software package available for install on a managed instance.
    """

    #: A constant which can be used with the update_type property of a UpdatablePackageSummary.
    #: This constant has a value of "SECURITY"
    UPDATE_TYPE_SECURITY = "SECURITY"

    #: A constant which can be used with the update_type property of a UpdatablePackageSummary.
    #: This constant has a value of "BUGFIX"
    UPDATE_TYPE_BUGFIX = "BUGFIX"

    #: A constant which can be used with the update_type property of a UpdatablePackageSummary.
    #: This constant has a value of "ENHANCEMENT"
    UPDATE_TYPE_ENHANCEMENT = "ENHANCEMENT"

    #: A constant which can be used with the update_type property of a UpdatablePackageSummary.
    #: This constant has a value of "OTHER"
    UPDATE_TYPE_OTHER = "OTHER"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdatablePackageSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.os_management_hub.models.UpdatablePackageSummary.package_classification` attribute
        of this class is ``UPDATABLE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdatablePackageSummary.
        :type display_name: str

        :param name:
            The value to assign to the name property of this UpdatablePackageSummary.
        :type name: str

        :param type:
            The value to assign to the type property of this UpdatablePackageSummary.
        :type type: str

        :param version:
            The value to assign to the version property of this UpdatablePackageSummary.
        :type version: str

        :param architecture:
            The value to assign to the architecture property of this UpdatablePackageSummary.
            Allowed values for this property are: "X86_64", "AARCH64", "I686", "NOARCH", "SRC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type architecture: str

        :param software_sources:
            The value to assign to the software_sources property of this UpdatablePackageSummary.
        :type software_sources: list[oci.os_management_hub.models.SoftwareSourceDetails]

        :param package_classification:
            The value to assign to the package_classification property of this UpdatablePackageSummary.
            Allowed values for this property are: "INSTALLED", "AVAILABLE", "UPDATABLE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type package_classification: str

        :param installed_version:
            The value to assign to the installed_version property of this UpdatablePackageSummary.
        :type installed_version: str

        :param update_type:
            The value to assign to the update_type property of this UpdatablePackageSummary.
            Allowed values for this property are: "SECURITY", "BUGFIX", "ENHANCEMENT", "OTHER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type update_type: str

        :param errata:
            The value to assign to the errata property of this UpdatablePackageSummary.
        :type errata: list[str]

        :param related_cves:
            The value to assign to the related_cves property of this UpdatablePackageSummary.
        :type related_cves: list[str]

        """
        self.swagger_types = {
            'display_name': 'str',
            'name': 'str',
            'type': 'str',
            'version': 'str',
            'architecture': 'str',
            'software_sources': 'list[SoftwareSourceDetails]',
            'package_classification': 'str',
            'installed_version': 'str',
            'update_type': 'str',
            'errata': 'list[str]',
            'related_cves': 'list[str]'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'name': 'name',
            'type': 'type',
            'version': 'version',
            'architecture': 'architecture',
            'software_sources': 'softwareSources',
            'package_classification': 'packageClassification',
            'installed_version': 'installedVersion',
            'update_type': 'updateType',
            'errata': 'errata',
            'related_cves': 'relatedCves'
        }

        self._display_name = None
        self._name = None
        self._type = None
        self._version = None
        self._architecture = None
        self._software_sources = None
        self._package_classification = None
        self._installed_version = None
        self._update_type = None
        self._errata = None
        self._related_cves = None
        self._package_classification = 'UPDATABLE'

    @property
    def installed_version(self):
        """
        Gets the installed_version of this UpdatablePackageSummary.
        The version of this upgradable package already installed on the instance.


        :return: The installed_version of this UpdatablePackageSummary.
        :rtype: str
        """
        return self._installed_version

    @installed_version.setter
    def installed_version(self, installed_version):
        """
        Sets the installed_version of this UpdatablePackageSummary.
        The version of this upgradable package already installed on the instance.


        :param installed_version: The installed_version of this UpdatablePackageSummary.
        :type: str
        """
        self._installed_version = installed_version

    @property
    def update_type(self):
        """
        **[Required]** Gets the update_type of this UpdatablePackageSummary.
        The classification of this update.

        Allowed values for this property are: "SECURITY", "BUGFIX", "ENHANCEMENT", "OTHER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The update_type of this UpdatablePackageSummary.
        :rtype: str
        """
        return self._update_type

    @update_type.setter
    def update_type(self, update_type):
        """
        Sets the update_type of this UpdatablePackageSummary.
        The classification of this update.


        :param update_type: The update_type of this UpdatablePackageSummary.
        :type: str
        """
        allowed_values = ["SECURITY", "BUGFIX", "ENHANCEMENT", "OTHER"]
        if not value_allowed_none_or_none_sentinel(update_type, allowed_values):
            update_type = 'UNKNOWN_ENUM_VALUE'
        self._update_type = update_type

    @property
    def errata(self):
        """
        Gets the errata of this UpdatablePackageSummary.
        List of errata containing this update.


        :return: The errata of this UpdatablePackageSummary.
        :rtype: list[str]
        """
        return self._errata

    @errata.setter
    def errata(self, errata):
        """
        Sets the errata of this UpdatablePackageSummary.
        List of errata containing this update.


        :param errata: The errata of this UpdatablePackageSummary.
        :type: list[str]
        """
        self._errata = errata

    @property
    def related_cves(self):
        """
        Gets the related_cves of this UpdatablePackageSummary.
        List of CVEs applicable to this erratum.


        :return: The related_cves of this UpdatablePackageSummary.
        :rtype: list[str]
        """
        return self._related_cves

    @related_cves.setter
    def related_cves(self, related_cves):
        """
        Sets the related_cves of this UpdatablePackageSummary.
        List of CVEs applicable to this erratum.


        :param related_cves: The related_cves of this UpdatablePackageSummary.
        :type: list[str]
        """
        self._related_cves = related_cves

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
