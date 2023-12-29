Feature: Message logging System

    Scenario: Log a message from the calling function using message_logger
    Given a function "callingFunction" that calls message_logger with "Special message"
    When I call the calling function
    Then a log entry with "MESSAGE LOGGER: Special message" should be saved in the database
    And the log entry should indicate that it was called from "callingFunction"
