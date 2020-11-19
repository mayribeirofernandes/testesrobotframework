*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${URL}                https://robotizandotestes.blogspot.com/
${BROWSER}            chrome
${BTN_PESQUISA}       css=.search-expand.touch-icon-button
${INPUT_PESQUISA}     name=q
${SUBMIT_PESQUISA}    css=.search-action.flat-button
${LINK_POST}          xpath=//a[contains(text(),'Season Premiere: Introdução ao Robot Framework')]
${IMG_ROBO}           xpath=//img[contains(@src,'if_Robot_18_385830_grande')]

*** Keywords ***
Acessar página inicial do blog
  Open Browser      ${URL}  ${BROWSER}
  Title Should Be   Robotizando Testes

Fechar Navegador
  Close Browser

Pesquisar por um post com "${TEXTO_PESQUISA}"
  Wait Until Element Is Visible  ${BTN_PESQUISA}
  Click Button    ${BTN_PESQUISA}
  Input Text    ${INPUT_PESQUISA}    ${TEXTO_PESQUISA}
  Click Button    ${SUBMIT_PESQUISA}

Conferir mensagem de pesquisa por "${TEXTO_PESQUISA}"
  Page Should Contain    Mostrando postagens que correspondem à pesquisa por ${TEXTO_PESQUISA}

Acessar o post "${POST}"
  Pesquisar por um post com "${POST}"
  Click Element    ${LINK_POST}
  Wait Until Page Contains    O que é Robot Framework?

Conferir se a imagem do robô aparece
  Page Should Contain Image    ${IMG_ROBO}

Conferir se o texto "${TEXTO_DESEJADO}" aparece
  Page Should Contain    ${TEXTO_DESEJADO}
