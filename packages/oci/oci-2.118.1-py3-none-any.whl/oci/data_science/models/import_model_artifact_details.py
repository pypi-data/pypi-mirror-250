# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20190101


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ImportModelArtifactDetails(object):
    """
    Details required for importing the artifact from service bucket
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ImportModelArtifactDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param artifact_import_details:
            The value to assign to the artifact_import_details property of this ImportModelArtifactDetails.
        :type artifact_import_details: oci.data_science.models.ArtifactImportDetails

        """
        self.swagger_types = {
            'artifact_import_details': 'ArtifactImportDetails'
        }

        self.attribute_map = {
            'artifact_import_details': 'artifactImportDetails'
        }

        self._artifact_import_details = None

    @property
    def artifact_import_details(self):
        """
        **[Required]** Gets the artifact_import_details of this ImportModelArtifactDetails.

        :return: The artifact_import_details of this ImportModelArtifactDetails.
        :rtype: oci.data_science.models.ArtifactImportDetails
        """
        return self._artifact_import_details

    @artifact_import_details.setter
    def artifact_import_details(self, artifact_import_details):
        """
        Sets the artifact_import_details of this ImportModelArtifactDetails.

        :param artifact_import_details: The artifact_import_details of this ImportModelArtifactDetails.
        :type: oci.data_science.models.ArtifactImportDetails
        """
        self._artifact_import_details = artifact_import_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
