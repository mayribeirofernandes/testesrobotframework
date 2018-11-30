*** Settings ***
Documentation   Faker com dados brasileiros
Library         FakerLibrary    locale=pt_BR

*** Test Cases ***
Teste dados fakes BRASILEIROS
    ${CPF}      FakerLibrary.cpf
    ${NOME}     FakerLibrary.name
    ${CIDADE}   FakerLibrary.city
    ${CEP}      FakerLibrary.postcode
    ${ESTADO}   FakerLibrary.state
