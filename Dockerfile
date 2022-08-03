# Passo 01: Instancio uma imagem de SO linux, no caso usei o FEDORA,
# mas pode ser o Ubunto, Alpine, Debian, etc...
# Procure no Docker Hub a imagem que desejar! https://hub.docker.com
FROM fedora:29

# Passo 02: Vou mapear os volumes (diretórios do container) onde deixarei
# os testes (inputs) e os resultados (outputs).
VOLUME /opt/robotframework/results
VOLUME /opt/robotframework/tests

# Passo 03: Vou rodar os comandos que instalam tudo que preciso para rodar o robot
# nesse container linux. Como estou usando o FEDORA, os comandos aqui executados
# devem ser compatíveis com ele!!
RUN dnf upgrade -y && dnf install -y python37

# Passo 04: Instalo o Robot e as libraries que precisarei. No caso abaixo,
# especifiquei a versão do robot que eu quero e não especifiquei a da
# library Faker, com isso ele pegara a mais recente liberada.
# Obs.: As barras são para indicar quebra de linha, mas o comando é um só,
# é como se eu tivesso rodando tudo numa linha só.
RUN pip3 install \
robotframework \
robotframework-faker \
robotframework-requests