# NYTimes Scraper - Automação RPA com ReFramework, Docker e WSL2

## 📌 Descrição

Este projeto é uma automação RPA desenvolvida em Python seguindo o padrão ReFramework, utilizando Selenium para extrair notícias do site The New York Times.

Os dados extraídos são:

Título da notícia

Data da publicação

Descrição (se disponível)

As notícias são salvas em um arquivo Excel (noticias.xlsx) e, em caso de erro durante a extração, uma captura de tela é salva para análise.

📽️ Demonstração

(Adicione aqui um vídeo mostrando o projeto em execução)

🛠️ Tecnologias e Ferramentas Utilizadas

Python 🐍

Selenium WebDriver 🌐

Pandas 📊

ReFramework (Robotic Enterprise Framework) 🤖

Docker & Docker Hub 🐳

WSL2 (Windows Subsystem for Linux 2) 💻

📂 Estrutura do Projeto

📦 NYTimesScraper-RPA
├── 📜 config.json        # Configuração com parâmetros de busca
├── 📜 main.py            # Script principal que gerencia o fluxo
├── 📜 Dockerfile         # Configuração para containerização
├── 📜 requirements.txt   # Dependências do projeto
├── 📜 README.md          # Documentação do projeto

⚙️ Configuração e Execução

🔹 1. Pré-requisitos

Antes de rodar a aplicação, certifique-se de ter instalado:

Python 3.8+

Docker e Docker Desktop (com integração WSL2 ativada)

WSL2 configurado e habilitado para o Docker

🔹 2. Clonar o Repositório

git clone https://github.com/seu-usuario/NYTimesScraper-RPA.git
cd NYTimesScraper-RPA

🔹 3. Configurar as Variáveis no config.json

Abra o arquivo config.json e edite os valores conforme necessário:

{
    "frase": "inteligência artificial",
    "categoria": "technology",
    "meses": 3
}

🔹 4. Executar Localmente

Instale as dependências:

pip install -r requirements.txt

Rode o script principal:

python main.py

🐳 Uso com Docker

🔹 1. Construir a Imagem Docker

docker build -t nytimes_scraper .

🔹 2. Executar o Container

docker run --rm -v $(pwd)/output:/app/output nytimes_scraper

🔹 3. Enviar a Imagem para o Docker Hub

docker tag nytimes_scraper meuusuario/nytimes_scraper:latest
docker push meuusuario/nytimes_scraper:latest

🔹 4. Baixar e Executar em Outra Máquina

docker pull meuusuario/nytimes_scraper:latest
docker run --rm meuusuario/nytimes_scraper

📝 Observações

Em caso de erro, uma captura de tela será salva na pasta do projeto. Além de tentar 3 vezes realizar a extração dos dados

Certifique-se de que o ChromeDriver está compatível com a versão do Google Chrome instalada.

Se o Docker não estiver rodando no WSL2, verifique as configurações no Docker Desktop.

🏆 Contribuições

Fique à vontade para abrir um Pull Request ou relatar problemas na aba Issues!

🔗 GitHub: https://github.com/seu-usuario/NYTimesScraper-RPA
