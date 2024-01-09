# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: v1


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SettingsCloudGateCorsSettings(object):
    """
    A complex attribute that specifies the Cloud Gate cross origin resource sharing settings.

    **Added In:** 2011192329

    **SCIM++ Properties:**
    - caseExact: false
    - idcsSearchable: false
    - multiValued: false
    - mutability: readWrite
    - required: false
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SettingsCloudGateCorsSettings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param cloud_gate_cors_allow_null_origin:
            The value to assign to the cloud_gate_cors_allow_null_origin property of this SettingsCloudGateCorsSettings.
        :type cloud_gate_cors_allow_null_origin: bool

        :param cloud_gate_cors_enabled:
            The value to assign to the cloud_gate_cors_enabled property of this SettingsCloudGateCorsSettings.
        :type cloud_gate_cors_enabled: bool

        :param cloud_gate_cors_allowed_origins:
            The value to assign to the cloud_gate_cors_allowed_origins property of this SettingsCloudGateCorsSettings.
        :type cloud_gate_cors_allowed_origins: list[str]

        :param cloud_gate_cors_max_age:
            The value to assign to the cloud_gate_cors_max_age property of this SettingsCloudGateCorsSettings.
        :type cloud_gate_cors_max_age: int

        :param cloud_gate_cors_exposed_headers:
            The value to assign to the cloud_gate_cors_exposed_headers property of this SettingsCloudGateCorsSettings.
        :type cloud_gate_cors_exposed_headers: list[str]

        """
        self.swagger_types = {
            'cloud_gate_cors_allow_null_origin': 'bool',
            'cloud_gate_cors_enabled': 'bool',
            'cloud_gate_cors_allowed_origins': 'list[str]',
            'cloud_gate_cors_max_age': 'int',
            'cloud_gate_cors_exposed_headers': 'list[str]'
        }

        self.attribute_map = {
            'cloud_gate_cors_allow_null_origin': 'cloudGateCorsAllowNullOrigin',
            'cloud_gate_cors_enabled': 'cloudGateCorsEnabled',
            'cloud_gate_cors_allowed_origins': 'cloudGateCorsAllowedOrigins',
            'cloud_gate_cors_max_age': 'cloudGateCorsMaxAge',
            'cloud_gate_cors_exposed_headers': 'cloudGateCorsExposedHeaders'
        }

        self._cloud_gate_cors_allow_null_origin = None
        self._cloud_gate_cors_enabled = None
        self._cloud_gate_cors_allowed_origins = None
        self._cloud_gate_cors_max_age = None
        self._cloud_gate_cors_exposed_headers = None

    @property
    def cloud_gate_cors_allow_null_origin(self):
        """
        Gets the cloud_gate_cors_allow_null_origin of this SettingsCloudGateCorsSettings.
        Allow Null Origin (CORS) for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The cloud_gate_cors_allow_null_origin of this SettingsCloudGateCorsSettings.
        :rtype: bool
        """
        return self._cloud_gate_cors_allow_null_origin

    @cloud_gate_cors_allow_null_origin.setter
    def cloud_gate_cors_allow_null_origin(self, cloud_gate_cors_allow_null_origin):
        """
        Sets the cloud_gate_cors_allow_null_origin of this SettingsCloudGateCorsSettings.
        Allow Null Origin (CORS) for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param cloud_gate_cors_allow_null_origin: The cloud_gate_cors_allow_null_origin of this SettingsCloudGateCorsSettings.
        :type: bool
        """
        self._cloud_gate_cors_allow_null_origin = cloud_gate_cors_allow_null_origin

    @property
    def cloud_gate_cors_enabled(self):
        """
        Gets the cloud_gate_cors_enabled of this SettingsCloudGateCorsSettings.
        Enable Cloud Gate Cross-Origin Resource Sharing (CORS) for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The cloud_gate_cors_enabled of this SettingsCloudGateCorsSettings.
        :rtype: bool
        """
        return self._cloud_gate_cors_enabled

    @cloud_gate_cors_enabled.setter
    def cloud_gate_cors_enabled(self, cloud_gate_cors_enabled):
        """
        Sets the cloud_gate_cors_enabled of this SettingsCloudGateCorsSettings.
        Enable Cloud Gate Cross-Origin Resource Sharing (CORS) for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param cloud_gate_cors_enabled: The cloud_gate_cors_enabled of this SettingsCloudGateCorsSettings.
        :type: bool
        """
        self._cloud_gate_cors_enabled = cloud_gate_cors_enabled

    @property
    def cloud_gate_cors_allowed_origins(self):
        """
        Gets the cloud_gate_cors_allowed_origins of this SettingsCloudGateCorsSettings.
        Cloud Gate Allowed Cross-Origin Resource Sharing (CORS) Origins for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The cloud_gate_cors_allowed_origins of this SettingsCloudGateCorsSettings.
        :rtype: list[str]
        """
        return self._cloud_gate_cors_allowed_origins

    @cloud_gate_cors_allowed_origins.setter
    def cloud_gate_cors_allowed_origins(self, cloud_gate_cors_allowed_origins):
        """
        Sets the cloud_gate_cors_allowed_origins of this SettingsCloudGateCorsSettings.
        Cloud Gate Allowed Cross-Origin Resource Sharing (CORS) Origins for this tenant.

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param cloud_gate_cors_allowed_origins: The cloud_gate_cors_allowed_origins of this SettingsCloudGateCorsSettings.
        :type: list[str]
        """
        self._cloud_gate_cors_allowed_origins = cloud_gate_cors_allowed_origins

    @property
    def cloud_gate_cors_max_age(self):
        """
        Gets the cloud_gate_cors_max_age of this SettingsCloudGateCorsSettings.
        Maximum number of seconds a CORS Pre-flight Response may be cached by client.

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The cloud_gate_cors_max_age of this SettingsCloudGateCorsSettings.
        :rtype: int
        """
        return self._cloud_gate_cors_max_age

    @cloud_gate_cors_max_age.setter
    def cloud_gate_cors_max_age(self, cloud_gate_cors_max_age):
        """
        Sets the cloud_gate_cors_max_age of this SettingsCloudGateCorsSettings.
        Maximum number of seconds a CORS Pre-flight Response may be cached by client.

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param cloud_gate_cors_max_age: The cloud_gate_cors_max_age of this SettingsCloudGateCorsSettings.
        :type: int
        """
        self._cloud_gate_cors_max_age = cloud_gate_cors_max_age

    @property
    def cloud_gate_cors_exposed_headers(self):
        """
        Gets the cloud_gate_cors_exposed_headers of this SettingsCloudGateCorsSettings.
        List of Response Headers Cloud Gate is allowed to expose in the CORS Response Header: Access-Control-Expose-Headers.

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The cloud_gate_cors_exposed_headers of this SettingsCloudGateCorsSettings.
        :rtype: list[str]
        """
        return self._cloud_gate_cors_exposed_headers

    @cloud_gate_cors_exposed_headers.setter
    def cloud_gate_cors_exposed_headers(self, cloud_gate_cors_exposed_headers):
        """
        Sets the cloud_gate_cors_exposed_headers of this SettingsCloudGateCorsSettings.
        List of Response Headers Cloud Gate is allowed to expose in the CORS Response Header: Access-Control-Expose-Headers.

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param cloud_gate_cors_exposed_headers: The cloud_gate_cors_exposed_headers of this SettingsCloudGateCorsSettings.
        :type: list[str]
        """
        self._cloud_gate_cors_exposed_headers = cloud_gate_cors_exposed_headers

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
