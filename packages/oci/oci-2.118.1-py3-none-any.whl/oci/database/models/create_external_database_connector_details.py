# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateExternalDatabaseConnectorDetails(object):
    """
    Details for creating an external database connector resource.
    """

    #: A constant which can be used with the connector_type property of a CreateExternalDatabaseConnectorDetails.
    #: This constant has a value of "MACS"
    CONNECTOR_TYPE_MACS = "MACS"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateExternalDatabaseConnectorDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database.models.CreateExternalMacsConnectorDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateExternalDatabaseConnectorDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateExternalDatabaseConnectorDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this CreateExternalDatabaseConnectorDetails.
        :type display_name: str

        :param connector_type:
            The value to assign to the connector_type property of this CreateExternalDatabaseConnectorDetails.
            Allowed values for this property are: "MACS"
        :type connector_type: str

        :param external_database_id:
            The value to assign to the external_database_id property of this CreateExternalDatabaseConnectorDetails.
        :type external_database_id: str

        """
        self.swagger_types = {
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'connector_type': 'str',
            'external_database_id': 'str'
        }

        self.attribute_map = {
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'connector_type': 'connectorType',
            'external_database_id': 'externalDatabaseId'
        }

        self._freeform_tags = None
        self._defined_tags = None
        self._display_name = None
        self._connector_type = None
        self._external_database_id = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['connectorType']

        if type == 'MACS':
            return 'CreateExternalMacsConnectorDetails'
        else:
            return 'CreateExternalDatabaseConnectorDetails'

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateExternalDatabaseConnectorDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateExternalDatabaseConnectorDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateExternalDatabaseConnectorDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateExternalDatabaseConnectorDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateExternalDatabaseConnectorDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateExternalDatabaseConnectorDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateExternalDatabaseConnectorDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateExternalDatabaseConnectorDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateExternalDatabaseConnectorDetails.
        The user-friendly name for the
        :func:`create_external_database_connector_details`.
        The name does not have to be unique.


        :return: The display_name of this CreateExternalDatabaseConnectorDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateExternalDatabaseConnectorDetails.
        The user-friendly name for the
        :func:`create_external_database_connector_details`.
        The name does not have to be unique.


        :param display_name: The display_name of this CreateExternalDatabaseConnectorDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def connector_type(self):
        """
        Gets the connector_type of this CreateExternalDatabaseConnectorDetails.
        The type of connector used by the external database resource.

        Allowed values for this property are: "MACS"


        :return: The connector_type of this CreateExternalDatabaseConnectorDetails.
        :rtype: str
        """
        return self._connector_type

    @connector_type.setter
    def connector_type(self, connector_type):
        """
        Sets the connector_type of this CreateExternalDatabaseConnectorDetails.
        The type of connector used by the external database resource.


        :param connector_type: The connector_type of this CreateExternalDatabaseConnectorDetails.
        :type: str
        """
        allowed_values = ["MACS"]
        if not value_allowed_none_or_none_sentinel(connector_type, allowed_values):
            raise ValueError(
                f"Invalid value for `connector_type`, must be None or one of {allowed_values}"
            )
        self._connector_type = connector_type

    @property
    def external_database_id(self):
        """
        **[Required]** Gets the external_database_id of this CreateExternalDatabaseConnectorDetails.
        The `OCID`__ of the external database resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_database_id of this CreateExternalDatabaseConnectorDetails.
        :rtype: str
        """
        return self._external_database_id

    @external_database_id.setter
    def external_database_id(self, external_database_id):
        """
        Sets the external_database_id of this CreateExternalDatabaseConnectorDetails.
        The `OCID`__ of the external database resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_database_id: The external_database_id of this CreateExternalDatabaseConnectorDetails.
        :type: str
        """
        self._external_database_id = external_database_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
