*** Settings ***
Documentation     Sikuli Library Demo
Test Setup        Add Needed Image Path
Test Teardown     Stop Remote Server
Library           SikuliLibrary

*** Variables ***
${IMAGE_DIR}      ${CURDIR}\\img

*** Test Cases ***
Windows Notpad Hellow World
    Open Windows Start Menu
    Open Notepad
    Input In Notepad
    Quit Without Save

*** Keywords ***
Add Needed Image Path
    Add Image Path    ${IMAGE_DIR}

Open Windows Start Menu
    Click    windows_start_menu.png

Open Notepad
    Click    notepad.png

Input In Notepad
    Input Text    notepad_workspace.png    Hello World
    Screen Should Contain    helloword.png

Quit Without Save
    Click    close.png