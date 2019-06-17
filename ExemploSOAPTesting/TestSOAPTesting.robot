*** Settings ***
Resource     ResourceSOAPTesting.robot
Resource     ResourceSOAPTesting_withXMLinput.robot

*** Test Case ***
Teste SOAP preenchendo campo a campo da requisição
    Enviar requisição SOAP preenchendo campo a campo da requisição

Teste SOAP enviando um arquivo XML na requisição
    Enviar requisição SOAP enviando arquivo XML de input
