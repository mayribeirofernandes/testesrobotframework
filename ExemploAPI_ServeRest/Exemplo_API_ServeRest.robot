*** Settings ***
Library   RequestsLibrary
Library   Collections
Library   String


*** Variables ***
${ALIAS}   API_serverest


*** Test Cases ***
Testar a API pública de estudos serverest
    Iniciar sessão na API serverest
    Cadastrar usuário de teste
    Obter Token
    Cadastrar um produto
    Listar os produtos cadastrados


*** Keywords ***
Iniciar sessão na API serverest
    ${HEADERS}   Create Dictionary  Content-Type=application/json
    Create Session    alias=${ALIAS}    url=https://serverest.dev   headers=${HEADERS}

Cadastrar usuário de teste
    ${RANDOM_EMAIL}   Generate Random String    length=8    chars=[LETTERS]
    Set Suite Variable    ${RANDOM_EMAIL}
    ${BODY}   Create Dictionary    nome=Fulano de Teste   email=${RANDOM_EMAIL}@qa.com   password=teste   administrador=true
    ${RESPONSE}  Post Request    alias=${ALIAS}    uri=usuarios    data=${BODY}
    Log   ${RESPONSE.text}

Obter Token
    ${BODY}   Create Dictionary    email=${RANDOM_EMAIL}@qa.com   password=teste
    ${RESPONSE}  Post Request    alias=${ALIAS}    uri=login    data=${BODY}
    Log   ${RESPONSE.text}
    Dictionary Should Contain Item    ${RESPONSE.json()}    message    Login realizado com sucesso
    ${TOKEN}   Get From Dictionary    ${RESPONSE.json()}    authorization
    Set Suite Variable    ${TOKEN}

Cadastrar um produto
    ${BODY}   Create Dictionary    nome=TesteProd   preco=155   descricao=meu produto de teste   quantidade=10
    ${HEADERS}   Create Dictionary    Authorization=${TOKEN}
    ${RESPONSE}  Post Request    alias=${ALIAS}    uri=produtos    data=${BODY}  headers=${HEADERS}
    Log   ${RESPONSE.text}
    Dictionary Should Contain Item    ${RESPONSE.json()}    message    Cadastro realizado com sucesso
    ${ID_PRODUTO_CADASTRADO}  Get From Dictionary    ${RESPONSE.json()}    _id
    Set Suite Variable   ${ID_PRODUTO_CADASTRADO}

Listar os produtos cadastrados
    ${HEADERS}   Create Dictionary    Authorization=${TOKEN}
    ${PARAMS}    Create Dictionary    _id=${ID_PRODUTO_CADASTRADO}
    ${RESPONSE}  Get Request    alias=${ALIAS}    uri=produtos   params=${PARAMS}  headers=${HEADERS}
    Log   ${RESPONSE.text}
