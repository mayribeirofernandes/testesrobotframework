*** Settings ***
Library     AutoItLibrary

*** Test Cases ***
Joaninha
    Abrir Joaninha
    Digitar Defeito

*** Keywords ***
Abrir Joaninha
	# O diretório desse executavel, configurei nas variáveis de ambiente do windows
    Run             SEALsScript.exe
    Win Wait        WindowTitle=SEAL´s Scripts

Digitar Defeito
    Control Focus   strTitle=SEAL´s Scripts    strText=${EMPTY}    strControl=TMemo4
    Send            Meu texto para o campo Descrição do Defeito
    Control Focus   strTitle=SEAL´s Scripts    strText=${EMPTY}    strControl=TEdit1
    Send            Meu texto para o campo Aplicativo
    Control Focus   strTitle=SEAL´s Scripts    strText=${EMPTY}    strControl=TMemo2
    Send            Meu texto para o campo Procedimento do Teste
    Control Focus   strTitle=SEAL´s Scripts    strText=${EMPTY}    strControl=TMemo1
    Send            Meu texto para o campo Evidências
    Control Click   strTitle=SEAL´s Scripts    strText=Copiar      strControl=TBitBtn2
