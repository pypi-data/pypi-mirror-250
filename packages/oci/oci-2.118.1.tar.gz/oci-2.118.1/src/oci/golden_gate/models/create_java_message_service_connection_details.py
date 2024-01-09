# coding: utf-8
# Copyright (c) 2016, 2024, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20200407

from .create_connection_details import CreateConnectionDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateJavaMessageServiceConnectionDetails(CreateConnectionDetails):
    """
    The information about a new Java Message Service Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateJavaMessageServiceConnectionDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.CreateJavaMessageServiceConnectionDetails.connection_type` attribute
        of this class is ``JAVA_MESSAGE_SERVICE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this CreateJavaMessageServiceConnectionDetails.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB", "AMAZON_KINESIS", "AMAZON_REDSHIFT", "REDIS", "ELASTICSEARCH", "GENERIC", "GOOGLE_CLOUD_STORAGE", "GOOGLE_BIGQUERY"
        :type connection_type: str

        :param display_name:
            The value to assign to the display_name property of this CreateJavaMessageServiceConnectionDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateJavaMessageServiceConnectionDetails.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateJavaMessageServiceConnectionDetails.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateJavaMessageServiceConnectionDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateJavaMessageServiceConnectionDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param vault_id:
            The value to assign to the vault_id property of this CreateJavaMessageServiceConnectionDetails.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this CreateJavaMessageServiceConnectionDetails.
        :type key_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this CreateJavaMessageServiceConnectionDetails.
        :type nsg_ids: list[str]

        :param subnet_id:
            The value to assign to the subnet_id property of this CreateJavaMessageServiceConnectionDetails.
        :type subnet_id: str

        :param routing_method:
            The value to assign to the routing_method property of this CreateJavaMessageServiceConnectionDetails.
            Allowed values for this property are: "SHARED_SERVICE_ENDPOINT", "SHARED_DEPLOYMENT_ENDPOINT", "DEDICATED_ENDPOINT"
        :type routing_method: str

        :param technology_type:
            The value to assign to the technology_type property of this CreateJavaMessageServiceConnectionDetails.
        :type technology_type: str

        :param should_use_jndi:
            The value to assign to the should_use_jndi property of this CreateJavaMessageServiceConnectionDetails.
        :type should_use_jndi: bool

        :param jndi_connection_factory:
            The value to assign to the jndi_connection_factory property of this CreateJavaMessageServiceConnectionDetails.
        :type jndi_connection_factory: str

        :param jndi_provider_url:
            The value to assign to the jndi_provider_url property of this CreateJavaMessageServiceConnectionDetails.
        :type jndi_provider_url: str

        :param jndi_initial_context_factory:
            The value to assign to the jndi_initial_context_factory property of this CreateJavaMessageServiceConnectionDetails.
        :type jndi_initial_context_factory: str

        :param jndi_security_principal:
            The value to assign to the jndi_security_principal property of this CreateJavaMessageServiceConnectionDetails.
        :type jndi_security_principal: str

        :param jndi_security_credentials:
            The value to assign to the jndi_security_credentials property of this CreateJavaMessageServiceConnectionDetails.
        :type jndi_security_credentials: str

        :param connection_url:
            The value to assign to the connection_url property of this CreateJavaMessageServiceConnectionDetails.
        :type connection_url: str

        :param connection_factory:
            The value to assign to the connection_factory property of this CreateJavaMessageServiceConnectionDetails.
        :type connection_factory: str

        :param username:
            The value to assign to the username property of this CreateJavaMessageServiceConnectionDetails.
        :type username: str

        :param password:
            The value to assign to the password property of this CreateJavaMessageServiceConnectionDetails.
        :type password: str

        :param security_protocol:
            The value to assign to the security_protocol property of this CreateJavaMessageServiceConnectionDetails.
        :type security_protocol: str

        :param authentication_type:
            The value to assign to the authentication_type property of this CreateJavaMessageServiceConnectionDetails.
        :type authentication_type: str

        :param trust_store:
            The value to assign to the trust_store property of this CreateJavaMessageServiceConnectionDetails.
        :type trust_store: str

        :param trust_store_password:
            The value to assign to the trust_store_password property of this CreateJavaMessageServiceConnectionDetails.
        :type trust_store_password: str

        :param key_store:
            The value to assign to the key_store property of this CreateJavaMessageServiceConnectionDetails.
        :type key_store: str

        :param key_store_password:
            The value to assign to the key_store_password property of this CreateJavaMessageServiceConnectionDetails.
        :type key_store_password: str

        :param ssl_key_password:
            The value to assign to the ssl_key_password property of this CreateJavaMessageServiceConnectionDetails.
        :type ssl_key_password: str

        :param private_ip:
            The value to assign to the private_ip property of this CreateJavaMessageServiceConnectionDetails.
        :type private_ip: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'vault_id': 'str',
            'key_id': 'str',
            'nsg_ids': 'list[str]',
            'subnet_id': 'str',
            'routing_method': 'str',
            'technology_type': 'str',
            'should_use_jndi': 'bool',
            'jndi_connection_factory': 'str',
            'jndi_provider_url': 'str',
            'jndi_initial_context_factory': 'str',
            'jndi_security_principal': 'str',
            'jndi_security_credentials': 'str',
            'connection_url': 'str',
            'connection_factory': 'str',
            'username': 'str',
            'password': 'str',
            'security_protocol': 'str',
            'authentication_type': 'str',
            'trust_store': 'str',
            'trust_store_password': 'str',
            'key_store': 'str',
            'key_store_password': 'str',
            'ssl_key_password': 'str',
            'private_ip': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'nsg_ids': 'nsgIds',
            'subnet_id': 'subnetId',
            'routing_method': 'routingMethod',
            'technology_type': 'technologyType',
            'should_use_jndi': 'shouldUseJndi',
            'jndi_connection_factory': 'jndiConnectionFactory',
            'jndi_provider_url': 'jndiProviderUrl',
            'jndi_initial_context_factory': 'jndiInitialContextFactory',
            'jndi_security_principal': 'jndiSecurityPrincipal',
            'jndi_security_credentials': 'jndiSecurityCredentials',
            'connection_url': 'connectionUrl',
            'connection_factory': 'connectionFactory',
            'username': 'username',
            'password': 'password',
            'security_protocol': 'securityProtocol',
            'authentication_type': 'authenticationType',
            'trust_store': 'trustStore',
            'trust_store_password': 'trustStorePassword',
            'key_store': 'keyStore',
            'key_store_password': 'keyStorePassword',
            'ssl_key_password': 'sslKeyPassword',
            'private_ip': 'privateIp'
        }

        self._connection_type = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._vault_id = None
        self._key_id = None
        self._nsg_ids = None
        self._subnet_id = None
        self._routing_method = None
        self._technology_type = None
        self._should_use_jndi = None
        self._jndi_connection_factory = None
        self._jndi_provider_url = None
        self._jndi_initial_context_factory = None
        self._jndi_security_principal = None
        self._jndi_security_credentials = None
        self._connection_url = None
        self._connection_factory = None
        self._username = None
        self._password = None
        self._security_protocol = None
        self._authentication_type = None
        self._trust_store = None
        self._trust_store_password = None
        self._key_store = None
        self._key_store_password = None
        self._ssl_key_password = None
        self._private_ip = None
        self._connection_type = 'JAVA_MESSAGE_SERVICE'

    @property
    def technology_type(self):
        """
        **[Required]** Gets the technology_type of this CreateJavaMessageServiceConnectionDetails.
        The Java Message Service technology type.


        :return: The technology_type of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        """
        Sets the technology_type of this CreateJavaMessageServiceConnectionDetails.
        The Java Message Service technology type.


        :param technology_type: The technology_type of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._technology_type = technology_type

    @property
    def should_use_jndi(self):
        """
        **[Required]** Gets the should_use_jndi of this CreateJavaMessageServiceConnectionDetails.
        If set to true, Java Naming and Directory Interface (JNDI) properties should be provided.


        :return: The should_use_jndi of this CreateJavaMessageServiceConnectionDetails.
        :rtype: bool
        """
        return self._should_use_jndi

    @should_use_jndi.setter
    def should_use_jndi(self, should_use_jndi):
        """
        Sets the should_use_jndi of this CreateJavaMessageServiceConnectionDetails.
        If set to true, Java Naming and Directory Interface (JNDI) properties should be provided.


        :param should_use_jndi: The should_use_jndi of this CreateJavaMessageServiceConnectionDetails.
        :type: bool
        """
        self._should_use_jndi = should_use_jndi

    @property
    def jndi_connection_factory(self):
        """
        Gets the jndi_connection_factory of this CreateJavaMessageServiceConnectionDetails.
        The Connection Factory can be looked up using this name.
        e.g.: 'ConnectionFactory'


        :return: The jndi_connection_factory of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_connection_factory

    @jndi_connection_factory.setter
    def jndi_connection_factory(self, jndi_connection_factory):
        """
        Sets the jndi_connection_factory of this CreateJavaMessageServiceConnectionDetails.
        The Connection Factory can be looked up using this name.
        e.g.: 'ConnectionFactory'


        :param jndi_connection_factory: The jndi_connection_factory of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_connection_factory = jndi_connection_factory

    @property
    def jndi_provider_url(self):
        """
        Gets the jndi_provider_url of this CreateJavaMessageServiceConnectionDetails.
        The URL that Java Message Service will use to contact the JNDI provider.
        e.g.: 'tcp://myjms.host.domain:61616?jms.prefetchPolicy.all=1000'


        :return: The jndi_provider_url of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_provider_url

    @jndi_provider_url.setter
    def jndi_provider_url(self, jndi_provider_url):
        """
        Sets the jndi_provider_url of this CreateJavaMessageServiceConnectionDetails.
        The URL that Java Message Service will use to contact the JNDI provider.
        e.g.: 'tcp://myjms.host.domain:61616?jms.prefetchPolicy.all=1000'


        :param jndi_provider_url: The jndi_provider_url of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_provider_url = jndi_provider_url

    @property
    def jndi_initial_context_factory(self):
        """
        Gets the jndi_initial_context_factory of this CreateJavaMessageServiceConnectionDetails.
        The implementation of javax.naming.spi.InitialContextFactory interface
        that the client uses to obtain initial naming context.
        e.g.: 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'


        :return: The jndi_initial_context_factory of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_initial_context_factory

    @jndi_initial_context_factory.setter
    def jndi_initial_context_factory(self, jndi_initial_context_factory):
        """
        Sets the jndi_initial_context_factory of this CreateJavaMessageServiceConnectionDetails.
        The implementation of javax.naming.spi.InitialContextFactory interface
        that the client uses to obtain initial naming context.
        e.g.: 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'


        :param jndi_initial_context_factory: The jndi_initial_context_factory of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_initial_context_factory = jndi_initial_context_factory

    @property
    def jndi_security_principal(self):
        """
        Gets the jndi_security_principal of this CreateJavaMessageServiceConnectionDetails.
        Specifies the identity of the principal (user) to be authenticated.
        e.g.: 'admin2'


        :return: The jndi_security_principal of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_security_principal

    @jndi_security_principal.setter
    def jndi_security_principal(self, jndi_security_principal):
        """
        Sets the jndi_security_principal of this CreateJavaMessageServiceConnectionDetails.
        Specifies the identity of the principal (user) to be authenticated.
        e.g.: 'admin2'


        :param jndi_security_principal: The jndi_security_principal of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_security_principal = jndi_security_principal

    @property
    def jndi_security_credentials(self):
        """
        Gets the jndi_security_credentials of this CreateJavaMessageServiceConnectionDetails.
        The password associated to the principal.


        :return: The jndi_security_credentials of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_security_credentials

    @jndi_security_credentials.setter
    def jndi_security_credentials(self, jndi_security_credentials):
        """
        Sets the jndi_security_credentials of this CreateJavaMessageServiceConnectionDetails.
        The password associated to the principal.


        :param jndi_security_credentials: The jndi_security_credentials of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_security_credentials = jndi_security_credentials

    @property
    def connection_url(self):
        """
        Gets the connection_url of this CreateJavaMessageServiceConnectionDetails.
        Connectin URL of the Java Message Service, specifying the protocol, host, and port.
        e.g.: 'mq://myjms.host.domain:7676'


        :return: The connection_url of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._connection_url

    @connection_url.setter
    def connection_url(self, connection_url):
        """
        Sets the connection_url of this CreateJavaMessageServiceConnectionDetails.
        Connectin URL of the Java Message Service, specifying the protocol, host, and port.
        e.g.: 'mq://myjms.host.domain:7676'


        :param connection_url: The connection_url of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._connection_url = connection_url

    @property
    def connection_factory(self):
        """
        Gets the connection_factory of this CreateJavaMessageServiceConnectionDetails.
        The of Java class implementing javax.jms.ConnectionFactory interface
        supplied by the Java Message Service provider.
        e.g.: 'com.stc.jmsjca.core.JConnectionFactoryXA'


        :return: The connection_factory of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._connection_factory

    @connection_factory.setter
    def connection_factory(self, connection_factory):
        """
        Sets the connection_factory of this CreateJavaMessageServiceConnectionDetails.
        The of Java class implementing javax.jms.ConnectionFactory interface
        supplied by the Java Message Service provider.
        e.g.: 'com.stc.jmsjca.core.JConnectionFactoryXA'


        :param connection_factory: The connection_factory of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._connection_factory = connection_factory

    @property
    def username(self):
        """
        Gets the username of this CreateJavaMessageServiceConnectionDetails.
        The username Oracle GoldenGate uses to connect to the Java Message Service.
        This username must already exist and be available by the Java Message Service to be connected to.


        :return: The username of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this CreateJavaMessageServiceConnectionDetails.
        The username Oracle GoldenGate uses to connect to the Java Message Service.
        This username must already exist and be available by the Java Message Service to be connected to.


        :param username: The username of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._username = username

    @property
    def password(self):
        """
        Gets the password of this CreateJavaMessageServiceConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated Java Message Service.


        :return: The password of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this CreateJavaMessageServiceConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated Java Message Service.


        :param password: The password of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._password = password

    @property
    def security_protocol(self):
        """
        Gets the security_protocol of this CreateJavaMessageServiceConnectionDetails.
        Security protocol for Java Message Service. If not provided, default is PLAIN.
        Optional until 2024-06-27, in the release after it will be made required.


        :return: The security_protocol of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._security_protocol

    @security_protocol.setter
    def security_protocol(self, security_protocol):
        """
        Sets the security_protocol of this CreateJavaMessageServiceConnectionDetails.
        Security protocol for Java Message Service. If not provided, default is PLAIN.
        Optional until 2024-06-27, in the release after it will be made required.


        :param security_protocol: The security_protocol of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._security_protocol = security_protocol

    @property
    def authentication_type(self):
        """
        Gets the authentication_type of this CreateJavaMessageServiceConnectionDetails.
        Authentication type for Java Message Service.  If not provided, default is NONE.
        Optional until 2024-06-27, in the release after it will be made required.


        :return: The authentication_type of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._authentication_type

    @authentication_type.setter
    def authentication_type(self, authentication_type):
        """
        Sets the authentication_type of this CreateJavaMessageServiceConnectionDetails.
        Authentication type for Java Message Service.  If not provided, default is NONE.
        Optional until 2024-06-27, in the release after it will be made required.


        :param authentication_type: The authentication_type of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._authentication_type = authentication_type

    @property
    def trust_store(self):
        """
        Gets the trust_store of this CreateJavaMessageServiceConnectionDetails.
        The base64 encoded content of the TrustStore file.


        :return: The trust_store of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._trust_store

    @trust_store.setter
    def trust_store(self, trust_store):
        """
        Sets the trust_store of this CreateJavaMessageServiceConnectionDetails.
        The base64 encoded content of the TrustStore file.


        :param trust_store: The trust_store of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._trust_store = trust_store

    @property
    def trust_store_password(self):
        """
        Gets the trust_store_password of this CreateJavaMessageServiceConnectionDetails.
        The TrustStore password.


        :return: The trust_store_password of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._trust_store_password

    @trust_store_password.setter
    def trust_store_password(self, trust_store_password):
        """
        Sets the trust_store_password of this CreateJavaMessageServiceConnectionDetails.
        The TrustStore password.


        :param trust_store_password: The trust_store_password of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._trust_store_password = trust_store_password

    @property
    def key_store(self):
        """
        Gets the key_store of this CreateJavaMessageServiceConnectionDetails.
        The base64 encoded content of the KeyStore file.


        :return: The key_store of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._key_store

    @key_store.setter
    def key_store(self, key_store):
        """
        Sets the key_store of this CreateJavaMessageServiceConnectionDetails.
        The base64 encoded content of the KeyStore file.


        :param key_store: The key_store of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._key_store = key_store

    @property
    def key_store_password(self):
        """
        Gets the key_store_password of this CreateJavaMessageServiceConnectionDetails.
        The KeyStore password.


        :return: The key_store_password of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._key_store_password

    @key_store_password.setter
    def key_store_password(self, key_store_password):
        """
        Sets the key_store_password of this CreateJavaMessageServiceConnectionDetails.
        The KeyStore password.


        :param key_store_password: The key_store_password of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._key_store_password = key_store_password

    @property
    def ssl_key_password(self):
        """
        Gets the ssl_key_password of this CreateJavaMessageServiceConnectionDetails.
        The password for the cert inside of the KeyStore.
        In case it differs from the KeyStore password, it should be provided.


        :return: The ssl_key_password of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._ssl_key_password

    @ssl_key_password.setter
    def ssl_key_password(self, ssl_key_password):
        """
        Sets the ssl_key_password of this CreateJavaMessageServiceConnectionDetails.
        The password for the cert inside of the KeyStore.
        In case it differs from the KeyStore password, it should be provided.


        :param ssl_key_password: The ssl_key_password of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._ssl_key_password = ssl_key_password

    @property
    def private_ip(self):
        """
        Gets the private_ip of this CreateJavaMessageServiceConnectionDetails.
        Deprecated: this field will be removed in future versions. Either specify the private IP in the connectionString or host
        field, or make sure the host name is resolvable in the target VCN.

        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :return: The private_ip of this CreateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this CreateJavaMessageServiceConnectionDetails.
        Deprecated: this field will be removed in future versions. Either specify the private IP in the connectionString or host
        field, or make sure the host name is resolvable in the target VCN.

        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :param private_ip: The private_ip of this CreateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._private_ip = private_ip

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
