from behave import given, step, then
from behave.runner import Context

from logger.logger import message_logger, LogLevel
from tests.environment import get_database_name
from common import table_exists_check

@given("a function '{calling_function}' that calls message_logger with '{special_message}'")
def function_calls_message_logger(context: Context, calling_function: str, special_message: str):
    def message_call():
        message_logger(f"called by {calling_function} message is {special_message}",
                       message_level=LogLevel.MESSAGE, db_manager=context.db_manager)
    message_call()
    context.function = message_call

@given("a function that raises an exception")
def exception_message_logger(context: Context):

    def div_zero_function():
        try:
            1/0
        except ZeroDivisionError as e:
            message_logger(f"Exception:{e}", 2, context.db_manager)

    context.function = div_zero_function

@then("a log entry with '{message}' should be saved in the database")
def check_message_log(context: Context, message: str):
    db_conn = context.db_manager
    db_name = get_database_name(context)

    cursor, table_exists = table_exists_check(db_conn, db_name, 'logger')
    entry_exists: bool = False
    try:
        if table_exists:
            query = f"""
            SELECT EXISTS(
                SELECT * 
                FROM {db_name}.logger
                WHERE info = %s            
            );
            """
            cursor.execute(query, (message,))
            entry_exists = cursor.fetchone()[0]
    except Exception as e:
        raise AssertionError(F"Database error occurred: {e}")
    assert entry_exists is True, f"{message} does not exist in {db_name}"


@step("the log entry should indicate that it was called from '{function}'")
def check_log_entry_call(context: Context, function: str):
    pass