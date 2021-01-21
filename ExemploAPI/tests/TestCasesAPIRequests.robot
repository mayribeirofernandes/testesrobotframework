*** Settings ***
Documentation       Suíte de Exemplo de testes API com o Robot Framework
Resource            ../resources/BDDImplementation.robot

*** Test Case ***
Cenário 01: Consulta de endereço existente
    [Tags]  jenkins
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
    Então a mensagem "CEP INVÁLIDO" deve ser retornada
