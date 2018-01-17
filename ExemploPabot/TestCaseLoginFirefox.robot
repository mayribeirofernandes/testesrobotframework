*** Settings ***
Resource  ./Resource_steps_login.robot
Suite Teardown  Close browser

*** Test Cases ***
Cenário: Login com sucesso
    Dado que estou na tela de login no Firefox
    Quando realizo o login
    Então devo visualizar a mensagem "You logged into a secure area!"
