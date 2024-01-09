# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20181201


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecurityPolicyDeployment(object):
    """
    The resource represents the state of the deployment of a security policy on a target.
    """

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "DEPLOYED"
    LIFECYCLE_STATE_DEPLOYED = "DEPLOYED"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a SecurityPolicyDeployment.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new SecurityPolicyDeployment object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this SecurityPolicyDeployment.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this SecurityPolicyDeployment.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this SecurityPolicyDeployment.
        :type display_name: str

        :param description:
            The value to assign to the description property of this SecurityPolicyDeployment.
        :type description: str

        :param target_id:
            The value to assign to the target_id property of this SecurityPolicyDeployment.
        :type target_id: str

        :param security_policy_id:
            The value to assign to the security_policy_id property of this SecurityPolicyDeployment.
        :type security_policy_id: str

        :param time_created:
            The value to assign to the time_created property of this SecurityPolicyDeployment.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this SecurityPolicyDeployment.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this SecurityPolicyDeployment.
            Allowed values for this property are: "CREATING", "UPDATING", "DEPLOYED", "NEEDS_ATTENTION", "FAILED", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this SecurityPolicyDeployment.
        :type lifecycle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this SecurityPolicyDeployment.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this SecurityPolicyDeployment.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this SecurityPolicyDeployment.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'target_id': 'str',
            'security_policy_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'target_id': 'targetId',
            'security_policy_id': 'securityPolicyId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._target_id = None
        self._security_policy_id = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this SecurityPolicyDeployment.
        The OCID of the security policy deployment.


        :return: The id of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SecurityPolicyDeployment.
        The OCID of the security policy deployment.


        :param id: The id of this SecurityPolicyDeployment.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this SecurityPolicyDeployment.
        The OCID of the compartment containing the security policy deployment.


        :return: The compartment_id of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this SecurityPolicyDeployment.
        The OCID of the compartment containing the security policy deployment.


        :param compartment_id: The compartment_id of this SecurityPolicyDeployment.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this SecurityPolicyDeployment.
        The display name of the security policy deployment.


        :return: The display_name of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this SecurityPolicyDeployment.
        The display name of the security policy deployment.


        :param display_name: The display_name of this SecurityPolicyDeployment.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this SecurityPolicyDeployment.
        The description of the security policy deployment.


        :return: The description of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SecurityPolicyDeployment.
        The description of the security policy deployment.


        :param description: The description of this SecurityPolicyDeployment.
        :type: str
        """
        self._description = description

    @property
    def target_id(self):
        """
        **[Required]** Gets the target_id of this SecurityPolicyDeployment.
        The OCID of the target where the security policy is deployed.


        :return: The target_id of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this SecurityPolicyDeployment.
        The OCID of the target where the security policy is deployed.


        :param target_id: The target_id of this SecurityPolicyDeployment.
        :type: str
        """
        self._target_id = target_id

    @property
    def security_policy_id(self):
        """
        **[Required]** Gets the security_policy_id of this SecurityPolicyDeployment.
        The OCID of the security policy corresponding to the security policy deployment.


        :return: The security_policy_id of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._security_policy_id

    @security_policy_id.setter
    def security_policy_id(self, security_policy_id):
        """
        Sets the security_policy_id of this SecurityPolicyDeployment.
        The OCID of the security policy corresponding to the security policy deployment.


        :param security_policy_id: The security_policy_id of this SecurityPolicyDeployment.
        :type: str
        """
        self._security_policy_id = security_policy_id

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this SecurityPolicyDeployment.
        The time that the security policy deployment was created, in the format defined by RFC3339.


        :return: The time_created of this SecurityPolicyDeployment.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this SecurityPolicyDeployment.
        The time that the security policy deployment was created, in the format defined by RFC3339.


        :param time_created: The time_created of this SecurityPolicyDeployment.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this SecurityPolicyDeployment.
        The last date and time the security policy deployment was updated, in the format defined by RFC3339.


        :return: The time_updated of this SecurityPolicyDeployment.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this SecurityPolicyDeployment.
        The last date and time the security policy deployment was updated, in the format defined by RFC3339.


        :param time_updated: The time_updated of this SecurityPolicyDeployment.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this SecurityPolicyDeployment.
        The current state of the security policy deployment.

        Allowed values for this property are: "CREATING", "UPDATING", "DEPLOYED", "NEEDS_ATTENTION", "FAILED", "DELETING", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this SecurityPolicyDeployment.
        The current state of the security policy deployment.


        :param lifecycle_state: The lifecycle_state of this SecurityPolicyDeployment.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "DEPLOYED", "NEEDS_ATTENTION", "FAILED", "DELETING", "DELETED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this SecurityPolicyDeployment.
        Details about the current state of the security policy deployment in Data Safe.


        :return: The lifecycle_details of this SecurityPolicyDeployment.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this SecurityPolicyDeployment.
        Details about the current state of the security policy deployment in Data Safe.


        :param lifecycle_details: The lifecycle_details of this SecurityPolicyDeployment.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this SecurityPolicyDeployment.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this SecurityPolicyDeployment.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this SecurityPolicyDeployment.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this SecurityPolicyDeployment.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this SecurityPolicyDeployment.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this SecurityPolicyDeployment.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this SecurityPolicyDeployment.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this SecurityPolicyDeployment.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this SecurityPolicyDeployment.
        System tags for this resource. Each key is predefined and scoped to a namespace. For more information, see Resource Tags.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this SecurityPolicyDeployment.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this SecurityPolicyDeployment.
        System tags for this resource. Each key is predefined and scoped to a namespace. For more information, see Resource Tags.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this SecurityPolicyDeployment.
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
