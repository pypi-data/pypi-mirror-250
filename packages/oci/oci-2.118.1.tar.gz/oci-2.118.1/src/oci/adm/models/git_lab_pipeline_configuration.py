# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220421

from .verify_configuration import VerifyConfiguration
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GitLabPipelineConfiguration(VerifyConfiguration):
    """
    Extends a Verify configuration with appropriate data to reach and use the build service provided by a GitLab Pipeline.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new GitLabPipelineConfiguration object with values from keyword arguments. The default value of the :py:attr:`~oci.adm.models.GitLabPipelineConfiguration.build_service_type` attribute
        of this class is ``GITLAB_PIPELINE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param build_service_type:
            The value to assign to the build_service_type property of this GitLabPipelineConfiguration.
            Allowed values for this property are: "OCI_DEVOPS_BUILD", "GITLAB_PIPELINE", "GITHUB_ACTIONS", "JENKINS_PIPELINE", "NONE"
        :type build_service_type: str

        :param repository_url:
            The value to assign to the repository_url property of this GitLabPipelineConfiguration.
        :type repository_url: str

        :param username:
            The value to assign to the username property of this GitLabPipelineConfiguration.
        :type username: str

        :param pat_secret_id:
            The value to assign to the pat_secret_id property of this GitLabPipelineConfiguration.
        :type pat_secret_id: str

        :param trigger_secret_id:
            The value to assign to the trigger_secret_id property of this GitLabPipelineConfiguration.
        :type trigger_secret_id: str

        :param additional_parameters:
            The value to assign to the additional_parameters property of this GitLabPipelineConfiguration.
        :type additional_parameters: dict(str, str)

        """
        self.swagger_types = {
            'build_service_type': 'str',
            'repository_url': 'str',
            'username': 'str',
            'pat_secret_id': 'str',
            'trigger_secret_id': 'str',
            'additional_parameters': 'dict(str, str)'
        }

        self.attribute_map = {
            'build_service_type': 'buildServiceType',
            'repository_url': 'repositoryUrl',
            'username': 'username',
            'pat_secret_id': 'patSecretId',
            'trigger_secret_id': 'triggerSecretId',
            'additional_parameters': 'additionalParameters'
        }

        self._build_service_type = None
        self._repository_url = None
        self._username = None
        self._pat_secret_id = None
        self._trigger_secret_id = None
        self._additional_parameters = None
        self._build_service_type = 'GITLAB_PIPELINE'

    @property
    def repository_url(self):
        """
        **[Required]** Gets the repository_url of this GitLabPipelineConfiguration.
        The location of the Repository where the GitLab Pipeline will be run.
        The expected format is https://gitlab.com/[groupName]/[repoName]


        :return: The repository_url of this GitLabPipelineConfiguration.
        :rtype: str
        """
        return self._repository_url

    @repository_url.setter
    def repository_url(self, repository_url):
        """
        Sets the repository_url of this GitLabPipelineConfiguration.
        The location of the Repository where the GitLab Pipeline will be run.
        The expected format is https://gitlab.com/[groupName]/[repoName]


        :param repository_url: The repository_url of this GitLabPipelineConfiguration.
        :type: str
        """
        self._repository_url = repository_url

    @property
    def username(self):
        """
        **[Required]** Gets the username of this GitLabPipelineConfiguration.
        The username that will trigger the GitLab Pipeline.


        :return: The username of this GitLabPipelineConfiguration.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this GitLabPipelineConfiguration.
        The username that will trigger the GitLab Pipeline.


        :param username: The username of this GitLabPipelineConfiguration.
        :type: str
        """
        self._username = username

    @property
    def pat_secret_id(self):
        """
        **[Required]** Gets the pat_secret_id of this GitLabPipelineConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the Private Access Token (PAT) Secret.
        The PAT provides the credentials to access the GitLab pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The pat_secret_id of this GitLabPipelineConfiguration.
        :rtype: str
        """
        return self._pat_secret_id

    @pat_secret_id.setter
    def pat_secret_id(self, pat_secret_id):
        """
        Sets the pat_secret_id of this GitLabPipelineConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the Private Access Token (PAT) Secret.
        The PAT provides the credentials to access the GitLab pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param pat_secret_id: The pat_secret_id of this GitLabPipelineConfiguration.
        :type: str
        """
        self._pat_secret_id = pat_secret_id

    @property
    def trigger_secret_id(self):
        """
        **[Required]** Gets the trigger_secret_id of this GitLabPipelineConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the trigger Secret.
        The Secret provides access to the trigger for a GitLab pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The trigger_secret_id of this GitLabPipelineConfiguration.
        :rtype: str
        """
        return self._trigger_secret_id

    @trigger_secret_id.setter
    def trigger_secret_id(self, trigger_secret_id):
        """
        Sets the trigger_secret_id of this GitLabPipelineConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the trigger Secret.
        The Secret provides access to the trigger for a GitLab pipeline.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param trigger_secret_id: The trigger_secret_id of this GitLabPipelineConfiguration.
        :type: str
        """
        self._trigger_secret_id = trigger_secret_id

    @property
    def additional_parameters(self):
        """
        Gets the additional_parameters of this GitLabPipelineConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :return: The additional_parameters of this GitLabPipelineConfiguration.
        :rtype: dict(str, str)
        """
        return self._additional_parameters

    @additional_parameters.setter
    def additional_parameters(self, additional_parameters):
        """
        Sets the additional_parameters of this GitLabPipelineConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :param additional_parameters: The additional_parameters of this GitLabPipelineConfiguration.
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
