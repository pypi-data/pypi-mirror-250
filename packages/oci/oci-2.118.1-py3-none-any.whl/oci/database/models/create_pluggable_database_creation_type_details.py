# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreatePluggableDatabaseCreationTypeDetails(object):
    """
    The Pluggable Database creation type.
    Use `LOCAL_CLONE_PDB` for creating a new PDB using Local Clone on Source Pluggable Database. This will Clone and starts a
    pluggable database (PDB) in the same database (CDB) as the source PDB. The source PDB must be in the `READ_WRITE` openMode to
    perform the clone operation.
    Use `REMOTE_CLONE_PDB` for creating a new PDB using Remote Clone on Source Pluggable Database. This will Clone a pluggable
    database (PDB) to a different database from the source PDB. The cloned PDB will be started upon completion of the clone
    operation. The source PDB must be in the `READ_WRITE` openMode when performing the clone.
    For Exadata Cloud@Customer instances, the source pluggable database (PDB) must be on the same Exadata Infrastructure as the
    target container database (CDB) to create a remote clone.

    Use `RELOCATE_PDB` for relocating the Pluggable Database from Source CDB and creating it in target CDB. This will relocate a
    pluggable database (PDB) to a different database from the source PDB. The source PDB must be in the `READ_WRITE` openMode when
    performing the relocate.
    """

    #: A constant which can be used with the creation_type property of a CreatePluggableDatabaseCreationTypeDetails.
    #: This constant has a value of "LOCAL_CLONE_PDB"
    CREATION_TYPE_LOCAL_CLONE_PDB = "LOCAL_CLONE_PDB"

    #: A constant which can be used with the creation_type property of a CreatePluggableDatabaseCreationTypeDetails.
    #: This constant has a value of "REMOTE_CLONE_PDB"
    CREATION_TYPE_REMOTE_CLONE_PDB = "REMOTE_CLONE_PDB"

    #: A constant which can be used with the creation_type property of a CreatePluggableDatabaseCreationTypeDetails.
    #: This constant has a value of "RELOCATE_PDB"
    CREATION_TYPE_RELOCATE_PDB = "RELOCATE_PDB"

    def __init__(self, **kwargs):
        """
        Initializes a new CreatePluggableDatabaseCreationTypeDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database.models.CreatePluggableDatabaseFromRelocateDetails`
        * :class:`~oci.database.models.CreatePluggableDatabaseFromRemoteCloneDetails`
        * :class:`~oci.database.models.CreatePluggableDatabaseFromLocalCloneDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param creation_type:
            The value to assign to the creation_type property of this CreatePluggableDatabaseCreationTypeDetails.
            Allowed values for this property are: "LOCAL_CLONE_PDB", "REMOTE_CLONE_PDB", "RELOCATE_PDB"
        :type creation_type: str

        """
        self.swagger_types = {
            'creation_type': 'str'
        }

        self.attribute_map = {
            'creation_type': 'creationType'
        }

        self._creation_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['creationType']

        if type == 'RELOCATE_PDB':
            return 'CreatePluggableDatabaseFromRelocateDetails'

        if type == 'REMOTE_CLONE_PDB':
            return 'CreatePluggableDatabaseFromRemoteCloneDetails'

        if type == 'LOCAL_CLONE_PDB':
            return 'CreatePluggableDatabaseFromLocalCloneDetails'
        else:
            return 'CreatePluggableDatabaseCreationTypeDetails'

    @property
    def creation_type(self):
        """
        **[Required]** Gets the creation_type of this CreatePluggableDatabaseCreationTypeDetails.
        The Pluggable Database creation type.

        Allowed values for this property are: "LOCAL_CLONE_PDB", "REMOTE_CLONE_PDB", "RELOCATE_PDB"


        :return: The creation_type of this CreatePluggableDatabaseCreationTypeDetails.
        :rtype: str
        """
        return self._creation_type

    @creation_type.setter
    def creation_type(self, creation_type):
        """
        Sets the creation_type of this CreatePluggableDatabaseCreationTypeDetails.
        The Pluggable Database creation type.


        :param creation_type: The creation_type of this CreatePluggableDatabaseCreationTypeDetails.
        :type: str
        """
        allowed_values = ["LOCAL_CLONE_PDB", "REMOTE_CLONE_PDB", "RELOCATE_PDB"]
        if not value_allowed_none_or_none_sentinel(creation_type, allowed_values):
            raise ValueError(
                f"Invalid value for `creation_type`, must be None or one of {allowed_values}"
            )
        self._creation_type = creation_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
