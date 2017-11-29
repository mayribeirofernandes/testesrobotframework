*** Settings ***
Resource    ResourceCadastroQANinja.robot
Test Teardown   Close Browser

*** Test Cases ***
Validar Cadastro de Usuário: Email Válido
    Acessar Página Principal
    Clicar em Cadastro
    Inserir Nome Completo
    Inserir Email Válido
    Inserir Senha
    Submeter Cadastro
    Conferir Mensagem de Boas Vindas

Validar Cadastro de Usuário: Email Inválido
    Acessar Página Principal
    Clicar em Cadastro
    Inserir Nome Completo
    Inserir Email Inválido
    Inserir Senha
    Submeter Cadastro
    Conferir Mensagem de Alerta de Email Inválido    