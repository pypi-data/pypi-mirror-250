# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220421

from .verify_configuration import VerifyConfiguration
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OciDevOpsBuildConfiguration(VerifyConfiguration):
    """
    OCI DevOps configuration extends a Verify Configuration with necessary data to reach and use the OCI DevOps Build Service.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new OciDevOpsBuildConfiguration object with values from keyword arguments. The default value of the :py:attr:`~oci.adm.models.OciDevOpsBuildConfiguration.build_service_type` attribute
        of this class is ``OCI_DEVOPS_BUILD`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param build_service_type:
            The value to assign to the build_service_type property of this OciDevOpsBuildConfiguration.
            Allowed values for this property are: "OCI_DEVOPS_BUILD", "GITLAB_PIPELINE", "GITHUB_ACTIONS", "JENKINS_PIPELINE", "NONE"
        :type build_service_type: str

        :param pipeline_id:
            The value to assign to the pipeline_id property of this OciDevOpsBuildConfiguration.
        :type pipeline_id: str

        :param additional_parameters:
            The value to assign to the additional_parameters property of this OciDevOpsBuildConfiguration.
        :type additional_parameters: dict(str, str)

        """
        self.swagger_types = {
            'build_service_type': 'str',
            'pipeline_id': 'str',
            'additional_parameters': 'dict(str, str)'
        }

        self.attribute_map = {
            'build_service_type': 'buildServiceType',
            'pipeline_id': 'pipelineId',
            'additional_parameters': 'additionalParameters'
        }

        self._build_service_type = None
        self._pipeline_id = None
        self._additional_parameters = None
        self._build_service_type = 'OCI_DEVOPS_BUILD'

    @property
    def pipeline_id(self):
        """
        **[Required]** Gets the pipeline_id of this OciDevOpsBuildConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the user's DevOps Build Pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The pipeline_id of this OciDevOpsBuildConfiguration.
        :rtype: str
        """
        return self._pipeline_id

    @pipeline_id.setter
    def pipeline_id(self, pipeline_id):
        """
        Sets the pipeline_id of this OciDevOpsBuildConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the user's DevOps Build Pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param pipeline_id: The pipeline_id of this OciDevOpsBuildConfiguration.
        :type: str
        """
        self._pipeline_id = pipeline_id

    @property
    def additional_parameters(self):
        """
        Gets the additional_parameters of this OciDevOpsBuildConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :return: The additional_parameters of this OciDevOpsBuildConfiguration.
        :rtype: dict(str, str)
        """
        return self._additional_parameters

    @additional_parameters.setter
    def additional_parameters(self, additional_parameters):
        """
        Sets the additional_parameters of this OciDevOpsBuildConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :param additional_parameters: The additional_parameters of this OciDevOpsBuildConfiguration.
        :type: dict(str, str)
        """
        self._additional_parameters = additional_parameters

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
