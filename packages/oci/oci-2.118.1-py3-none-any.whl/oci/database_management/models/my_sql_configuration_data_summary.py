# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20201101


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MySqlConfigurationDataSummary(object):
    """
    The configuration variables for a MySQL Database.
    """

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "COMPILED"
    SOURCE_COMPILED = "COMPILED"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "GLOBAL"
    SOURCE_GLOBAL = "GLOBAL"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "SERVER"
    SOURCE_SERVER = "SERVER"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "EXPLICIT"
    SOURCE_EXPLICIT = "EXPLICIT"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "EXTRA"
    SOURCE_EXTRA = "EXTRA"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "USER"
    SOURCE_USER = "USER"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "LOGIN"
    SOURCE_LOGIN = "LOGIN"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "COMMAND_LINE"
    SOURCE_COMMAND_LINE = "COMMAND_LINE"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "PERSISTED"
    SOURCE_PERSISTED = "PERSISTED"

    #: A constant which can be used with the source property of a MySqlConfigurationDataSummary.
    #: This constant has a value of "DYNAMIC"
    SOURCE_DYNAMIC = "DYNAMIC"

    def __init__(self, **kwargs):
        """
        Initializes a new MySqlConfigurationDataSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this MySqlConfigurationDataSummary.
        :type name: str

        :param value:
            The value to assign to the value property of this MySqlConfigurationDataSummary.
        :type value: str

        :param source:
            The value to assign to the source property of this MySqlConfigurationDataSummary.
            Allowed values for this property are: "COMPILED", "GLOBAL", "SERVER", "EXPLICIT", "EXTRA", "USER", "LOGIN", "COMMAND_LINE", "PERSISTED", "DYNAMIC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type source: str

        :param min_value:
            The value to assign to the min_value property of this MySqlConfigurationDataSummary.
        :type min_value: float

        :param max_value:
            The value to assign to the max_value property of this MySqlConfigurationDataSummary.
        :type max_value: float

        :param type:
            The value to assign to the type property of this MySqlConfigurationDataSummary.
        :type type: str

        :param default_value:
            The value to assign to the default_value property of this MySqlConfigurationDataSummary.
        :type default_value: str

        :param time_set:
            The value to assign to the time_set property of this MySqlConfigurationDataSummary.
        :type time_set: datetime

        :param host_set:
            The value to assign to the host_set property of this MySqlConfigurationDataSummary.
        :type host_set: str

        :param user_set:
            The value to assign to the user_set property of this MySqlConfigurationDataSummary.
        :type user_set: str

        :param is_dynamic:
            The value to assign to the is_dynamic property of this MySqlConfigurationDataSummary.
        :type is_dynamic: bool

        :param is_init:
            The value to assign to the is_init property of this MySqlConfigurationDataSummary.
        :type is_init: bool

        :param is_configurable:
            The value to assign to the is_configurable property of this MySqlConfigurationDataSummary.
        :type is_configurable: bool

        :param path:
            The value to assign to the path property of this MySqlConfigurationDataSummary.
        :type path: str

        :param description:
            The value to assign to the description property of this MySqlConfigurationDataSummary.
        :type description: str

        :param possible_values:
            The value to assign to the possible_values property of this MySqlConfigurationDataSummary.
        :type possible_values: str

        :param supported_versions:
            The value to assign to the supported_versions property of this MySqlConfigurationDataSummary.
        :type supported_versions: str

        """
        self.swagger_types = {
            'name': 'str',
            'value': 'str',
            'source': 'str',
            'min_value': 'float',
            'max_value': 'float',
            'type': 'str',
            'default_value': 'str',
            'time_set': 'datetime',
            'host_set': 'str',
            'user_set': 'str',
            'is_dynamic': 'bool',
            'is_init': 'bool',
            'is_configurable': 'bool',
            'path': 'str',
            'description': 'str',
            'possible_values': 'str',
            'supported_versions': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'value': 'value',
            'source': 'source',
            'min_value': 'minValue',
            'max_value': 'maxValue',
            'type': 'type',
            'default_value': 'defaultValue',
            'time_set': 'timeSet',
            'host_set': 'hostSet',
            'user_set': 'userSet',
            'is_dynamic': 'isDynamic',
            'is_init': 'isInit',
            'is_configurable': 'isConfigurable',
            'path': 'path',
            'description': 'description',
            'possible_values': 'possibleValues',
            'supported_versions': 'supportedVersions'
        }

        self._name = None
        self._value = None
        self._source = None
        self._min_value = None
        self._max_value = None
        self._type = None
        self._default_value = None
        self._time_set = None
        self._host_set = None
        self._user_set = None
        self._is_dynamic = None
        self._is_init = None
        self._is_configurable = None
        self._path = None
        self._description = None
        self._possible_values = None
        self._supported_versions = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this MySqlConfigurationDataSummary.
        The name of the configuration variable


        :return: The name of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MySqlConfigurationDataSummary.
        The name of the configuration variable


        :param name: The name of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        **[Required]** Gets the value of this MySqlConfigurationDataSummary.
        The value of the variable.


        :return: The value of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this MySqlConfigurationDataSummary.
        The value of the variable.


        :param value: The value of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._value = value

    @property
    def source(self):
        """
        **[Required]** Gets the source of this MySqlConfigurationDataSummary.
        The source from which the variable was most recently set.

        Allowed values for this property are: "COMPILED", "GLOBAL", "SERVER", "EXPLICIT", "EXTRA", "USER", "LOGIN", "COMMAND_LINE", "PERSISTED", "DYNAMIC", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The source of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this MySqlConfigurationDataSummary.
        The source from which the variable was most recently set.


        :param source: The source of this MySqlConfigurationDataSummary.
        :type: str
        """
        allowed_values = ["COMPILED", "GLOBAL", "SERVER", "EXPLICIT", "EXTRA", "USER", "LOGIN", "COMMAND_LINE", "PERSISTED", "DYNAMIC"]
        if not value_allowed_none_or_none_sentinel(source, allowed_values):
            source = 'UNKNOWN_ENUM_VALUE'
        self._source = source

    @property
    def min_value(self):
        """
        **[Required]** Gets the min_value of this MySqlConfigurationDataSummary.
        The minimum value of the variable.


        :return: The min_value of this MySqlConfigurationDataSummary.
        :rtype: float
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        """
        Sets the min_value of this MySqlConfigurationDataSummary.
        The minimum value of the variable.


        :param min_value: The min_value of this MySqlConfigurationDataSummary.
        :type: float
        """
        self._min_value = min_value

    @property
    def max_value(self):
        """
        **[Required]** Gets the max_value of this MySqlConfigurationDataSummary.
        The maximum value of the variable.


        :return: The max_value of this MySqlConfigurationDataSummary.
        :rtype: float
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """
        Sets the max_value of this MySqlConfigurationDataSummary.
        The maximum value of the variable.


        :param max_value: The max_value of this MySqlConfigurationDataSummary.
        :type: float
        """
        self._max_value = max_value

    @property
    def type(self):
        """
        **[Required]** Gets the type of this MySqlConfigurationDataSummary.
        The type of variable.


        :return: The type of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this MySqlConfigurationDataSummary.
        The type of variable.


        :param type: The type of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._type = type

    @property
    def default_value(self):
        """
        **[Required]** Gets the default_value of this MySqlConfigurationDataSummary.
        The default value of the variable.


        :return: The default_value of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """
        Sets the default_value of this MySqlConfigurationDataSummary.
        The default value of the variable.


        :param default_value: The default_value of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._default_value = default_value

    @property
    def time_set(self):
        """
        **[Required]** Gets the time_set of this MySqlConfigurationDataSummary.
        The time when the value of the variable was set.


        :return: The time_set of this MySqlConfigurationDataSummary.
        :rtype: datetime
        """
        return self._time_set

    @time_set.setter
    def time_set(self, time_set):
        """
        Sets the time_set of this MySqlConfigurationDataSummary.
        The time when the value of the variable was set.


        :param time_set: The time_set of this MySqlConfigurationDataSummary.
        :type: datetime
        """
        self._time_set = time_set

    @property
    def host_set(self):
        """
        **[Required]** Gets the host_set of this MySqlConfigurationDataSummary.
        The host from where the value of the variable was set. This is empty for a MySQL Database System.


        :return: The host_set of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._host_set

    @host_set.setter
    def host_set(self, host_set):
        """
        Sets the host_set of this MySqlConfigurationDataSummary.
        The host from where the value of the variable was set. This is empty for a MySQL Database System.


        :param host_set: The host_set of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._host_set = host_set

    @property
    def user_set(self):
        """
        **[Required]** Gets the user_set of this MySqlConfigurationDataSummary.
        The user who sets the value of the variable. This is empty for a MySQL Database System.


        :return: The user_set of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._user_set

    @user_set.setter
    def user_set(self, user_set):
        """
        Sets the user_set of this MySqlConfigurationDataSummary.
        The user who sets the value of the variable. This is empty for a MySQL Database System.


        :param user_set: The user_set of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._user_set = user_set

    @property
    def is_dynamic(self):
        """
        **[Required]** Gets the is_dynamic of this MySqlConfigurationDataSummary.
        Indicates whether the variable can be set dynamically or not.


        :return: The is_dynamic of this MySqlConfigurationDataSummary.
        :rtype: bool
        """
        return self._is_dynamic

    @is_dynamic.setter
    def is_dynamic(self, is_dynamic):
        """
        Sets the is_dynamic of this MySqlConfigurationDataSummary.
        Indicates whether the variable can be set dynamically or not.


        :param is_dynamic: The is_dynamic of this MySqlConfigurationDataSummary.
        :type: bool
        """
        self._is_dynamic = is_dynamic

    @property
    def is_init(self):
        """
        **[Required]** Gets the is_init of this MySqlConfigurationDataSummary.
        Indicates whether the variable is set at server startup.


        :return: The is_init of this MySqlConfigurationDataSummary.
        :rtype: bool
        """
        return self._is_init

    @is_init.setter
    def is_init(self, is_init):
        """
        Sets the is_init of this MySqlConfigurationDataSummary.
        Indicates whether the variable is set at server startup.


        :param is_init: The is_init of this MySqlConfigurationDataSummary.
        :type: bool
        """
        self._is_init = is_init

    @property
    def is_configurable(self):
        """
        **[Required]** Gets the is_configurable of this MySqlConfigurationDataSummary.
        Indicates whether the variable is configurable.


        :return: The is_configurable of this MySqlConfigurationDataSummary.
        :rtype: bool
        """
        return self._is_configurable

    @is_configurable.setter
    def is_configurable(self, is_configurable):
        """
        Sets the is_configurable of this MySqlConfigurationDataSummary.
        Indicates whether the variable is configurable.


        :param is_configurable: The is_configurable of this MySqlConfigurationDataSummary.
        :type: bool
        """
        self._is_configurable = is_configurable

    @property
    def path(self):
        """
        **[Required]** Gets the path of this MySqlConfigurationDataSummary.
        The path name of the option file (VARIABLE_PATH), if the variable was set in an option file. If the variable was not set in an


        :return: The path of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this MySqlConfigurationDataSummary.
        The path name of the option file (VARIABLE_PATH), if the variable was set in an option file. If the variable was not set in an


        :param path: The path of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._path = path

    @property
    def description(self):
        """
        **[Required]** Gets the description of this MySqlConfigurationDataSummary.
        The description of the variable.


        :return: The description of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this MySqlConfigurationDataSummary.
        The description of the variable.


        :param description: The description of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._description = description

    @property
    def possible_values(self):
        """
        **[Required]** Gets the possible_values of this MySqlConfigurationDataSummary.
        The comma-separated list of possible values for the variable in value:valueDescription format.


        :return: The possible_values of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._possible_values

    @possible_values.setter
    def possible_values(self, possible_values):
        """
        Sets the possible_values of this MySqlConfigurationDataSummary.
        The comma-separated list of possible values for the variable in value:valueDescription format.


        :param possible_values: The possible_values of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._possible_values = possible_values

    @property
    def supported_versions(self):
        """
        **[Required]** Gets the supported_versions of this MySqlConfigurationDataSummary.
        The comma-separated list of MySQL versions that support the variable.


        :return: The supported_versions of this MySqlConfigurationDataSummary.
        :rtype: str
        """
        return self._supported_versions

    @supported_versions.setter
    def supported_versions(self, supported_versions):
        """
        Sets the supported_versions of this MySqlConfigurationDataSummary.
        The comma-separated list of MySQL versions that support the variable.


        :param supported_versions: The supported_versions of this MySqlConfigurationDataSummary.
        :type: str
        """
        self._supported_versions = supported_versions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
