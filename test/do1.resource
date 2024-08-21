*** Settings ***
Library            RobotFrameworkBasic

*** Keywords ***
suite-setup
    Log    setup

test-setup
    Log    test setup

test-setup2
    Log    123
    
func1
    [Arguments]    ${param1}
    Log    ${param1}