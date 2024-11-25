*** Settings ***
Library            RobotFrameworkBasic

*** Keywords ***
suite-setup
    Print    setup

test-setup
    Print    test setup

test-setup2
    Print    123
    
func1
    [Arguments]    ${param1}
    Print    ${param1}