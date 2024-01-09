# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: v1


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SelfRegistrationProfileUserAttributes(object):
    """
    User Attributes
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SelfRegistrationProfileUserAttributes object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this SelfRegistrationProfileUserAttributes.
        :type value: str

        :param fully_qualified_attribute_name:
            The value to assign to the fully_qualified_attribute_name property of this SelfRegistrationProfileUserAttributes.
        :type fully_qualified_attribute_name: str

        :param seq_number:
            The value to assign to the seq_number property of this SelfRegistrationProfileUserAttributes.
        :type seq_number: int

        :param deletable:
            The value to assign to the deletable property of this SelfRegistrationProfileUserAttributes.
        :type deletable: bool

        :param metadata:
            The value to assign to the metadata property of this SelfRegistrationProfileUserAttributes.
        :type metadata: str

        """
        self.swagger_types = {
            'value': 'str',
            'fully_qualified_attribute_name': 'str',
            'seq_number': 'int',
            'deletable': 'bool',
            'metadata': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'fully_qualified_attribute_name': 'fullyQualifiedAttributeName',
            'seq_number': 'seqNumber',
            'deletable': 'deletable',
            'metadata': 'metadata'
        }

        self._value = None
        self._fully_qualified_attribute_name = None
        self._seq_number = None
        self._deletable = None
        self._metadata = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this SelfRegistrationProfileUserAttributes.
        name of the attribute

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this SelfRegistrationProfileUserAttributes.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this SelfRegistrationProfileUserAttributes.
        name of the attribute

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this SelfRegistrationProfileUserAttributes.
        :type: str
        """
        self._value = value

    @property
    def fully_qualified_attribute_name(self):
        """
        Gets the fully_qualified_attribute_name of this SelfRegistrationProfileUserAttributes.
        **SCIM++ Properties:**
        - idcsSearchable: true
        - multiValued: false
        - mutability: readWrite
        - required: false
        - returned: default
        - type: string
        - uniqueness: none
        Fully Qualified Attribute Name


        :return: The fully_qualified_attribute_name of this SelfRegistrationProfileUserAttributes.
        :rtype: str
        """
        return self._fully_qualified_attribute_name

    @fully_qualified_attribute_name.setter
    def fully_qualified_attribute_name(self, fully_qualified_attribute_name):
        """
        Sets the fully_qualified_attribute_name of this SelfRegistrationProfileUserAttributes.
        **SCIM++ Properties:**
        - idcsSearchable: true
        - multiValued: false
        - mutability: readWrite
        - required: false
        - returned: default
        - type: string
        - uniqueness: none
        Fully Qualified Attribute Name


        :param fully_qualified_attribute_name: The fully_qualified_attribute_name of this SelfRegistrationProfileUserAttributes.
        :type: str
        """
        self._fully_qualified_attribute_name = fully_qualified_attribute_name

    @property
    def seq_number(self):
        """
        **[Required]** Gets the seq_number of this SelfRegistrationProfileUserAttributes.
        **SCIM++ Properties:**
        - idcsSearchable: true
        - multiValued: false
        - mutability: readWrite
        - required: true
        - returned: default
        - type: integer
        - uniqueness: none
        Sequence Number for the attribute


        :return: The seq_number of this SelfRegistrationProfileUserAttributes.
        :rtype: int
        """
        return self._seq_number

    @seq_number.setter
    def seq_number(self, seq_number):
        """
        Sets the seq_number of this SelfRegistrationProfileUserAttributes.
        **SCIM++ Properties:**
        - idcsSearchable: true
        - multiValued: false
        - mutability: readWrite
        - required: true
        - returned: default
        - type: integer
        - uniqueness: none
        Sequence Number for the attribute


        :param seq_number: The seq_number of this SelfRegistrationProfileUserAttributes.
        :type: int
        """
        self._seq_number = seq_number

    @property
    def deletable(self):
        """
        Gets the deletable of this SelfRegistrationProfileUserAttributes.
        If this attribute can be deleted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The deletable of this SelfRegistrationProfileUserAttributes.
        :rtype: bool
        """
        return self._deletable

    @deletable.setter
    def deletable(self, deletable):
        """
        Sets the deletable of this SelfRegistrationProfileUserAttributes.
        If this attribute can be deleted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param deletable: The deletable of this SelfRegistrationProfileUserAttributes.
        :type: bool
        """
        self._deletable = deletable

    @property
    def metadata(self):
        """
        Gets the metadata of this SelfRegistrationProfileUserAttributes.
        Metadata of the user attribute

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The metadata of this SelfRegistrationProfileUserAttributes.
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this SelfRegistrationProfileUserAttributes.
        Metadata of the user attribute

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param metadata: The metadata of this SelfRegistrationProfileUserAttributes.
        :type: str
        """
        self._metadata = metadata

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
