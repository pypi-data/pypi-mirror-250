# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190111


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OrganizationSubscriptionSummary(object):
    """
    Subscription summary
    """

    def __init__(self, **kwargs):
        """
        Initializes a new OrganizationSubscriptionSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this OrganizationSubscriptionSummary.
        :type id: str

        :param service_name:
            The value to assign to the service_name property of this OrganizationSubscriptionSummary.
        :type service_name: str

        :param type:
            The value to assign to the type property of this OrganizationSubscriptionSummary.
        :type type: str

        :param status:
            The value to assign to the status property of this OrganizationSubscriptionSummary.
        :type status: str

        :param time_start:
            The value to assign to the time_start property of this OrganizationSubscriptionSummary.
        :type time_start: datetime

        :param time_end:
            The value to assign to the time_end property of this OrganizationSubscriptionSummary.
        :type time_end: datetime

        :param currency:
            The value to assign to the currency property of this OrganizationSubscriptionSummary.
        :type currency: oci.onesubscription.models.OrgnizationSubsCurrency

        :param total_value:
            The value to assign to the total_value property of this OrganizationSubscriptionSummary.
        :type total_value: str

        """
        self.swagger_types = {
            'id': 'str',
            'service_name': 'str',
            'type': 'str',
            'status': 'str',
            'time_start': 'datetime',
            'time_end': 'datetime',
            'currency': 'OrgnizationSubsCurrency',
            'total_value': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'service_name': 'serviceName',
            'type': 'type',
            'status': 'status',
            'time_start': 'timeStart',
            'time_end': 'timeEnd',
            'currency': 'currency',
            'total_value': 'totalValue'
        }

        self._id = None
        self._service_name = None
        self._type = None
        self._status = None
        self._time_start = None
        self._time_end = None
        self._currency = None
        self._total_value = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this OrganizationSubscriptionSummary.
        SPM internal Subscription ID


        :return: The id of this OrganizationSubscriptionSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OrganizationSubscriptionSummary.
        SPM internal Subscription ID


        :param id: The id of this OrganizationSubscriptionSummary.
        :type: str
        """
        self._id = id

    @property
    def service_name(self):
        """
        Gets the service_name of this OrganizationSubscriptionSummary.
        Customer friendly service name provided by PRG


        :return: The service_name of this OrganizationSubscriptionSummary.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this OrganizationSubscriptionSummary.
        Customer friendly service name provided by PRG


        :param service_name: The service_name of this OrganizationSubscriptionSummary.
        :type: str
        """
        self._service_name = service_name

    @property
    def type(self):
        """
        Gets the type of this OrganizationSubscriptionSummary.
        Subscription Type i.e. IAAS,SAAS,PAAS


        :return: The type of this OrganizationSubscriptionSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this OrganizationSubscriptionSummary.
        Subscription Type i.e. IAAS,SAAS,PAAS


        :param type: The type of this OrganizationSubscriptionSummary.
        :type: str
        """
        self._type = type

    @property
    def status(self):
        """
        Gets the status of this OrganizationSubscriptionSummary.
        Status of the plan


        :return: The status of this OrganizationSubscriptionSummary.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this OrganizationSubscriptionSummary.
        Status of the plan


        :param status: The status of this OrganizationSubscriptionSummary.
        :type: str
        """
        self._status = status

    @property
    def time_start(self):
        """
        Gets the time_start of this OrganizationSubscriptionSummary.
        Represents the date when the first service of the subscription was activated


        :return: The time_start of this OrganizationSubscriptionSummary.
        :rtype: datetime
        """
        return self._time_start

    @time_start.setter
    def time_start(self, time_start):
        """
        Sets the time_start of this OrganizationSubscriptionSummary.
        Represents the date when the first service of the subscription was activated


        :param time_start: The time_start of this OrganizationSubscriptionSummary.
        :type: datetime
        """
        self._time_start = time_start

    @property
    def time_end(self):
        """
        Gets the time_end of this OrganizationSubscriptionSummary.
        Represents the date when the last service of the subscription ends


        :return: The time_end of this OrganizationSubscriptionSummary.
        :rtype: datetime
        """
        return self._time_end

    @time_end.setter
    def time_end(self, time_end):
        """
        Sets the time_end of this OrganizationSubscriptionSummary.
        Represents the date when the last service of the subscription ends


        :param time_end: The time_end of this OrganizationSubscriptionSummary.
        :type: datetime
        """
        self._time_end = time_end

    @property
    def currency(self):
        """
        Gets the currency of this OrganizationSubscriptionSummary.

        :return: The currency of this OrganizationSubscriptionSummary.
        :rtype: oci.onesubscription.models.OrgnizationSubsCurrency
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """
        Sets the currency of this OrganizationSubscriptionSummary.

        :param currency: The currency of this OrganizationSubscriptionSummary.
        :type: oci.onesubscription.models.OrgnizationSubsCurrency
        """
        self._currency = currency

    @property
    def total_value(self):
        """
        Gets the total_value of this OrganizationSubscriptionSummary.
        Total aggregate TCLV of all lines for the subscription including expired, active, and signed


        :return: The total_value of this OrganizationSubscriptionSummary.
        :rtype: str
        """
        return self._total_value

    @total_value.setter
    def total_value(self, total_value):
        """
        Sets the total_value of this OrganizationSubscriptionSummary.
        Total aggregate TCLV of all lines for the subscription including expired, active, and signed


        :param total_value: The total_value of this OrganizationSubscriptionSummary.
        :type: str
        """
        self._total_value = total_value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
