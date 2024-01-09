# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190801


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SoftwarePackage(object):
    """
    The details for a software package
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SoftwarePackage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this SoftwarePackage.
        :type display_name: str

        :param name:
            The value to assign to the name property of this SoftwarePackage.
        :type name: str

        :param type:
            The value to assign to the type property of this SoftwarePackage.
        :type type: str

        :param version:
            The value to assign to the version property of this SoftwarePackage.
        :type version: str

        :param architecture:
            The value to assign to the architecture property of this SoftwarePackage.
        :type architecture: str

        :param last_modified_date:
            The value to assign to the last_modified_date property of this SoftwarePackage.
        :type last_modified_date: str

        :param checksum:
            The value to assign to the checksum property of this SoftwarePackage.
        :type checksum: str

        :param checksum_type:
            The value to assign to the checksum_type property of this SoftwarePackage.
        :type checksum_type: str

        :param description:
            The value to assign to the description property of this SoftwarePackage.
        :type description: str

        :param size_in_bytes:
            The value to assign to the size_in_bytes property of this SoftwarePackage.
        :type size_in_bytes: int

        :param dependencies:
            The value to assign to the dependencies property of this SoftwarePackage.
        :type dependencies: list[oci.os_management.models.SoftwarePackageDependency]

        :param files:
            The value to assign to the files property of this SoftwarePackage.
        :type files: list[oci.os_management.models.SoftwarePackageFile]

        :param software_sources:
            The value to assign to the software_sources property of this SoftwarePackage.
        :type software_sources: list[oci.os_management.models.SoftwareSourceId]

        """
        self.swagger_types = {
            'display_name': 'str',
            'name': 'str',
            'type': 'str',
            'version': 'str',
            'architecture': 'str',
            'last_modified_date': 'str',
            'checksum': 'str',
            'checksum_type': 'str',
            'description': 'str',
            'size_in_bytes': 'int',
            'dependencies': 'list[SoftwarePackageDependency]',
            'files': 'list[SoftwarePackageFile]',
            'software_sources': 'list[SoftwareSourceId]'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'name': 'name',
            'type': 'type',
            'version': 'version',
            'architecture': 'architecture',
            'last_modified_date': 'lastModifiedDate',
            'checksum': 'checksum',
            'checksum_type': 'checksumType',
            'description': 'description',
            'size_in_bytes': 'sizeInBytes',
            'dependencies': 'dependencies',
            'files': 'files',
            'software_sources': 'softwareSources'
        }

        self._display_name = None
        self._name = None
        self._type = None
        self._version = None
        self._architecture = None
        self._last_modified_date = None
        self._checksum = None
        self._checksum_type = None
        self._description = None
        self._size_in_bytes = None
        self._dependencies = None
        self._files = None
        self._software_sources = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this SoftwarePackage.
        Package name


        :return: The display_name of this SoftwarePackage.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this SoftwarePackage.
        Package name


        :param display_name: The display_name of this SoftwarePackage.
        :type: str
        """
        self._display_name = display_name

    @property
    def name(self):
        """
        **[Required]** Gets the name of this SoftwarePackage.
        Unique identifier for the package. NOTE - This is not an OCID


        :return: The name of this SoftwarePackage.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SoftwarePackage.
        Unique identifier for the package. NOTE - This is not an OCID


        :param name: The name of this SoftwarePackage.
        :type: str
        """
        self._name = name

    @property
    def type(self):
        """
        **[Required]** Gets the type of this SoftwarePackage.
        Type of the package


        :return: The type of this SoftwarePackage.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this SoftwarePackage.
        Type of the package


        :param type: The type of this SoftwarePackage.
        :type: str
        """
        self._type = type

    @property
    def version(self):
        """
        **[Required]** Gets the version of this SoftwarePackage.
        Version of the package


        :return: The version of this SoftwarePackage.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this SoftwarePackage.
        Version of the package


        :param version: The version of this SoftwarePackage.
        :type: str
        """
        self._version = version

    @property
    def architecture(self):
        """
        Gets the architecture of this SoftwarePackage.
        the architecture for which this software was built


        :return: The architecture of this SoftwarePackage.
        :rtype: str
        """
        return self._architecture

    @architecture.setter
    def architecture(self, architecture):
        """
        Sets the architecture of this SoftwarePackage.
        the architecture for which this software was built


        :param architecture: The architecture of this SoftwarePackage.
        :type: str
        """
        self._architecture = architecture

    @property
    def last_modified_date(self):
        """
        Gets the last_modified_date of this SoftwarePackage.
        date of the last update to the package


        :return: The last_modified_date of this SoftwarePackage.
        :rtype: str
        """
        return self._last_modified_date

    @last_modified_date.setter
    def last_modified_date(self, last_modified_date):
        """
        Sets the last_modified_date of this SoftwarePackage.
        date of the last update to the package


        :param last_modified_date: The last_modified_date of this SoftwarePackage.
        :type: str
        """
        self._last_modified_date = last_modified_date

    @property
    def checksum(self):
        """
        Gets the checksum of this SoftwarePackage.
        checksum of the package


        :return: The checksum of this SoftwarePackage.
        :rtype: str
        """
        return self._checksum

    @checksum.setter
    def checksum(self, checksum):
        """
        Sets the checksum of this SoftwarePackage.
        checksum of the package


        :param checksum: The checksum of this SoftwarePackage.
        :type: str
        """
        self._checksum = checksum

    @property
    def checksum_type(self):
        """
        Gets the checksum_type of this SoftwarePackage.
        type of the checksum


        :return: The checksum_type of this SoftwarePackage.
        :rtype: str
        """
        return self._checksum_type

    @checksum_type.setter
    def checksum_type(self, checksum_type):
        """
        Sets the checksum_type of this SoftwarePackage.
        type of the checksum


        :param checksum_type: The checksum_type of this SoftwarePackage.
        :type: str
        """
        self._checksum_type = checksum_type

    @property
    def description(self):
        """
        Gets the description of this SoftwarePackage.
        description of the package


        :return: The description of this SoftwarePackage.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this SoftwarePackage.
        description of the package


        :param description: The description of this SoftwarePackage.
        :type: str
        """
        self._description = description

    @property
    def size_in_bytes(self):
        """
        Gets the size_in_bytes of this SoftwarePackage.
        size of the package in bytes


        :return: The size_in_bytes of this SoftwarePackage.
        :rtype: int
        """
        return self._size_in_bytes

    @size_in_bytes.setter
    def size_in_bytes(self, size_in_bytes):
        """
        Sets the size_in_bytes of this SoftwarePackage.
        size of the package in bytes


        :param size_in_bytes: The size_in_bytes of this SoftwarePackage.
        :type: int
        """
        self._size_in_bytes = size_in_bytes

    @property
    def dependencies(self):
        """
        Gets the dependencies of this SoftwarePackage.
        list of dependencies for the software package


        :return: The dependencies of this SoftwarePackage.
        :rtype: list[oci.os_management.models.SoftwarePackageDependency]
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies):
        """
        Sets the dependencies of this SoftwarePackage.
        list of dependencies for the software package


        :param dependencies: The dependencies of this SoftwarePackage.
        :type: list[oci.os_management.models.SoftwarePackageDependency]
        """
        self._dependencies = dependencies

    @property
    def files(self):
        """
        Gets the files of this SoftwarePackage.
        list of files for the software package


        :return: The files of this SoftwarePackage.
        :rtype: list[oci.os_management.models.SoftwarePackageFile]
        """
        return self._files

    @files.setter
    def files(self, files):
        """
        Sets the files of this SoftwarePackage.
        list of files for the software package


        :param files: The files of this SoftwarePackage.
        :type: list[oci.os_management.models.SoftwarePackageFile]
        """
        self._files = files

    @property
    def software_sources(self):
        """
        Gets the software_sources of this SoftwarePackage.
        list of software sources that provide the software package


        :return: The software_sources of this SoftwarePackage.
        :rtype: list[oci.os_management.models.SoftwareSourceId]
        """
        return self._software_sources

    @software_sources.setter
    def software_sources(self, software_sources):
        """
        Sets the software_sources of this SoftwarePackage.
        list of software sources that provide the software package


        :param software_sources: The software_sources of this SoftwarePackage.
        :type: list[oci.os_management.models.SoftwareSourceId]
        """
        self._software_sources = software_sources

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
