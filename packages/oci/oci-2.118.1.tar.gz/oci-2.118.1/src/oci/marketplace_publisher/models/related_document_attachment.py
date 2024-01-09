# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220901

from .listing_revision_attachment import ListingRevisionAttachment
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RelatedDocumentAttachment(ListingRevisionAttachment):
    """
    Related document attachment for the listing revision.
    """

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "CASE_STUDIES"
    DOCUMENT_CATEGORY_CASE_STUDIES = "CASE_STUDIES"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "CUSTOMIZATION_GUIDES"
    DOCUMENT_CATEGORY_CUSTOMIZATION_GUIDES = "CUSTOMIZATION_GUIDES"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "DATA_SHEETS"
    DOCUMENT_CATEGORY_DATA_SHEETS = "DATA_SHEETS"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "PRESS_RELEASE"
    DOCUMENT_CATEGORY_PRESS_RELEASE = "PRESS_RELEASE"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "PRODUCT_DOCUMENTATION"
    DOCUMENT_CATEGORY_PRODUCT_DOCUMENTATION = "PRODUCT_DOCUMENTATION"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "USER_GUIDES"
    DOCUMENT_CATEGORY_USER_GUIDES = "USER_GUIDES"

    #: A constant which can be used with the document_category property of a RelatedDocumentAttachment.
    #: This constant has a value of "WEBINAR"
    DOCUMENT_CATEGORY_WEBINAR = "WEBINAR"

    def __init__(self, **kwargs):
        """
        Initializes a new RelatedDocumentAttachment object with values from keyword arguments. The default value of the :py:attr:`~oci.marketplace_publisher.models.RelatedDocumentAttachment.attachment_type` attribute
        of this class is ``RELATED_DOCUMENT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this RelatedDocumentAttachment.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this RelatedDocumentAttachment.
        :type compartment_id: str

        :param listing_revision_id:
            The value to assign to the listing_revision_id property of this RelatedDocumentAttachment.
        :type listing_revision_id: str

        :param display_name:
            The value to assign to the display_name property of this RelatedDocumentAttachment.
        :type display_name: str

        :param description:
            The value to assign to the description property of this RelatedDocumentAttachment.
        :type description: str

        :param attachment_type:
            The value to assign to the attachment_type property of this RelatedDocumentAttachment.
            Allowed values for this property are: "RELATED_DOCUMENT", "SCREENSHOT", "VIDEO", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type attachment_type: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this RelatedDocumentAttachment.
            Allowed values for this property are: "ACTIVE", "INACTIVE", "DELETED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this RelatedDocumentAttachment.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this RelatedDocumentAttachment.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this RelatedDocumentAttachment.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this RelatedDocumentAttachment.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this RelatedDocumentAttachment.
        :type system_tags: dict(str, dict(str, object))

        :param document_category:
            The value to assign to the document_category property of this RelatedDocumentAttachment.
            Allowed values for this property are: "CASE_STUDIES", "CUSTOMIZATION_GUIDES", "DATA_SHEETS", "PRESS_RELEASE", "PRODUCT_DOCUMENTATION", "USER_GUIDES", "WEBINAR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type document_category: str

        :param content_url:
            The value to assign to the content_url property of this RelatedDocumentAttachment.
        :type content_url: str

        :param mime_type:
            The value to assign to the mime_type property of this RelatedDocumentAttachment.
        :type mime_type: str

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'listing_revision_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'attachment_type': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'document_category': 'str',
            'content_url': 'str',
            'mime_type': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'listing_revision_id': 'listingRevisionId',
            'display_name': 'displayName',
            'description': 'description',
            'attachment_type': 'attachmentType',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'document_category': 'documentCategory',
            'content_url': 'contentUrl',
            'mime_type': 'mimeType'
        }

        self._id = None
        self._compartment_id = None
        self._listing_revision_id = None
        self._display_name = None
        self._description = None
        self._attachment_type = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._document_category = None
        self._content_url = None
        self._mime_type = None
        self._attachment_type = 'RELATED_DOCUMENT'

    @property
    def document_category(self):
        """
        Gets the document_category of this RelatedDocumentAttachment.
        Possible lifecycle states.

        Allowed values for this property are: "CASE_STUDIES", "CUSTOMIZATION_GUIDES", "DATA_SHEETS", "PRESS_RELEASE", "PRODUCT_DOCUMENTATION", "USER_GUIDES", "WEBINAR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The document_category of this RelatedDocumentAttachment.
        :rtype: str
        """
        return self._document_category

    @document_category.setter
    def document_category(self, document_category):
        """
        Sets the document_category of this RelatedDocumentAttachment.
        Possible lifecycle states.


        :param document_category: The document_category of this RelatedDocumentAttachment.
        :type: str
        """
        allowed_values = ["CASE_STUDIES", "CUSTOMIZATION_GUIDES", "DATA_SHEETS", "PRESS_RELEASE", "PRODUCT_DOCUMENTATION", "USER_GUIDES", "WEBINAR"]
        if not value_allowed_none_or_none_sentinel(document_category, allowed_values):
            document_category = 'UNKNOWN_ENUM_VALUE'
        self._document_category = document_category

    @property
    def content_url(self):
        """
        Gets the content_url of this RelatedDocumentAttachment.
        URL of the uploaded document.


        :return: The content_url of this RelatedDocumentAttachment.
        :rtype: str
        """
        return self._content_url

    @content_url.setter
    def content_url(self, content_url):
        """
        Sets the content_url of this RelatedDocumentAttachment.
        URL of the uploaded document.


        :param content_url: The content_url of this RelatedDocumentAttachment.
        :type: str
        """
        self._content_url = content_url

    @property
    def mime_type(self):
        """
        Gets the mime_type of this RelatedDocumentAttachment.
        The MIME type of the uploaded data.


        :return: The mime_type of this RelatedDocumentAttachment.
        :rtype: str
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type):
        """
        Sets the mime_type of this RelatedDocumentAttachment.
        The MIME type of the uploaded data.


        :param mime_type: The mime_type of this RelatedDocumentAttachment.
        :type: str
        """
        self._mime_type = mime_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
