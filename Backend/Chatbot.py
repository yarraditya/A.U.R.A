from groq import Groq # importing the groq library to use its api
from json import load, dump # importing the functions to read and write json files
import datetime # importing the datetime module to get real-time information
from dotenv import dotenv_values #importing dotenv to load environment variables from a .env file

# Load environment variables
env_vars = dotenv_values(".env")

#Retrieve specific environment variables , i.e. Username, Assistantname, GroqAPIKey
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

#intialize the groq client using the provided API Key
client = Groq(api_key=GroqAPIKey)
 
 # Intialize an empy list to store user messages
messages = []
# Define a system message that providese the context and instructions for the chatbot

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""
# a list of system instructions
SystemChatBot = [
    {"role": "system", "content": System}
]

#  attempt to load the chat log from a json file
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    # if the file does not exist, create and json file to store chat logs
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
        
# funcion to get real time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # get current date and time
    day = current_date_time.strftime("%A") # get day of the week
    date = current_date_time.strftime("%d") # get date
    month = current_date_time.strftime("%B") # get month
    year = current_date_time.strftime("%Y") # get year
    hour = current_date_time.strftime("%I") # get hour
    minute = current_date_time.strftime("%M") # get minute
    second = current_date_time.strftime("%S") # get second  
    
    #format the information into a string
    data = f"Please use this real_time information if needed,\n"
    data += f"Day:{day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes: {second} seconds.\n"
    return data
 #funttion to modify chatbot's resposne
def AnswerModifier(Answer):
 lines = Answer.split("\n") #split the answer into lines
 non_empty_lines = [line for line in lines if line.strip()] #remove empty lines
 modified_answer = "\n".join(non_empty_lines) #join the non-empty lines into a single string
 return modified_answer

#main chatbot function to handle user queries
def ChatBot(Query):
    """ This function sends the user's query to chatbot and returns the Ai's response"""
    
    try:
        #Load the existing chat log from the json file
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
        #append the user's query to messages list 
        messages.append({"role": "user", "content": Query})
        #make a reques to the groq api to get the chatbot's response
        completion = client.chat.completions.create (
            model = "llama3-70b-8192", # specify the model to use
            messages = SystemChatBot + [{"role": "user", "content": RealtimeInformation()}] + messages, #pass the user's query
            max_tokens = 1024,
            temperature=0.7, #set the creativity level of the model
            top_p=1,
            stream = True,
            stop = None
        )
        Answer = "" #initialize an empty string to store the chatbot's response
        # process the streamed response
        for chunk in completion:
            if chunk.choices[0].delta.content: # check if there is any content in the chunk
                Answer += chunk.choices[0].delta.content # append the content to the Answer string
        Answer = Answer.replace("</s>", "") # remove the </s> tag from the Answer string
        # Append the chatbot's response to the messages list
        messages.append({"role": "assistant", "content": Answer})
        # Save the updated chat log to the json file
        with open("Data/ChatLog.json", "w") as f:
            dump(messages, f,indent=4)
            
        #return the formatted response
        return AnswerModifier(Answer= Answer)    
    except Exception as e:
        # handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        with open("Data/ChatLog.json", "w") as f:
            dump([], f,indent=4)
        return ChatBot(Query)
    
    
 #Main Program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # Prompt the user for input
        print(ChatBot(user_input))  # Print the chatbot's response       
       
        