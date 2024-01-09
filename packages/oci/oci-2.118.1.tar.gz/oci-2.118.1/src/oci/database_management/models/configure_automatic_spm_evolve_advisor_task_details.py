# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConfigureAutomaticSpmEvolveAdvisorTaskDetails(object):
    """
    The configuration details of the Automatic SPM Evolve Advisor task.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ConfigureAutomaticSpmEvolveAdvisorTaskDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param task_parameters:
            The value to assign to the task_parameters property of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :type task_parameters: oci.database_management.models.SpmEvolveTaskParameters

        :param credentials:
            The value to assign to the credentials property of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :type credentials: oci.database_management.models.ManagedDatabaseCredential

        """
        self.swagger_types = {
            'task_parameters': 'SpmEvolveTaskParameters',
            'credentials': 'ManagedDatabaseCredential'
        }

        self.attribute_map = {
            'task_parameters': 'taskParameters',
            'credentials': 'credentials'
        }

        self._task_parameters = None
        self._credentials = None

    @property
    def task_parameters(self):
        """
        **[Required]** Gets the task_parameters of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.

        :return: The task_parameters of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :rtype: oci.database_management.models.SpmEvolveTaskParameters
        """
        return self._task_parameters

    @task_parameters.setter
    def task_parameters(self, task_parameters):
        """
        Sets the task_parameters of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.

        :param task_parameters: The task_parameters of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :type: oci.database_management.models.SpmEvolveTaskParameters
        """
        self._task_parameters = task_parameters

    @property
    def credentials(self):
        """
        **[Required]** Gets the credentials of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.

        :return: The credentials of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :rtype: oci.database_management.models.ManagedDatabaseCredential
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.

        :param credentials: The credentials of this ConfigureAutomaticSpmEvolveAdvisorTaskDetails.
        :type: oci.database_management.models.ManagedDatabaseCredential
        """
        self._credentials = credentials

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
