from googlesearch import search
from groq import Groq
from json import load, dump # importing the functions to read and write json files
import datetime # importing the datetime module to get real-time information
from dotenv import dotenv_values #importing dotenv to load environment variables from a .env file

# Load environment variables
env_vars = dotenv_values(".env")

#Retrieve specific environment variables , i.e. Username, Assistantname, GroqAPIKey
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey") 

#Intialize the groq client using the provided API Key
client = Groq(api_key=GroqAPIKey)
#Define the system instructions for chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON , or create an empty one if it doesn't exist
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open("Data/ChatLog.json", "w") as f:
        dump([], f)
    
# Function to perform a google search and format the results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"Here are the search results for '{query}'are:\n[start]\n"
    
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
        
    Answer += "[end]"
    return Answer

# Funtion to clean up the answer by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split("\n") #split the answer into lines
    non_empty_lines = [line for line in lines if line.strip()] #remove empty lines
    modified_answer = "\n".join(non_empty_lines) #join the non-empty lines into a single string
    return modified_answer

# predefined chatbot conversation system message and an initial user message
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "Hello, how can i help you?"}  
]      

#funtion to get real-time information like the current date and time
def Information():
    data = ""
    current_date_time = datetime.datetime.now() # get current date and time
    day = current_date_time.strftime("%A") # get day of the week
    date = current_date_time.strftime("%d") # get date
    month = current_date_time.strftime("%B") # get month
    year = current_date_time.strftime("%Y") # get year
    hour = current_date_time.strftime("%I") # get hour
    minute = current_date_time.strftime("%M") # get minute
    second = current_date_time.strftime("%S") # get second  
    data += f"Please use this real_time information if needed,\n"
    data += f"Day:{day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes: {second} seconds.\n"
    return data

#function to handle real-time search and response generation
def RealTimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    #Load the chat log from the JSON file
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})#append the user's query to messages list
    
    # Add google search results to the system chatbot messages
    SystemChatBot.append({"role": "user", "content": GoogleSearch(prompt)})
    
    # Generate a response using the Groq client
    completion = client.chat.completions.create (
        model = "llama3-70b-8192", # specify the model to use
        messages = SystemChatBot + [{"role": "user", "content": Information()}] + messages, #pass the user's query
        max_tokens = 2048,
        temperature=0.7, #set the creativity level of the model
        top_p=1,
        stream = True,
        stop = None
    )
    Answer = ""
    
    #Concatenate response chunks from the streaming output
    for chunk in completion:
     if chunk.choices[0].delta.content:
        Answer += chunk.choices[0].delta.content
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    #Save the updated chat log to the JSON file
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f,indent=4)
    SystemChatBot.pop()
    return AnswerModifier(Answer= Answer)

# Main entry point of  the program for interactive querying
if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Question: ")  # Prompt the user for input
        print(RealTimeSearchEngine(prompt))  # Print the chatbot's response
      
      