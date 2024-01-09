# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200430


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateExternalPublicationDetails(object):
    """
    Properties used to publish an Oracle Cloud Infrastructure Data Flow object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateExternalPublicationDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param application_id:
            The value to assign to the application_id property of this CreateExternalPublicationDetails.
        :type application_id: str

        :param application_compartment_id:
            The value to assign to the application_compartment_id property of this CreateExternalPublicationDetails.
        :type application_compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateExternalPublicationDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateExternalPublicationDetails.
        :type description: str

        :param resource_configuration:
            The value to assign to the resource_configuration property of this CreateExternalPublicationDetails.
        :type resource_configuration: oci.data_integration.models.ResourceConfiguration

        :param configuration_details:
            The value to assign to the configuration_details property of this CreateExternalPublicationDetails.
        :type configuration_details: oci.data_integration.models.ConfigurationDetails

        """
        self.swagger_types = {
            'application_id': 'str',
            'application_compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'resource_configuration': 'ResourceConfiguration',
            'configuration_details': 'ConfigurationDetails'
        }

        self.attribute_map = {
            'application_id': 'applicationId',
            'application_compartment_id': 'applicationCompartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'resource_configuration': 'resourceConfiguration',
            'configuration_details': 'configurationDetails'
        }

        self._application_id = None
        self._application_compartment_id = None
        self._display_name = None
        self._description = None
        self._resource_configuration = None
        self._configuration_details = None

    @property
    def application_id(self):
        """
        Gets the application_id of this CreateExternalPublicationDetails.
        The unique OCID of the identifier that is returned after creating the Oracle Cloud Infrastructure Data Flow application.


        :return: The application_id of this CreateExternalPublicationDetails.
        :rtype: str
        """
        return self._application_id

    @application_id.setter
    def application_id(self, application_id):
        """
        Sets the application_id of this CreateExternalPublicationDetails.
        The unique OCID of the identifier that is returned after creating the Oracle Cloud Infrastructure Data Flow application.


        :param application_id: The application_id of this CreateExternalPublicationDetails.
        :type: str
        """
        self._application_id = application_id

    @property
    def application_compartment_id(self):
        """
        **[Required]** Gets the application_compartment_id of this CreateExternalPublicationDetails.
        The OCID of the compartment where the application is created in the Oracle Cloud Infrastructure Data Flow Service.


        :return: The application_compartment_id of this CreateExternalPublicationDetails.
        :rtype: str
        """
        return self._application_compartment_id

    @application_compartment_id.setter
    def application_compartment_id(self, application_compartment_id):
        """
        Sets the application_compartment_id of this CreateExternalPublicationDetails.
        The OCID of the compartment where the application is created in the Oracle Cloud Infrastructure Data Flow Service.


        :param application_compartment_id: The application_compartment_id of this CreateExternalPublicationDetails.
        :type: str
        """
        self._application_compartment_id = application_compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateExternalPublicationDetails.
        The name of the application.


        :return: The display_name of this CreateExternalPublicationDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateExternalPublicationDetails.
        The name of the application.


        :param display_name: The display_name of this CreateExternalPublicationDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this CreateExternalPublicationDetails.
        The details of the data flow or the application.


        :return: The description of this CreateExternalPublicationDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateExternalPublicationDetails.
        The details of the data flow or the application.


        :param description: The description of this CreateExternalPublicationDetails.
        :type: str
        """
        self._description = description

    @property
    def resource_configuration(self):
        """
        Gets the resource_configuration of this CreateExternalPublicationDetails.

        :return: The resource_configuration of this CreateExternalPublicationDetails.
        :rtype: oci.data_integration.models.ResourceConfiguration
        """
        return self._resource_configuration

    @resource_configuration.setter
    def resource_configuration(self, resource_configuration):
        """
        Sets the resource_configuration of this CreateExternalPublicationDetails.

        :param resource_configuration: The resource_configuration of this CreateExternalPublicationDetails.
        :type: oci.data_integration.models.ResourceConfiguration
        """
        self._resource_configuration = resource_configuration

    @property
    def configuration_details(self):
        """
        Gets the configuration_details of this CreateExternalPublicationDetails.

        :return: The configuration_details of this CreateExternalPublicationDetails.
        :rtype: oci.data_integration.models.ConfigurationDetails
        """
        return self._configuration_details

    @configuration_details.setter
    def configuration_details(self, configuration_details):
        """
        Sets the configuration_details of this CreateExternalPublicationDetails.

        :param configuration_details: The configuration_details of this CreateExternalPublicationDetails.
        :type: oci.data_integration.models.ConfigurationDetails
        """
        self._configuration_details = configuration_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
