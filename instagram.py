from logging import exception
#from turtle import pos
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import pthread_getcpuclockid, sleep
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from googletrans import Translator
import re
# Import libraries
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import xlsxwriter
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import settings

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class instagramScrap:
    def login_to_instagram(self,username,password):

        # Set Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Create a new ChromeDriver instance
        driver = webdriver.Chrome(options=chrome_options)

        # options = FirefoxOptions()
        # options.add_argument("--headless")
        # #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
		# #driver.get(baseurl)
        # service = Service(GeckoDriverManager().install())
        # driver = webdriver.Firefox(service=service, options=options)


        driver.get("https://www.instagram.com/")
        driver.maximize_window()

        # Wait for up to 10 seconds for the element to be present
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        sleep(5)
        # Input the username into the input field
        username_input = driver.find_element(By.XPATH,"//input[@name='username']")
        username_input.send_keys(username)
        sleep(5)
        # Input the Password into the input field
        password_input = driver.find_element(By.XPATH,"//input[@name='password']")
        password_input.send_keys(password)
        sleep(10)
        #Click on login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        sleep(20)
        print("Login Successfully")
        return driver
    
    #Define function to translate hindi lang to English lang, 
    #Return english senetence
    def hindToEnglish(self,sent):
        max_retries=3
        translator = Translator()
        hindi_sentence = sent
        for retry in range(max_retries):
            try:
                english_sentence = translator.translate(hindi_sentence, dest='en').text
                return english_sentence
            except:
                print(f"Translation request timed out ")
                time.sleep(3)  # Wait for a few seconds before retrying\
    
    # Define function to get sentiment
    def get_sentiment(self,text):
    
        # Load pre-trained DistilBERT model and tokenizer
        # Use a smaller DistilBERT model for faster inference
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Tokenize text
        encoded_text = tokenizer.encode_plus(text, return_tensors='pt')

        # Get sentiment prediction 
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = torch.nn.functional.softmax(torch.tensor(scores), dim=0)
        #print("dsarsadf saddddddddd",scores)
        # Get sentiment label
        label = 'Positive_'+str(scores[1]) if scores[1] > scores[0] else 'Negative_'+str(scores[0])

        return label
    def scrap_post(self,driver,page,pageName,no_of_page):
        driver.get(page)
        twittPost = list()

        timestr = time.strftime("%Y%m%d-%H%M%S")
        fileName = pageName+timestr

       # Create a new Excel workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(fileName+'.xlsx')
        worksheet = workbook.add_worksheet()

        # Write data to the worksheet.

        worksheet.write('A1', 'Post')
        worksheet.write('B1', 'Name')
        worksheet.write('C1', 'Comment')
        worksheet.write('D1', 'Anti/Pro')
        worksheet.write('E1', 'Sentiment Score')
        # Close the workbook to save it.
        workbook.close()

        i=0
        while i<no_of_page:
            
            i+=1
            # try:
            wait = WebDriverWait(driver, 50)  # Increased to 20 seconds
            popup_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_aabd _aa8k  _al3l']")))
            sleep(5)
            # Locate post elements
            post_elements = driver.find_elements(By.XPATH, "//div[@class='_aabd _aa8k  _al3l']")
            
            for post_element in post_elements:
                try:
                    sleep(3)
                    post_element.click()

                    wait = WebDriverWait(driver, 10)  # Increased to 20 seconds
                    popup_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='_a9ym']")))

                    post_description = driver.find_elements(By.XPATH, "//h1[@class='_aacl _aaco _aacu _aacx _aad7 _aade']")
                    instagramPost =post_description[0].text
                    
                    post_comments = driver.find_elements(By.XPATH, "//ul[@class='_a9ym']")
                    for post_comment in post_comments:
                        
                        # h2_elements = post_comment.find_element(By.TAG_NAME, 'h2')  # Find the h2 element
                        html_content = post_comment.get_attribute("outerHTML")
                        
                        soup = BeautifulSoup(html_content, 'html.parser')
                        h2Tag = soup.find('h3')
                        print("User Name", h2Tag.text)

                        comment = soup.find(attrs={'dir': 'auto'})
                        print("Comment",comment.text)
                        comment = comment.text
                        #arg= 'नमस्ते, कैसे हो?'
                        # if comment:
                        #     comment_english = self.hindToEnglish(comment)
                        # else:
                        #     comment_english = 'None'

                        if comment:
                            #'Positive' if scores[1] > scores[0] else 'Negative'
                            pos_neg_comment = self.get_sentiment(comment)

                            # Anti Government or Pro Government
                            print(pos_neg_comment)
                            scoreList = pos_neg_comment.split('_')
                            scoreNo = re.findall("\d+\.\d+", scoreList[1])

                            print(f"convert string float to float {float(scoreNo[0])}")
                            if scoreList[0].strip()=='Positive':
                                if float(scoreNo[0]) > 0.9000:
                                    antPro = 'Pro Government'
                                else:
                                    antPro = 'Anti Government'    
                            else:
                                if float(scoreNo[0]) > 0.9000:
                                    antPro = 'Anti Government'
                                else:
                                    antPro = 'Pro Government'
                            score = scoreNo[0]

                        else:
                            antPro = "Neutral"
                            score = "00.00"

                        data = {
                            "Post":[instagramPost],
                            "Name":[h2Tag.text],
                            "Comment":[comment],
                            'Anti/Pro':[antPro],
                            'Sentiment Score':[score]
                        }
                        print(data)
                        df = pd.DataFrame(data)

                        # appending the data of df after the data of demo1.xlsx
                        with pd.ExcelWriter(fileName+".xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
                            df.to_excel(writer, sheet_name="Sheet1",header=None, startrow=writer.sheets["Sheet1"].max_row,index=False)
                            print("Data Inserted into Excel Sheet")
                            time.sleep(3)

                    sleep(2)
                except Exception as error:
                    fullURL = driver.current_url
                    print(fullURL)
                    if fullURL!=page:
                        driver.execute_script("window.history.go(-1)")  # Simulate the browser's back button with JavaScript
                    print(error)
                    
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(3)
            # except Exception as error:
            #     #driver.execute_script("window.history.go(-1)")  # Simulate the browser's back button with JavaScript
            #     print(error)

        df = pd.read_excel(fileName+'.xlsx', sheet_name='Sheet1')
        # Create a SQLAlchemy engine
        engine = create_engine(settings.PostgreSQL_Connection)
        # Write data to PostgreSQL
        df.to_sql(settings.tables_name, engine, if_exists='append', index=False)

    
        