*** Settings ***
Documentation     Sikuli Library Demo
Test Setup        Carrega diretório de imagens
Test Teardown     Stop Remote Server
Library           SikuliLibrary

*** Variables ***
#As imagens da pasta img devem estar de acordo com a interface do seu PC!!!! Tire os prints necessários!
${IMAGE_DIR}      ${CURDIR}\\img

*** Test Cases ***
Windows Notepad Hello World
    Abre o menu inicial do windows
    Abre o notepad++
    Digita "Hello Word"
    Fecha o notepad++

*** Keywords ***
Carrega diretório de imagens
    Add Image Path    ${IMAGE_DIR}

Abre o menu inicial do windows
    Click    windows_start_menu.png

Abre o notepad++
    Click    notepad.png

Digita "${TEXTO}"
    Input Text    notepad_workspace.png    ${TEXTO}
    Screen Should Contain    helloword.png

Fecha o notepad++
    Click    close.png