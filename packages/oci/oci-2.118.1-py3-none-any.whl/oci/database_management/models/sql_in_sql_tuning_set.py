# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SqlInSqlTuningSet(object):
    """
    Sql information in the Sql tuning set.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SqlInSqlTuningSet object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param sql_id:
            The value to assign to the sql_id property of this SqlInSqlTuningSet.
        :type sql_id: str

        :param sql_text:
            The value to assign to the sql_text property of this SqlInSqlTuningSet.
        :type sql_text: str

        :param container_database_id:
            The value to assign to the container_database_id property of this SqlInSqlTuningSet.
        :type container_database_id: int

        :param plan_hash_value:
            The value to assign to the plan_hash_value property of this SqlInSqlTuningSet.
        :type plan_hash_value: int

        :param schema:
            The value to assign to the schema property of this SqlInSqlTuningSet.
        :type schema: str

        :param module:
            The value to assign to the module property of this SqlInSqlTuningSet.
        :type module: str

        :param metrics:
            The value to assign to the metrics property of this SqlInSqlTuningSet.
        :type metrics: list[oci.database_management.models.SqlMetrics]

        """
        self.swagger_types = {
            'sql_id': 'str',
            'sql_text': 'str',
            'container_database_id': 'int',
            'plan_hash_value': 'int',
            'schema': 'str',
            'module': 'str',
            'metrics': 'list[SqlMetrics]'
        }

        self.attribute_map = {
            'sql_id': 'sqlId',
            'sql_text': 'sqlText',
            'container_database_id': 'containerDatabaseId',
            'plan_hash_value': 'planHashValue',
            'schema': 'schema',
            'module': 'module',
            'metrics': 'metrics'
        }

        self._sql_id = None
        self._sql_text = None
        self._container_database_id = None
        self._plan_hash_value = None
        self._schema = None
        self._module = None
        self._metrics = None

    @property
    def sql_id(self):
        """
        **[Required]** Gets the sql_id of this SqlInSqlTuningSet.
        The unique Sql identifier.


        :return: The sql_id of this SqlInSqlTuningSet.
        :rtype: str
        """
        return self._sql_id

    @sql_id.setter
    def sql_id(self, sql_id):
        """
        Sets the sql_id of this SqlInSqlTuningSet.
        The unique Sql identifier.


        :param sql_id: The sql_id of this SqlInSqlTuningSet.
        :type: str
        """
        self._sql_id = sql_id

    @property
    def sql_text(self):
        """
        Gets the sql_text of this SqlInSqlTuningSet.
        Sql text.


        :return: The sql_text of this SqlInSqlTuningSet.
        :rtype: str
        """
        return self._sql_text

    @sql_text.setter
    def sql_text(self, sql_text):
        """
        Sets the sql_text of this SqlInSqlTuningSet.
        Sql text.


        :param sql_text: The sql_text of this SqlInSqlTuningSet.
        :type: str
        """
        self._sql_text = sql_text

    @property
    def container_database_id(self):
        """
        Gets the container_database_id of this SqlInSqlTuningSet.
        The unique container database identifier.


        :return: The container_database_id of this SqlInSqlTuningSet.
        :rtype: int
        """
        return self._container_database_id

    @container_database_id.setter
    def container_database_id(self, container_database_id):
        """
        Sets the container_database_id of this SqlInSqlTuningSet.
        The unique container database identifier.


        :param container_database_id: The container_database_id of this SqlInSqlTuningSet.
        :type: int
        """
        self._container_database_id = container_database_id

    @property
    def plan_hash_value(self):
        """
        **[Required]** Gets the plan_hash_value of this SqlInSqlTuningSet.
        Plan hash value of the Sql statement.


        :return: The plan_hash_value of this SqlInSqlTuningSet.
        :rtype: int
        """
        return self._plan_hash_value

    @plan_hash_value.setter
    def plan_hash_value(self, plan_hash_value):
        """
        Sets the plan_hash_value of this SqlInSqlTuningSet.
        Plan hash value of the Sql statement.


        :param plan_hash_value: The plan_hash_value of this SqlInSqlTuningSet.
        :type: int
        """
        self._plan_hash_value = plan_hash_value

    @property
    def schema(self):
        """
        Gets the schema of this SqlInSqlTuningSet.
        The schema name of the Sql.


        :return: The schema of this SqlInSqlTuningSet.
        :rtype: str
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """
        Sets the schema of this SqlInSqlTuningSet.
        The schema name of the Sql.


        :param schema: The schema of this SqlInSqlTuningSet.
        :type: str
        """
        self._schema = schema

    @property
    def module(self):
        """
        Gets the module of this SqlInSqlTuningSet.
        The module of the Sql.


        :return: The module of this SqlInSqlTuningSet.
        :rtype: str
        """
        return self._module

    @module.setter
    def module(self, module):
        """
        Sets the module of this SqlInSqlTuningSet.
        The module of the Sql.


        :param module: The module of this SqlInSqlTuningSet.
        :type: str
        """
        self._module = module

    @property
    def metrics(self):
        """
        Gets the metrics of this SqlInSqlTuningSet.
        A list of the Sqls associated with the Sql tuning set.


        :return: The metrics of this SqlInSqlTuningSet.
        :rtype: list[oci.database_management.models.SqlMetrics]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """
        Sets the metrics of this SqlInSqlTuningSet.
        A list of the Sqls associated with the Sql tuning set.


        :param metrics: The metrics of this SqlInSqlTuningSet.
        :type: list[oci.database_management.models.SqlMetrics]
        """
        self._metrics = metrics

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
