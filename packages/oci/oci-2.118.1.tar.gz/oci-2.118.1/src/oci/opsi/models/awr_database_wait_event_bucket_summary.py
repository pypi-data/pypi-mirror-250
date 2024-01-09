# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200630


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AwrDatabaseWaitEventBucketSummary(object):
    """
    A summary of the AWR wait event bucket and waits percentage.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AwrDatabaseWaitEventBucketSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param category:
            The value to assign to the category property of this AwrDatabaseWaitEventBucketSummary.
        :type category: str

        :param percentage:
            The value to assign to the percentage property of this AwrDatabaseWaitEventBucketSummary.
        :type percentage: float

        """
        self.swagger_types = {
            'category': 'str',
            'percentage': 'float'
        }

        self.attribute_map = {
            'category': 'category',
            'percentage': 'percentage'
        }

        self._category = None
        self._percentage = None

    @property
    def category(self):
        """
        **[Required]** Gets the category of this AwrDatabaseWaitEventBucketSummary.
        The name of the wait event frequency category. Normally, it is the upper range of the waits within the AWR wait event bucket.


        :return: The category of this AwrDatabaseWaitEventBucketSummary.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this AwrDatabaseWaitEventBucketSummary.
        The name of the wait event frequency category. Normally, it is the upper range of the waits within the AWR wait event bucket.


        :param category: The category of this AwrDatabaseWaitEventBucketSummary.
        :type: str
        """
        self._category = category

    @property
    def percentage(self):
        """
        **[Required]** Gets the percentage of this AwrDatabaseWaitEventBucketSummary.
        The percentage of waits in a wait event bucket over the total waits of the database.


        :return: The percentage of this AwrDatabaseWaitEventBucketSummary.
        :rtype: float
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """
        Sets the percentage of this AwrDatabaseWaitEventBucketSummary.
        The percentage of waits in a wait event bucket over the total waits of the database.


        :param percentage: The percentage of this AwrDatabaseWaitEventBucketSummary.
        :type: float
        """
        self._percentage = percentage

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
