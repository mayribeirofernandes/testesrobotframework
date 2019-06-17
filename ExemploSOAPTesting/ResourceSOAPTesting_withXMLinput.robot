*** Settings ***
### Para rodar esse exemplo foi necessária uma correção na Library SudsLibrary
### Issue: https://github.com/ombre42/robotframework-sudslibrary/issues/32
### Por isso uso a minha library customizada MySudsLibrary.py, que já fiz a correção
Library    ./MyCustomSudsLibrary/MySudsLibrary.py
Library    OperatingSystem

*** Variables ***
### Você vai precisar o WSDL do seu webservice/SOAP Client destino
${WSDL_URL}         http://localhost:8077/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl

*** Keywords ***
Enviar requisição SOAP enviando arquivo XML de input
    ### Abra a conexão com o SOAP Cliente destino
    MySudsLibrary.Create Soap Client      ${WSDL_URL}

    ### Pegue um XML no diretório
    ${MESSAGE}          Get File            consultaProcesso_envio.xml

    ### Transforme ele em um Raw Message para ser enviado na requisição
    ${MESSAGE}          MySudsLibrary.Create Raw Soap Message         ${MESSAGE}
    Log                 Mensagem enviada:\n${MESSAGE}

    ### Faça a requisição SOAP
    MySudsLibrary.Call Soap Method    consultarProcesso    ${MESSAGE}

    ### Pegue o XML recebido
    ${RESPOSTA_XML}     MySudsLibrary.Get Last Received
    Log                 Mensagem Recebida:\n${RESPOSTA_XML}
