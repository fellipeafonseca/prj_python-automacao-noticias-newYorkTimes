import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode


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
        self.driver = webdriver.Chrome(options=options)
    
    def search_news(self):
        url = "https://www.nytimes.com/search"
        attempts = 0
        max_attempts = 3
        news_list = []
        

        startDate = datetime.now() - relativedelta(months=self.config.get("meses")-1)

        startDate = datetime(startDate.year, startDate.month, 1)
        startDate =  startDate.strftime("%Y-%m-%d")
        endDate = datetime.now().strftime("%Y-%m-%d")

       
        params = {"query":self.config.get("frase"), "startDate": startDate, "endDate": endDate,"lang":"en",  "types":"", "sections":"", "sort": "newest"}
        url = f"{url}?{urlencode(params)}"
        print(url)  


    #  https://www.nytimes.com/search?dropmab=false&endDate=2025-02-28&lang=en&query=Technology%20Review&sort=newest&startDate=2024-12-01

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
                
            #    search_box = self.driver.find_element(By.ID, "searchTextField")
               # search_box.send_keys(self.config.get("frase"))
            #    search_box.send_keys(Keys.RETURN)
            #    sleep(5)
                

              #  date_range = self.driver.find_element(By.XPATH, "//span[text()='Date Range']")
              #  date_range.click()
#

                while self.driver.find_elements(By.XPATH, "//button[text()='Show More']"):
                    input_box = self.driver.find_element(By.XPATH, "//button[text()='Show More']")
                    input_box.click()
                    sleep(2)

                articles = self.driver.find_elements(By.CSS_SELECTOR, "li.css-1l4w6pd")
                
                for article in articles:
                    try:
                        title = article.find_element(By.CSS_SELECTOR, "h4").text
                        #date = article.find_element(By.CSS_SELECTOR, "span.css-17ubb9w").text
                     #   description = article.find_element(By.CSS_SELECTOR, "p").text if article.find_elements(By.CSS_SELECTOR, "p") else ""
                        
                        news_list.append({
                            "Título": title
                       #     "Data": date,
                        #    "Descrição": description
                        })
                    except:
                        continue
                
                if news_list:
                    break
            except Exception as e:
                print(f"Tentativa {attempts + 1} falhou: {e}")
                attempts += 1
                sleep(5)
        
        self.driver.quit()
        return news_list

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
