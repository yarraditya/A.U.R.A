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
