"""
This module provides functionality for interacting with Databricks SQL queries.
It includes a class, DatabricksSQL, that contains methods for fetching and saving pipelines,
handling exceptions, and preprocessing query text.

The module also imports various libraries and modules required for error handling, logging,
web scraping, and environment management.

Author: [Your Name]
Date: [Current Date]
"""

import traceback  # don't remove required for error handling
import json
import base64
import re
import os
import sys
import requests
from html.parser import HTMLParser  # web scraping html
from string import Formatter
from importlib import util  # library management


# spark
# https://superuser.com/questions/1436855/port-binding-error-in-pyspark

pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    # import pyspark.pandas  as pd
    # bug - pyspark version will not read local files in the repo
    os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
    import pyspark.pandas as pd
else:
    import pandas as pd


OS_NAME = os.name
sys.path.append("../..")

if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


import cdh_dav_python.cdc_admin_service.environment_tracing as cdc_env_tracing
import cdh_dav_python.cdc_admin_service.environment_logging as cdc_env_logging
import cdh_dav_python.cdc_tech_environment_service.environment_file as cdc_env_file
import cdh_dav_python.cdc_tech_environment_service.environment_http as cdc_env_http

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class DatabricksSQL:
    """
    A class that provides methods for interacting with Databricks SQL queries.
    """

    @staticmethod
    def initialize_logging_and_tracing():
        """
        Initializes logging and tracing for the application.

        Returns:
            logger (Logger): The logger instance for logging.
            tracer (Tracer): The tracer instance for tracing.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()

        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        return tracer, logger, logger_singleton

    @classmethod
    def fetch_and_save_pipeline(
        cls,
        databricks_access_token,
        repository_path,
        environment,
        databricks_instance_id,
        data_product_id_root,
        data_product_id,
        query_name,
        pipeline_name,
        execute_results_flag,
        arg_dictionary,
        running_local,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
    ):
        """
        Fetches SQL query, saves the pipeline, and returns the status.

        Args:
            cls: The class object.
            databricks_access_token (str): The access token for Databricks.
            repository_path (str): The path to the repository.
            environment (str): The environment name.
            databricks_instance_id (str): The ID of the Databricks instance.
            data_product_id_root (str): The root ID of the data product.
            data_product_id (str): The ID of the data product.
            query_name (str): The name of the query.
            pipeline_name (str): The name of the pipeline.
            execute_results_flag (bool): Flag indicating whether to execute the results.
            arg_dictionary (dict): The dictionary of arguments.
            running_local (bool): Flag indicating whether the code is running locally.
            yyyy_param (str): The year parameter.
            mm_param (str): The month parameter.
            dd_param (str): The day parameter.
            transmission_period (str): The transmission period.

        Returns:
            str: The status of the operation (success or error).

        Raises:
            Exception: If an error occurs during the operation.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_and_save_pipeline"):
            try:
                logger.info("------- FETCH-SQL ----------------")
                (
                    query_text,
                    variable_text,
                    query_text_original,
                ) = cls.fetch_sql(
                    databricks_access_token,
                    databricks_instance_id,
                    query_name,
                    environment,
                    execute_results_flag,
                    yyyy_param,
                    mm_param,
                    dd_param,
                    transmission_period,
                    arg_dictionary,
                )

                logger.info("------- SAVE-PIPELINE ----------------")
                cls.save_pipeline(
                    arg_dictionary,
                    environment,
                    query_name,
                    query_text,
                    variable_text,
                    databricks_access_token,
                    repository_path,
                    data_product_id,
                    databricks_instance_id,
                    pipeline_name,
                    yyyy_param,
                    mm_param,
                    dd_param,
                    transmission_period,
                    running_local,
                )

                return "success"

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def handle_exception(err, logger_singleton):
        """
        Handles an exception by logging the error message and exception information.

        Args:
            err: The exception object.
            logger_singleton: The logger singleton object.

        Returns:
            None
        """
        error_msg = "Error: %s", err
        exc_info = sys.exc_info()
        logger_singleton.error_with_exception(error_msg, exc_info)

    @staticmethod
    def handle_json_conversion_error(exception_check, response_text_raw, logger):
        """
        Handles the error that occurs when converting response text to JSON.

        Args:
            exception_check (Exception): The exception that occurred during JSON conversion.
            response_text_raw (str): The raw response text.
            logger (Logger): The logger object for logging error messages.

        Returns:
            None
        """
        html_filter = HTMLFilter()
        html_filter.feed(response_text_raw)
        response_text = html_filter.text
        logger.error(f"- response : error - {str(exception_check)}")
        logger.error(f"Error converting response text:{response_text} to json")

    @staticmethod
    def get_query_text(data):
        """
        Get the query text from the provided data.

        Args:
            data (dict): The data containing the query information.

        Returns:
            str: The query text.
        """

        query_text = (
            "# Check configuration of view in list - no query content was found"
        )

        for i in data["results"]:
            query_text_original = i["query"]
            query_text = query_text_original.replace(
                "{{", "TEMPORARY_OPEN_BRACKET"
            ).replace("}}", "TEMPORARY_CLOSE_BRACKET")
            query_text = query_text.replace("{", "{{").replace("}", "}}")
            query_text = query_text.lstrip()
            query_text = query_text.rstrip()
            return query_text

    @staticmethod
    def preprocess_query_text(query_text_original):
        """
        Preprocesses the query text by replacing special characters to avoid conflicts with string formatting.

        Args:
            query_text_original (str): The original query text.

        Returns:
            str: The preprocessed query text.
        """
        query_text = query_text_original.replace(
            "{{", "TEMPORARY_OPEN_BRACKET"
        ).replace("}}", "TEMPORARY_CLOSE_BRACKET")
        query_text = query_text.replace("{", "{{").replace("}", "}}")
        return query_text

    @classmethod
    def fetch_sql(
        cls,
        databricks_access_token,
        databricks_instance_id,
        query_name,
        environment,
        execute_results_flag,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
        arg_dictionary,
    ):
        """
        Fetches SQL query from DataBricks and returns the query text, variable text, original query text,
        Python directory name, and SQL directory name.

        Args:
            cls (class): The class object.
            databricks_access_token (str): The access token for DataBricks.
            repository_path (str): The path to the repository.
            data_product_id_root (str): The root ID of the data product.
            data_product_id (str): The ID of the data product.
            databricks_instance_id (str): The ID of the DataBricks instance.
            query_name (str): The name of the SQL query.
            environment (str): The environment.
            execute_results_flag (str): The flag to execute results.
            yyyy_param (str): The year parameter.
            mm_param (str): The month parameter.
            dd_param (str): The day parameter.
            transmission_period (str): The transmission period.
            arg_dictionary (dict): The dictionary of argument values.

        Returns:
            tuple: A tuple containing the query text, variable text, original query text,
            Python directory name, and SQL directory name.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_sql"):
            try:
                api_command = cls.get_api_command(query_name)
                url = cls.get_url(databricks_instance_id, api_command)

                try:
                    logger.info(
                        f"fetch_sql request start for query_name:{query_name} url:{str(url)}"
                    )
                    response = cls.process_request(url, databricks_access_token)
                    logger.info(
                        f"process_response start for query_name:{query_name} url:{str(url)}"
                    )
                    results = cls.process_response(response)
                    response_text = json.dumps(results)
                    logger.info(
                        f"process_response complete for query_name:{query_name} with response_text_legnth {len(response_text)}"
                    )
                except requests.exceptions.HTTPError as http_err:
                    error_msg = "Error: %s", http_err
                    exc_info = sys.exc_info()
                    logger_singleton.error_with_exception(error_msg, exc_info)
                    raise
                except Exception as err:
                    cls.handle_exception(err, logger_singleton)
                    raise

                data = None

                try:
                    data = cls.load_json(response)
                    response_text_string = cls.get_response_text_string(
                        response_text, url, query_name
                    )
                    logger.info("- response : success  -")
                    logger.info(f"{response_text_string}")
                except Exception as exception_check:
                    response_text_raw = response.text
                    cls.handle_json_conversion_error(
                        exception_check, response_text_raw, logger
                    )

                variable_text = "Not Set : Data was not loaded"
                query_text_original = "Not Set : Data was not loaded"
                if data is None:
                    logger.info("Error loading sql query:{query_name}")
                    raise ValueError(f"Error loading sql query:{query_name}")
                else:
                    query_text = cls.get_query_text(data)
                    response = "not set"

                    for i in data["results"]:
                        query_text_original = i["query"]
                        query_text = cls.preprocess_query_text(query_text_original)
                        query_text = cls.escape_brackets(query_text)
                        query_text = query_text.strip()
                        query_text = query_text.replace('"', '\\"')

                        # remove -- comments
                        query_text = re.sub(
                            r"^--.*\n?", "", query_text, flags=re.MULTILINE
                        )

                        if query_text == "":
                            logger.info(f"query name{query_name}:")
                            logger.info(f"{query_text} not found in DataBricks SQL")
                        else:
                            if not query_text.endswith(";"):
                                query_text += ";"
                        # ph = "TEMPORARY_OPEN_BRACKET"
                        variable_text = (
                            f'execute_results_flag = "{execute_results_flag}"'
                        )

                        cls.set_query_parameters(
                            query_text,
                            environment,
                            arg_dictionary,
                            yyyy_param,
                            mm_param,
                            dd_param,
                            transmission_period,
                        )

                return (
                    str(query_text),
                    str(variable_text),
                    str(query_text_original),
                )

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def set_query_parameters(
        cls,
        environment,
        arg_dictionary,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
        query_text_original,
    ):
        """
        Sets the query parameters for executing a SQL query.

        Args:
            cls: The class object.
            environment (str): The environment value.
            arg_dictionary (dict): A dictionary containing the argument values.
            yyyy_param (str): The yyyy parameter value.
            mm_param (str): The mm parameter value.
            dd_param (str): The dd parameter value.
            transmission_period (str): The transmission period value.
            query_text_original (str): The original query text.

        Returns:
            str: The generated code for setting the query parameters.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("set_query_parameters"):
            try:
                query_parse = query_text_original.replace("{{", "{").replace("}}", "}")
                logger.info(f"query_parse:{query_parse}")
                param_list = [
                    fname for _, fname, _, _ in Formatter().parse(query_parse) if fname
                ]

                dict_param_unique = dict()
                for line in list(dict.fromkeys(param_list)):
                    line = line.replace('"', "").replace("'", "")
                    if line.strip() == "environment":
                        dict_param_unique["'" + line.strip() + "'"] = environment
                    else:
                        dict_param_unique["'" + line.strip() + "'"] = (
                            "'enter " + line.strip() + " value'"
                        )

                dict_param_unique["yyyy"] = yyyy_param
                dict_param_unique["mm"] = mm_param
                dict_param_unique["dd"] = dd_param
                dict_param_unique["transmission_period"] = transmission_period

                new_param_code = ""
                for line in dict_param_unique:
                    line = line.replace('"', "").replace("'", "")
                    if line in arg_dictionary:
                        new_param_code = (
                            new_param_code
                            + f"dbutils.widgets.text('{line}', '{arg_dictionary[line]}')\n"
                        )
                    else:
                        logger.warning(f"{line} not in arg_dictionary")
                        new_param_code = (
                            new_param_code
                            + f"dbutils.widgets.text('{line}', 'default')\n"
                        )
                    new_param_code = (
                        new_param_code + f"{line} = dbutils.widgets.get('{line}')\n"
                    )

                dict_code = ""
                for line in dict_param_unique:
                    line = line.replace('"', "").replace("'", "")
                    if line in arg_dictionary:
                        line_strip = line.strip().replace('"', "")
                        dict_code = (
                            dict_code + f"'{line_strip}':'{arg_dictionary[line]}',"
                        )
                    else:
                        logger.warning(f"{line} not in arg_dictionary")
                        line_strip = line.strip().replace('"', "")
                        dict_code = dict_code + f"'{line_strip}':'default',"

                dict_code = dict_code + f"'environment':'{environment}',"
                dict_parameters = "dict_parameters = {" + dict_code.rstrip(",") + "}\n"

                new_param_code = new_param_code + dict_parameters

                return new_param_code

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_pipeline_python(
        cls,
        arg_dictionary,
        environment,
        query_text,
        variable_text,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
    ):
        # Set query parameters
        new_param_code = cls.set_query_parameters(
            environment,
            arg_dictionary,
            yyyy_param,
            mm_param,
            dd_param,
            transmission_period,
            query_text,
        )

        # Generate content text
        sql_command_text = (
            'sql_command_text = """' + query_text + '""".format(**dict_parameters)'
        )
        print_query_text = "print(sql_command_text)"
        print_df_results_text = """
        from pyspark.sql.functions import col
        dfResults = spark.sql(sql_command_text)
        #display(dfResults)
        listColumns=dfResults.columns
        #if ("sql_statement"  in listColumns):
        #    print(dfResults.first().sql_statement)
        if (dfResults.count() > 0):
            if ("sql_statement"  in listColumns):
                dfMerge = spark.sql(dfResults.first().sql_statement)
                display(dfMerge)
        """

        content_text = (
            new_param_code
            + " # COMMAND ----------\n"
            + sql_command_text
            + " # COMMAND ----------\n"
            + print_query_text
            + " # COMMAND ----------\n"
            + variable_text
            + " # COMMAND ----------\n"
            + print_df_results_text
            + " # COMMAND ----------\n"
        )
        content_text = content_text.lstrip()

        return content_text

    @classmethod
    def save_pipeline(
        cls,
        arg_dictionary,
        environment,
        query_name,
        query_text,
        variable_text,
        databricks_access_token,
        dir_name_python_local,
        dir_name_sql_local,
        data_product_id,
        databricks_instance_id,
        pipeline_name,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
        running_local,
    ):
        """
        Process the pipeline by generating the Python code, saving it, and saving the SQL query.

        Args:
            cls (class): The class object.
            arg_dictionary (dict): The dictionary containing the arguments.
            environment (str): The environment name.
            query_name (str): The name of the query.
            query_text (str): The SQL query text.
            variable_text (str): The variable text.
            databricks_access_token (str): The access token for Databricks.
            dir_name_python_local (str): The directory name for saving Python code.
            dir_name_sql_local (str): The directory name for saving SQL query.
            data_product_id (str): The data product ID.
            databricks_instance_id (str): The Databricks instance ID.
            pipeline_name (str): The name of the pipeline.
            yyyy_param (str): The year parameter.
            mm_param (str): The month parameter.
            dd_param (str): The day parameter.
            transmission_period (str): The transmission period.
            running_local (bool): Flag indicating if running locally.

        Returns:
            None
        """

        # Get Pipeline Python
        python_text = cls.get_pipeline_python(
            arg_dictionary,
            environment,
            query_text,
            variable_text,
            yyyy_param,
            mm_param,
            dd_param,
            transmission_period,
        )

        # Save Python pipeline
        pipeline_name = pipeline_name.replace(data_product_id, "")
        pipeline_name = pipeline_name.replace(".", "")
        pipeline_name = data_product_id + "_" + pipeline_name
        cls.save_pipeline_python(
            databricks_instance_id,
            databricks_access_token,
            dir_name_python_local,
            pipeline_name,
            python_text,
            data_product_id,
            running_local,
        )

        # Save SQL query
        cls.save_pipline_sql(
            databricks_instance_id,
            databricks_access_token,
            dir_name_sql_local,
            query_name,
            query_text,
        )

    @classmethod
    def save_pipeline_python(
        cls,
        databricks_instance_id,
        databricks_access_token,
        repository_path,
        pipeline_name,
        content_text,
        data_product_id,
        running_local,
    ):
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        logger.info(f"running_local:{running_local}")

        with tracer.start_as_current_span("save_pipeline_python"):
            try:
                # configure api

                base_path_local = repository_path
                base_path_server = repository_path

                dir_name_python_local = cls.get_dir_name_python_local(base_path_local)
                dir_name_python_server = cls.get_dir_name_python_server(
                    base_path_server
                )

                api_version = "/api/2.0"
                api_command = "/workspace/import"
                url = f"https://{databricks_instance_id}{api_version}{api_command}"

                # Prepare File to  Save
                pipeline_name = pipeline_name.replace(".", "")
                if not pipeline_name.startswith(data_product_id):
                    pipeline_name = data_product_id + "_" + pipeline_name

                # Content
                content_python = base64.b64encode(content_text.encode("UTF-8")).decode(
                    "UTF-8"
                )

                if running_local:
                    # save to file system
                    # File Path
                    new_path_python = str(
                        os.path.join(dir_name_python_local, pipeline_name)
                    )
                    if not new_path_python.endswith(".py"):
                        new_path_python = new_path_python + ".py"

                    obj_file = cdc_env_file.EnvironmentFile()
                    if obj_file.file_exists(True, new_path_python, None):
                        try:
                            os.remove(new_path_python)
                        except OSError as e:
                            logger.error(f"Error: {e.filename} - {e.strerror}.")

                    logger.info(f"Save Python {pipeline_name} to {new_path_python}")
                    obj_file.save_text_to_file(
                        dir_name_python_local, content_text, new_path_python, "py"
                    )

                    # Directory Path
                    sys.path.append(dir_name_python_local)
                    isdir = os.path.isdir(dir_name_python_local)
                    logger.info(f"dir_name_python_local: isdir:{isdir}")

                # save to server
                data_python = {
                    "content": content_python,
                    "path": new_path_python,
                    "language": "PYTHON",
                    "overwrite": True,
                    "format": "SOURCE",
                }
                logger.info(f"------- Save Python {pipeline_name}  -------")
                logger.info(f"url:{str(url)}")

                headers_import = cls.get_headers(databricks_access_token)
                headers_redacted = str(headers_import).replace(
                    databricks_access_token, "[databricks_access_token REDACTED]"
                )
                logger.info(f"headers:{headers_redacted}")
                logger.info(f"json:{str(data_python)}")

                # Post to Save File
                obj_http = cdc_env_http.EnvironmentHttp()
                response_python = obj_http.post(
                    url=url, headers=headers_import, timeout=60, json=data_python
                )

                # Get Response
                try:
                    response_python_text = json.dumps(response_python.json())
                    logger.info("- response : success  -")
                    response_python_text_message = "Received SAVE-PYTHON-RESPONSE : "
                    response_python_text_message += (
                        f"{response_python.text} when posting to : {url}  "
                    )
                    response_python_text_message += (
                        f"to save python pipeline with sql query: {pipeline_name}"
                    )
                    response_python_text_message += f"to {new_path_python}"

                    logger.info(response_python_text)

                except Exception as exception_check:
                    html_filter = HTMLFilter()
                    html_filter.feed(response_python.text)
                    response_python_text = html_filter.text
                    error_message = f"response : error - {str(exception_check)}"
                    error_message = (
                        error_message
                        + f"Error SAVE-PYTHON-RESPONSE converting response text:{response_python_text} to json"
                    )
                    exc_info = sys.exc_info()
                    # Detailed traceback
                    logger_singleton.error_with_exception(error_message, exc_info)
                    raise
            except requests.exceptions.HTTPError as err:
                # Log error details
                exc_info = sys.exc_info()
                error_msg = f"HTTP Error occurred: {err}"
                error_msg = error_msg + (f"Status Code: {response_python.status_code}")
                error_msg = error_msg + (f"Response Content: {response_python.text}")
                error_msg = error_msg + (f"Request URL: {response_python.url}")
                error_msg = error_msg + (
                    f"Request Headers: {response_python.request.headers}"
                )
                if response_python.request.body:
                    error_msg = error_msg + (
                        f"Request Body: {response_python.request.body}"
                    )

                # Detailed traceback
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def save_pipline_sql(
        cls,
        databricks_instance_id,
        databricks_access_token,
        dir_name_sql_local,
        query_name,
        query_text_original,
    ):
        """
        Saves a SQL query to a Databricks workspace.

        Args:
            cls: The class object.
            databricks_instance_id (str): The ID of the Databricks instance.
            databricks_access_token (str): The access token for the Databricks instance.
            dir_name_sql_local (str): The directory name where the SQL query will be saved.
            query_name (str): The name of the SQL query.
            query_text_original (str): The original text of the SQL query.

        Returns:
            dict: A dictionary containing the response from the API call.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("save_pipline_sql"):
            try:
                headers = cls.get_headers(databricks_access_token)
                # configure api
                api_version = "/api/2.0"
                api_command = "/workspace/import"
                url = f"https://{databricks_instance_id}{api_version}{api_command}"

                query_name = query_name.replace(".", "_")

                # File Path
                new_path_sql = str(os.path.join(dir_name_sql_local, query_name))
                if not new_path_sql.endswith(".sql"):
                    new_path_sql = new_path_sql + ".sql"

                obj_file = cdc_env_file.EnvironmentFile()
                if obj_file.file_exists(True, new_path_sql, None):
                    logger.info(f"File exists:{new_path_sql} - will attempt to remove")
                    try:
                        os.remove(new_path_sql)
                    except OSError as e:
                        logger.error(f"Error: {e.filename} - {e.strerror}.")
                else:
                    logger.info(f"File does not exist:{new_path_sql}")

                logger.info(f"Save SQL {query_name} to {new_path_sql}")
                obj_file.save_text_to_file(
                    dir_name_sql_local, query_text_original, new_path_sql, "sql"
                )

                # Prepare File to  Save
                content_sql = base64.b64encode(
                    query_text_original.encode("UTF-8")
                ).decode("UTF-8")

                data_sql = {
                    "content": content_sql,
                    "path": new_path_sql,
                    "language": "SQL",
                    "overwrite": True,
                    "format": "SOURCE",
                }

                # Post to Save File
                logger.info("------- Save SQL ----------------")
                logger.info(f"url:{str(url)}")
                headers_redacted = str(headers).replace(
                    databricks_access_token, "[databricks_access_token REDACTED]"
                )
                logger.info(f"headers:{headers_redacted}")
                logger.info(f"json:{str(data_sql)}")

                # Get Response
                # Post to Save File
                obj_http = cdc_env_http.EnvironmentHttp()
                response_sql = obj_http.post(
                    url=url, headers=headers, timeout=60, json=data_sql
                )

                # Get Response
                try:
                    response_sql_text = json.dumps(response_sql.json())
                    logger.info("- response : success  -")
                    response_sql_text_message = "Received SAVE-SQL-RESPONSE : "
                    response_sql_text_message += (
                        f"{response_sql.text} when posting to : {url}  "
                    )
                    response_sql_text_message += (
                        f"to save python pipeline with sql query: {query_name}"
                    )
                    response_sql_text_message += f"to {new_path_sql}"

                    logger.info(response_sql_text_message)

                except Exception as exception_check:
                    html_filter = HTMLFilter()
                    html_filter.feed(response_sql.text)
                    response_sql_text = html_filter.text
                    error_message = f"response : error - {str(exception_check)}"
                    error_message = (
                        error_message
                        + f"Error SAVE-SQL-RESPONSE converting response text:{response_sql_text} to json"
                    )
                    exc_info = sys.exc_info()
                    # Detailed traceback
                    logger_singleton.error_with_exception(error_message, exc_info)
                    raise
            except requests.exceptions.HTTPError as err:
                # Log error details
                exc_info = sys.exc_info()
                error_msg = f"HTTP Error occurred: {err}"
                error_msg = error_msg + (f"Status Code: {response_sql.status_code}")
                error_msg = error_msg + (f"Response Content: {response_sql.text}")
                error_msg = error_msg + (f"Request URL: {response_sql.url}")
                error_msg = error_msg + (
                    f"Request Headers: {response_sql.request.headers}"
                )
                if response_sql.request.body:
                    error_msg = error_msg + (
                        f"Request Body: {response_sql.request.body}"
                    )

                # Detailed traceback
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def extract_text_from_html(html_content):
        """
        Extracts text from HTML content.

        Args:
            html_content (str): The HTML content to extract text from.

        Returns:
            str: The extracted text from the HTML content.
        """
        html_filter = HTMLFilter()
        html_filter.feed(html_content)
        return html_filter.text

    # Helper functions

    @staticmethod
    def escape_brackets(query_text):
        """
        Escapes double quotes in the given query text.

        Args:
            query_text (str): The query text to escape.

        Returns:
            str: The query text with double quotes escaped.
        """
        query_text = query_text.replace('"', '\\"')
        return query_text

    @classmethod
    def get_base_path_local(
        cls, repository_path, data_product_id_root, data_product_id
    ):
        """
        Get the base path for a given repository path, data product ID root, and data product ID.

        Args:
            repository_path (str): The path of the repository.
            data_product_id_root (str): The root ID of the data product.
            data_product_id (str): The ID of the data product.

        Returns:
            str: The base path formed by concatenating the repository path, data product ID root, and data product ID.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_base_path_local"):
            try:
                base_path_local = "".join(
                    [
                        repository_path.rstrip("/"),
                        "/",
                        data_product_id_root,
                        "/",
                        data_product_id,
                        "/",
                    ]
                )
                base_path_local = base_path_local.replace("/Workspace", "")
                logger.info(f"base_path_local:{base_path_local}")
                return base_path_local

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_dir_name_python_local(cls, base_path_local):
        """
        Get the directory name for Python autogenerated files.

        Args:
            base_path_local (str): The base path for the directory.

        Returns:
            str: The directory name for Python autogenerated files.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_dir_name_python_local"):
            try:
                dir_name_python_local = "".join(
                    [base_path_local.rstrip("/"), "/autogenerated/python/"]
                )
                obj_file = cdc_env_file.EnvironmentFile()
                dir_name_python_local = obj_file.convert_to_current_os_dir(
                    dir_name_python_local
                )
                logger.info(f"dir_name_python_local:{dir_name_python_local}")
                return dir_name_python_local
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_dir_name_sql_server(cls, base_path_local_server):
        """
        Returns the directory name for SQL server based on the base path.

        Args:
            base_path_local_server (str): The base path for the SQL server.

        Returns:
            str: The directory name for SQL server.

        Raises:
            Exception: If an error occurs during the process.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("dir_name_sql_server"):
            try:
                dir_name_sql_server = "".join(
                    [base_path_local_server.rstrip("/"), "/autogenerated/sql/"]
                )
                dir_name_sql_server = dir_name_sql_server.replace("//", "/")
                logger.info(f"dir_name_sql_server:{dir_name_sql_server}")
                return dir_name_sql_server
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_dir_name_python_server(cls, base_path_local_server):
        """
        Returns the directory name for SQL server on the Python server.

        Args:
            base_path_local_server (str): The base path of the local server.

        Returns:
            str: The directory name for SQL server on the Python server.

        Raises:
            Exception: If an error occurs during the process.
        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("dir_name_sql_server"):
            try:
                dir_name_sql_server = "".join(
                    [base_path_local_server.rstrip("/"), "/autogenerated/sql/"]
                )
                dir_name_sql_server = dir_name_sql_server.replace("//", "/")
                logger.info(f"dir_name_sql_server:{dir_name_sql_server}")
                return dir_name_sql_server
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_dir_name_sql_local(cls, base_path_local):
        """
        Returns the directory name for SQL files based on the given base path.

        Args:
            base_path_local (str): The base path for the directory.

        Returns:
            str: The directory name for SQL files.

        """

        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_dir_name_sql_local"):
            try:
                dir_name_sql_local = "".join(
                    [base_path_local.rstrip("/"), "/autogenerated/sql/"]
                )
                dir_name_sql_local = dir_name_sql_local.replace("//", "/")
                obj_file = cdc_env_file.EnvironmentFile()
                dir_name_sql_local = obj_file.convert_to_current_os_dir(
                    dir_name_sql_local
                )
                logger.info(f"dir_name_sql_local:{dir_name_sql_local}")
                return dir_name_sql_local
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_headers(databricks_access_token):
        """
        Returns the headers required for making API requests with the specified access token.

        Parameters:
        databricks_access_token (str): The access token used for authentication.

        Returns:
        dict: The headers dictionary containing the authorization and content-type headers.
        """
        bearer = "Bearer " + databricks_access_token
        headers = {"Authorization": bearer, "Content-Type": "application/json"}
        return headers

    @staticmethod
    def get_api_command(query_name):
        """
        Returns the API command for retrieving a specific query by name.

        Args:
            query_name (str): The name of the query.

        Returns:
            str: The API command for retrieving the query.
        """
        api_command = f"/queries?page_size=50&page=1&order=-executed_at&q={query_name}"
        return api_command

    @staticmethod
    def get_url(databricks_instance_id, api_command):
        """
        Constructs the URL for the SQL API endpoint based on the Databricks instance ID and API command.

        Parameters:
        - databricks_instance_id (str): The ID of the Databricks instance.
        - api_command (str): The API command to be appended to the URL.

        Returns:
        - url (str): The constructed URL for the SQL API endpoint.
        """
        api_version = "/api/2.0/preview/sql"
        url = f"https://{databricks_instance_id}{api_version}{api_command}"
        return url

    @classmethod
    def process_request(cls, url, databricks_access_token):
        """
        Process a request to the specified URL with the provided access token.

        Args:
            url (str): The URL to send the request to.
            databricks_access_token (str): The access token to include in the request headers.

        Returns:
            requests.Response: The response object returned by the request.

        Raises:
            Exception: If an error occurs during the request.
        """
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("process_request"):
            try:
                headers = cls.get_headers(databricks_access_token)
                obj_http = cdc_env_http.EnvironmentHttp()
                response = obj_http.get(url, headers, 60, None)
                response.raise_for_status()
                logger.info("------- FETCH-SQL-RESPONSE ----------------")
                return response
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def process_response(response):
        results = response.json()
        return results

    @staticmethod
    def load_json(response):
        data = json.loads(response.text)
        return data

    @staticmethod
    def get_response_text_string(response_text, url, query_name):
        """
        Returns a formatted string describing the response received when fetching SQL query.

        Args:
            response_text (str): The response text received.
            url (str): The URL to which the request was posted.
            query_name (str): The name of the SQL query.

        Returns:
            str: A formatted string describing the response.

        """
        response_text_string = (
            f"Received FETCH-SQL with length : {len(str(response_text))}"
        )
        response_text_string += (
            f" when posting to : {url} to fetch sql query: {query_name}"
        )
        return response_text_string


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


class CDHObject(object):
    pass
