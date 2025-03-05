import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode
import re

# Classe para gerenciar a configuração do projeto
class ConfigManager:
    def __init__(self, config_path="config.json"):
        import json
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)
    
    def get(self, key):
        return self.config.get(key, None)

# Classe para gerenciar a extração de dados
class NYTimesScraper:
    def __init__(self, config):
        self.config = config
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        
        #options.add_argument("--headless")  # Rodar sem interface gráfica
        #options.add_argument("--no-sandbox")  # Necessário para rodar no Docker
        #options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória

        self.driver = webdriver.Chrome(options=options)
    
    def search_news(self):
        url = self.config.get("url")
        attempts = 0
        max_attempts = 3
        news_list = []
        regexDollars = r"(?:US\$|\$)\s?\d{1,3}(\.\d{3})*(,\d{1,2})?|(?<!\S)\d{1,3}(\.\d{3})*(,\d{1,2})?\s+dollars"
        regexDate = r"\b\d{4}[-/]\d{2}[-/]\d{2}\b"

        if self.config.get("meses") > 0:
            startDate = datetime.now() - relativedelta(months=self.config.get("meses")-1)
        else:
            startDate = datetime.now() - relativedelta(months=self.config.get("meses"))

        startDate = datetime(startDate.year, startDate.month, 1)
        startDate =  startDate.strftime("%Y-%m-%d")
        endDate = datetime.now().strftime("%Y-%m-%d")

       
        params = {"query":self.config.get("frase"), "startDate": startDate, "endDate": endDate,
                  "lang":self.config.get("idioma"),  "types":self.config.get("tipo"), 
                  "sections":self.config.get("secao"), "sort": self.config.get("ordenacao")}
        
        url = f"{url}?{urlencode(params)}"
        print(url)  


        while attempts < max_attempts:
            try:
                self.driver.get(url)
                sleep(3)


                if self.driver.find_elements(By.XPATH, "//button[text()='Reject all']"):
                    input_box = self.driver.find_element(By.XPATH, "//button[text()='Reject all']")
                    input_box.click()

                sleep(2)

                if self.driver.find_elements(By.XPATH, "//span[text()='Continue']"):
                    input_box = self.driver.find_element(By.XPATH, "//span[text()='Continue']")
                    input_box.click()
                
                sleep(2)
                
                # Expandindo as páginas de resultados encontrados
                while self.driver.find_elements(By.XPATH, "//button[text()='Show More']"):
                    input_box = self.driver.find_element(By.XPATH, "//button[text()='Show More']")
                    input_box.click()
                    sleep(2)

                articles = self.driver.find_elements(By.CSS_SELECTOR, "li.css-1l4w6pd")
                
                for article in articles:
                    try:
                        title = article.find_element(By.CSS_SELECTOR, "h4").text
                        date = article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        image = article.find_element(By.CLASS_NAME, "css-rq4mmj").get_attribute("src") if article.find_elements(By.CLASS_NAME, "css-rq4mmj") else ""
                        description = article.find_element(By.CLASS_NAME, "css-e5tzus").text if article.find_elements(By.CLASS_NAME, "css-e5tzus") else ""
                        

                        # Extraindo data do link da notícia
                        date = re.search(regexDate, date)

                        # Encontrar todas as correspondências de valores monetários dollars na "descrição" e no "título" da notícia
                        matchesMoney = bool(re.search(regexDollars, title)) if bool(re.search(regexDollars, title)) else bool(re.search(regexDollars, description))

                        # Conta quantas vezes a frase aparece no texto, ignorando maiúsculas e minúsculas
                        ocorrencias = title.lower().count(self.config.get("frase").lower()) + description.lower().count(self.config.get("frase").lower()) 

                        news_list.append({
                            "Título": title,
                            "Data": date[0],
                            "Descrição": description,
                            "Imagem": image,
                            "Número de Ocorrência": ocorrencias,
                            "Valor Monetário": matchesMoney
                        })
                    except:
                        continue
                
                if news_list:
                    break
            except Exception as e:
                print(f"Tentativa {attempts + 1} falhou: {e}")
                self.save_screenshot(f"error_attempt_{attempts + 1}.png")
                attempts += 1
                sleep(5)
        
        self.driver.quit()
        return news_list


    def save_screenshot(self, filename):
            try:
                self.driver.save_screenshot(filename)
                print(f"Screenshot salva: {filename}")
            except Exception as e:
                print(f"Erro ao salvar screenshot: {e}")

# Classe para gerenciar o armazenamento dos dados
class DataStorage:
    @staticmethod
    def save_to_excel(data, file_name="noticias.xlsx"):
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)

# Classe principal do fluxo de trabalho
class NYTimesBot:
    def __init__(self, config_path="config.json"):
        self.config_manager = ConfigManager(config_path)
        self.scraper = NYTimesScraper(self.config_manager)
    
    def run(self):
        print("Buscando notícias...")
        news_data = self.scraper.search_news()
        print(f"{len(news_data)} notícias encontradas!")
        
        print("Salvando no Excel...")
        DataStorage.save_to_excel(news_data)
        print("Processo concluído!")

if __name__ == "__main__":
    bot = NYTimesBot()
    bot.run()
