# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918

from .endpoint import Endpoint
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ComputeInstanceEndpoint(Endpoint):
    """
    Defines the details required for a COMPUTE_INSTANCE-type `Endpoint`.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ComputeInstanceEndpoint object with values from keyword arguments. The default value of the :py:attr:`~oci.vn_monitoring.models.ComputeInstanceEndpoint.type` attribute
        of this class is ``COMPUTE_INSTANCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this ComputeInstanceEndpoint.
            Allowed values for this property are: "IP_ADDRESS", "SUBNET", "COMPUTE_INSTANCE", "VNIC", "LOAD_BALANCER", "LOAD_BALANCER_LISTENER", "NETWORK_LOAD_BALANCER", "NETWORK_LOAD_BALANCER_LISTENER", "VLAN"
        :type type: str

        :param address:
            The value to assign to the address property of this ComputeInstanceEndpoint.
        :type address: str

        :param instance_id:
            The value to assign to the instance_id property of this ComputeInstanceEndpoint.
        :type instance_id: str

        :param vnic_id:
            The value to assign to the vnic_id property of this ComputeInstanceEndpoint.
        :type vnic_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'address': 'str',
            'instance_id': 'str',
            'vnic_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'address': 'address',
            'instance_id': 'instanceId',
            'vnic_id': 'vnicId'
        }

        self._type = None
        self._address = None
        self._instance_id = None
        self._vnic_id = None
        self._type = 'COMPUTE_INSTANCE'

    @property
    def address(self):
        """
        **[Required]** Gets the address of this ComputeInstanceEndpoint.
        The IPv4 address of the COMPUTE_INSTANCE-type `Endpoint` object.


        :return: The address of this ComputeInstanceEndpoint.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this ComputeInstanceEndpoint.
        The IPv4 address of the COMPUTE_INSTANCE-type `Endpoint` object.


        :param address: The address of this ComputeInstanceEndpoint.
        :type: str
        """
        self._address = address

    @property
    def instance_id(self):
        """
        **[Required]** Gets the instance_id of this ComputeInstanceEndpoint.
        The `OCID`__ of the compute instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The instance_id of this ComputeInstanceEndpoint.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """
        Sets the instance_id of this ComputeInstanceEndpoint.
        The `OCID`__ of the compute instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param instance_id: The instance_id of this ComputeInstanceEndpoint.
        :type: str
        """
        self._instance_id = instance_id

    @property
    def vnic_id(self):
        """
        **[Required]** Gets the vnic_id of this ComputeInstanceEndpoint.
        The `OCID`__ of the VNIC attached to the compute instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The vnic_id of this ComputeInstanceEndpoint.
        :rtype: str
        """
        return self._vnic_id

    @vnic_id.setter
    def vnic_id(self, vnic_id):
        """
        Sets the vnic_id of this ComputeInstanceEndpoint.
        The `OCID`__ of the VNIC attached to the compute instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param vnic_id: The vnic_id of this ComputeInstanceEndpoint.
        :type: str
        """
        self._vnic_id = vnic_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
