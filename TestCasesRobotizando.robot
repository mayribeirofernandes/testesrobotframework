*** Settings ***
Resource        ResourceRobotizando.robot        
Suite Setup     Abrir Navegador
Suite Teardown  Fechar Navegador

*** Test Case ***
Validar acesso ao blog robotizandotestes
    Pesquisar a postagem "introdução"
#    Digitar um comentário
#    Submeter o comentário