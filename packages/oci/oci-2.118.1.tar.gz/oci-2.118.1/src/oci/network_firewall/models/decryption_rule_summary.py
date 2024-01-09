# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20230501


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DecryptionRuleSummary(object):
    """
    Summary for Decryption Rule used in the firewall policy rules.
    A Decryption Rule is used to define which traffic should be decrypted by the firewall, and how it should do so.
    """

    #: A constant which can be used with the action property of a DecryptionRuleSummary.
    #: This constant has a value of "NO_DECRYPT"
    ACTION_NO_DECRYPT = "NO_DECRYPT"

    #: A constant which can be used with the action property of a DecryptionRuleSummary.
    #: This constant has a value of "DECRYPT"
    ACTION_DECRYPT = "DECRYPT"

    def __init__(self, **kwargs):
        """
        Initializes a new DecryptionRuleSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this DecryptionRuleSummary.
        :type name: str

        :param action:
            The value to assign to the action property of this DecryptionRuleSummary.
            Allowed values for this property are: "NO_DECRYPT", "DECRYPT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action: str

        :param decryption_profile:
            The value to assign to the decryption_profile property of this DecryptionRuleSummary.
        :type decryption_profile: str

        :param secret:
            The value to assign to the secret property of this DecryptionRuleSummary.
        :type secret: str

        :param priority_order:
            The value to assign to the priority_order property of this DecryptionRuleSummary.
        :type priority_order: int

        :param parent_resource_id:
            The value to assign to the parent_resource_id property of this DecryptionRuleSummary.
        :type parent_resource_id: str

        """
        self.swagger_types = {
            'name': 'str',
            'action': 'str',
            'decryption_profile': 'str',
            'secret': 'str',
            'priority_order': 'int',
            'parent_resource_id': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'action': 'action',
            'decryption_profile': 'decryptionProfile',
            'secret': 'secret',
            'priority_order': 'priorityOrder',
            'parent_resource_id': 'parentResourceId'
        }

        self._name = None
        self._action = None
        self._decryption_profile = None
        self._secret = None
        self._priority_order = None
        self._parent_resource_id = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this DecryptionRuleSummary.
        Name for the decryption rule, must be unique within the policy.


        :return: The name of this DecryptionRuleSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DecryptionRuleSummary.
        Name for the decryption rule, must be unique within the policy.


        :param name: The name of this DecryptionRuleSummary.
        :type: str
        """
        self._name = name

    @property
    def action(self):
        """
        **[Required]** Gets the action of this DecryptionRuleSummary.
        Action:

        * NO_DECRYPT - Matching traffic is not decrypted.
        * DECRYPT - Matching traffic is decrypted with the specified `secret` according to the specified `decryptionProfile`.

        Allowed values for this property are: "NO_DECRYPT", "DECRYPT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action of this DecryptionRuleSummary.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this DecryptionRuleSummary.
        Action:

        * NO_DECRYPT - Matching traffic is not decrypted.
        * DECRYPT - Matching traffic is decrypted with the specified `secret` according to the specified `decryptionProfile`.


        :param action: The action of this DecryptionRuleSummary.
        :type: str
        """
        allowed_values = ["NO_DECRYPT", "DECRYPT"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            action = 'UNKNOWN_ENUM_VALUE'
        self._action = action

    @property
    def decryption_profile(self):
        """
        **[Required]** Gets the decryption_profile of this DecryptionRuleSummary.
        The name of the decryption profile to use.


        :return: The decryption_profile of this DecryptionRuleSummary.
        :rtype: str
        """
        return self._decryption_profile

    @decryption_profile.setter
    def decryption_profile(self, decryption_profile):
        """
        Sets the decryption_profile of this DecryptionRuleSummary.
        The name of the decryption profile to use.


        :param decryption_profile: The decryption_profile of this DecryptionRuleSummary.
        :type: str
        """
        self._decryption_profile = decryption_profile

    @property
    def secret(self):
        """
        **[Required]** Gets the secret of this DecryptionRuleSummary.
        The name of a mapped secret. Its `type` must match that of the specified decryption profile.


        :return: The secret of this DecryptionRuleSummary.
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """
        Sets the secret of this DecryptionRuleSummary.
        The name of a mapped secret. Its `type` must match that of the specified decryption profile.


        :param secret: The secret of this DecryptionRuleSummary.
        :type: str
        """
        self._secret = secret

    @property
    def priority_order(self):
        """
        **[Required]** Gets the priority_order of this DecryptionRuleSummary.
        The priority order in which this rule should be evaluated.


        :return: The priority_order of this DecryptionRuleSummary.
        :rtype: int
        """
        return self._priority_order

    @priority_order.setter
    def priority_order(self, priority_order):
        """
        Sets the priority_order of this DecryptionRuleSummary.
        The priority order in which this rule should be evaluated.


        :param priority_order: The priority_order of this DecryptionRuleSummary.
        :type: int
        """
        self._priority_order = priority_order

    @property
    def parent_resource_id(self):
        """
        **[Required]** Gets the parent_resource_id of this DecryptionRuleSummary.
        OCID of the Network Firewall Policy this application belongs to.


        :return: The parent_resource_id of this DecryptionRuleSummary.
        :rtype: str
        """
        return self._parent_resource_id

    @parent_resource_id.setter
    def parent_resource_id(self, parent_resource_id):
        """
        Sets the parent_resource_id of this DecryptionRuleSummary.
        OCID of the Network Firewall Policy this application belongs to.


        :param parent_resource_id: The parent_resource_id of this DecryptionRuleSummary.
        :type: str
        """
        self._parent_resource_id = parent_resource_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
