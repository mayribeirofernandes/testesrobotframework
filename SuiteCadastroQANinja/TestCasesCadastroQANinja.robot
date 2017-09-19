*** Settings ***
Resource    ResourceCadastroQANinja.robot
Test Teardown   Close Browser

*** Test Cases ***
Validar Acesso ao Site QA Ninja
    Acessar Página Principal

Validar Acesso à Página de Cadastro
    Acessar Página Principal
    Clicar em Cadastro

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