# NYTimes - Automação RPA com ReFramework, Docker e WSL2 para coleta de notícias

## 📌 Descrição

Este projeto é uma automação RPA desenvolvida em **Python** seguindo o padrão **ReFramework**, utilizando **Selenium** para extrair notícias do site [The New York Times](https://www.nytimes.com/search).

Os dados extraídos são:

- **Título da notícia**
- **Data da publicação**
- **Descrição**
- **Imagem da Publicação**
- **Contagem de Ocorrências da frase de busca na notícia (título e descrição)**
- **Valor monetário (Dollars) na notícia (Verdadeiro/Falso)**



As notícias são salvas e é gerado um arquivo **Excel** (`noticias.xlsx`) na raiz do projeto com dados extraídos.

## 📽️ Demonstração

### Execução Local
https://github.com/user-attachments/assets/9985e790-60a4-434e-a34a-0e1c4f1fdace


### Relatório gerado
![Relatorio Excel](https://github.com/user-attachments/assets/07ee2c78-ac0a-446b-86ae-b223e2c54578)


### Execução via docker
![image](https://github.com/user-attachments/assets/7f470fd7-6610-4582-b8fc-90dc4470e6ad)


---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Python** 🐍
- **Selenium WebDriver** 🌐
- **Pandas** 📊
- **ReFramework** (Robotic Enterprise Framework) 🤖
- **Docker & Docker Hub** 🐳
- **WSL2 (Windows Subsystem for Linux 2)** 💻

---

## 📂 Estrutura do Projeto

```
📦 NYTimesScraper-RPA
├── 📜 config.json        # Configuração com parâmetros de busca
├── 📜 main.py            # Script principal que gerencia o fluxo
├── 📜 Dockerfile         # Configuração para containerização
├── 📜 requirements.txt   # Dependências do projeto
├── 📜 README.md          # Documentação do projeto
```

---

## ⚙️ Configuração e Execução

### 🔹 **1. Pré-requisitos**

Antes de rodar a aplicação, certifique-se de ter instalado:

- **Python 3.8+**
- **Docker e Docker Desktop (com integração WSL2 ativada)**
- **WSL2** configurado e habilitado para o Docker

### 🔹 **2. Clonar o Repositório**

```bash
git clone https://github.com/fellipeafonseca/prj_python-automacao-noticias-newYorkTimes.git

```

### 🔹 **3. Configurar as Variáveis no Config**

Abra o arquivo `config.json` e edite os valores conforme necessário:

```json
{
    "url": "https://www.nytimes.com/search",
    "frase": "trump",
    "meses": 1,
    "idioma": "en",
    "tipo": "",
    "secao": "",
    "ordenacao":"newest"
}
```

### 🔹 **4. Executar Localmente**

Instale as dependências:

```bash
pip install -r requirements.txt
```

Rode o script principal:

```bash
python main.py
```

---

## 🐳 Uso com Docker - https://hub.docker.com/repository/docker/fellipedockerfon/prj_python-automacao-noticias-newyorktimes-nytimes_scraper/general

### 🔹 **1. Construir a Imagem Docker**

```bash
docker build -t prj_python-automacao-noticias-newyorktimes-nytimes_scraper .
```

### 🔹 **2. Executar o Container**

```bash
docker run --rm -v $(pwd)/output:/app/output prj_python-automacao-noticias-newyorktimes-nytimes_scraper
```

### 🔹 **3. Enviar a Imagem para o Docker Hub**

```bash
docker tag nytimes_scraper fellipedockerfon/prj_python-automacao-noticias-newyorktimes-nytimes_scraper:latest
docker push fellipedockerfon/prj_python-automacao-noticias-newyorktimes-nytimes_scraper:latest
```

### 🔹 **4. Baixar e Executar em Outra Máquina**

```bash
docker pull fellipedockerfon/prj_python-automacao-noticias-newyorktimes-nytimes_scraper:latest
docker run --rm fellipedockerfon/prj_python-automacao-noticias-newyorktimes-nytimes_scraper
```

---

## 📝 Observações

- Em caso de erro, uma captura de tela será salva na pasta do projeto.
- É realizado até 3 tentativas para a extração de dados no site. 
- Certifique-se de que o **ChromeDriver** está compatível com a versão do Google Chrome instalada.
- Se o Docker não estiver rodando no **WSL2**, verifique as configurações no **Docker Desktop**.

---

## 🏆 Contribuições

Melhorias futuras para implementação:
- Estruturação melhor do reframework separando as responsabilidades em novas classes;
- Utilização de imagem de Banco de Dados para salvar os arquivos gerados e/ou Envio por E-mail;
- Utilização de Docker Secrets para armazenamento de usuário, senha e chaves de conexão no Dockerfile.

Fique à vontade para abrir um **Pull Request** ou relatar problemas na aba **Issues**!

🔗 **GitHub:** https://github.com/fellipeafonseca/prj_python-automacao-noticias-newYorkTimes

