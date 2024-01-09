# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200430


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TypeSystem(object):
    """
    The type system maps from and to a type.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TypeSystem object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this TypeSystem.
        :type key: str

        :param model_type:
            The value to assign to the model_type property of this TypeSystem.
        :type model_type: str

        :param model_version:
            The value to assign to the model_version property of this TypeSystem.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this TypeSystem.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this TypeSystem.
        :type name: str

        :param description:
            The value to assign to the description property of this TypeSystem.
        :type description: str

        :param object_version:
            The value to assign to the object_version property of this TypeSystem.
        :type object_version: int

        :param type_mapping_to:
            The value to assign to the type_mapping_to property of this TypeSystem.
        :type type_mapping_to: dict(str, str)

        :param type_mapping_from:
            The value to assign to the type_mapping_from property of this TypeSystem.
        :type type_mapping_from: dict(str, str)

        :param object_status:
            The value to assign to the object_status property of this TypeSystem.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this TypeSystem.
        :type identifier: str

        :param types:
            The value to assign to the types property of this TypeSystem.
        :type types: list[oci.data_integration.models.DataType]

        """
        self.swagger_types = {
            'key': 'str',
            'model_type': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_version': 'int',
            'type_mapping_to': 'dict(str, str)',
            'type_mapping_from': 'dict(str, str)',
            'object_status': 'int',
            'identifier': 'str',
            'types': 'list[DataType]'
        }

        self.attribute_map = {
            'key': 'key',
            'model_type': 'modelType',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_version': 'objectVersion',
            'type_mapping_to': 'typeMappingTo',
            'type_mapping_from': 'typeMappingFrom',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'types': 'types'
        }

        self._key = None
        self._model_type = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_version = None
        self._type_mapping_to = None
        self._type_mapping_from = None
        self._object_status = None
        self._identifier = None
        self._types = None

    @property
    def key(self):
        """
        Gets the key of this TypeSystem.
        The key of the object.


        :return: The key of this TypeSystem.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this TypeSystem.
        The key of the object.


        :param key: The key of this TypeSystem.
        :type: str
        """
        self._key = key

    @property
    def model_type(self):
        """
        Gets the model_type of this TypeSystem.
        The type of the object.


        :return: The model_type of this TypeSystem.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this TypeSystem.
        The type of the object.


        :param model_type: The model_type of this TypeSystem.
        :type: str
        """
        self._model_type = model_type

    @property
    def model_version(self):
        """
        Gets the model_version of this TypeSystem.
        The model version of an object.


        :return: The model_version of this TypeSystem.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this TypeSystem.
        The model version of an object.


        :param model_version: The model_version of this TypeSystem.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this TypeSystem.

        :return: The parent_ref of this TypeSystem.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this TypeSystem.

        :param parent_ref: The parent_ref of this TypeSystem.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def name(self):
        """
        Gets the name of this TypeSystem.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :return: The name of this TypeSystem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this TypeSystem.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :param name: The name of this TypeSystem.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this TypeSystem.
        A user defined description for the object.


        :return: The description of this TypeSystem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this TypeSystem.
        A user defined description for the object.


        :param description: The description of this TypeSystem.
        :type: str
        """
        self._description = description

    @property
    def object_version(self):
        """
        Gets the object_version of this TypeSystem.
        The version of the object that is used to track changes in the object instance.


        :return: The object_version of this TypeSystem.
        :rtype: int
        """
        return self._object_version

    @object_version.setter
    def object_version(self, object_version):
        """
        Sets the object_version of this TypeSystem.
        The version of the object that is used to track changes in the object instance.


        :param object_version: The object_version of this TypeSystem.
        :type: int
        """
        self._object_version = object_version

    @property
    def type_mapping_to(self):
        """
        Gets the type_mapping_to of this TypeSystem.
        The type system to map to.


        :return: The type_mapping_to of this TypeSystem.
        :rtype: dict(str, str)
        """
        return self._type_mapping_to

    @type_mapping_to.setter
    def type_mapping_to(self, type_mapping_to):
        """
        Sets the type_mapping_to of this TypeSystem.
        The type system to map to.


        :param type_mapping_to: The type_mapping_to of this TypeSystem.
        :type: dict(str, str)
        """
        self._type_mapping_to = type_mapping_to

    @property
    def type_mapping_from(self):
        """
        Gets the type_mapping_from of this TypeSystem.
        The type system to map from.


        :return: The type_mapping_from of this TypeSystem.
        :rtype: dict(str, str)
        """
        return self._type_mapping_from

    @type_mapping_from.setter
    def type_mapping_from(self, type_mapping_from):
        """
        Sets the type_mapping_from of this TypeSystem.
        The type system to map from.


        :param type_mapping_from: The type_mapping_from of this TypeSystem.
        :type: dict(str, str)
        """
        self._type_mapping_from = type_mapping_from

    @property
    def object_status(self):
        """
        Gets the object_status of this TypeSystem.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this TypeSystem.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this TypeSystem.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this TypeSystem.
        :type: int
        """
        self._object_status = object_status

    @property
    def identifier(self):
        """
        Gets the identifier of this TypeSystem.
        Value can only contain upper case letters, underscore, and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :return: The identifier of this TypeSystem.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this TypeSystem.
        Value can only contain upper case letters, underscore, and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :param identifier: The identifier of this TypeSystem.
        :type: str
        """
        self._identifier = identifier

    @property
    def types(self):
        """
        Gets the types of this TypeSystem.
        An array of types.


        :return: The types of this TypeSystem.
        :rtype: list[oci.data_integration.models.DataType]
        """
        return self._types

    @types.setter
    def types(self, types):
        """
        Sets the types of this TypeSystem.
        An array of types.


        :param types: The types of this TypeSystem.
        :type: list[oci.data_integration.models.DataType]
        """
        self._types = types

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
