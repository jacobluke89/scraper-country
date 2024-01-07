from behave import when, step
from behave.runner import Context

from tests.environment import get_database_name


@when("I call the decorated function")
@when("I call the message function")
@when("I call the exception function")
def call_function(context: Context):
    func = context.function
    func()

@step("the log level should be {level_name} and function name is {func_name}")
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

    if exists is True:
        assert True
        return
    assert False
