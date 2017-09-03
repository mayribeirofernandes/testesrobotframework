*** Settings ***
Library     SeleniumLibrary

*** Variable ***
${BROWSER}              firefox
${URL}                  https://robotizandotestes.blogspot.com.br/  
${BOTAO_LUPA}           css=.search-expand.touch-icon-button    
${CAMPO_PESQUISAR}      css=.search-input>input
${BOTAO_PESQUISAR}      css=.search-action.flat-button

*** Keywords ***
Abrir Navegador
    Open Browser    ${URL}  ${BROWSER}

Fechar Navegador
    Close Browser

Pesquisar a postagem "${PESQUISA}"
    Click Element   ${BOTAO_LUPA}
    Input Text      ${CAMPO_PESQUISAR}    ${PESQUISA}
    Click Element   ${BOTAO_PESQUISAR}

#Digitar um comentário

#Submeter o comentário

