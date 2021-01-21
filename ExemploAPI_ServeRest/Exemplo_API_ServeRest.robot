*** Settings ***
Documentation   Testes utilizando as novas keywords da RequestsLibrary na versão 8
Library         RequestsLibrary
Library         Collections
Library         FakerLibrary   locale=pt_br


*** Variables ***
${ALIAS}   API_serverest


*** Test Cases ***
Testar a API pública de estudos serverest
    Iniciar sessão na API serverest
    Cadastrar usuário de teste
    Obter Token
    Cadastrar um produto
    Listar o produto cadastrado


*** Keywords ***
Cria dados aleatórios do usuário
    ${RANDOM_NOME}    FakerLibrary.Name
    ${RANDOM_EMAIL}   FakerLibrary.Email
    ${RANDOM_PWD}     FakerLibrary.Password
    ${USUARIO}    Create Dictionary    nome=${RANDOM_NOME}  email=${RANDOM_EMAIL}  senha=${RANDOM_PWD}
    Set Suite Variable    ${USUARIO}

Iniciar sessão na API serverest
    ${HEADERS}   Create Dictionary  Content-Type=application/json
    Create Session    alias=${ALIAS}    url=https://serverest.dev   headers=${HEADERS}   disable_warnings=1

Cadastrar usuário de teste
    Cria dados aleatórios do usuário
    ${BODY}      Create Dictionary   nome=${USUARIO.nome}   email=${USUARIO.email}   password=${USUARIO.senha}   administrador=true
    ${RESPONSE}  POST On Session     alias=${ALIAS}    url=usuarios    json=${BODY}
    Log   Resposta Retornada: ${\n}${RESPONSE.text}

Obter Token
    ${BODY}      Create Dictionary   email=${USUARIO.email}   password=${USUARIO.senha}
    ${RESPONSE}  POST On Session     alias=${ALIAS}    url=login    json=${BODY}
    Log   Resposta Retornada: ${\n}${RESPONSE.text}
    Dictionary Should Contain Item    ${RESPONSE.json()}    message    Login realizado com sucesso
    ${TOKEN}     Get From Dictionary    ${RESPONSE.json()}    authorization
    Set Suite Variable    ${TOKEN}

Cadastrar um produto
    ${RANDOM_PROD}   FakerLibrary.Word
    Set Suite Variable    ${RANDOM_PROD}
    ${BODY}      Create Dictionary  nome=${RANDOM_PROD}   preco=155   descricao=meu produto de teste   quantidade=10
    ${HEADERS}   Create Dictionary  Authorization=${TOKEN}
    ${RESPONSE}  POST On Session    alias=${ALIAS}    url=produtos    json=${BODY}  headers=${HEADERS}
    Log   Resposta Retornada: ${\n}${RESPONSE.text}
    Dictionary Should Contain Item    ${RESPONSE.json()}    message    Cadastro realizado com sucesso
    ${ID_PRODUTO_CADASTRADO}  Get From Dictionary    ${RESPONSE.json()}    _id
    Set Suite Variable   ${ID_PRODUTO_CADASTRADO}

Listar o produto cadastrado
    ${HEADERS}   Create Dictionary  Authorization=${TOKEN}
    ${PARAMS}    Create Dictionary  _id=${ID_PRODUTO_CADASTRADO}
    ${RESPONSE}  GET On Session     alias=${ALIAS}    url=produtos   params=${PARAMS}  headers=${HEADERS}
    Log   Resposta Retornada: ${\n}${RESPONSE.text}
    Dictionary Should Contain Item    ${RESPONSE.json()}    quantidade   1
    Dictionary Should Contain Item    ${RESPONSE.json()["produtos"][0]}    nome        ${RANDOM_PROD}
    Dictionary Should Contain Item    ${RESPONSE.json()["produtos"][0]}    preco       155
    Dictionary Should Contain Item    ${RESPONSE.json()["produtos"][0]}    descricao   meu produto de teste
    Dictionary Should Contain Item    ${RESPONSE.json()["produtos"][0]}    quantidade  10
    Dictionary Should Contain Key     ${RESPONSE.json()["produtos"][0]}    _id
