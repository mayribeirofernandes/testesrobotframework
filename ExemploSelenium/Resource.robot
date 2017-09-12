*** Settings ***
Library     SeleniumLibrary

*** Variable ***
${BROWSER}              firefox
${URL}                  https://robotizandotestes.blogspot.com.br/  
${CABEÇALHO}            Header1
${BOTAO_LUPA}           css=.search-expand.touch-icon-button    
${CAMPO_PESQUISAR}      css=.search-input>input
${BOTAO_PESQUISAR}      css=.search-action.flat-button
${LINK_POST}            xpath=.//*[@id='Blog1']/div[1]/article/div/div/h3/a
${TITULO_POST}          xpath=.//*[@id='Blog1']/div/article/div[1]/div/h3

*** Keywords ***
Acessar blog robotizandotestes
    Open Browser    ${URL}  ${BROWSER}
    Wait Until Element Is Visible   ${CABEÇALHO}
    Title Should Be     Robotizando Testes

Pesquisar a postagem "${PESQUISA}"
    Click Element   ${BOTAO_LUPA}
    Input Text      ${CAMPO_PESQUISAR}    ${PESQUISA}
    Click Element   ${BOTAO_PESQUISAR}
    Wait Until Element Is Visible  ${LINK_POST}

Clicar no post "${TITULO_POST_DESC}" encontrado
    Click Element    ${LINK_POST}
    Wait Until Element Is Visible  ${TITULO_POST}
    Title Should Be  ${TITULO_POST_DESC}

Fechar Navegador
    Close Browser
