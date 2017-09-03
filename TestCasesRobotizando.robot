*** Settings ***
Resource        ResourceRobotizando.robot        
Suite Setup     Abrir Navegador
Suite Teardown  Fechar Navegador

*** Test Case ***
Validar acesso ao blog robotizandotestes
    Pesquisar a postagem "season premiere"
    Clicar no post encontrado
#    Digitar um comentário
#    Submeter o comentário