@setup_message_logger_database
@teardown_message_logger_database
Feature: Message logging System

    Scenario: Log a message from the calling function using message_logger
    Given a function 'message_call' that calls message_logger with 'Special message'
    When I call the message function
    Then a log entry with 'MESSAGE LOGGER: called by message_call message is Special message' should be saved in the database
    And the log level should be message and function name is message_call
