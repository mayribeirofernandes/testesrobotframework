*** Settings ***
Library     DateTime

*** Variable ***
${DATA}     2018-01-16

*** Test Cases ***
Teste Operações com Datas
    ####Pegando a data de hoje e convertendo para formato yyyy-mm-dd
    ${TODAY}    Get Current Date    result_format=%Y-%m-%d
    ${DATA}     Convert Date        ${DATA}     result_format=%Y-%m-%d

    ####Fazendo o cálculo
    ${RESULT}   Subtract Date From Date     ${TODAY}    ${DATA}
    ${MONTHS}   Evaluate  ${RESULT}/60/60/24/30

    ####Formatando para ficar no formato dd-mm-yyyy
    ${DATA}     Convert Date    ${DATA}    result_format=%d-%m-%Y
    ${TODAY}    Convert Date    ${TODAY}   result_format=%d-%m-%Y
    Log         Entre ${TODAY} e ${DATA} existem ${MONTHS} meses.
