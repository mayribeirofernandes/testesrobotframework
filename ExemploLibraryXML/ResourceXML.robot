*** Settings ***
Library     OperatingSystem
Library     String
Library     XML

*** Keywords ***
Manipular e conferir XML
    ############ OPÇÃO 01 - Manipular como STRING ############
    ### Pegue um XML no diretório, armazene em uma variável e manipule como STRING
    ${XML_CONTENT}          Get File           xmlBaseExemplo.xml
    ${XML_CONTENT}          Replace String     ${XML_CONTENT}    <idConsultante>ID_ANTES</idConsultante>   <idConsultante>ID_DEPOIS</idConsultante>
    Log                     ${XML_CONTENT}

    ############ OPÇÃO 02 - Manipular como XML ############
    ### Pegando Elementos e Atributos com a library XML
    ${ELEMENTO}             Get Element Text        ${XML_CONTENT}    xpath=.//idConsultante
    Log                     ${ELEMENTO}
    ${ATRIBUTO}             Get Element Attribute   ${XML_CONTENT}    nome    xpath=.//outroParametro[1]
    Log                     ${ATRIBUTO}

    ### Manipulando Elementos com a library XML
    ${XML_CONTENT}          Remove Element          ${XML_CONTENT}    xpath=.//senhaConsultante
    Log Element             ${XML_CONTENT}
    ${XML_CONTENT}          Add Element             ${XML_CONTENT}    <senhaConsultante>9999999</senhaConsultante>   xpath=.//consultarAvisosPendentes   index=2
    Log Element             ${XML_CONTENT}
    ${XML_CONTENT}          Set Element Text        ${XML_CONTENT}    02072019   xpath=.//dataReferencia
    Log Element             ${XML_CONTENT}
    ${XML_CONTENT}          Add Element             ${XML_CONTENT}    <outroParametro>true</outroParametro>    xpath=.//consultarAvisosPendentes
    ${XML_CONTENT}          Set Element Attribute   ${XML_CONTENT}    nome     mayara   xpath=.//outroParametro[3]
    ${XML_CONTENT}          Set Element Attribute   ${XML_CONTENT}    valor    QA       xpath=.//outroParametro[3]
    Log Element             ${XML_CONTENT}

    ### Após manipular, salve o XML e use como preferir
    Save Xml                ${XML_CONTENT}     meuXMLmanipulado.xml
    ${XML_FINAL}            Get File           meuXMLmanipulado.xml
    Log                     ${XML_FINAL}

    ### Conferências com a library XML
    Element Text Should Be         ${XML_FINAL}    ID_DEPOIS     xpath=.//idConsultante
    Element Attribute Should Be    ${XML_FINAL}    nome          atendimentoPlantao         xpath=.//outroParametro[1]
    Element Attribute Should Be    ${XML_FINAL}    valor         false                      xpath=.//outroParametro[1]
    Element Attribute Should Be    ${XML_FINAL}    nome          urgente                    xpath=.//outroParametro[2]
    Element Attribute Should Be    ${XML_FINAL}    valor         true                       xpath=.//outroParametro[2]
    Element Attribute Should Be    ${XML_FINAL}    nome          mayara                     xpath=.//outroParametro[3]
    Element Attribute Should Be    ${XML_FINAL}    valor         QA                         xpath=.//outroParametro[3]
