*** Settings ***
Library     SeleniumLibrary

*** Variable ***
${BROWSER}              firefox
${URL}                  https://robotizandotestes.blogspot.com.br/  
${BOTAO_LUPA}           css=.search-expand.touch-icon-button    
${CAMPO_PESQUISAR}      css=.search-input>input
${BOTAO_PESQUISAR}      css=.search-action.flat-button
${LINK_POST}            xpath=.//*[@id='Blog1']/div[1]/article/div/div/h3/a
${TITULO_POST}          xpath=.//*[@id='Blog1']/div/article/div[1]/div/h3
${TITULO_POST_DESC}     Season Premiere: Introdução ao Robot Framework

*** Keywords ***
Abrir Navegador
    Open Browser    ${URL}  ${BROWSER}

Fechar Navegador
    Close Browser

Pesquisar a postagem "${PESQUISA}"
    Click Element   ${BOTAO_LUPA}
    Input Text      ${CAMPO_PESQUISAR}    ${PESQUISA}
    Click Element   ${BOTAO_PESQUISAR}
    Wait Until Element Is Visible  ${LINK_POST}

Clicar no post encontrado
    Click Element    ${LINK_POST}
    Wait Until Element Is Visible  ${TITULO_POST}
    Title Should Be  ${TITULO_POST_DESC}

#Digitar um comentário

#Submeter o comentário

