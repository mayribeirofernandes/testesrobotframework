*** Settings ***
Library     RequestsLibrary
Library     Collections

*** Variable ***
${HOST}         https://webmaniabr.com/api/1/cep
${APP_KEY}      njMf2EiyQ17g6C3vLUxk1yEsWTforVqf
${APP_SECRET}   EgpTuUcM93IqHY8icgR3cK6Cn4bOlkQwSlfLd6ryMjrhhwMW

*** Keywords ***
#### STEPS
Conecta ao WebService
    Create Session      consultaCEP     ${HOST}    disable_warnings=True

Realiza requisição do CEP
    [Arguments]         ${CEP_DESEJADO}
    ${RESPOSTA}=        Get Request  consultaCEP  /${CEP_DESEJADO}/?app_key=${APP_KEY}&app_secret=${APP_SECRET}
    Log                 Resposta: ${RESPOSTA.text}
    Set Test Variable   ${RESPOSTA}

Confere o status code
    [Arguments]     ${STATUS_ESPERADO}
    Should Be Equal As Strings   ${RESPOSTA.status_code}  ${STATUS_ESPERADO}
    Log             Status Code Retornado: ${RESPOSTA.status_code} -- Status Code Esperado: ${STATUS_ESPERADO}

Confere endereço do CEP
    [Arguments]         ${ENDERECO}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  endereco   ${ENDERECO}

Confere bairro do CEP
    [Arguments]         ${BAIRRO}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  bairro   ${BAIRRO}

Confere cidade do CEP
    [Arguments]         ${CIDADE}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  cidade   ${CIDADE}

Confere UF do CEP
    [Arguments]         ${UF}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  uf   ${UF}

Confere CEP
    [Arguments]         ${CEP}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  cep   ${CEP}

Confere Mensagem de Erro
    [Arguments]         ${ERROR_MSG}
    Dictionary Should Contain Item  ${RESPOSTA.json()}  error   ${ERROR_MSG}
