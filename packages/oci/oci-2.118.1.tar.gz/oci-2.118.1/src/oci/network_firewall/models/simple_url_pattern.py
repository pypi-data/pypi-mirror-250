# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20230501

from .url_pattern import UrlPattern
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SimpleUrlPattern(UrlPattern):
    """
    Pattern describing an http/https URL or set thereof
    as a concatenation of optional host component and optional path component.

    `*.example.com` will match http://example.com/ and https://foo.example.com/foo?bar.

    `www.example.com/foo*` will match https://www.example.com/foo and http://www.exampe.com/foobar and https://www.example.com/foo/bar?baz, but not
    http://sub.www.example.com/foo or https://www.example.com/FOO.

    `*.example.com/foo*` will match http://example.com/foo and https://sub2.sub.example.com/foo/bar?baz, but not http://example.com/FOO.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SimpleUrlPattern object with values from keyword arguments. The default value of the :py:attr:`~oci.network_firewall.models.SimpleUrlPattern.type` attribute
        of this class is ``SIMPLE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this SimpleUrlPattern.
            Allowed values for this property are: "SIMPLE"
        :type type: str

        :param pattern:
            The value to assign to the pattern property of this SimpleUrlPattern.
        :type pattern: str

        """
        self.swagger_types = {
            'type': 'str',
            'pattern': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'pattern': 'pattern'
        }

        self._type = None
        self._pattern = None
        self._type = 'SIMPLE'

    @property
    def pattern(self):
        """
        **[Required]** Gets the pattern of this SimpleUrlPattern.
        A string consisting of a concatenation of optional host component and optional path component.
        The host component may start with `*.` to match the case-insensitive domain and all its subdomains.
        The path component must start with a `/`, and may end with `*` to match all paths of which it is a case-sensitive prefix.
        A missing host component matches all request domains, and a missing path component matches all request paths.
        An empty value matches all requests.


        :return: The pattern of this SimpleUrlPattern.
        :rtype: str
        """
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        """
        Sets the pattern of this SimpleUrlPattern.
        A string consisting of a concatenation of optional host component and optional path component.
        The host component may start with `*.` to match the case-insensitive domain and all its subdomains.
        The path component must start with a `/`, and may end with `*` to match all paths of which it is a case-sensitive prefix.
        A missing host component matches all request domains, and a missing path component matches all request paths.
        An empty value matches all requests.


        :param pattern: The pattern of this SimpleUrlPattern.
        :type: str
        """
        self._pattern = pattern

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
