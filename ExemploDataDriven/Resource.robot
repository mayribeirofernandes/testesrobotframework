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
${TITULO}               xpath=.//*[@id='Blog1']/div/article/div[1]/div/h3

*** Keywords ***
Acessar blog robotizandotestes
    Open Browser    ${URL}  ${BROWSER}
    Wait Until Element Is Visible   ${CABEÇALHO}
    Title Should Be     Robotizando Testes

Pesquisar a postagem pela palavra "${BUSCA}"
    Click Element   ${BOTAO_LUPA}
    Input Text      ${CAMPO_PESQUISAR}    ${BUSCA}
    Click Element   ${BOTAO_PESQUISAR}
    Wait Until Element Is Visible   ${LINK_POST}

Verificar resultado da pesquisa
    [Arguments]   ${TITULO_POSTAGEM}
    Page Should Contain     ${TITULO_POSTAGEM}

Clicar no post encontrado
    Click Element    ${LINK_POST}

Verificar tela da postagem
    [Arguments]   ${TITULO_POSTAGEM}    
    Wait Until Element Is Visible  ${TITULO}
    Title Should Be  ${TITULO_POSTAGEM}

Fechar Navegador
    Close Browser   