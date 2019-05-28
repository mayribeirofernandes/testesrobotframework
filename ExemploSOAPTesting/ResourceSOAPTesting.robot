*** Settings ***
### Instale a library:   pip install robotframework-sudslibrary-aljcalandra
Library    SudsLibrary

*** Variables ***
### Você vai precisar o WSDL do seu webservice/SOAP Client destino
${WSDL_URL}         http://localhost:8077/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl

### Você deverá montar um dicionário com os dados que precisa passar na chamada do método
### Esse exemplo abaixo são os campos obrigatórios do método
### Esses campos são os mesmos do arquivo consultaProcesso_envio.xml
&{MSG_ENVIO}        idConsultante=PGMBH    senhaConsultante=12345678    numeroProcesso=50224418220178130024

*** Keywords ***
Enviar requisição SOAP
    ### Abra a conexão com o SOAP Cliente destino
    Create Soap Client      ${WSDL_URL}

    ### Chame o método passando campo a campo da requisição
    ### A resposta será armazenada na variável ${RESPOSTA_XML}
    ${RESPOSTA_XML}         Call Soap Method        consultarProcesso
    ...                     ${MSG_ENVIO.idConsultante}
    ...                     ${MSG_ENVIO.senhaConsultante}
    ...                     ${MSG_ENVIO.numeroProcesso}

    Log                     ${RESPOSTA_XML}
