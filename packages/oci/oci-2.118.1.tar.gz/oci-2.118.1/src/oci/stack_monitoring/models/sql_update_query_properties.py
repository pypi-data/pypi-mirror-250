# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210330

from .metric_extension_update_query_properties import MetricExtensionUpdateQueryProperties
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SqlUpdateQueryProperties(MetricExtensionUpdateQueryProperties):
    """
    Query Properties applicable to SQL type of collection method
    """

    #: A constant which can be used with the sql_type property of a SqlUpdateQueryProperties.
    #: This constant has a value of "STATEMENT"
    SQL_TYPE_STATEMENT = "STATEMENT"

    #: A constant which can be used with the sql_type property of a SqlUpdateQueryProperties.
    #: This constant has a value of "SQL_SCRIPT"
    SQL_TYPE_SQL_SCRIPT = "SQL_SCRIPT"

    def __init__(self, **kwargs):
        """
        Initializes a new SqlUpdateQueryProperties object with values from keyword arguments. The default value of the :py:attr:`~oci.stack_monitoring.models.SqlUpdateQueryProperties.collection_method` attribute
        of this class is ``SQL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param collection_method:
            The value to assign to the collection_method property of this SqlUpdateQueryProperties.
            Allowed values for this property are: "OS_COMMAND", "SQL", "JMX"
        :type collection_method: str

        :param sql_type:
            The value to assign to the sql_type property of this SqlUpdateQueryProperties.
            Allowed values for this property are: "STATEMENT", "SQL_SCRIPT"
        :type sql_type: str

        :param sql_details:
            The value to assign to the sql_details property of this SqlUpdateQueryProperties.
        :type sql_details: oci.stack_monitoring.models.SqlDetails

        :param in_param_details:
            The value to assign to the in_param_details property of this SqlUpdateQueryProperties.
        :type in_param_details: list[oci.stack_monitoring.models.SqlInParamDetails]

        :param out_param_details:
            The value to assign to the out_param_details property of this SqlUpdateQueryProperties.
        :type out_param_details: oci.stack_monitoring.models.SqlOutParamDetails

        """
        self.swagger_types = {
            'collection_method': 'str',
            'sql_type': 'str',
            'sql_details': 'SqlDetails',
            'in_param_details': 'list[SqlInParamDetails]',
            'out_param_details': 'SqlOutParamDetails'
        }

        self.attribute_map = {
            'collection_method': 'collectionMethod',
            'sql_type': 'sqlType',
            'sql_details': 'sqlDetails',
            'in_param_details': 'inParamDetails',
            'out_param_details': 'outParamDetails'
        }

        self._collection_method = None
        self._sql_type = None
        self._sql_details = None
        self._in_param_details = None
        self._out_param_details = None
        self._collection_method = 'SQL'

    @property
    def sql_type(self):
        """
        Gets the sql_type of this SqlUpdateQueryProperties.
        Type of SQL data collection method i.e. either a Statement or SQL Script File

        Allowed values for this property are: "STATEMENT", "SQL_SCRIPT"


        :return: The sql_type of this SqlUpdateQueryProperties.
        :rtype: str
        """
        return self._sql_type

    @sql_type.setter
    def sql_type(self, sql_type):
        """
        Sets the sql_type of this SqlUpdateQueryProperties.
        Type of SQL data collection method i.e. either a Statement or SQL Script File


        :param sql_type: The sql_type of this SqlUpdateQueryProperties.
        :type: str
        """
        allowed_values = ["STATEMENT", "SQL_SCRIPT"]
        if not value_allowed_none_or_none_sentinel(sql_type, allowed_values):
            raise ValueError(
                f"Invalid value for `sql_type`, must be None or one of {allowed_values}"
            )
        self._sql_type = sql_type

    @property
    def sql_details(self):
        """
        Gets the sql_details of this SqlUpdateQueryProperties.

        :return: The sql_details of this SqlUpdateQueryProperties.
        :rtype: oci.stack_monitoring.models.SqlDetails
        """
        return self._sql_details

    @sql_details.setter
    def sql_details(self, sql_details):
        """
        Sets the sql_details of this SqlUpdateQueryProperties.

        :param sql_details: The sql_details of this SqlUpdateQueryProperties.
        :type: oci.stack_monitoring.models.SqlDetails
        """
        self._sql_details = sql_details

    @property
    def in_param_details(self):
        """
        Gets the in_param_details of this SqlUpdateQueryProperties.
        List of values and position of PL/SQL procedure IN parameters


        :return: The in_param_details of this SqlUpdateQueryProperties.
        :rtype: list[oci.stack_monitoring.models.SqlInParamDetails]
        """
        return self._in_param_details

    @in_param_details.setter
    def in_param_details(self, in_param_details):
        """
        Sets the in_param_details of this SqlUpdateQueryProperties.
        List of values and position of PL/SQL procedure IN parameters


        :param in_param_details: The in_param_details of this SqlUpdateQueryProperties.
        :type: list[oci.stack_monitoring.models.SqlInParamDetails]
        """
        self._in_param_details = in_param_details

    @property
    def out_param_details(self):
        """
        Gets the out_param_details of this SqlUpdateQueryProperties.

        :return: The out_param_details of this SqlUpdateQueryProperties.
        :rtype: oci.stack_monitoring.models.SqlOutParamDetails
        """
        return self._out_param_details

    @out_param_details.setter
    def out_param_details(self, out_param_details):
        """
        Sets the out_param_details of this SqlUpdateQueryProperties.

        :param out_param_details: The out_param_details of this SqlUpdateQueryProperties.
        :type: oci.stack_monitoring.models.SqlOutParamDetails
        """
        self._out_param_details = out_param_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
