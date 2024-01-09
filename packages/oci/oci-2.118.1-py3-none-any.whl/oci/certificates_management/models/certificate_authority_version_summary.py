# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20210224


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CertificateAuthorityVersionSummary(object):
    """
    The metadata details of the certificate authority (CA) version. This summary object does not contain the CA contents.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CertificateAuthorityVersionSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param certificate_authority_id:
            The value to assign to the certificate_authority_id property of this CertificateAuthorityVersionSummary.
        :type certificate_authority_id: str

        :param issuer_ca_version_number:
            The value to assign to the issuer_ca_version_number property of this CertificateAuthorityVersionSummary.
        :type issuer_ca_version_number: int

        :param serial_number:
            The value to assign to the serial_number property of this CertificateAuthorityVersionSummary.
        :type serial_number: str

        :param time_created:
            The value to assign to the time_created property of this CertificateAuthorityVersionSummary.
        :type time_created: datetime

        :param version_number:
            The value to assign to the version_number property of this CertificateAuthorityVersionSummary.
        :type version_number: int

        :param version_name:
            The value to assign to the version_name property of this CertificateAuthorityVersionSummary.
        :type version_name: str

        :param time_of_deletion:
            The value to assign to the time_of_deletion property of this CertificateAuthorityVersionSummary.
        :type time_of_deletion: datetime

        :param validity:
            The value to assign to the validity property of this CertificateAuthorityVersionSummary.
        :type validity: oci.certificates_management.models.Validity

        :param stages:
            The value to assign to the stages property of this CertificateAuthorityVersionSummary.
        :type stages: list[oci.certificates_management.models.VersionStage]

        :param revocation_status:
            The value to assign to the revocation_status property of this CertificateAuthorityVersionSummary.
        :type revocation_status: oci.certificates_management.models.RevocationStatus

        """
        self.swagger_types = {
            'certificate_authority_id': 'str',
            'issuer_ca_version_number': 'int',
            'serial_number': 'str',
            'time_created': 'datetime',
            'version_number': 'int',
            'version_name': 'str',
            'time_of_deletion': 'datetime',
            'validity': 'Validity',
            'stages': 'list[VersionStage]',
            'revocation_status': 'RevocationStatus'
        }

        self.attribute_map = {
            'certificate_authority_id': 'certificateAuthorityId',
            'issuer_ca_version_number': 'issuerCaVersionNumber',
            'serial_number': 'serialNumber',
            'time_created': 'timeCreated',
            'version_number': 'versionNumber',
            'version_name': 'versionName',
            'time_of_deletion': 'timeOfDeletion',
            'validity': 'validity',
            'stages': 'stages',
            'revocation_status': 'revocationStatus'
        }

        self._certificate_authority_id = None
        self._issuer_ca_version_number = None
        self._serial_number = None
        self._time_created = None
        self._version_number = None
        self._version_name = None
        self._time_of_deletion = None
        self._validity = None
        self._stages = None
        self._revocation_status = None

    @property
    def certificate_authority_id(self):
        """
        **[Required]** Gets the certificate_authority_id of this CertificateAuthorityVersionSummary.
        The OCID of the CA.


        :return: The certificate_authority_id of this CertificateAuthorityVersionSummary.
        :rtype: str
        """
        return self._certificate_authority_id

    @certificate_authority_id.setter
    def certificate_authority_id(self, certificate_authority_id):
        """
        Sets the certificate_authority_id of this CertificateAuthorityVersionSummary.
        The OCID of the CA.


        :param certificate_authority_id: The certificate_authority_id of this CertificateAuthorityVersionSummary.
        :type: str
        """
        self._certificate_authority_id = certificate_authority_id

    @property
    def issuer_ca_version_number(self):
        """
        Gets the issuer_ca_version_number of this CertificateAuthorityVersionSummary.
        The version number of the issuing CA.


        :return: The issuer_ca_version_number of this CertificateAuthorityVersionSummary.
        :rtype: int
        """
        return self._issuer_ca_version_number

    @issuer_ca_version_number.setter
    def issuer_ca_version_number(self, issuer_ca_version_number):
        """
        Sets the issuer_ca_version_number of this CertificateAuthorityVersionSummary.
        The version number of the issuing CA.


        :param issuer_ca_version_number: The issuer_ca_version_number of this CertificateAuthorityVersionSummary.
        :type: int
        """
        self._issuer_ca_version_number = issuer_ca_version_number

    @property
    def serial_number(self):
        """
        Gets the serial_number of this CertificateAuthorityVersionSummary.
        A unique certificate identifier used in certificate revocation tracking, formatted as octets.
        Example: `03 AC FC FA CC B3 CB 02 B8 F8 DE F5 85 E7 7B FF`


        :return: The serial_number of this CertificateAuthorityVersionSummary.
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """
        Sets the serial_number of this CertificateAuthorityVersionSummary.
        A unique certificate identifier used in certificate revocation tracking, formatted as octets.
        Example: `03 AC FC FA CC B3 CB 02 B8 F8 DE F5 85 E7 7B FF`


        :param serial_number: The serial_number of this CertificateAuthorityVersionSummary.
        :type: str
        """
        self._serial_number = serial_number

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this CertificateAuthorityVersionSummary.
        A optional property indicating when the CA version was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this CertificateAuthorityVersionSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this CertificateAuthorityVersionSummary.
        A optional property indicating when the CA version was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this CertificateAuthorityVersionSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def version_number(self):
        """
        **[Required]** Gets the version_number of this CertificateAuthorityVersionSummary.
        The version number of the CA.


        :return: The version_number of this CertificateAuthorityVersionSummary.
        :rtype: int
        """
        return self._version_number

    @version_number.setter
    def version_number(self, version_number):
        """
        Sets the version_number of this CertificateAuthorityVersionSummary.
        The version number of the CA.


        :param version_number: The version_number of this CertificateAuthorityVersionSummary.
        :type: int
        """
        self._version_number = version_number

    @property
    def version_name(self):
        """
        Gets the version_name of this CertificateAuthorityVersionSummary.
        The name of the CA version. When this value is not null, the name is unique across CA versions for a given CA.


        :return: The version_name of this CertificateAuthorityVersionSummary.
        :rtype: str
        """
        return self._version_name

    @version_name.setter
    def version_name(self, version_name):
        """
        Sets the version_name of this CertificateAuthorityVersionSummary.
        The name of the CA version. When this value is not null, the name is unique across CA versions for a given CA.


        :param version_name: The version_name of this CertificateAuthorityVersionSummary.
        :type: str
        """
        self._version_name = version_name

    @property
    def time_of_deletion(self):
        """
        Gets the time_of_deletion of this CertificateAuthorityVersionSummary.
        An optional property indicating when to delete the CA version, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_of_deletion of this CertificateAuthorityVersionSummary.
        :rtype: datetime
        """
        return self._time_of_deletion

    @time_of_deletion.setter
    def time_of_deletion(self, time_of_deletion):
        """
        Sets the time_of_deletion of this CertificateAuthorityVersionSummary.
        An optional property indicating when to delete the CA version, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_of_deletion: The time_of_deletion of this CertificateAuthorityVersionSummary.
        :type: datetime
        """
        self._time_of_deletion = time_of_deletion

    @property
    def validity(self):
        """
        Gets the validity of this CertificateAuthorityVersionSummary.

        :return: The validity of this CertificateAuthorityVersionSummary.
        :rtype: oci.certificates_management.models.Validity
        """
        return self._validity

    @validity.setter
    def validity(self, validity):
        """
        Sets the validity of this CertificateAuthorityVersionSummary.

        :param validity: The validity of this CertificateAuthorityVersionSummary.
        :type: oci.certificates_management.models.Validity
        """
        self._validity = validity

    @property
    def stages(self):
        """
        **[Required]** Gets the stages of this CertificateAuthorityVersionSummary.
        A list of rotation states for this CA version.


        :return: The stages of this CertificateAuthorityVersionSummary.
        :rtype: list[oci.certificates_management.models.VersionStage]
        """
        return self._stages

    @stages.setter
    def stages(self, stages):
        """
        Sets the stages of this CertificateAuthorityVersionSummary.
        A list of rotation states for this CA version.


        :param stages: The stages of this CertificateAuthorityVersionSummary.
        :type: list[oci.certificates_management.models.VersionStage]
        """
        self._stages = stages

    @property
    def revocation_status(self):
        """
        Gets the revocation_status of this CertificateAuthorityVersionSummary.

        :return: The revocation_status of this CertificateAuthorityVersionSummary.
        :rtype: oci.certificates_management.models.RevocationStatus
        """
        return self._revocation_status

    @revocation_status.setter
    def revocation_status(self, revocation_status):
        """
        Sets the revocation_status of this CertificateAuthorityVersionSummary.

        :param revocation_status: The revocation_status of this CertificateAuthorityVersionSummary.
        :type: oci.certificates_management.models.RevocationStatus
        """
        self._revocation_status = revocation_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
