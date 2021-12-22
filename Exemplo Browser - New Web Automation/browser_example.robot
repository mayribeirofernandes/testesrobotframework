*** Settings ***
Library    Browser   auto_closing_level=MANUAL


*** Test Cases ***
Exemplo com a library Browser
    Abrindo uma tab no navegador no site    http://www.google.com.br
    Fazer pesquisa com a frase   robot framework
    Verificar se aparece o header do Robot Framework


*** Keywords ***
Abrindo uma tab no navegador no site
    [Arguments]  ${URL}
    New Browser  
    New Context  recordVideo={'dir': '${OUTPUT_DIR}/video'}
    New Page  url=${URL}

Fazer pesquisa com a frase
    [Arguments]  ${FRASE_PESQUISA}
    Fill Text    css=input[name=q]    ${FRASE_PESQUISA}
    Click    :nth-match(:text("Pesquisa Google"), 2)

Verificar se aparece o header do Robot Framework
    Get Text  h2 > span   ==   Robot Framework
