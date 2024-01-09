# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20180115


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalDownstream(object):
    """
    External downstream nameserver for the zone.
    This field is currently not supported when `zoneType` is `SECONDARY` or `scope` is `PRIVATE`.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalDownstream object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param address:
            The value to assign to the address property of this ExternalDownstream.
        :type address: str

        :param port:
            The value to assign to the port property of this ExternalDownstream.
        :type port: int

        :param tsig_key_id:
            The value to assign to the tsig_key_id property of this ExternalDownstream.
        :type tsig_key_id: str

        """
        self.swagger_types = {
            'address': 'str',
            'port': 'int',
            'tsig_key_id': 'str'
        }

        self.attribute_map = {
            'address': 'address',
            'port': 'port',
            'tsig_key_id': 'tsigKeyId'
        }

        self._address = None
        self._port = None
        self._tsig_key_id = None

    @property
    def address(self):
        """
        **[Required]** Gets the address of this ExternalDownstream.
        The server's IP address (IPv4 or IPv6).


        :return: The address of this ExternalDownstream.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this ExternalDownstream.
        The server's IP address (IPv4 or IPv6).


        :param address: The address of this ExternalDownstream.
        :type: str
        """
        self._address = address

    @property
    def port(self):
        """
        Gets the port of this ExternalDownstream.
        The server's port. Port value must be a value of 53, otherwise omit
        the port value.


        :return: The port of this ExternalDownstream.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this ExternalDownstream.
        The server's port. Port value must be a value of 53, otherwise omit
        the port value.


        :param port: The port of this ExternalDownstream.
        :type: int
        """
        self._port = port

    @property
    def tsig_key_id(self):
        """
        Gets the tsig_key_id of this ExternalDownstream.
        The OCID of the TSIG key.
        A TSIG key is used to secure DNS messages (in this case, zone transfers) between two systems that both have the (shared) secret.


        :return: The tsig_key_id of this ExternalDownstream.
        :rtype: str
        """
        return self._tsig_key_id

    @tsig_key_id.setter
    def tsig_key_id(self, tsig_key_id):
        """
        Sets the tsig_key_id of this ExternalDownstream.
        The OCID of the TSIG key.
        A TSIG key is used to secure DNS messages (in this case, zone transfers) between two systems that both have the (shared) secret.


        :param tsig_key_id: The tsig_key_id of this ExternalDownstream.
        :type: str
        """
        self._tsig_key_id = tsig_key_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
