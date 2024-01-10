import os
import sys
import unittest
from unittest.mock import patch
import cdh_dav_python.databricks_service.sql as databricks_sql
import cdh_dav_python.az_key_vault_service.az_key_vault as az_key_vault


class TestSavePipelineSql(unittest.TestCase):
    """
    Unit tests for the save_pipeline_sql function.
    """

    def setUp(self):
        """
        Set up the test environment before running each test case.
        """

        ENVIRONMENT = "dev"

        dbutils_exists = "dbutils" in locals() or "dbutils" in globals()
        if dbutils_exists is False:
            dbutils = None

        spark_exists = "spark" in locals() or "spark" in globals()
        if spark_exists is False:
            spark = None

        running_local = dbutils is None
        print(f"running_local: {running_local}")

        initial_script_dir = (
            os.path.dirname(os.path.abspath(__file__))
            if "__file__" in globals()
            else os.getcwd()
        )
        print(f"initial_script_dir: {initial_script_dir}")

        parent_dir = os.path.abspath(os.path.join(initial_script_dir, "..", ".."))
        print(f"parent_dir: {parent_dir}")
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        repository_path_default = str(parent_dir)

        print(f"repository_path_default: {repository_path_default}")

        import run_install_cdh_dav_python

        (
            spark,
            obj_environment_metadata,
            obj_job_core,
            config,
        ) = run_install_cdh_dav_python.setup_core(
            running_local,
            initial_script_dir,
            dbutils,
            spark,
        )

        self.config = config

        az_sub_client_secret_key = config.get("az_sub_client_secret_key")
        self.client_secret = os.getenv(az_sub_client_secret_key)
        self.tenant_id = config.get("az_sub_tenant_id")
        self.client_id = config.get("az_sub_client_id")
        self.vault_url = config.get("az_kv_key_vault_name")
        self.running_interactive = True

        self.key_vault = az_key_vault.AzKeyVault(
            self.tenant_id,
            self.client_id,
            self.client_secret,
            self.vault_url,
            self.running_interactive,
        )

    @patch("cdh_dav_python.databricks_service.sql.requests.get")
    def test_save_pipeline_sql_success(self, mock_get):
        """
        Test the save_pipeline_sql function with a successful response.

        Mocks the response from the requests.get method and asserts that the
        function returns "success".
        """
        # Mock the response from the requests.get method
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [{"query": "SELECT * FROM table"}]
        }

        config = self.config

        access_token = config.get("access_token")
        repository_path = config.get("repository_path")
        yyyy_param = config.get("repository_path")
        mm_param = config.get("mm_param")
        dd_param = config.get("dd_param")
        environment = config.get("environment")
        databricks_instance_id = config.get("databricks_instance_id")
        data_product_id_root = config.get("data_product_id_root")
        data_product_id = config.get("data_product_id")
        query_name = config.get("query_name")
        pipeline_name = (config.get("pipeline_name"),)
        execute_results_flag = (True,)
        arg_dictionary = ({},)
        transmission_period = "daily"

        # Call the save_pipeline_sql function with sample parameters
        obj_sql = databricks_sql.DatabricksSQL()

        result = obj_sql.save_pipeline_sql(
            access_token=access_token,
            repository_path=repository_path,
            yyyy_param=yyyy_param,
            mm_param=mm_param,
            dd_param=dd_param,
            environment=environment,
            databricks_instance_id=databricks_instance_id,
            data_product_id_root=data_product_id_root,
            data_product_id=data_product_id,
            query_name=query_name,
            pipeline_name=pipeline_name,
            execute_results_flag=execute_results_flag,
            arg_dictionary=arg_dictionary,
            transmission_period=transmission_period,
        )

        # Assert that the response is successful
        self.assertEqual(result, "success")

    @patch("cdh_dav_python.databricks_service.sql.requests.get")
    def test_save_pipeline_sql_failure(self, mock_get):
        """
        Test the save_pipeline_sql function with a failure response.

        Mocks the response from the requests.get method and asserts that the
        function raises an Exception.
        """
        # Mock the response from the requests.get method
        mock_get.return_value.status_code = 500

        # Call the save_pipeline_sql function with sample parameters
        with self.assertRaises(Exception):
            sql.save_pipeline_sql(
                token="sample_token",
                repository_path="/path/to/repository",
                yyyy_param="2022",
                mm_param="01",
                dd_param="01",
                environment="dev",
                databricks_instance_id="sample_instance_id",
                data_product_id_root="sample_root",
                data_product_id="sample_id",
                query_name="sample_query",
                pipeline_name="sample_pipeline",
                execute_results_flag=True,
                arg_dictionary={},
                transmission_period="daily",
            )


if __name__ == "__main__":
    unittest.main()
