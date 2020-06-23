*** Settings ***
Resource        Resource.robot
Suite Setup     Acessar blog robotizandotestes
Suite Teardown  Fechar Navegador
Test Template   Validar pesquisa de postagens

*** Test Case ***
Pesquisar Post Premiere no template 1
    [Template]    Validar pesquisa de postagens 1
    # Busca       Título do Post
    introdução    Season Running - Ep. 08: Executando seus testes no Docker

Pesquisar Post Premiere no template 2
    [Template]    Validar pesquisa de postagens 2
    # Busca       Título do Post
    introdução    Season Running - Ep. 08: Executando seus testes no Docker

Pesquisar Post Editores Ep.01 no template 1
    [Template]    Validar pesquisa de postagens 1
    # Busca       Título do Post
    visual code   Season Editores - Ep. 02: Visual Studio Code - Configurando o VS Code para o Robot Framework

Pesquisar Post Editores Ep.01 no template 2
    [Template]    Validar pesquisa de postagens 2
    # Busca       Título do Post
    visual code   Season Editores - Ep. 02: Visual Studio Code - Configurando o VS Code para o Robot Framework

Pesquisar Post Tutoriais Ep.01 no template 1
    [Template]    Validar pesquisa de postagens 1
    # Busca       Título do Post
    windows       Season Mobile com Appium - Ep.01: Instalação Windows

Pesquisar Post Tutoriais Ep.01 no template 2
    [Template]    Validar pesquisa de postagens 2
    # Busca       Título do Post
    windows       Season Mobile com Appium - Ep.01: Instalação Windows

*** Keyword ***
Validar pesquisa de postagens 1
    [Arguments]     ${BUSCA}        ${TITULO_POSTAGEM}
    Pesquisar a postagem pela palavra "${BUSCA}"
    Verificar resultado da pesquisa   ${TITULO_POSTAGEM}
    Clicar no post encontrado
    Verificar tela da postagem        ${TITULO_POSTAGEM}

Validar pesquisa de postagens 2
    [Arguments]     ${BUSCA}        ${TITULO_POSTAGEM}
    Pesquisar a postagem pela palavra "${BUSCA}"
    Verificar resultado da pesquisa   ${TITULO_POSTAGEM}
    Clicar no post encontrado
    Verificar tela da postagem        ${TITULO_POSTAGEM}
