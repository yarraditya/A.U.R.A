import cohere  # import the cohere library for AI services
from rich import print # import the rich library to enhance terminal outputs 
from dotenv import dotenv_values # import dotenv to load environment variables form a .env file.

#load enivronment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key 
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the porvided API Key
co = cohere.Client(api_key= CohereAPIKey)

#Define a list of recognized function keywords for task categorization
func = [
    "exit", "general" , "realtime" , "open" , "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

#Initialize an empty list to store user messages
message = []

#Define the preamble that guides the AI model on how to categorize queries.
preamble = """"""

# Define a chat history with predefined user-chatbot interactions for context.
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "gneral hwo are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on th aug at 11pm."},
    {"role": "Chatbot", "message": "general what is today's date , reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me"},
]

#Define th emain function for decision making on queries.
def FirstLayerDMM(prompt: str = "test"):
    #add the user query to the messages list.
    
    
