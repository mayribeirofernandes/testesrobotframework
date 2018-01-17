*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${url}      https://the-internet.herokuapp.com/login

*** Keywords ***
Dado que estou na tela de login no ${browser}
    open browser    ${url}   ${browser}

Quando realizo o login
    input text  id=username  tomsmith
    input text  id=password  SuperSecretPassword!
    click button   Login

Então devo visualizar a mensagem "${mensagem}"
    element text should be  id=flash  You logged into a secure area!\n×
