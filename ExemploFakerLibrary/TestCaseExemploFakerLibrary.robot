*** Settings ***
Documentation     Exemplo de uso da Library Faker
Library           FakerLibrary

*** Test Cases ***
Imprime exemplos de utilidades da library FakerLibrary
  Exemplos relacionados a pessoa
  Exemplos relacionados a datas
  Exemplos diversos

*** Keywords ***
Exemplos relacionados a pessoa
  ${NOMEFAKE}                 FakerLibrary.Name
  ${ENDERECOFAKE}             FakerLibrary.Address
  ${TELEFONEFAKE}             FakerLibrary.Phone Number
  ${CIDADEFAKE}               FakerLibrary.City
  ${CODIGOPOSTALFAKE}         FakerLibrary.Postalcode
  ${TRABALHOFAKE}             FakerLibrary.Job
  @{PESSOA}                   Create List    Nome Aleatório: ${NOMEFAKE}  Endereço Aleatório: ${ENDERECOFAKE}
  ...                         Telefone Aleatório: ${TELEFONEFAKE}  Cidade Aleatória: ${CIDADEFAKE}
  ...                         CódigoPostal Aleatório: ${CODIGOPOSTALFAKE}   Trabalho: ${TRABALHOFAKE}
  Log Many    @{PESSOA}

Exemplos relacionados a datas
  ${DATAFAKE}                 FakerLibrary.Date
  ${MESFAKE}                  FakerLibrary.Month
  ${ANOFAKE}                  FakerLibrary.Year
  ${DIADASEMANAFAKE}          FakerLibrary.Day Of Week
  ${DIADOMESFAKE}             FakerLibrary.Day Of Month
  @{DATAS}                    Create List    Data Aleatória: ${DATAFAKE}  Mês Aleatório: ${MESFAKE}  Ano Aleatório: ${ANOFAKE}
  ...                         Dia da Semana Aleatório: ${DIADASEMANAFAKE}   Dia do Mês Aleatório: ${DIADOMESFAKE}
  Log Many    @{DATAS}

Exemplos diversos
  ${EMAILFAKE}                FakerLibrary.Email
  ${PASSWORDFAKE}             FakerLibrary.Password
  ${CORFAKE}                  FakerLibrary.Color Name
  ${CARTAODECREDITOFAKE}      FakerLibrary.Credit Card Number
  ${PALAVRAFAKE}              FakerLibrary.Word
  @{OUTROS}                   Create List    E-mail Aleatório: ${EMAILFAKE}   Senha Aleatória: ${PASSWORDFAKE}
  ...                         Cor Aleatório: ${CORFAKE}   Cartão de Crédito Aleatório: ${CARTAODECREDITOFAKE}
  ...                         Palavra Aleatória: ${PALAVRAFAKE}
  Log Many    @{OUTROS}
