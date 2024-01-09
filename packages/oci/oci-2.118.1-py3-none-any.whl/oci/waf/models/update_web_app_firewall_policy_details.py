# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210930


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateWebAppFirewallPolicyDetails(object):
    """
    The information to be updated.
    When updating WebAppFirewallPolicy, shallow merge is used for all top-level fields,
    meaning that top-level fields with defined values are completely overwritten and
    top-level fields without defined values are unchanged.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateWebAppFirewallPolicyDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateWebAppFirewallPolicyDetails.
        :type display_name: str

        :param actions:
            The value to assign to the actions property of this UpdateWebAppFirewallPolicyDetails.
        :type actions: list[oci.waf.models.Action]

        :param request_access_control:
            The value to assign to the request_access_control property of this UpdateWebAppFirewallPolicyDetails.
        :type request_access_control: oci.waf.models.RequestAccessControl

        :param request_rate_limiting:
            The value to assign to the request_rate_limiting property of this UpdateWebAppFirewallPolicyDetails.
        :type request_rate_limiting: oci.waf.models.RequestRateLimiting

        :param request_protection:
            The value to assign to the request_protection property of this UpdateWebAppFirewallPolicyDetails.
        :type request_protection: oci.waf.models.RequestProtection

        :param response_access_control:
            The value to assign to the response_access_control property of this UpdateWebAppFirewallPolicyDetails.
        :type response_access_control: oci.waf.models.ResponseAccessControl

        :param response_protection:
            The value to assign to the response_protection property of this UpdateWebAppFirewallPolicyDetails.
        :type response_protection: oci.waf.models.ResponseProtection

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateWebAppFirewallPolicyDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateWebAppFirewallPolicyDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this UpdateWebAppFirewallPolicyDetails.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'actions': 'list[Action]',
            'request_access_control': 'RequestAccessControl',
            'request_rate_limiting': 'RequestRateLimiting',
            'request_protection': 'RequestProtection',
            'response_access_control': 'ResponseAccessControl',
            'response_protection': 'ResponseProtection',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'actions': 'actions',
            'request_access_control': 'requestAccessControl',
            'request_rate_limiting': 'requestRateLimiting',
            'request_protection': 'requestProtection',
            'response_access_control': 'responseAccessControl',
            'response_protection': 'responseProtection',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._display_name = None
        self._actions = None
        self._request_access_control = None
        self._request_rate_limiting = None
        self._request_protection = None
        self._response_access_control = None
        self._response_protection = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateWebAppFirewallPolicyDetails.
        WebAppFirewallPolicy display name, can be renamed.


        :return: The display_name of this UpdateWebAppFirewallPolicyDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateWebAppFirewallPolicyDetails.
        WebAppFirewallPolicy display name, can be renamed.


        :param display_name: The display_name of this UpdateWebAppFirewallPolicyDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def actions(self):
        """
        Gets the actions of this UpdateWebAppFirewallPolicyDetails.
        Predefined actions for use in multiple different rules. Not all actions are supported in every module.
        Some actions terminate further execution of modules and rules in a module and some do not.
        Actions names must be unique within this array.


        :return: The actions of this UpdateWebAppFirewallPolicyDetails.
        :rtype: list[oci.waf.models.Action]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this UpdateWebAppFirewallPolicyDetails.
        Predefined actions for use in multiple different rules. Not all actions are supported in every module.
        Some actions terminate further execution of modules and rules in a module and some do not.
        Actions names must be unique within this array.


        :param actions: The actions of this UpdateWebAppFirewallPolicyDetails.
        :type: list[oci.waf.models.Action]
        """
        self._actions = actions

    @property
    def request_access_control(self):
        """
        Gets the request_access_control of this UpdateWebAppFirewallPolicyDetails.

        :return: The request_access_control of this UpdateWebAppFirewallPolicyDetails.
        :rtype: oci.waf.models.RequestAccessControl
        """
        return self._request_access_control

    @request_access_control.setter
    def request_access_control(self, request_access_control):
        """
        Sets the request_access_control of this UpdateWebAppFirewallPolicyDetails.

        :param request_access_control: The request_access_control of this UpdateWebAppFirewallPolicyDetails.
        :type: oci.waf.models.RequestAccessControl
        """
        self._request_access_control = request_access_control

    @property
    def request_rate_limiting(self):
        """
        Gets the request_rate_limiting of this UpdateWebAppFirewallPolicyDetails.

        :return: The request_rate_limiting of this UpdateWebAppFirewallPolicyDetails.
        :rtype: oci.waf.models.RequestRateLimiting
        """
        return self._request_rate_limiting

    @request_rate_limiting.setter
    def request_rate_limiting(self, request_rate_limiting):
        """
        Sets the request_rate_limiting of this UpdateWebAppFirewallPolicyDetails.

        :param request_rate_limiting: The request_rate_limiting of this UpdateWebAppFirewallPolicyDetails.
        :type: oci.waf.models.RequestRateLimiting
        """
        self._request_rate_limiting = request_rate_limiting

    @property
    def request_protection(self):
        """
        Gets the request_protection of this UpdateWebAppFirewallPolicyDetails.

        :return: The request_protection of this UpdateWebAppFirewallPolicyDetails.
        :rtype: oci.waf.models.RequestProtection
        """
        return self._request_protection

    @request_protection.setter
    def request_protection(self, request_protection):
        """
        Sets the request_protection of this UpdateWebAppFirewallPolicyDetails.

        :param request_protection: The request_protection of this UpdateWebAppFirewallPolicyDetails.
        :type: oci.waf.models.RequestProtection
        """
        self._request_protection = request_protection

    @property
    def response_access_control(self):
        """
        Gets the response_access_control of this UpdateWebAppFirewallPolicyDetails.

        :return: The response_access_control of this UpdateWebAppFirewallPolicyDetails.
        :rtype: oci.waf.models.ResponseAccessControl
        """
        return self._response_access_control

    @response_access_control.setter
    def response_access_control(self, response_access_control):
        """
        Sets the response_access_control of this UpdateWebAppFirewallPolicyDetails.

        :param response_access_control: The response_access_control of this UpdateWebAppFirewallPolicyDetails.
        :type: oci.waf.models.ResponseAccessControl
        """
        self._response_access_control = response_access_control

    @property
    def response_protection(self):
        """
        Gets the response_protection of this UpdateWebAppFirewallPolicyDetails.

        :return: The response_protection of this UpdateWebAppFirewallPolicyDetails.
        :rtype: oci.waf.models.ResponseProtection
        """
        return self._response_protection

    @response_protection.setter
    def response_protection(self, response_protection):
        """
        Sets the response_protection of this UpdateWebAppFirewallPolicyDetails.

        :param response_protection: The response_protection of this UpdateWebAppFirewallPolicyDetails.
        :type: oci.waf.models.ResponseProtection
        """
        self._response_protection = response_protection

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateWebAppFirewallPolicyDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateWebAppFirewallPolicyDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateWebAppFirewallPolicyDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateWebAppFirewallPolicyDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateWebAppFirewallPolicyDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateWebAppFirewallPolicyDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateWebAppFirewallPolicyDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateWebAppFirewallPolicyDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this UpdateWebAppFirewallPolicyDetails.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this UpdateWebAppFirewallPolicyDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this UpdateWebAppFirewallPolicyDetails.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this UpdateWebAppFirewallPolicyDetails.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
