# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180222


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ClusterMigrateToNativeVcnDetails(object):
    """
    The properties that define a request to migrate a cluster to Native VCN.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ClusterMigrateToNativeVcnDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param endpoint_config:
            The value to assign to the endpoint_config property of this ClusterMigrateToNativeVcnDetails.
        :type endpoint_config: oci.container_engine.models.ClusterEndpointConfig

        :param decommission_delay_duration:
            The value to assign to the decommission_delay_duration property of this ClusterMigrateToNativeVcnDetails.
        :type decommission_delay_duration: str

        """
        self.swagger_types = {
            'endpoint_config': 'ClusterEndpointConfig',
            'decommission_delay_duration': 'str'
        }

        self.attribute_map = {
            'endpoint_config': 'endpointConfig',
            'decommission_delay_duration': 'decommissionDelayDuration'
        }

        self._endpoint_config = None
        self._decommission_delay_duration = None

    @property
    def endpoint_config(self):
        """
        **[Required]** Gets the endpoint_config of this ClusterMigrateToNativeVcnDetails.
        The network configuration for access to the Cluster control plane.


        :return: The endpoint_config of this ClusterMigrateToNativeVcnDetails.
        :rtype: oci.container_engine.models.ClusterEndpointConfig
        """
        return self._endpoint_config

    @endpoint_config.setter
    def endpoint_config(self, endpoint_config):
        """
        Sets the endpoint_config of this ClusterMigrateToNativeVcnDetails.
        The network configuration for access to the Cluster control plane.


        :param endpoint_config: The endpoint_config of this ClusterMigrateToNativeVcnDetails.
        :type: oci.container_engine.models.ClusterEndpointConfig
        """
        self._endpoint_config = endpoint_config

    @property
    def decommission_delay_duration(self):
        """
        Gets the decommission_delay_duration of this ClusterMigrateToNativeVcnDetails.
        The optional override of the non-native endpoint decommission time after migration is complete. Defaults to 30 days.


        :return: The decommission_delay_duration of this ClusterMigrateToNativeVcnDetails.
        :rtype: str
        """
        return self._decommission_delay_duration

    @decommission_delay_duration.setter
    def decommission_delay_duration(self, decommission_delay_duration):
        """
        Sets the decommission_delay_duration of this ClusterMigrateToNativeVcnDetails.
        The optional override of the non-native endpoint decommission time after migration is complete. Defaults to 30 days.


        :param decommission_delay_duration: The decommission_delay_duration of this ClusterMigrateToNativeVcnDetails.
        :type: str
        """
        self._decommission_delay_duration = decommission_delay_duration

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
