# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20181201


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecurityPolicyEntryState(object):
    """
    The resource represents the state of a specific entry type deployment on a target.
    """

    #: A constant which can be used with the deployment_status property of a SecurityPolicyEntryState.
    #: This constant has a value of "CREATED"
    DEPLOYMENT_STATUS_CREATED = "CREATED"

    #: A constant which can be used with the deployment_status property of a SecurityPolicyEntryState.
    #: This constant has a value of "MODIFIED"
    DEPLOYMENT_STATUS_MODIFIED = "MODIFIED"

    #: A constant which can be used with the deployment_status property of a SecurityPolicyEntryState.
    #: This constant has a value of "CONFLICT"
    DEPLOYMENT_STATUS_CONFLICT = "CONFLICT"

    #: A constant which can be used with the deployment_status property of a SecurityPolicyEntryState.
    #: This constant has a value of "UNAUTHORIZED"
    DEPLOYMENT_STATUS_UNAUTHORIZED = "UNAUTHORIZED"

    #: A constant which can be used with the deployment_status property of a SecurityPolicyEntryState.
    #: This constant has a value of "DELETED"
    DEPLOYMENT_STATUS_DELETED = "DELETED"

    def __init__(self, **kwargs):
        """
        Initializes a new SecurityPolicyEntryState object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this SecurityPolicyEntryState.
        :type id: str

        :param security_policy_entry_id:
            The value to assign to the security_policy_entry_id property of this SecurityPolicyEntryState.
        :type security_policy_entry_id: str

        :param security_policy_deployment_id:
            The value to assign to the security_policy_deployment_id property of this SecurityPolicyEntryState.
        :type security_policy_deployment_id: str

        :param deployment_status:
            The value to assign to the deployment_status property of this SecurityPolicyEntryState.
            Allowed values for this property are: "CREATED", "MODIFIED", "CONFLICT", "UNAUTHORIZED", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type deployment_status: str

        :param entry_details:
            The value to assign to the entry_details property of this SecurityPolicyEntryState.
        :type entry_details: oci.data_safe.models.EntryDetails

        """
        self.swagger_types = {
            'id': 'str',
            'security_policy_entry_id': 'str',
            'security_policy_deployment_id': 'str',
            'deployment_status': 'str',
            'entry_details': 'EntryDetails'
        }

        self.attribute_map = {
            'id': 'id',
            'security_policy_entry_id': 'securityPolicyEntryId',
            'security_policy_deployment_id': 'securityPolicyDeploymentId',
            'deployment_status': 'deploymentStatus',
            'entry_details': 'entryDetails'
        }

        self._id = None
        self._security_policy_entry_id = None
        self._security_policy_deployment_id = None
        self._deployment_status = None
        self._entry_details = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this SecurityPolicyEntryState.
        Unique id of the security policy entry state.


        :return: The id of this SecurityPolicyEntryState.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SecurityPolicyEntryState.
        Unique id of the security policy entry state.


        :param id: The id of this SecurityPolicyEntryState.
        :type: str
        """
        self._id = id

    @property
    def security_policy_entry_id(self):
        """
        **[Required]** Gets the security_policy_entry_id of this SecurityPolicyEntryState.
        The OCID of the security policy entry type associated.


        :return: The security_policy_entry_id of this SecurityPolicyEntryState.
        :rtype: str
        """
        return self._security_policy_entry_id

    @security_policy_entry_id.setter
    def security_policy_entry_id(self, security_policy_entry_id):
        """
        Sets the security_policy_entry_id of this SecurityPolicyEntryState.
        The OCID of the security policy entry type associated.


        :param security_policy_entry_id: The security_policy_entry_id of this SecurityPolicyEntryState.
        :type: str
        """
        self._security_policy_entry_id = security_policy_entry_id

    @property
    def security_policy_deployment_id(self):
        """
        Gets the security_policy_deployment_id of this SecurityPolicyEntryState.
        The OCID of the security policy deployment associated.


        :return: The security_policy_deployment_id of this SecurityPolicyEntryState.
        :rtype: str
        """
        return self._security_policy_deployment_id

    @security_policy_deployment_id.setter
    def security_policy_deployment_id(self, security_policy_deployment_id):
        """
        Sets the security_policy_deployment_id of this SecurityPolicyEntryState.
        The OCID of the security policy deployment associated.


        :param security_policy_deployment_id: The security_policy_deployment_id of this SecurityPolicyEntryState.
        :type: str
        """
        self._security_policy_deployment_id = security_policy_deployment_id

    @property
    def deployment_status(self):
        """
        **[Required]** Gets the deployment_status of this SecurityPolicyEntryState.
        The current deployment status of the security policy deployment and the security policy entry associated.

        Allowed values for this property are: "CREATED", "MODIFIED", "CONFLICT", "UNAUTHORIZED", "DELETED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The deployment_status of this SecurityPolicyEntryState.
        :rtype: str
        """
        return self._deployment_status

    @deployment_status.setter
    def deployment_status(self, deployment_status):
        """
        Sets the deployment_status of this SecurityPolicyEntryState.
        The current deployment status of the security policy deployment and the security policy entry associated.


        :param deployment_status: The deployment_status of this SecurityPolicyEntryState.
        :type: str
        """
        allowed_values = ["CREATED", "MODIFIED", "CONFLICT", "UNAUTHORIZED", "DELETED"]
        if not value_allowed_none_or_none_sentinel(deployment_status, allowed_values):
            deployment_status = 'UNKNOWN_ENUM_VALUE'
        self._deployment_status = deployment_status

    @property
    def entry_details(self):
        """
        Gets the entry_details of this SecurityPolicyEntryState.

        :return: The entry_details of this SecurityPolicyEntryState.
        :rtype: oci.data_safe.models.EntryDetails
        """
        return self._entry_details

    @entry_details.setter
    def entry_details(self, entry_details):
        """
        Sets the entry_details of this SecurityPolicyEntryState.

        :param entry_details: The entry_details of this SecurityPolicyEntryState.
        :type: oci.data_safe.models.EntryDetails
        """
        self._entry_details = entry_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
