# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20160918


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateContainerRepositoryDetails(object):
    """
    Update container repository request details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateContainerRepositoryDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_immutable:
            The value to assign to the is_immutable property of this UpdateContainerRepositoryDetails.
        :type is_immutable: bool

        :param is_public:
            The value to assign to the is_public property of this UpdateContainerRepositoryDetails.
        :type is_public: bool

        :param readme:
            The value to assign to the readme property of this UpdateContainerRepositoryDetails.
        :type readme: oci.artifacts.models.ContainerRepositoryReadme

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateContainerRepositoryDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateContainerRepositoryDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'is_immutable': 'bool',
            'is_public': 'bool',
            'readme': 'ContainerRepositoryReadme',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'is_immutable': 'isImmutable',
            'is_public': 'isPublic',
            'readme': 'readme',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._is_immutable = None
        self._is_public = None
        self._readme = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def is_immutable(self):
        """
        Gets the is_immutable of this UpdateContainerRepositoryDetails.
        Whether the repository is immutable. Images cannot be overwritten in an immutable repository.


        :return: The is_immutable of this UpdateContainerRepositoryDetails.
        :rtype: bool
        """
        return self._is_immutable

    @is_immutable.setter
    def is_immutable(self, is_immutable):
        """
        Sets the is_immutable of this UpdateContainerRepositoryDetails.
        Whether the repository is immutable. Images cannot be overwritten in an immutable repository.


        :param is_immutable: The is_immutable of this UpdateContainerRepositoryDetails.
        :type: bool
        """
        self._is_immutable = is_immutable

    @property
    def is_public(self):
        """
        Gets the is_public of this UpdateContainerRepositoryDetails.
        Whether the repository is public. A public repository allows unauthenticated access.


        :return: The is_public of this UpdateContainerRepositoryDetails.
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """
        Sets the is_public of this UpdateContainerRepositoryDetails.
        Whether the repository is public. A public repository allows unauthenticated access.


        :param is_public: The is_public of this UpdateContainerRepositoryDetails.
        :type: bool
        """
        self._is_public = is_public

    @property
    def readme(self):
        """
        Gets the readme of this UpdateContainerRepositoryDetails.

        :return: The readme of this UpdateContainerRepositoryDetails.
        :rtype: oci.artifacts.models.ContainerRepositoryReadme
        """
        return self._readme

    @readme.setter
    def readme(self, readme):
        """
        Sets the readme of this UpdateContainerRepositoryDetails.

        :param readme: The readme of this UpdateContainerRepositoryDetails.
        :type: oci.artifacts.models.ContainerRepositoryReadme
        """
        self._readme = readme

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateContainerRepositoryDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateContainerRepositoryDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateContainerRepositoryDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateContainerRepositoryDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateContainerRepositoryDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateContainerRepositoryDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateContainerRepositoryDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateContainerRepositoryDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
