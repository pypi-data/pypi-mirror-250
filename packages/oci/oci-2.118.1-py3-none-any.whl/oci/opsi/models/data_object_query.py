# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200630


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DataObjectQuery(object):
    """
    Information required to form and execute query on a data object.
    """

    #: A constant which can be used with the query_type property of a DataObjectQuery.
    #: This constant has a value of "TEMPLATIZED_QUERY"
    QUERY_TYPE_TEMPLATIZED_QUERY = "TEMPLATIZED_QUERY"

    #: A constant which can be used with the query_type property of a DataObjectQuery.
    #: This constant has a value of "STANDARD_QUERY"
    QUERY_TYPE_STANDARD_QUERY = "STANDARD_QUERY"

    def __init__(self, **kwargs):
        """
        Initializes a new DataObjectQuery object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.opsi.models.DataObjectStandardQuery`
        * :class:`~oci.opsi.models.DataObjectTemplatizedQuery`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param query_type:
            The value to assign to the query_type property of this DataObjectQuery.
            Allowed values for this property are: "TEMPLATIZED_QUERY", "STANDARD_QUERY"
        :type query_type: str

        :param bind_params:
            The value to assign to the bind_params property of this DataObjectQuery.
        :type bind_params: list[oci.opsi.models.DataObjectBindParameter]

        :param query_execution_timeout_in_seconds:
            The value to assign to the query_execution_timeout_in_seconds property of this DataObjectQuery.
        :type query_execution_timeout_in_seconds: float

        """
        self.swagger_types = {
            'query_type': 'str',
            'bind_params': 'list[DataObjectBindParameter]',
            'query_execution_timeout_in_seconds': 'float'
        }

        self.attribute_map = {
            'query_type': 'queryType',
            'bind_params': 'bindParams',
            'query_execution_timeout_in_seconds': 'queryExecutionTimeoutInSeconds'
        }

        self._query_type = None
        self._bind_params = None
        self._query_execution_timeout_in_seconds = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['queryType']

        if type == 'STANDARD_QUERY':
            return 'DataObjectStandardQuery'

        if type == 'TEMPLATIZED_QUERY':
            return 'DataObjectTemplatizedQuery'
        else:
            return 'DataObjectQuery'

    @property
    def query_type(self):
        """
        **[Required]** Gets the query_type of this DataObjectQuery.
        Type of Query

        Allowed values for this property are: "TEMPLATIZED_QUERY", "STANDARD_QUERY"


        :return: The query_type of this DataObjectQuery.
        :rtype: str
        """
        return self._query_type

    @query_type.setter
    def query_type(self, query_type):
        """
        Sets the query_type of this DataObjectQuery.
        Type of Query


        :param query_type: The query_type of this DataObjectQuery.
        :type: str
        """
        allowed_values = ["TEMPLATIZED_QUERY", "STANDARD_QUERY"]
        if not value_allowed_none_or_none_sentinel(query_type, allowed_values):
            raise ValueError(
                f"Invalid value for `query_type`, must be None or one of {allowed_values}"
            )
        self._query_type = query_type

    @property
    def bind_params(self):
        """
        Gets the bind_params of this DataObjectQuery.
        List of bind parameters to be applied in the query.


        :return: The bind_params of this DataObjectQuery.
        :rtype: list[oci.opsi.models.DataObjectBindParameter]
        """
        return self._bind_params

    @bind_params.setter
    def bind_params(self, bind_params):
        """
        Sets the bind_params of this DataObjectQuery.
        List of bind parameters to be applied in the query.


        :param bind_params: The bind_params of this DataObjectQuery.
        :type: list[oci.opsi.models.DataObjectBindParameter]
        """
        self._bind_params = bind_params

    @property
    def query_execution_timeout_in_seconds(self):
        """
        Gets the query_execution_timeout_in_seconds of this DataObjectQuery.
        Timeout (in seconds) to be set for the data object query execution.


        :return: The query_execution_timeout_in_seconds of this DataObjectQuery.
        :rtype: float
        """
        return self._query_execution_timeout_in_seconds

    @query_execution_timeout_in_seconds.setter
    def query_execution_timeout_in_seconds(self, query_execution_timeout_in_seconds):
        """
        Sets the query_execution_timeout_in_seconds of this DataObjectQuery.
        Timeout (in seconds) to be set for the data object query execution.


        :param query_execution_timeout_in_seconds: The query_execution_timeout_in_seconds of this DataObjectQuery.
        :type: float
        """
        self._query_execution_timeout_in_seconds = query_execution_timeout_in_seconds

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
