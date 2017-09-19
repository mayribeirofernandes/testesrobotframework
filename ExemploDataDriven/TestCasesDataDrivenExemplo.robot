*** Settings ***
Resource        Resource.robot
Suite Setup     Acessar blog robotizandotestes        
Suite Teardown  Fechar Navegador
Test Template   Validar pesquisa de postagens

*** Test Case ***                  Busca          Título do Post

Pesquisar Post Premiere            introdução     Season Premiere: Introdução ao Robot Framework
Pesquisar Post Editores Ep.01      visual code    Season Editores - Ep. 02: Visual Studio Code
Pesquisar Post Tutoriais Ep.01     windows        Season Tutoriais - Ep. 01: Instalando o Robot Framework (Windows)

*** Keyword ***    
Validar pesquisa de postagens
    [Arguments]     ${BUSCA}        ${TITULO_POSTAGEM}
    Pesquisar a postagem pela palavra "${BUSCA}"
    Verificar resultado da pesquisa   ${TITULO_POSTAGEM}
    Clicar no post encontrado
    Verificar tela da postagem        ${TITULO_POSTAGEM}