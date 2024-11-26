*** Settings ***
Resource    ./do1.resource

*** Test Cases ***
01_do1
    Evaluate    print(sys.argv)
    Robot Check Param    467    str
    Robot Check Param    1    int
    Robot Check Param    1   float
    Robot Check Param    true    bool
    Robot Check Param    false    bool
    Robot Check Param    ${EMPTY}    bool
    Robot Check Param    [1,2,3]    list
    Robot Check Param    {1:1,2:2}    dict
    Set Global Variable    ${global_var}    123
    Error    asdfa.error
    Warn    asdfa.warn
    Get Robot Variable    global_var
    Always True
    Print    123    log=1
    Assert Equal    111    111
    Assert Equal    1.0    1    float
    Assert Calculate    12    +    13    >    10    <=    25
    ${number1}    Convert Value To Number    1
    Should Be Equal    ${number1}    ${1}
    ${number1}    Convert Value To Number    1.2
    Should Be Equal    ${number1}    ${1.2}
    ${number1}    Convert Value To Number    ${3.3}
    Should Be Equal    ${number1}    ${3.3}
    ${number1}    Convert Value To Number    ${6}
    Should Be Equal    ${number1}    ${6}
#    Log    ${_config}[a]
#    Func1    ${_config}[a]

#02_do2
#    Log    ${_config}[a]
#    Func1    ${_config}[a]
