*** Settings ***
Library    Browser


*** Test Cases ***
Exemplo com a library Browser
    Abrindo uma tab no navegador no site    http://www.google.com.br
    Fazer pesquisa com a frase   robot framework
    Verificar se aparece o header do Robot Framework


*** Keywords ***
Abrindo uma tab no navegador no site
    [Arguments]  ${url}
    # Por default o browser será headless, aqui optamos por ver o browser
    New Browser  headless=False
    
    # Quero um contexto de teste que GRAVE as execuções
    New Context  recordVideo={'dir': '${OUTPUT_DIR}/video'}

    # Abro uma ABA no navegador com a URL desejada
    New Page     url=${url}

Fazer pesquisa com a frase
    [Arguments]  ${frase_pesquisa}
    Fill Text    css=input[name=q]    ${frase_pesquisa}
    Click        :nth-match(:text("Pesquisa Google"), 2)

Verificar se aparece o header do Robot Framework
    # As asserções são feitas com Getters, onde passamos o locator +
    # a condição + o valor esperado tudo na mesma linha, nessa ordem
    Get Text     h2 > span   ==   Robot Framework
