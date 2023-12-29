from behave import given
from behave.runner import Context

from logger.logger import logger


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
