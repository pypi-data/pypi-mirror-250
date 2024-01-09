# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LoadSqlPlanBaselinesFromAwrDetails(object):
    """
    The details required to load plans from Automatic Workload Repository (AWR).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LoadSqlPlanBaselinesFromAwrDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param job_name:
            The value to assign to the job_name property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type job_name: str

        :param job_description:
            The value to assign to the job_description property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type job_description: str

        :param begin_snapshot:
            The value to assign to the begin_snapshot property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type begin_snapshot: int

        :param end_snapshot:
            The value to assign to the end_snapshot property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type end_snapshot: int

        :param sql_text_filter:
            The value to assign to the sql_text_filter property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type sql_text_filter: str

        :param is_fixed:
            The value to assign to the is_fixed property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type is_fixed: bool

        :param is_enabled:
            The value to assign to the is_enabled property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type is_enabled: bool

        :param credentials:
            The value to assign to the credentials property of this LoadSqlPlanBaselinesFromAwrDetails.
        :type credentials: oci.database_management.models.ManagedDatabaseCredential

        """
        self.swagger_types = {
            'job_name': 'str',
            'job_description': 'str',
            'begin_snapshot': 'int',
            'end_snapshot': 'int',
            'sql_text_filter': 'str',
            'is_fixed': 'bool',
            'is_enabled': 'bool',
            'credentials': 'ManagedDatabaseCredential'
        }

        self.attribute_map = {
            'job_name': 'jobName',
            'job_description': 'jobDescription',
            'begin_snapshot': 'beginSnapshot',
            'end_snapshot': 'endSnapshot',
            'sql_text_filter': 'sqlTextFilter',
            'is_fixed': 'isFixed',
            'is_enabled': 'isEnabled',
            'credentials': 'credentials'
        }

        self._job_name = None
        self._job_description = None
        self._begin_snapshot = None
        self._end_snapshot = None
        self._sql_text_filter = None
        self._is_fixed = None
        self._is_enabled = None
        self._credentials = None

    @property
    def job_name(self):
        """
        **[Required]** Gets the job_name of this LoadSqlPlanBaselinesFromAwrDetails.
        The name of the database job used for loading SQL plan baselines.


        :return: The job_name of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: str
        """
        return self._job_name

    @job_name.setter
    def job_name(self, job_name):
        """
        Sets the job_name of this LoadSqlPlanBaselinesFromAwrDetails.
        The name of the database job used for loading SQL plan baselines.


        :param job_name: The job_name of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: str
        """
        self._job_name = job_name

    @property
    def job_description(self):
        """
        Gets the job_description of this LoadSqlPlanBaselinesFromAwrDetails.
        The description of the job.


        :return: The job_description of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: str
        """
        return self._job_description

    @job_description.setter
    def job_description(self, job_description):
        """
        Sets the job_description of this LoadSqlPlanBaselinesFromAwrDetails.
        The description of the job.


        :param job_description: The job_description of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: str
        """
        self._job_description = job_description

    @property
    def begin_snapshot(self):
        """
        **[Required]** Gets the begin_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        The begin snapshot.


        :return: The begin_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: int
        """
        return self._begin_snapshot

    @begin_snapshot.setter
    def begin_snapshot(self, begin_snapshot):
        """
        Sets the begin_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        The begin snapshot.


        :param begin_snapshot: The begin_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: int
        """
        self._begin_snapshot = begin_snapshot

    @property
    def end_snapshot(self):
        """
        **[Required]** Gets the end_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        The end snapshot.


        :return: The end_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: int
        """
        return self._end_snapshot

    @end_snapshot.setter
    def end_snapshot(self, end_snapshot):
        """
        Sets the end_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        The end snapshot.


        :param end_snapshot: The end_snapshot of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: int
        """
        self._end_snapshot = end_snapshot

    @property
    def sql_text_filter(self):
        """
        Gets the sql_text_filter of this LoadSqlPlanBaselinesFromAwrDetails.
        A filter applied to AWR to select only qualifying plans to be loaded.
        By default all plans in AWR are selected. The filter can take the form of
        any `WHERE` clause predicate that can be specified against the column
        `DBA_HIST_SQLTEXT.SQL_TEXT`. An example is `sql_text like 'SELECT %'`.


        :return: The sql_text_filter of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: str
        """
        return self._sql_text_filter

    @sql_text_filter.setter
    def sql_text_filter(self, sql_text_filter):
        """
        Sets the sql_text_filter of this LoadSqlPlanBaselinesFromAwrDetails.
        A filter applied to AWR to select only qualifying plans to be loaded.
        By default all plans in AWR are selected. The filter can take the form of
        any `WHERE` clause predicate that can be specified against the column
        `DBA_HIST_SQLTEXT.SQL_TEXT`. An example is `sql_text like 'SELECT %'`.


        :param sql_text_filter: The sql_text_filter of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: str
        """
        self._sql_text_filter = sql_text_filter

    @property
    def is_fixed(self):
        """
        Gets the is_fixed of this LoadSqlPlanBaselinesFromAwrDetails.
        Indicates whether the plans are loaded as fixed plans (`true`) or non-fixed plans (`false`).
        By default, they are loaded as non-fixed plans.


        :return: The is_fixed of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: bool
        """
        return self._is_fixed

    @is_fixed.setter
    def is_fixed(self, is_fixed):
        """
        Sets the is_fixed of this LoadSqlPlanBaselinesFromAwrDetails.
        Indicates whether the plans are loaded as fixed plans (`true`) or non-fixed plans (`false`).
        By default, they are loaded as non-fixed plans.


        :param is_fixed: The is_fixed of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: bool
        """
        self._is_fixed = is_fixed

    @property
    def is_enabled(self):
        """
        Gets the is_enabled of this LoadSqlPlanBaselinesFromAwrDetails.
        Indicates whether the loaded plans are enabled (`true`) or not (`false`).
        By default, they are enabled.


        :return: The is_enabled of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this LoadSqlPlanBaselinesFromAwrDetails.
        Indicates whether the loaded plans are enabled (`true`) or not (`false`).
        By default, they are enabled.


        :param is_enabled: The is_enabled of this LoadSqlPlanBaselinesFromAwrDetails.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def credentials(self):
        """
        **[Required]** Gets the credentials of this LoadSqlPlanBaselinesFromAwrDetails.

        :return: The credentials of this LoadSqlPlanBaselinesFromAwrDetails.
        :rtype: oci.database_management.models.ManagedDatabaseCredential
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this LoadSqlPlanBaselinesFromAwrDetails.

        :param credentials: The credentials of this LoadSqlPlanBaselinesFromAwrDetails.
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
