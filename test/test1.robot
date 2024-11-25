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
    Assert Calculate    100    -    16    ==    88
#    Log    ${_config}[a]
#    Func1    ${_config}[a]

#02_do2
#    Log    ${_config}[a]
#    Func1    ${_config}[a]
