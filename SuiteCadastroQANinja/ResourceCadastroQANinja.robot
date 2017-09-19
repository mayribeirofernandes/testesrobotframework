*** Settings ***
Library     Selenium2Library
Library     FakerLibrary

*** Variables ***
${URL}                      http://ninjainvoices.herokuapp.com/
${NAVEGADOR}                chrome
${TITULO_PAGINA}                Ninja Invoices
${BOTAO_CADASTRO}               xpath=.//*[@id="register"]
${TITULO_PAGINA_CADASTRO}       css=#register_form > h5
${TEXTO_ESPERADO_PAGINA_CAD}    Seja bem vindo ao Invoices faça seu cadastro aqui
${CAMPO_NOME}                   register_name
${CAMPO_EMAIL}                  register_email
${CAMPO_SENHA}                  register_password
${BOTAO_CAD_USUARIO}            register_form
${TITULO_PAGINA_BOASVINDAS}     xpath=.//*[@id="page_title"]
${NOME_USUARIO}                 Usuario Novo Teste
${EMAIL_INVALIDO}               teste_email_invalido
${ALERTA}                       xpath=.//div[@class='alert alert-warning']
${ALERTA_EMAIL_INVALIDO}        Please enter valid e-mail address.

*** Keywords ***
Acessar Página Principal
    Open Browser        ${URL}  ${NAVEGADOR}
    Title Should Be     ${TITULO_PAGINA}

Clicar em Cadastro
    Wait Until Element Is Enabled   ${BOTAO_CADASTRO}
    Click Element                   ${BOTAO_CADASTRO}
    Wait Until Element Is Visible   ${TITULO_PAGINA_CADASTRO}
    ${TEXTO_ATUAL_PAGINA_CAD}=      Get Text    ${TITULO_PAGINA_CADASTRO}
    Element Text Should Be          ${TITULO_PAGINA_CADASTRO}   ${TEXTO_ESPERADO_PAGINA_CAD}    O Título atual [${TEXTO_ATUAL_PAGINA_CAD}] está errado. Esperado: [${TEXTO_ESPERADO_PAGINA_CAD}]

Inserir Nome Completo
    Wait Until Element Is Enabled   ${CAMPO_NOME}
    Input Text                      ${CAMPO_NOME}   ${NOME_USUARIO}

Inserir Email Válido
    Wait Until Element Is Enabled   ${CAMPO_EMAIL}
    ${EMAIL_USUARIO}=               FakerLibrary.Email
    Input Text                      ${CAMPO_EMAIL}   ${EMAIL_USUARIO}

Inserir Senha
    Wait Until Element Is Enabled   ${CAMPO_SENHA}
    ${SENHA_USUARIO}=               FakerLibrary.Password   8   True
    Input Password                  ${CAMPO_SENHA}   ${SENHA_USUARIO}

Submeter Cadastro
    Wait Until Element Is Enabled   ${BOTAO_CAD_USUARIO}
    Submit Form                     ${BOTAO_CAD_USUARIO}

Conferir Mensagem de Boas Vindas 
    Wait Until Element Is Visible   ${TITULO_PAGINA_BOASVINDAS}
    Page Should Contain             Olá, ${NOME_USUARIO}, seja bem vindo ao Invoices.

Inserir Email Inválido
    Wait Until Element Is Enabled   ${CAMPO_EMAIL}
    Input Text                      ${CAMPO_EMAIL}   ${EMAIL_INVALIDO}   

Conferir Mensagem de Alerta de Email Inválido 
    Wait Until Element Is Enabled   ${ALERTA}
    ${ALERTA_ATUAL}=                Get Text    ${ALERTA}
    Element Text Should Be          ${ALERTA}   ${ALERTA_EMAIL_INVALIDO}    O Alerta atual [${ALERTA_ATUAL}] está errado. Esperado: [${ALERTA_EMAIL_INVALIDO}]

    

