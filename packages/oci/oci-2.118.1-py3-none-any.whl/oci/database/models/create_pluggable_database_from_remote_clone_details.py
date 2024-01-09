# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918

from .create_pluggable_database_creation_type_details import CreatePluggableDatabaseCreationTypeDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreatePluggableDatabaseFromRemoteCloneDetails(CreatePluggableDatabaseCreationTypeDetails):
    """
    Specifies the creation type Remote Clone.
    Additional input 'dblinkUsername` and `dblinkUserPassword` can be provided for RemoteClone/Create RefreshableClone Operation.
    If not provided, Backend will create a temporary user to perform RemoteClone operation. It is a required input parameter in case of creating Refreshable Clone PDB.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreatePluggableDatabaseFromRemoteCloneDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.database.models.CreatePluggableDatabaseFromRemoteCloneDetails.creation_type` attribute
        of this class is ``REMOTE_CLONE_PDB`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param creation_type:
            The value to assign to the creation_type property of this CreatePluggableDatabaseFromRemoteCloneDetails.
            Allowed values for this property are: "LOCAL_CLONE_PDB", "REMOTE_CLONE_PDB", "RELOCATE_PDB"
        :type creation_type: str

        :param dblink_username:
            The value to assign to the dblink_username property of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type dblink_username: str

        :param dblink_user_password:
            The value to assign to the dblink_user_password property of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type dblink_user_password: str

        :param source_pluggable_database_id:
            The value to assign to the source_pluggable_database_id property of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type source_pluggable_database_id: str

        :param source_container_database_admin_password:
            The value to assign to the source_container_database_admin_password property of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type source_container_database_admin_password: str

        :param refreshable_clone_details:
            The value to assign to the refreshable_clone_details property of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type refreshable_clone_details: oci.database.models.CreatePluggableDatabaseRefreshableCloneDetails

        """
        self.swagger_types = {
            'creation_type': 'str',
            'dblink_username': 'str',
            'dblink_user_password': 'str',
            'source_pluggable_database_id': 'str',
            'source_container_database_admin_password': 'str',
            'refreshable_clone_details': 'CreatePluggableDatabaseRefreshableCloneDetails'
        }

        self.attribute_map = {
            'creation_type': 'creationType',
            'dblink_username': 'dblinkUsername',
            'dblink_user_password': 'dblinkUserPassword',
            'source_pluggable_database_id': 'sourcePluggableDatabaseId',
            'source_container_database_admin_password': 'sourceContainerDatabaseAdminPassword',
            'refreshable_clone_details': 'refreshableCloneDetails'
        }

        self._creation_type = None
        self._dblink_username = None
        self._dblink_user_password = None
        self._source_pluggable_database_id = None
        self._source_container_database_admin_password = None
        self._refreshable_clone_details = None
        self._creation_type = 'REMOTE_CLONE_PDB'

    @property
    def dblink_username(self):
        """
        Gets the dblink_username of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The name of the DB link user.


        :return: The dblink_username of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :rtype: str
        """
        return self._dblink_username

    @dblink_username.setter
    def dblink_username(self, dblink_username):
        """
        Sets the dblink_username of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The name of the DB link user.


        :param dblink_username: The dblink_username of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type: str
        """
        self._dblink_username = dblink_username

    @property
    def dblink_user_password(self):
        """
        Gets the dblink_user_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The DB link user password.


        :return: The dblink_user_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :rtype: str
        """
        return self._dblink_user_password

    @dblink_user_password.setter
    def dblink_user_password(self, dblink_user_password):
        """
        Sets the dblink_user_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The DB link user password.


        :param dblink_user_password: The dblink_user_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type: str
        """
        self._dblink_user_password = dblink_user_password

    @property
    def source_pluggable_database_id(self):
        """
        **[Required]** Gets the source_pluggable_database_id of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The OCID of the Source Pluggable Database.


        :return: The source_pluggable_database_id of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :rtype: str
        """
        return self._source_pluggable_database_id

    @source_pluggable_database_id.setter
    def source_pluggable_database_id(self, source_pluggable_database_id):
        """
        Sets the source_pluggable_database_id of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The OCID of the Source Pluggable Database.


        :param source_pluggable_database_id: The source_pluggable_database_id of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type: str
        """
        self._source_pluggable_database_id = source_pluggable_database_id

    @property
    def source_container_database_admin_password(self):
        """
        **[Required]** Gets the source_container_database_admin_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The DB system administrator password of the source Container Database.


        :return: The source_container_database_admin_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :rtype: str
        """
        return self._source_container_database_admin_password

    @source_container_database_admin_password.setter
    def source_container_database_admin_password(self, source_container_database_admin_password):
        """
        Sets the source_container_database_admin_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        The DB system administrator password of the source Container Database.


        :param source_container_database_admin_password: The source_container_database_admin_password of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type: str
        """
        self._source_container_database_admin_password = source_container_database_admin_password

    @property
    def refreshable_clone_details(self):
        """
        Gets the refreshable_clone_details of this CreatePluggableDatabaseFromRemoteCloneDetails.

        :return: The refreshable_clone_details of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :rtype: oci.database.models.CreatePluggableDatabaseRefreshableCloneDetails
        """
        return self._refreshable_clone_details

    @refreshable_clone_details.setter
    def refreshable_clone_details(self, refreshable_clone_details):
        """
        Sets the refreshable_clone_details of this CreatePluggableDatabaseFromRemoteCloneDetails.

        :param refreshable_clone_details: The refreshable_clone_details of this CreatePluggableDatabaseFromRemoteCloneDetails.
        :type: oci.database.models.CreatePluggableDatabaseRefreshableCloneDetails
        """
        self._refreshable_clone_details = refreshable_clone_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
