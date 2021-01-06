*** Settings ***
Resource  Steps.robot

*** Keywords ***
#### DADO
Dado que esteja conectado no webservice de consultas de CEP
    Conecta ao WebService

#### QUANDO
Quando o usuário consultar o CEP "${CEP_CONSULTADO}"
    Realiza requisição do CEP   ${CEP_CONSULTADO}

#### ENTÃO
Então deve ser mostrado o endereço "${ENDERECO}"
    Confere o status code       200
    Confere endereço do CEP     ${ENDERECO}

E deve ser mostrado o bairro "${BAIRRO}"
    Confere bairro do CEP       ${BAIRRO}

E deve ser mostrada a cidade "${CIDADE}"
    Confere cidade do CEP       ${CIDADE}

E deve ser mostrada a UF "${UF}"
    Confere UF do CEP       ${UF}

E deve ser mostrado o CEP "${CEP}"
    Confere CEP       ${CEP}

Então a mensagem "${ERROR_MSG}" deve ser retornada
    Confere o status code     200
    Confere Mensagem de Erro  ${ERROR_MSG}
