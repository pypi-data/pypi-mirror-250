# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220528

from .create_batching_strategy_details import CreateBatchingStrategyDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateSequentialBatchingStrategyDetails(CreateBatchingStrategyDetails):
    """
    Sequential batching strategy details to use during PRECHECK and APPLY Cycle Actions.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateSequentialBatchingStrategyDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.fleet_software_update.models.CreateSequentialBatchingStrategyDetails.type` attribute
        of this class is ``SEQUENTIAL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this CreateSequentialBatchingStrategyDetails.
            Allowed values for this property are: "SEQUENTIAL", "FIFTY_FIFTY", "SERVICE_AVAILABILITY_FACTOR", "NON_ROLLING"
        :type type: str

        :param is_force_rolling:
            The value to assign to the is_force_rolling property of this CreateSequentialBatchingStrategyDetails.
        :type is_force_rolling: bool

        """
        self.swagger_types = {
            'type': 'str',
            'is_force_rolling': 'bool'
        }

        self.attribute_map = {
            'type': 'type',
            'is_force_rolling': 'isForceRolling'
        }

        self._type = None
        self._is_force_rolling = None
        self._type = 'SEQUENTIAL'

    @property
    def is_force_rolling(self):
        """
        Gets the is_force_rolling of this CreateSequentialBatchingStrategyDetails.
        True to force rolling patching.


        :return: The is_force_rolling of this CreateSequentialBatchingStrategyDetails.
        :rtype: bool
        """
        return self._is_force_rolling

    @is_force_rolling.setter
    def is_force_rolling(self, is_force_rolling):
        """
        Sets the is_force_rolling of this CreateSequentialBatchingStrategyDetails.
        True to force rolling patching.


        :param is_force_rolling: The is_force_rolling of this CreateSequentialBatchingStrategyDetails.
        :type: bool
        """
        self._is_force_rolling = is_force_rolling

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
