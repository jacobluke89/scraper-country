@setup_logger_database
@teardown_logger_database
Feature: Database Logging System

  Scenario: Successfully log a message with default info level
    Given a function named successful_function
    And a log message 'Test log message' is prepared for logging
    When I call save_to_db with the function name and log message
    Then a log entry should be saved in the database
    And the log level should be info and function name is successful_function

  Scenario: Successfully log a message with a specified error level
    Given a function named error_function
    And a log message 'Error occurred' is prepared for logging
    When I call save_to_db with the function name, a log message and the log level, ERROR level
    Then a log entry should be saved in the database
    And the log level should be error and function name is error_function

  Scenario: Successfully log a message with a specified error level
    Given a function named debug_function
    And a log message 'Debugging..' is prepared for logging
    When I call save_to_db with the function name, a log message and the log level, DEBUG level
    Then a log entry should be saved in the database
    And the log level should be debug and function name is debug_function

  Scenario: Log a message before function execution
    Given a decorated function 'decoratedFunction' with a log message 'Executing function'
    When I call the decorated function
    Then a log entry with 'Executing function' should be saved in the database before the function execution
