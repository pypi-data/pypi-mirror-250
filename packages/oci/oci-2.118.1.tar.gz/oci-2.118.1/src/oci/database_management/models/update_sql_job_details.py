# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101

from .update_job_details import UpdateJobDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateSqlJobDetails(UpdateJobDetails):
    """
    The details specific to the SQL job request.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateSqlJobDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.UpdateSqlJobDetails.job_type` attribute
        of this class is ``SQL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param description:
            The value to assign to the description property of this UpdateSqlJobDetails.
        :type description: str

        :param job_type:
            The value to assign to the job_type property of this UpdateSqlJobDetails.
            Allowed values for this property are: "SQL"
        :type job_type: str

        :param timeout:
            The value to assign to the timeout property of this UpdateSqlJobDetails.
        :type timeout: str

        :param result_location:
            The value to assign to the result_location property of this UpdateSqlJobDetails.
        :type result_location: oci.database_management.models.JobExecutionResultLocation

        :param schedule_details:
            The value to assign to the schedule_details property of this UpdateSqlJobDetails.
        :type schedule_details: oci.database_management.models.JobScheduleDetails

        :param sql_text:
            The value to assign to the sql_text property of this UpdateSqlJobDetails.
        :type sql_text: str

        :param in_binds:
            The value to assign to the in_binds property of this UpdateSqlJobDetails.
        :type in_binds: oci.database_management.models.JobInBindsDetails

        :param out_binds:
            The value to assign to the out_binds property of this UpdateSqlJobDetails.
        :type out_binds: oci.database_management.models.JobOutBindsDetails

        :param sql_type:
            The value to assign to the sql_type property of this UpdateSqlJobDetails.
        :type sql_type: str

        :param user_name:
            The value to assign to the user_name property of this UpdateSqlJobDetails.
        :type user_name: str

        :param password:
            The value to assign to the password property of this UpdateSqlJobDetails.
        :type password: str

        :param secret_id:
            The value to assign to the secret_id property of this UpdateSqlJobDetails.
        :type secret_id: str

        :param role:
            The value to assign to the role property of this UpdateSqlJobDetails.
        :type role: str

        """
        self.swagger_types = {
            'description': 'str',
            'job_type': 'str',
            'timeout': 'str',
            'result_location': 'JobExecutionResultLocation',
            'schedule_details': 'JobScheduleDetails',
            'sql_text': 'str',
            'in_binds': 'JobInBindsDetails',
            'out_binds': 'JobOutBindsDetails',
            'sql_type': 'str',
            'user_name': 'str',
            'password': 'str',
            'secret_id': 'str',
            'role': 'str'
        }

        self.attribute_map = {
            'description': 'description',
            'job_type': 'jobType',
            'timeout': 'timeout',
            'result_location': 'resultLocation',
            'schedule_details': 'scheduleDetails',
            'sql_text': 'sqlText',
            'in_binds': 'inBinds',
            'out_binds': 'outBinds',
            'sql_type': 'sqlType',
            'user_name': 'userName',
            'password': 'password',
            'secret_id': 'secretId',
            'role': 'role'
        }

        self._description = None
        self._job_type = None
        self._timeout = None
        self._result_location = None
        self._schedule_details = None
        self._sql_text = None
        self._in_binds = None
        self._out_binds = None
        self._sql_type = None
        self._user_name = None
        self._password = None
        self._secret_id = None
        self._role = None
        self._job_type = 'SQL'

    @property
    def sql_text(self):
        """
        Gets the sql_text of this UpdateSqlJobDetails.
        The SQL text to be executed as part of the job.


        :return: The sql_text of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._sql_text

    @sql_text.setter
    def sql_text(self, sql_text):
        """
        Sets the sql_text of this UpdateSqlJobDetails.
        The SQL text to be executed as part of the job.


        :param sql_text: The sql_text of this UpdateSqlJobDetails.
        :type: str
        """
        self._sql_text = sql_text

    @property
    def in_binds(self):
        """
        Gets the in_binds of this UpdateSqlJobDetails.

        :return: The in_binds of this UpdateSqlJobDetails.
        :rtype: oci.database_management.models.JobInBindsDetails
        """
        return self._in_binds

    @in_binds.setter
    def in_binds(self, in_binds):
        """
        Sets the in_binds of this UpdateSqlJobDetails.

        :param in_binds: The in_binds of this UpdateSqlJobDetails.
        :type: oci.database_management.models.JobInBindsDetails
        """
        self._in_binds = in_binds

    @property
    def out_binds(self):
        """
        Gets the out_binds of this UpdateSqlJobDetails.

        :return: The out_binds of this UpdateSqlJobDetails.
        :rtype: oci.database_management.models.JobOutBindsDetails
        """
        return self._out_binds

    @out_binds.setter
    def out_binds(self, out_binds):
        """
        Sets the out_binds of this UpdateSqlJobDetails.

        :param out_binds: The out_binds of this UpdateSqlJobDetails.
        :type: oci.database_management.models.JobOutBindsDetails
        """
        self._out_binds = out_binds

    @property
    def sql_type(self):
        """
        Gets the sql_type of this UpdateSqlJobDetails.

        :return: The sql_type of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._sql_type

    @sql_type.setter
    def sql_type(self, sql_type):
        """
        Sets the sql_type of this UpdateSqlJobDetails.

        :param sql_type: The sql_type of this UpdateSqlJobDetails.
        :type: str
        """
        self._sql_type = sql_type

    @property
    def user_name(self):
        """
        Gets the user_name of this UpdateSqlJobDetails.
        The database user name used to execute the SQL job. If the job is being executed on a
        Managed Database Group, then the user name should exist on all the databases in the
        group with the same password.


        :return: The user_name of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this UpdateSqlJobDetails.
        The database user name used to execute the SQL job. If the job is being executed on a
        Managed Database Group, then the user name should exist on all the databases in the
        group with the same password.


        :param user_name: The user_name of this UpdateSqlJobDetails.
        :type: str
        """
        self._user_name = user_name

    @property
    def password(self):
        """
        Gets the password of this UpdateSqlJobDetails.
        The password for the database user name used to execute the SQL job.


        :return: The password of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this UpdateSqlJobDetails.
        The password for the database user name used to execute the SQL job.


        :param password: The password of this UpdateSqlJobDetails.
        :type: str
        """
        self._password = password

    @property
    def secret_id(self):
        """
        Gets the secret_id of this UpdateSqlJobDetails.
        The `OCID`__ of the secret containing the user password.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The secret_id of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._secret_id

    @secret_id.setter
    def secret_id(self, secret_id):
        """
        Sets the secret_id of this UpdateSqlJobDetails.
        The `OCID`__ of the secret containing the user password.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param secret_id: The secret_id of this UpdateSqlJobDetails.
        :type: str
        """
        self._secret_id = secret_id

    @property
    def role(self):
        """
        Gets the role of this UpdateSqlJobDetails.
        The role of the database user. Indicates whether the database user is a normal user or sysdba.


        :return: The role of this UpdateSqlJobDetails.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this UpdateSqlJobDetails.
        The role of the database user. Indicates whether the database user is a normal user or sysdba.


        :param role: The role of this UpdateSqlJobDetails.
        :type: str
        """
        self._role = role

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
