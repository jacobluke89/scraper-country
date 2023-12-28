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
    ans_2 = add(21,21, 'donkey!')
    ans = NEW_FUNCTION_DIV(21, 0)
    print(ans)
    print(ans_2)