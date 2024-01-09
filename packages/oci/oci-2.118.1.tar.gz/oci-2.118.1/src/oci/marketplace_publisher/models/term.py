# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Term(object):
    """
    Base model object for the term.
    """

    #: A constant which can be used with the author property of a Term.
    #: This constant has a value of "ORACLE"
    AUTHOR_ORACLE = "ORACLE"

    #: A constant which can be used with the author property of a Term.
    #: This constant has a value of "PARTNER"
    AUTHOR_PARTNER = "PARTNER"

    #: A constant which can be used with the lifecycle_state property of a Term.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Term.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    def __init__(self, **kwargs):
        """
        Initializes a new Term object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Term.
        :type id: str

        :param name:
            The value to assign to the name property of this Term.
        :type name: str

        :param author:
            The value to assign to the author property of this Term.
            Allowed values for this property are: "ORACLE", "PARTNER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type author: str

        :param compartment_id:
            The value to assign to the compartment_id property of this Term.
        :type compartment_id: str

        :param publisher_id:
            The value to assign to the publisher_id property of this Term.
        :type publisher_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Term.
            Allowed values for this property are: "ACTIVE", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this Term.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this Term.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Term.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Term.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this Term.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'author': 'str',
            'compartment_id': 'str',
            'publisher_id': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'author': 'author',
            'compartment_id': 'compartmentId',
            'publisher_id': 'publisherId',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._name = None
        self._author = None
        self._compartment_id = None
        self._publisher_id = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        Gets the id of this Term.
        Unique OCID identifier for the term.


        :return: The id of this Term.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Term.
        Unique OCID identifier for the term.


        :param id: The id of this Term.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this Term.
        The name for the term.


        :return: The name of this Term.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Term.
        The name for the term.


        :param name: The name of this Term.
        :type: str
        """
        self._name = name

    @property
    def author(self):
        """
        **[Required]** Gets the author of this Term.
        Who authored the term. Publisher terms will be defaulted to 'PARTNER'.

        Allowed values for this property are: "ORACLE", "PARTNER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The author of this Term.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """
        Sets the author of this Term.
        Who authored the term. Publisher terms will be defaulted to 'PARTNER'.


        :param author: The author of this Term.
        :type: str
        """
        allowed_values = ["ORACLE", "PARTNER"]
        if not value_allowed_none_or_none_sentinel(author, allowed_values):
            author = 'UNKNOWN_ENUM_VALUE'
        self._author = author

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this Term.
        The unique identifier for the compartment.


        :return: The compartment_id of this Term.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this Term.
        The unique identifier for the compartment.


        :param compartment_id: The compartment_id of this Term.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def publisher_id(self):
        """
        **[Required]** Gets the publisher_id of this Term.
        The unique identifier for the publisher.


        :return: The publisher_id of this Term.
        :rtype: str
        """
        return self._publisher_id

    @publisher_id.setter
    def publisher_id(self, publisher_id):
        """
        Sets the publisher_id of this Term.
        The unique identifier for the publisher.


        :param publisher_id: The publisher_id of this Term.
        :type: str
        """
        self._publisher_id = publisher_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this Term.
        The current state for the Term.

        Allowed values for this property are: "ACTIVE", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Term.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Term.
        The current state for the Term.


        :param lifecycle_state: The lifecycle_state of this Term.
        :type: str
        """
        allowed_values = ["ACTIVE", "INACTIVE"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this Term.
        The date and time the term was created, in the format defined by `RFC3339`__.

        Example: `2022-09-15T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this Term.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Term.
        The date and time the term was created, in the format defined by `RFC3339`__.

        Example: `2022-09-15T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this Term.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this Term.
        The date and time the term was updated, in the format defined by `RFC3339`__.

        Example: `2022-09-15T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this Term.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this Term.
        The date and time the term was updated, in the format defined by `RFC3339`__.

        Example: `2022-09-15T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this Term.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Term.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this Term.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Term.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this Term.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Term.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this Term.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Term.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this Term.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this Term.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this Term.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this Term.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this Term.
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
