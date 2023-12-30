from behave import given, step, when, then
from behave.runner import Context

from database_manager.connection import DBManager
from logger.logger import logger, save_to_db
from tests.environment import get_database_name


def successful_function():
    pass

def error_function():
    pass

def decorated_function():
    pass


run_functions_dict = {
    "successful_function": successful_function,
    "error_function": error_function,
    "decorated_function": decorated_function
}

@given("A function named {function_name}")
def run_function(context: Context, function_name):
    if function_name in run_functions_dict:
        context.function = run_functions_dict[function_name]
    else:
        raise ValueError(f"Function '{function_name}' is not defined.")

@given('a decorated function "{function_name}" with a log message "{log_message}"')
def given_decorated_function_with_log_message(context: Context, function_name: str, log_message: str):
    @logger(log_message)
    def inner_decorated_function():
        pass

    # Store the function in the context for use in subsequent steps
    context.function = inner_decorated_function

@step('a log message "{log_message}" is prepared for logging')
def set_log_message(context: Context, log_message: str):
    context.log_message = log_message

@when('I call save_to_db with the function name and log message')
def save_log_message(context):
    print(f'context.function: {context.function.__name__}')
    function_name = context.function.__name__
    save_to_db(function_name, context.log_message, db_manager=context.db_manager)

@then('a log entry should be saved in the database')
def check_for_log_entry(context: Context):

    db_connection = context.db_manager
    db_name = get_database_name(context)

    expected_function_name = context.function.__name__
    expected_message = context.log_message

    log_entry_exists = check_log_entry_exists(db_connection, db_name,  expected_function_name, expected_message)

    assert log_entry_exists, "Expected log entry was not found in the database"


@step('the log level should be {level_name} and function name is {func_name}')
def check_log_level(context: Context, level_name: str, func_name: str):
    db = get_database_name(context)
    with context.db_manager.get_cursor() as cursor:
        log_query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM {db}.logger
            WHERE function_name = %s AND level_name = %s
        );
        """
        cursor.execute(log_query, (func_name, level_name))
        exists = cursor.fetchone()[0]
        print('EXISTS', exists)
    if exists is True:
        assert True
        return
    assert False

def check_log_entry_exists(db_conn: DBManager, db: str, func_name: str, message: str):
    table_exists_query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = 'logger'
        );
        """
    with db_conn.get_cursor() as cursor:
        cursor.execute(table_exists_query, (db,))
        exists = cursor.fetchone()[0]
    if exists:
        log_query = f"""
        SELECT EXISTS (
            SELECT *
            FROM {db}.logger
            WHERE function_name = %s AND info = %s
        );
        """
        cursor.execute(log_query, (func_name, message))
        log_entry_exists = cursor.fetchone()[0]
        print(f'LOG ENTRY, {log_entry_exists}')
        return log_entry_exists
    else:
        print("Log table does not exist.")
        return False
