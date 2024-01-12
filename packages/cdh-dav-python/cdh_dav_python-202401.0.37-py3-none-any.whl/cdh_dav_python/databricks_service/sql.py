import traceback  # don't remove required for error handling
import json
import base64
import requests
import re
import os
import sys
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
    def fetch_and_process_pipeline(
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
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_and_process_pipeline"):
            try:
                logger.info("------- FETCH-SQL ----------------")
                (
                    query_text,
                    variable_text,
                    query_text_original,
                    dir_name_python,
                    dir_name_sql,
                ) = cls.fetch_sql(
                    databricks_access_token,
                    repository_path,
                    data_product_id_root,
                    data_product_id,
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

                logger.info("------- PROCESS-SQL ----------------")
                cls.process_pipeline(
                    arg_dictionary,
                    environment,
                    query_name,
                    query_text,
                    variable_text,
                    databricks_access_token,
                    dir_name_python,
                    dir_name_sql,
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
        response = "not set"

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
        query_text = query_text_original.replace(
            "{{", "TEMPORARY_OPEN_BRACKET"
        ).replace("}}", "TEMPORARY_CLOSE_BRACKET")
        query_text = query_text.replace("{", "{{").replace("}", "}}")
        return query_text

    @classmethod
    def fetch_sql(
        cls,
        databricks_access_token,
        repository_path,
        data_product_id_root,
        data_product_id,
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
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("fetch_sql"):
            try:
                base_path = cls.get_base_path(
                    repository_path, data_product_id_root, data_product_id
                )
                dir_name_python = cls.get_dir_name_python(base_path)
                dir_name_sql = cls.get_dir_name_sql(base_path)
                message = f"dir_name_sql:{dir_name_sql}"
                sys.path.append(dir_name_sql)
                logger.info(message)
                message = f"dir_name_python:{dir_name_python}"
                logger.info(message)
                api_command = cls.get_api_command(query_name)
                url = cls.get_url(databricks_instance_id, api_command)
                logger.info(
                    f"- Attempting FETCH-SQL for query_name:{query_name} url:{str(url)} ----"
                )

                try:
                    response = cls.process_request(url, databricks_access_token)
                    results = cls.process_response(response)
                    response_text = json.dumps(results)
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
                        ph = "TEMPORARY_OPEN_BRACKET"
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
                    str(dir_name_python),
                    str(dir_name_sql),
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
                    # new_param_code = new_param_code + f"-- MAGIC {line} =  ''\n"
                    if line in arg_dictionary:
                        new_param_code = (
                            new_param_code
                            + f"dbutils.widgets.text('{line}', '{arg_dictionary[line]}')\n"
                        )
                    else:
                        print(f"{line} not in arg_dictionary")
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
                    # new_param_code = new_param_code + f"-- MAGIC {line} =  ''\n"
                    if line in arg_dictionary:
                        line_strip = line.strip().replace('"', "")
                        dict_code = (
                            dict_code + f"'{line_strip}':'{arg_dictionary[line]}',"
                        )
                    else:
                        print(f"{line} not in arg_dictionary")
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
        print_query_text = f"print(sql_command_text)"
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
    def process_pipeline(
        cls,
        arg_dictionary,
        environment,
        query_name,
        query_text,
        variable_text,
        databricks_access_token,
        dir_name_python,
        dir_name_sql,
        data_product_id,
        databricks_instance_id,
        pipeline_name,
        yyyy_param,
        mm_param,
        dd_param,
        transmission_period,
        running_local,
    ):
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
            dir_name_python,
            pipeline_name,
            python_text,
            data_product_id,
            running_local,
        )

        # Save SQL query
        cls.save_pipline_sql(
            databricks_instance_id,
            databricks_access_token,
            dir_name_sql,
            query_name,
            query_text,
        )

    @classmethod
    def save_pipeline_python(
        cls,
        databricks_instance_id,
        databricks_access_token,
        dir_name_python,
        pipeline_name,
        content_text,
        data_product_id,
        running_local,
    ):
        tracer, logger, logger_singleton = cls.initialize_logging_and_tracing()

        with tracer.start_as_current_span("save_pipeline_python"):
            try:
                # configure api
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

                # File Path
                new_path_python = str(os.path.join(dir_name_python, pipeline_name))
                if not new_path_python.endswith(".py"):
                    new_path_python = new_path_python + ".py"

                obj_file = cdc_env_file.EnvironmentFile()
                if obj_file.file_exists(True, new_path_python, None):
                    try:
                        os.remove(new_path_python)
                    except OSError as e:
                        logger.error(f"Error: {e.filename} - {e.strerror}.")

                logger.info(f"Save Python {pipeline_name} to {new_path_python}")
                obj_file.save_text_to_file(content_text, new_path_python, "py")

                # Directory Path
                sys.path.append(dir_name_python)
                isdir = os.path.isdir(dir_name_python)
                logger.info(f"dir_name_python: isdir:{isdir}")

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
                    data = json.loads(response_python.text)
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
                except Exception as exception_check:
                    html_filter = HTMLFilter()
                    html_filter.feed(response_python.text)
                    response_python_text = html_filter.text
                    logger.info(f"- response : error - {str(exception_check)}")
                    logger.info(
                        f"Error SAVE-PYTHON-RESPONSE converting response text:{response_python_text} to json"
                    )

                logger.info(response_python_text)

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
        dir_name_sql,
        query_name,
        query_text_original,
    ):
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
                new_path_sql = str(os.path.join(dir_name_sql, query_name))
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
                obj_file.save_text_to_file(query_text_original, new_path_sql, "sql")

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
                    url=url, headers=headers, timeout=60, json=data_python
                )

                config_sql = {"response_sql": response_sql}
                return config_sql

            except requests.exceptions.HTTPError as err:
                # Log error details
                exc_info = sys.exc_info()
                error_msg = f"HTTP Error occurred: {err}"
                error_msg = error_msg + (f"Status Code: {response_sql.status_code}")
                error_msg = error_msg + (f"Response Content: {response_sql.text}")
                error_msg = error_msg + (f"Request URL: {response_sql.url}")
                if response_sql.request.body:
                    error_msg = error_msg + (
                        f"Request Body: {response_sql.request.body}"
                    )

                # Detailed traceback
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
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
        query_text = query_text.replace('"', '\\"')
        return query_text

    @staticmethod
    def get_base_path(repository_path, data_product_id_root, data_product_id):
        base_path = "".join(
            [
                repository_path.rstrip("/"),
                "/",
                data_product_id_root,
                "/",
                data_product_id,
                "/",
            ]
        )
        base_path = base_path.replace("/Workspace", "")
        return base_path

    @staticmethod
    def get_dir_name_python(base_path):
        """
        Get the directory name for Python autogenerated files.

        Args:
            base_path (str): The base path for the directory.

        Returns:
            str: The directory name for Python autogenerated files.
        """
        dir_name_python = "".join([base_path.rstrip("/"), "/autogenerated/python/"])
        obj_file = cdc_env_file.EnvironmentFile()
        dir_name_python = obj_file.convert_to_current_os_dir(dir_name_python)
        return dir_name_python

    @staticmethod
    def get_dir_name_sql(base_path):
        """
        Returns the directory name for SQL files based on the given base path.

        Args:
            base_path (str): The base path for the directory.

        Returns:
            str: The directory name for SQL files.

        """
        dir_name_sql = "".join([base_path.rstrip("/"), "/autogenerated/sql/"])
        dir_name_sql = dir_name_sql.replace("//", "/")
        obj_file = cdc_env_file.EnvironmentFile()
        dir_name_sql = obj_file.convert_to_current_os_dir(dir_name_sql)
        return dir_name_sql

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
        api_command = f"/queries?page_size=50&page=1&order=-executed_at&q={query_name}"
        return api_command

    @staticmethod
    def get_url(databricks_instance_id, api_command):
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
                logger.info(f"------- FETCH-SQL-RESPONSE ----------------")
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
