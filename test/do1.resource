*** Settings ***
Library            RobotFrameworkBasic

*** Keywords ***
suite-setup
    Config Init

test-setup
    Config Use Suite Case List

test-setup2
    Log    123
    
func1
    [Arguments]    ${param1}
    Log    ${param1}