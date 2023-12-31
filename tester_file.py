from logger.logger import logger, message_logger

@logger('hello there', )
def add(a,b, *args):
    return a + b

# @logger()
def NEW_FUNCTION_DIV(a, b):
    try:
        return a/b

    except ZeroDivisionError as e:
        message_logger(f'failed see in NEW_FUNCTION_DIV: {e}')


if __name__ == "__main__":
    # ans_2 = add(21,21, 'donkey!')
    # ans = NEW_FUNCTION_DIV(21, 0)
    # print(ans)
    # print(ans_2)
    log_level_dict = {"DEBUG": 1,
                      "ERROR": 2,
                      "INFO": 3}
    param = 'er'
    try:
        # Check if the key exists in the dictionary
        if param not in log_level_dict:
            raise ValueError(f"Key '{param}' not found in the dictionary")
        val = log_level_dict[param]
    except ValueError as e:
        # Handle the exception
        print(f"Error occurred: {e}")
    else:
        # This block executes if no exception was raised
        print(f"The value is {val}")