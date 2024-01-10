import unittest
from unittest.mock import patch
import cdh_dav_python.databricks_service.sql as databricks_sql


class TestSavePipelineSql(unittest.TestCase):
    """
    Unit tests for the save_pipeline_sql function.
    """

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

        # Call the save_pipeline_sql function with sample parameters
        obj_sql = databricks_sql.DatabricksSQL()

        result = obj_sql.save_pipeline_sql(
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
