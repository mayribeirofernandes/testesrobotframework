*** Settings ***
Library     ./RabbitMQCustom.py
Library     RequestsLibrary
Library     Collections

*** Keywords ***
Conectar no RabbitMQ
    [Documentation]  Efetua a conexão com o RabbitMQ.
    [Arguments]          ${RABBIT_HOST}   ${RABBIT_PORT}   ${RABBIT_USER}   ${RABBIT_PASSWORD}  ${RABBIT_ALIAS}=rmq_http
    Connect To RabbitMQ  host=${RABBIT_HOST}
    ...                  port=${RABBIT_PORT}
    ...                  username=${RABBIT_USER}
    ...                  password=${RABBIT_PASSWORD}
    ...                  alias=${RABBIT_ALIAS}

Criar fila com prioridade no RabbitMQ
    [Documentation]   Cria uma fila com prioridade. Default prioridade=5.
    [Arguments]       ${FILA}  ${PRIORIDADE}=${5}
    ${ARGUMENTS}      Create Dictionary    x-max-priority=${PRIORIDADE}
    Create Queues By Name     ${FILA}   arguments=${ARGUMENTS}

Criar filas com prioridade no RabbitMQ
    [Documentation]  Cria as filas listadas na lista enviada, com prioridade. Default prioridade=5.
    [Arguments]      @{FILAS_CRIAR}  ${PRIORIDADE}=${5}
    FOR   ${FILA}   IN   @{FILAS_CRIAR}
        Criar fila com prioridade no RabbitMQ   ${FILA}  ${PRIORIDADE}
    END

Limpar todas as filas do RabbitMQ
    [Documentation]   Limpa (purge) as filas listadas na lista enviada.
    [Arguments]  @{FILAS_LIMPAR}
    FOR   ${FILA}   IN   @{FILAS_LIMPAR}
        Purge Messages By Queue   ${FILA}
    END

Fechar conexão com o RabbitMQ
    [Documentation]   Encerra a conexão com o RabbitMQ.
    Disconnect From RabbitMQ

###### Requisições
Realizar requisição POST no RabbitMQ
    [Documentation]   Publica uma mensagem em uma determinada fila sem envio de headers.
    [Arguments]       ${MENSAGEM}     ${FILA}
    &{PROPERTIES}     Create Dictionary          delivery_mode=${1}
    ${PUBLISH}        Publish Message By Name    queue=${FILA}  msg=${MENSAGEM}  properties=${PROPERTIES}
    Verificar sucesso no publish    ${PUBLISH}

Realizar requisição POST com HEADERS no RabbitMQ
    [Documentation]   Publica uma mensagem em uma determinada fila com envio de headers.
    [Arguments]       ${MENSAGEM}     ${FILA}    ${HEADERS}
    &{PROPERTIES}     Create Dictionary          delivery_mode=${1}   headers=${HEADERS}
    ${PUBLISH}        Publish Message By Name    queue=${FILA}  msg=${MENSAGEM}  properties=${PROPERTIES}
    Verificar sucesso no publish    ${PUBLISH}

Verificar sucesso no publish
    [Documentation]   Verifica se houve sucesso em um publish realizado.
    [Arguments]       ${PUBLISH}
    Log Dictionary    ${PUBLISH}
    ${ROUTED}         Get From Dictionary        ${PUBLISH}      routed
    Should be True    ${ROUTED}  msg=Não foi possível publicar no RabbitMQ. Verifique!

Realizar requisição GET de uma mensagem no RabbitMQ
    [Documentation]   Pega a primeira mensagem da fila especificada. Faz tentativas de obtê-la até um limite de tempo. Default limte_wait=75.
    [Arguments]       ${FILA}  ${LIMITE_WAIT}=75
    FOR  ${SEGUNDO}   IN RANGE   0   ${LIMITE_WAIT}
       ${RESPOSTA}    Run Keyword And Ignore Error     Get Messages by Queue  ${FILA}    1
       ${TAMANHO}     Get Length      ${RESPOSTA[1]}
       Exit For Loop If    ${TAMANHO} > 0 and '${RESPOSTA[0]}'=='PASS'
       Run Keyword If      '${RESPOSTA[1]}' == 'CannotSendRequest: Request-sent'    Sleep   3s   ELSE   Sleep   0.2s
    END
    Log               Mensagem retornada:${\n}${RESPOSTA[1]}
    Validar se retornou mensagens  ${RESPOSTA[1]}  ${FILA}
    ${RESPOSTA}       To Json      ${RESPOSTA[1]["payload"]}
    [Return]          ${RESPOSTA}

Realizar requisição GET de várias mensagens no RabbitMQ
    [Documentation]   Pega as primeiras N mensagens da fila especificada.
    [Arguments]       ${FILA}    ${COUNT}
    ${RESPOSTA}       Get Messages by Queue  ${FILA}    ${COUNT}
    Log               Mensagens retornadas:${\n}${RESPOSTA}
    Validar se retornou mensagens  ${RESPOSTA}  ${FILA}
    ${RESPOSTA}       To Json      ${RESPOSTA[0]["payload"]}
    [Return]          ${RESPOSTA}

Validar se retornou mensagens
    [Arguments]       ${RESPOSTA}   ${FILA}
    ${TAMANHO}        Get Length    ${RESPOSTA[1]}
    Run Keyword If    ${TAMANHO} == 0    Fail    Não há mensagens na fila [${FILA}]. Verifique!
