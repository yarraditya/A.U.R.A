from AppOpener import close , open as appopen # import the appopener library to open and close applications
from webbrowser import open as webopen # import the webbrowser library to open websites
from pywhatkit import search, playonyt # import function for google search and youtube playback
from dotenv import dotenv_values # import dotenv to load environment variables from a .env file
from bs4 import BeautifulSoup # import BeautifulSoup to parse HTML content
from rich import print # import the rich library to enhance terminal outputs
from groq import Groq # import the groq library to use its api
import webbrowser # import the webbrowser library to open websites
import subprocess
import requests
import keyboard
import asyncio
import os

# load env variable 
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


# Define CSS classes for parsing specific elements in Html content
classes = ["zCubwf", "hgKElc","LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta"
           "IZ6rdc", "O5uR6d LTKOO", " vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sxLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-redsc", "SPZz6b"]


# desfine a user agent for making web requests

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36'

# intialize the groq client with the api key
client = Groq(api_key=GroqAPIKey)

# predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority ; feel free to reach out if there's anything else I can help you with.",
    "I'm here to assist you with any questions or concerns you may have. Let me know if there's anything else I can help you with.",
]

# list to store chat bot messages
messages = []

# system messaege to provide context to chatbot
SystemChatBot = [{"role": "system", "content": f"Hello , I am {os.environ['Username']}, You're a content writer . you have to write conent like lette."}]

# funnction to perform a google search
def GoogleSearch(Topic):
    search(Topic)
    return True 

#function to generate content using AI and save it to a file
def Content (Topic):
    
    #nested function to open a file in notepad
    def OpenNotepand(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])
        
    #nested function to generate content using ai chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content":f"{prompt}"}) 
        
        completion = client.chat.completions.create (
            model = "llama-3.1-8b-instant",
            messages = SystemChatBot + messages,
            max_tokens = 2048,
            temperature=0.7,
            top_p=1,
            stream = True,
            stop = None
        )   
        
        Answer = ""
        
        
        # process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
                
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})        
        return Answer
    
    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)
    
    # save the generated content to text file
    with open (rf"Data\{Topic.lower().replace(' ','')}", "w", encoding='utf-8') as file:
        file.write(ContentByAI)
        file.close()
    
    OpenNotepand(rf"Data\{Topic.lower().replace(' ','')}.txt") 
    return True   

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True
def PlayYoutube(query):
    playonyt(query)
    return True
def OpenApp( app, sess=requests.session()):
    try:
        appopen(app, match_closest = True, output = True , throw_error = True)
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]
        
        #nested function to perfrom a google search and retrieve HTML
        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {'User-Agent': useragent}
            response = sess.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                print("failed  to retrieve search results")
            return None
        
        html = search_google(app)
        
        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True
    
 # function to close an application
def CloseApp(app):
     
     if " chrome" in app:
      pass
     else:
         try:
             close(app,match_closest = True, output = True , throw_error = True)
             return True
         except:
             return False
# funtion to exceute system level commands
def System(command):
    #nested function    mute the system volume
    def mute():
        keyboard.press_and_release('volumemute')
        
    #nesetd function to unmute the system volume
    def unmute():
        keyboard.press_and_release('volumemute')    
        
    #nested function to increse the system volume
    def volumeup():
        keyboard.press_and_release('volumeup')
        
    #nested function to decrease the system volume
    def volumedown():
        keyboard.press_and_release('volumedown')
        
    # exceute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volumeup":
        volumeup() 
    elif command == "volumedown":
        volumedown()     
     
    return True

# asynchronous function to trnaslate and excute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []         
    
    for command in commands:
        if command.startswith("open "):
            if "open it " in command:
                pass
            if "open file" == command:
                pass    
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):            
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):    
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):    
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
           fun = asyncio.to_thread(System, command.removeprefix("system "))
           funcs.append(fun)             
           
        else:
            print(f"No Function Found. For{command}")   
     
    results = await asyncio.gather(*funcs)
    
    for result in results:
        if isinstance(result, str):
           yield result
        else:
            yield result

# async function to automate command exectuioon
async def Automation( commands: list[str]):
      async for result in TranslateAndExecute(commands):
          pass
      
      return True              
           
     
     