# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200601


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RecalledData(object):
    """
    This is the information about recalled data
    """

    #: A constant which can be used with the status property of a RecalledData.
    #: This constant has a value of "RECALLED"
    STATUS_RECALLED = "RECALLED"

    #: A constant which can be used with the status property of a RecalledData.
    #: This constant has a value of "PENDING"
    STATUS_PENDING = "PENDING"

    #: A constant which can be used with the status property of a RecalledData.
    #: This constant has a value of "FAILED"
    STATUS_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new RecalledData object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_data_ended:
            The value to assign to the time_data_ended property of this RecalledData.
        :type time_data_ended: datetime

        :param time_data_started:
            The value to assign to the time_data_started property of this RecalledData.
        :type time_data_started: datetime

        :param time_started:
            The value to assign to the time_started property of this RecalledData.
        :type time_started: datetime

        :param status:
            The value to assign to the status property of this RecalledData.
            Allowed values for this property are: "RECALLED", "PENDING", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param recall_count:
            The value to assign to the recall_count property of this RecalledData.
        :type recall_count: int

        :param storage_usage_in_bytes:
            The value to assign to the storage_usage_in_bytes property of this RecalledData.
        :type storage_usage_in_bytes: int

        :param not_recalled_data_in_bytes:
            The value to assign to the not_recalled_data_in_bytes property of this RecalledData.
        :type not_recalled_data_in_bytes: int

        :param purpose:
            The value to assign to the purpose property of this RecalledData.
        :type purpose: str

        :param query_string:
            The value to assign to the query_string property of this RecalledData.
        :type query_string: str

        :param log_sets:
            The value to assign to the log_sets property of this RecalledData.
        :type log_sets: str

        :param created_by:
            The value to assign to the created_by property of this RecalledData.
        :type created_by: str

        """
        self.swagger_types = {
            'time_data_ended': 'datetime',
            'time_data_started': 'datetime',
            'time_started': 'datetime',
            'status': 'str',
            'recall_count': 'int',
            'storage_usage_in_bytes': 'int',
            'not_recalled_data_in_bytes': 'int',
            'purpose': 'str',
            'query_string': 'str',
            'log_sets': 'str',
            'created_by': 'str'
        }

        self.attribute_map = {
            'time_data_ended': 'timeDataEnded',
            'time_data_started': 'timeDataStarted',
            'time_started': 'timeStarted',
            'status': 'status',
            'recall_count': 'recallCount',
            'storage_usage_in_bytes': 'storageUsageInBytes',
            'not_recalled_data_in_bytes': 'notRecalledDataInBytes',
            'purpose': 'purpose',
            'query_string': 'queryString',
            'log_sets': 'logSets',
            'created_by': 'createdBy'
        }

        self._time_data_ended = None
        self._time_data_started = None
        self._time_started = None
        self._status = None
        self._recall_count = None
        self._storage_usage_in_bytes = None
        self._not_recalled_data_in_bytes = None
        self._purpose = None
        self._query_string = None
        self._log_sets = None
        self._created_by = None

    @property
    def time_data_ended(self):
        """
        **[Required]** Gets the time_data_ended of this RecalledData.
        This is the end of the time range of the related data


        :return: The time_data_ended of this RecalledData.
        :rtype: datetime
        """
        return self._time_data_ended

    @time_data_ended.setter
    def time_data_ended(self, time_data_ended):
        """
        Sets the time_data_ended of this RecalledData.
        This is the end of the time range of the related data


        :param time_data_ended: The time_data_ended of this RecalledData.
        :type: datetime
        """
        self._time_data_ended = time_data_ended

    @property
    def time_data_started(self):
        """
        **[Required]** Gets the time_data_started of this RecalledData.
        This is the start of the time range of the related data


        :return: The time_data_started of this RecalledData.
        :rtype: datetime
        """
        return self._time_data_started

    @time_data_started.setter
    def time_data_started(self, time_data_started):
        """
        Sets the time_data_started of this RecalledData.
        This is the start of the time range of the related data


        :param time_data_started: The time_data_started of this RecalledData.
        :type: datetime
        """
        self._time_data_started = time_data_started

    @property
    def time_started(self):
        """
        **[Required]** Gets the time_started of this RecalledData.
        This is the time when the first recall operation was started for this RecalledData


        :return: The time_started of this RecalledData.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this RecalledData.
        This is the time when the first recall operation was started for this RecalledData


        :param time_started: The time_started of this RecalledData.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def status(self):
        """
        **[Required]** Gets the status of this RecalledData.
        This is the status of the recall

        Allowed values for this property are: "RECALLED", "PENDING", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this RecalledData.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this RecalledData.
        This is the status of the recall


        :param status: The status of this RecalledData.
        :type: str
        """
        allowed_values = ["RECALLED", "PENDING", "FAILED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def recall_count(self):
        """
        **[Required]** Gets the recall_count of this RecalledData.
        This is the number of recall operations for this recall.  Note one RecalledData can be merged from the results
        of several recall operations if the time duration of the results of the recall operations overlap.


        :return: The recall_count of this RecalledData.
        :rtype: int
        """
        return self._recall_count

    @recall_count.setter
    def recall_count(self, recall_count):
        """
        Sets the recall_count of this RecalledData.
        This is the number of recall operations for this recall.  Note one RecalledData can be merged from the results
        of several recall operations if the time duration of the results of the recall operations overlap.


        :param recall_count: The recall_count of this RecalledData.
        :type: int
        """
        self._recall_count = recall_count

    @property
    def storage_usage_in_bytes(self):
        """
        **[Required]** Gets the storage_usage_in_bytes of this RecalledData.
        This is the size in bytes


        :return: The storage_usage_in_bytes of this RecalledData.
        :rtype: int
        """
        return self._storage_usage_in_bytes

    @storage_usage_in_bytes.setter
    def storage_usage_in_bytes(self, storage_usage_in_bytes):
        """
        Sets the storage_usage_in_bytes of this RecalledData.
        This is the size in bytes


        :param storage_usage_in_bytes: The storage_usage_in_bytes of this RecalledData.
        :type: int
        """
        self._storage_usage_in_bytes = storage_usage_in_bytes

    @property
    def not_recalled_data_in_bytes(self):
        """
        **[Required]** Gets the not_recalled_data_in_bytes of this RecalledData.
        This is the size of the archival data not recalled yet within the specified time range


        :return: The not_recalled_data_in_bytes of this RecalledData.
        :rtype: int
        """
        return self._not_recalled_data_in_bytes

    @not_recalled_data_in_bytes.setter
    def not_recalled_data_in_bytes(self, not_recalled_data_in_bytes):
        """
        Sets the not_recalled_data_in_bytes of this RecalledData.
        This is the size of the archival data not recalled yet within the specified time range


        :param not_recalled_data_in_bytes: The not_recalled_data_in_bytes of this RecalledData.
        :type: int
        """
        self._not_recalled_data_in_bytes = not_recalled_data_in_bytes

    @property
    def purpose(self):
        """
        **[Required]** Gets the purpose of this RecalledData.
        This is the purpose of the recall


        :return: The purpose of this RecalledData.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this RecalledData.
        This is the purpose of the recall


        :param purpose: The purpose of this RecalledData.
        :type: str
        """
        self._purpose = purpose

    @property
    def query_string(self):
        """
        **[Required]** Gets the query_string of this RecalledData.
        This is the query associated with the recall


        :return: The query_string of this RecalledData.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string):
        """
        Sets the query_string of this RecalledData.
        This is the query associated with the recall


        :param query_string: The query_string of this RecalledData.
        :type: str
        """
        self._query_string = query_string

    @property
    def log_sets(self):
        """
        **[Required]** Gets the log_sets of this RecalledData.
        This is the list of logsets associated with the recall


        :return: The log_sets of this RecalledData.
        :rtype: str
        """
        return self._log_sets

    @log_sets.setter
    def log_sets(self, log_sets):
        """
        Sets the log_sets of this RecalledData.
        This is the list of logsets associated with the recall


        :param log_sets: The log_sets of this RecalledData.
        :type: str
        """
        self._log_sets = log_sets

    @property
    def created_by(self):
        """
        **[Required]** Gets the created_by of this RecalledData.
        This is the user who initiated the recall request


        :return: The created_by of this RecalledData.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this RecalledData.
        This is the user who initiated the recall request


        :param created_by: The created_by of this RecalledData.
        :type: str
        """
        self._created_by = created_by

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
