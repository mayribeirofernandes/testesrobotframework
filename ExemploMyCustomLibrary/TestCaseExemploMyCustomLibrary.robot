*** Settings ***
Documentation     Exemplo de uso de uma Library personalizada e criada por mim em Python
Library           ./libraries/decode64.py

*** Test Cases ***
Teste da minha custom library
  Exemplos decodificar "TWluaGEgZnJhc2UgZGUgdGVzdGUh"
  Conferir se o texto decodificado é "Minha frase de teste!"

*** Keywords ***
Exemplos decodificar "${TEXTO_CODIFICADO_BASE64}"
  ${TEXTO}    decode 64 to string   ${TEXTO_CODIFICADO_BASE64}
  Set Test Variable    ${TEXTO}
  Log    Frase codificada: ${TEXTO_CODIFICADO_BASE64} -- Frase decodificada: ${TEXTO}

Conferir se o texto decodificado é "${FRASE_ESPERADA}"
  Should Be Equal    ${TEXTO}    ${FRASE_ESPERADA}
