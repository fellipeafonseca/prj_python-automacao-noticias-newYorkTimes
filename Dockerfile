# Usar a imagem oficial do Selenium com Chrome
FROM selenium/standalone-chrome:latest

# Instalar Python e dependências necessárias
USER root
RUN apt-get update && apt-get install -y python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . .

# Criar e ativar um ambiente virtual
RUN python3 -m venv /venv

# Instalar as dependências no ambiente virtual
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Definir o comando padrão para execução (ativando o ambiente virtual)
CMD ["/venv/bin/python", "main.py"]
