from azure.identity import ClientSecretCredential, DeviceCodeCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, AzureDeveloperCliCredential
from azure.mgmt.resource import ResourceManagementClient
import azure.keyvault.secrets
import os
import sys

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging,
)

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class AzKeyVault:
    """Wrapper class for Azure Key Vault to get secrets.

    This class authenticates with the Azure Key Vault using a service
    principal and provides a method to retrieve secrets.
    """

    # Get the currently running file name
    NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
    # Get the parent folder name of the running file
    SERVICE_NAME = os.path.basename(__file__)

    def __init__(
        self, tenant_id, client_id, client_secret, key_vault_name, running_interactive
    ):
        """Initializes the KeyVaultSecrets object.

        Args:
            tenant_id (str): The tenant_id of your Azure account. This is the directory ID.
            client_id (str): The client ID of the service principal.
            client_secret (str): The client secret of the service principal.
            key_vault_name (str): The name of your Azure Key Vault. You can get it from the Key Vault properties in the Azure portal.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        cdc_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("__init__"):
            self.vault_url = f"https://{key_vault_name}.vault.azure.net/"
            self.running_interactive = running_interactive
            self.client_id = client_id
            self.client_secret = client_secret
            self.tenant_id = tenant_id
            logger.info(f"vault_url:{self.vault_url}")
            logger.info(f"tenant_id:{self.tenant_id}")
            logger.info(f"client_id:{self.client_id}")
            logger.info(f"client_secret_length:{len(str(self.client_secret))}")
            logger.info(f"running_interactive:{str(self.running_interactive)}")

            # self.credential_default = DefaultAzureCredential()
            # self.credential_dev =  AzureDeveloperCliCredential(  tenant_id=tenant_id,additionally_allowed_tenants=['*'])
            # self.client_default = SecretClient(vault_url,credential= self.credential_default)
            # self.client_dev = SecretClient(vault_url, credential=self.credential_dev)

            # Create a KeyVaultTokenCallback object
            # callback_dev = azure.keyvault.secrets.KeyVaultTokenCallback(self.credential_dev)
            # Set the KeyVaultTokenCallback object on the SecretClient object
            # self.client_dev.authentication_callback = self.callback_dev

    @classmethod
    def get_access_token(cls):
        """
        Retrieves an access token using the Azure Active Directory client secret credential.

        The function uses a client secret credential, which consists of the tenant ID, client ID,
        and client secret, to authenticate with Azure Active Directory and obtain an access token.
        The access token can then be used to authenticate requests to Azure services.

        The configuration settings and client secret are retrieved from the environment variables.

        Returns:
        str: The access token.

        Raises:
        azure.core.exceptions.ClientAuthenticationError: If there's a problem with
            client authentication, such as an invalid client secret.

        Note:
        Ensure that the required environment variables are set and the necessary permissions
        are granted in Azure AD for the app registration. The client secret should be stored securely,
        and it's recommended to use a secure method to retrieve it (such as Azure Key Vault).
        """

        credential = cls.get_credential()
        token = credential.get_token("https://management.azure.com/.default")
        return token.token

    @classmethod
    def cdc_authentication_callback(cls, client, context):
        """
        Callback function for CDC authentication.

        This function obtains an access token from a custom authentication mechanism.

        Args:
            cls: The class object.
            client: The client object.
            context: The authentication context.

        Returns:
            The access token.

        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("cdc_authentication_callback"):
            access_token = cls.get_access_token()

            # Return the access token
            return access_token

    def get_credential_device(self):
        """Gets the DeviceCodeCredential for interactive running mode.

        Returns:
            DeviceCodeCredential: The DeviceCodeCredential object for authentication.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_credential_device"):
            return DeviceCodeCredential(
                client_id=self.client_id,
                tenant_id=self.tenant_id,
                additionally_allowed_tenants=["*"],
            )

    def get_credential(self):
        """Gets the ClientSecretCredential for non-interactive running mode.

        Returns:
            ClientSecretCredential: The ClientSecretCredential object for authentication.

        Raises:
            Exception: If an error occurs while retrieving the credential.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_credential"):
            try:
                client_id = self.client_id
                tenant_id = self.tenant_id
                logger.info(f"get_credential client_id: {client_id}")
                logger.info(f"get_credential tenant_id: {tenant_id}")
                logger.info(
                    f"get_credential client_secret_length: {len(str(self.client_secret))}"
                )

                return ClientSecretCredential(
                    client_id=self.client_id,
                    tenant_id=self.tenant_id,
                    client_secret=self.client_secret,
                )

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_secret_client(self, credential):
        """
        Creates a SecretClient using a given credential.

        Args:
            credential: The credential used to authenticate with the Azure Key Vault.

        Returns:
            A SecretClient instance.

        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"get_secret_client"):
            try:
                return SecretClient(vault_url=self.vault_url, credential=credential)

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def retrieve_secret(self, secret_client, secret_name):
        """
        Attempts to retrieve a secret from the Azure Key Vault using a given SecretClient.

        Args:
            secret_client (SecretClient): The SecretClient object used to interact with the Azure Key Vault.
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret, or None if the retrieval fails.
        """
        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"retrieve_secret"):
            try:
                logger.info(f"secret_name: {secret_name}")
                return secret_client.get_secret(secret_name).value
            except Exception as e:
                error_msg = "Error: %s", secret_name + ":" + str(e)
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

                return None

    def get_secret(self, secret_name):
        """
        Retrieves a secret from the Azure Key Vault.

        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret.

        Raises:
            Exception: If an error occurs while retrieving the secret.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        span_name = f"get_secret:{secret_name}:from:{self.vault_url}"

        with tracer.start_as_current_span("get_secret"):
            try:
                logger.info(f"span_name:{span_name}")
                logger.info(f"vault_url:{self.vault_url}")
                logger.info(f"tenant_id:{self.tenant_id}")
                logger.info(f"client_id:{self.client_id}")
                logger.info(f"secret_name:{secret_name}")

                self.credential = self.get_credential()
                self.client = self.get_secret_client(self.credential)
                secret_value = self.retrieve_secret(self.client, secret_name)

                if secret_value is None:
                    if self.running_interactive is True:
                        logger.info(
                            f"running_interactive is True:{str(self.running_interactive)}"
                        )
                        self.credential_device = self.get_credential_device()
                        self.client_device = self.get_secret_client(
                            self.credential_device
                        )
                        secret_value = self.retrieve_secret(
                            self.client_device, secret_name
                        )

                        if secret_value is None:
                            logger.warning(
                                "Failed to retrieve secret using DeviceCodeCredential, falling back to ClientSecretCredential."
                            )
                            self.credential = self.get_credential()
                            self.client = self.get_secret_client(self.credential)
                            secret_value = self.retrieve_secret(
                                self.client, secret_name
                            )
                    else:
                        logger.info(
                            f"running_interactive is False:{str(self.running_interactive)}"
                        )
                        ex_message = "Unable to fetch secret"
                        error_msg = "Error: %s", secret_name + ":" + ex_message
                        exc_info = sys.exc_info()
                        logger_singleton.error_with_exception(error_msg, exc_info)
                        raise ValueError(error_msg)

                logger.info(
                    f"Retrieved secret for key: {secret_name} with length: {len(secret_value)}"
                )

                return secret_value

            except Exception as ex:
                error_msg = "Error: %s", secret_name + ":" + str(ex)
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
