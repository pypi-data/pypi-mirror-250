# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20221208


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateCccInfrastructureDetails(object):
    """
    Updates Compute Cloud@Customer infrastructure configuration details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateCccInfrastructureDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateCccInfrastructureDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateCccInfrastructureDetails.
        :type description: str

        :param subnet_id:
            The value to assign to the subnet_id property of this UpdateCccInfrastructureDetails.
        :type subnet_id: str

        :param connection_state:
            The value to assign to the connection_state property of this UpdateCccInfrastructureDetails.
        :type connection_state: str

        :param connection_details:
            The value to assign to the connection_details property of this UpdateCccInfrastructureDetails.
        :type connection_details: str

        :param ccc_upgrade_schedule_id:
            The value to assign to the ccc_upgrade_schedule_id property of this UpdateCccInfrastructureDetails.
        :type ccc_upgrade_schedule_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateCccInfrastructureDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateCccInfrastructureDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'subnet_id': 'str',
            'connection_state': 'str',
            'connection_details': 'str',
            'ccc_upgrade_schedule_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'subnet_id': 'subnetId',
            'connection_state': 'connectionState',
            'connection_details': 'connectionDetails',
            'ccc_upgrade_schedule_id': 'cccUpgradeScheduleId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._subnet_id = None
        self._connection_state = None
        self._connection_details = None
        self._ccc_upgrade_schedule_id = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateCccInfrastructureDetails.
        The name that will be used to display the Compute Cloud@Customer infrastructure
        in the Oracle Cloud Infrastructure console. Does not have to be unique and can be changed.
        Avoid entering confidential information.


        :return: The display_name of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateCccInfrastructureDetails.
        The name that will be used to display the Compute Cloud@Customer infrastructure
        in the Oracle Cloud Infrastructure console. Does not have to be unique and can be changed.
        Avoid entering confidential information.


        :param display_name: The display_name of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdateCccInfrastructureDetails.
        A mutable client-meaningful text description of the Compute Cloud@Customer infrastructure.
        Avoid entering confidential information.


        :return: The description of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateCccInfrastructureDetails.
        A mutable client-meaningful text description of the Compute Cloud@Customer infrastructure.
        Avoid entering confidential information.


        :param description: The description of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._description = description

    @property
    def subnet_id(self):
        """
        Gets the subnet_id of this UpdateCccInfrastructureDetails.
        `OCID`__ for the network subnet that is
        used to communicate with Compute Cloud@Customer infrastructure.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The subnet_id of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this UpdateCccInfrastructureDetails.
        `OCID`__ for the network subnet that is
        used to communicate with Compute Cloud@Customer infrastructure.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param subnet_id: The subnet_id of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def connection_state(self):
        """
        Gets the connection_state of this UpdateCccInfrastructureDetails.
        An updated connection state of the Compute Cloud@Customer infrastructure.


        :return: The connection_state of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._connection_state

    @connection_state.setter
    def connection_state(self, connection_state):
        """
        Sets the connection_state of this UpdateCccInfrastructureDetails.
        An updated connection state of the Compute Cloud@Customer infrastructure.


        :param connection_state: The connection_state of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._connection_state = connection_state

    @property
    def connection_details(self):
        """
        Gets the connection_details of this UpdateCccInfrastructureDetails.
        A message describing the current connection state in more detail.


        :return: The connection_details of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._connection_details

    @connection_details.setter
    def connection_details(self, connection_details):
        """
        Sets the connection_details of this UpdateCccInfrastructureDetails.
        A message describing the current connection state in more detail.


        :param connection_details: The connection_details of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._connection_details = connection_details

    @property
    def ccc_upgrade_schedule_id(self):
        """
        Gets the ccc_upgrade_schedule_id of this UpdateCccInfrastructureDetails.
        Schedule used for upgrades. If no schedule is associated with the infrastructure,
        it can be updated at any time.


        :return: The ccc_upgrade_schedule_id of this UpdateCccInfrastructureDetails.
        :rtype: str
        """
        return self._ccc_upgrade_schedule_id

    @ccc_upgrade_schedule_id.setter
    def ccc_upgrade_schedule_id(self, ccc_upgrade_schedule_id):
        """
        Sets the ccc_upgrade_schedule_id of this UpdateCccInfrastructureDetails.
        Schedule used for upgrades. If no schedule is associated with the infrastructure,
        it can be updated at any time.


        :param ccc_upgrade_schedule_id: The ccc_upgrade_schedule_id of this UpdateCccInfrastructureDetails.
        :type: str
        """
        self._ccc_upgrade_schedule_id = ccc_upgrade_schedule_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateCccInfrastructureDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateCccInfrastructureDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateCccInfrastructureDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateCccInfrastructureDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateCccInfrastructureDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateCccInfrastructureDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateCccInfrastructureDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateCccInfrastructureDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
