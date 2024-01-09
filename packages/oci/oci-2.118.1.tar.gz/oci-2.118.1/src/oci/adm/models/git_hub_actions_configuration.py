# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220421

from .verify_configuration import VerifyConfiguration
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GitHubActionsConfiguration(VerifyConfiguration):
    """
    Extends a Verify configuration with appropriate data to reach and use the build service provided by a GitHub Action.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new GitHubActionsConfiguration object with values from keyword arguments. The default value of the :py:attr:`~oci.adm.models.GitHubActionsConfiguration.build_service_type` attribute
        of this class is ``GITHUB_ACTIONS`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param build_service_type:
            The value to assign to the build_service_type property of this GitHubActionsConfiguration.
            Allowed values for this property are: "OCI_DEVOPS_BUILD", "GITLAB_PIPELINE", "GITHUB_ACTIONS", "JENKINS_PIPELINE", "NONE"
        :type build_service_type: str

        :param repository_url:
            The value to assign to the repository_url property of this GitHubActionsConfiguration.
        :type repository_url: str

        :param pat_secret_id:
            The value to assign to the pat_secret_id property of this GitHubActionsConfiguration.
        :type pat_secret_id: str

        :param username:
            The value to assign to the username property of this GitHubActionsConfiguration.
        :type username: str

        :param workflow_name:
            The value to assign to the workflow_name property of this GitHubActionsConfiguration.
        :type workflow_name: str

        :param additional_parameters:
            The value to assign to the additional_parameters property of this GitHubActionsConfiguration.
        :type additional_parameters: dict(str, str)

        """
        self.swagger_types = {
            'build_service_type': 'str',
            'repository_url': 'str',
            'pat_secret_id': 'str',
            'username': 'str',
            'workflow_name': 'str',
            'additional_parameters': 'dict(str, str)'
        }

        self.attribute_map = {
            'build_service_type': 'buildServiceType',
            'repository_url': 'repositoryUrl',
            'pat_secret_id': 'patSecretId',
            'username': 'username',
            'workflow_name': 'workflowName',
            'additional_parameters': 'additionalParameters'
        }

        self._build_service_type = None
        self._repository_url = None
        self._pat_secret_id = None
        self._username = None
        self._workflow_name = None
        self._additional_parameters = None
        self._build_service_type = 'GITHUB_ACTIONS'

    @property
    def repository_url(self):
        """
        **[Required]** Gets the repository_url of this GitHubActionsConfiguration.
        The location of the repository where the GitHub Actions is defined.
        For Non-Enterprise GitHub the expected format is https://github.com/[owner]/[repoName]
        For Enterprise GitHub the expected format is http(s)://[hostname]/api/v3/repos/[owner]/[repoName]


        :return: The repository_url of this GitHubActionsConfiguration.
        :rtype: str
        """
        return self._repository_url

    @repository_url.setter
    def repository_url(self, repository_url):
        """
        Sets the repository_url of this GitHubActionsConfiguration.
        The location of the repository where the GitHub Actions is defined.
        For Non-Enterprise GitHub the expected format is https://github.com/[owner]/[repoName]
        For Enterprise GitHub the expected format is http(s)://[hostname]/api/v3/repos/[owner]/[repoName]


        :param repository_url: The repository_url of this GitHubActionsConfiguration.
        :type: str
        """
        self._repository_url = repository_url

    @property
    def pat_secret_id(self):
        """
        **[Required]** Gets the pat_secret_id of this GitHubActionsConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the Private Access Token (PAT) Secret.
        The PAT provides the credentials to access the GitHub Action.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The pat_secret_id of this GitHubActionsConfiguration.
        :rtype: str
        """
        return self._pat_secret_id

    @pat_secret_id.setter
    def pat_secret_id(self, pat_secret_id):
        """
        Sets the pat_secret_id of this GitHubActionsConfiguration.
        The Oracle Cloud Identifier (`OCID`__) of the Private Access Token (PAT) Secret.
        The PAT provides the credentials to access the GitHub Action.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param pat_secret_id: The pat_secret_id of this GitHubActionsConfiguration.
        :type: str
        """
        self._pat_secret_id = pat_secret_id

    @property
    def username(self):
        """
        **[Required]** Gets the username of this GitHubActionsConfiguration.
        The username that will trigger the GitHub Action.


        :return: The username of this GitHubActionsConfiguration.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this GitHubActionsConfiguration.
        The username that will trigger the GitHub Action.


        :param username: The username of this GitHubActionsConfiguration.
        :type: str
        """
        self._username = username

    @property
    def workflow_name(self):
        """
        **[Required]** Gets the workflow_name of this GitHubActionsConfiguration.
        The name of the GitHub Actions workflow that defines the build pipeline.


        :return: The workflow_name of this GitHubActionsConfiguration.
        :rtype: str
        """
        return self._workflow_name

    @workflow_name.setter
    def workflow_name(self, workflow_name):
        """
        Sets the workflow_name of this GitHubActionsConfiguration.
        The name of the GitHub Actions workflow that defines the build pipeline.


        :param workflow_name: The workflow_name of this GitHubActionsConfiguration.
        :type: str
        """
        self._workflow_name = workflow_name

    @property
    def additional_parameters(self):
        """
        Gets the additional_parameters of this GitHubActionsConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :return: The additional_parameters of this GitHubActionsConfiguration.
        :rtype: dict(str, str)
        """
        return self._additional_parameters

    @additional_parameters.setter
    def additional_parameters(self, additional_parameters):
        """
        Sets the additional_parameters of this GitHubActionsConfiguration.
        Additional key-value pairs passed as parameters to the build service when running an experiment.


        :param additional_parameters: The additional_parameters of this GitHubActionsConfiguration.
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
