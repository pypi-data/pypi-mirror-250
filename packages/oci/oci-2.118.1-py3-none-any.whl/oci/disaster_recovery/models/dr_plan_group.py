# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220125


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DrPlanGroup(object):
    """
    Details of a group in a DR plan.
    """

    #: A constant which can be used with the type property of a DrPlanGroup.
    #: This constant has a value of "USER_DEFINED"
    TYPE_USER_DEFINED = "USER_DEFINED"

    #: A constant which can be used with the type property of a DrPlanGroup.
    #: This constant has a value of "BUILT_IN"
    TYPE_BUILT_IN = "BUILT_IN"

    #: A constant which can be used with the type property of a DrPlanGroup.
    #: This constant has a value of "BUILT_IN_PRECHECK"
    TYPE_BUILT_IN_PRECHECK = "BUILT_IN_PRECHECK"

    def __init__(self, **kwargs):
        """
        Initializes a new DrPlanGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DrPlanGroup.
        :type id: str

        :param type:
            The value to assign to the type property of this DrPlanGroup.
            Allowed values for this property are: "USER_DEFINED", "BUILT_IN", "BUILT_IN_PRECHECK", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param display_name:
            The value to assign to the display_name property of this DrPlanGroup.
        :type display_name: str

        :param steps:
            The value to assign to the steps property of this DrPlanGroup.
        :type steps: list[oci.disaster_recovery.models.DrPlanStep]

        """
        self.swagger_types = {
            'id': 'str',
            'type': 'str',
            'display_name': 'str',
            'steps': 'list[DrPlanStep]'
        }

        self.attribute_map = {
            'id': 'id',
            'type': 'type',
            'display_name': 'displayName',
            'steps': 'steps'
        }

        self._id = None
        self._type = None
        self._display_name = None
        self._steps = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DrPlanGroup.
        The unique id of the group. Must not be modified by user.

        Example: `sgid1.group..uniqueID`


        :return: The id of this DrPlanGroup.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DrPlanGroup.
        The unique id of the group. Must not be modified by user.

        Example: `sgid1.group..uniqueID`


        :param id: The id of this DrPlanGroup.
        :type: str
        """
        self._id = id

    @property
    def type(self):
        """
        **[Required]** Gets the type of this DrPlanGroup.
        The group type.

        Example: `BUILT_IN`

        Allowed values for this property are: "USER_DEFINED", "BUILT_IN", "BUILT_IN_PRECHECK", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this DrPlanGroup.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this DrPlanGroup.
        The group type.

        Example: `BUILT_IN`


        :param type: The type of this DrPlanGroup.
        :type: str
        """
        allowed_values = ["USER_DEFINED", "BUILT_IN", "BUILT_IN_PRECHECK"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DrPlanGroup.
        The display name of the group.

        Example: `DATABASE_SWITCHOVER`


        :return: The display_name of this DrPlanGroup.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DrPlanGroup.
        The display name of the group.

        Example: `DATABASE_SWITCHOVER`


        :param display_name: The display_name of this DrPlanGroup.
        :type: str
        """
        self._display_name = display_name

    @property
    def steps(self):
        """
        **[Required]** Gets the steps of this DrPlanGroup.
        The list of steps in the group.


        :return: The steps of this DrPlanGroup.
        :rtype: list[oci.disaster_recovery.models.DrPlanStep]
        """
        return self._steps

    @steps.setter
    def steps(self, steps):
        """
        Sets the steps of this DrPlanGroup.
        The list of steps in the group.


        :param steps: The steps of this DrPlanGroup.
        :type: list[oci.disaster_recovery.models.DrPlanStep]
        """
        self._steps = steps

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
