from selenium import webdriver
from selenium.webriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt 

# load envrionment variables from the . env file
env_vars = dotenv_values(".env")
#get the input language setting from the env variable
InputLanguage = env_vars.get("InputLanguage")

# Deine the HTML code for the speech recognition interface.
HtmlCode = """"""

# replace the language setting in the HTML code with the input language from the env variable
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# write the modified HTML code to file:
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)
    
# Get the current working directory
current_dir = os.getcwd
# generate the file path for the Html file
Link = f"{current_dir}/Data/Voice.html" 
#set chrom options for the WebDriver
chrome_options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36'
chrome_options.add_argument(f"user-agent={user_agent}" ) 
chrome_options.add_argument ("--use-fake-ui-for-media-stream")
chrome_options.add_argument ("--use-fake-device-for-media-stream")
chrome_options.add_argument ("--headless =new")

#intialize the chrome webdrive using the provided options
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#define the path for temporary files.
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant  status by writing it to a file
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)
        
 #function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
     new_query = Query.lower().strip()
     query_words = new_query.split
                           

