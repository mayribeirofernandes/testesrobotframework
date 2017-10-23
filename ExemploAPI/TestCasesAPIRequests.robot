*** Settings ***
Documentation       Suíte de Exemplo de testes API com o Robot Framework
Resource            BDDpt-br.robot
Resource            Resource.robot

*** Test Case ***
Cenário 01: Consulta de endereço existente
    Dado que esteja conectado no webservice de consultas de CEP
    Quando o usuário consultar o CEP "88056-000"
    Então deve ser mostrado o endereço "Avenida Luiz Boiteux Piazza"
    E deve ser mostrado o bairro "Cachoeira do Bom Jesus"
    E deve ser mostrada a cidade "Florianópolis"
    E deve ser mostrada a UF "SC"
    E deve ser mostrado o CEP "88056000"

Cenário 02: Consulta de endereço inexistente
    Dado que esteja conectado no webservice de consultas de CEP
    Quando o usuário consultar o CEP "99999-999"
    Então nenhum dado deve ser mostrado para o CEP "99999999"

*** Keywords ***
Que esteja conectado no webservice de consultas de CEP
    Conecta ao WebService

O usuário consultar o CEP "${CEP_CONSULTADO}"   
    Realiza requisição do CEP   ${CEP_CONSULTADO}

Deve ser mostrado o endereço "${ENDERECO}"
    Confere o status code       200
    Confere endereço do CEP     ${ENDERECO}

Deve ser mostrado o bairro "${BAIRRO}"
    Confere bairro do CEP       ${BAIRRO}

Deve ser mostrada a cidade "${CIDADE}"  
    Confere cidade do CEP       ${CIDADE}

Deve ser mostrada a UF "${UF}"  
    Confere UF do CEP       ${UF}    

Deve ser mostrado o CEP "${CEP}"
    Confere CEP       ${CEP}

Nenhum dado deve ser mostrado para o CEP "${CEP}"
    Confere o status code       200
    Confere endereço do CEP     ${EMPTY}
    Confere bairro do CEP       ${EMPTY}
    Confere cidade do CEP       ${EMPTY}
    Confere UF do CEP           ${EMPTY}
    Confere CEP                 ${CEP}