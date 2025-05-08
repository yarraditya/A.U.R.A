import pygame # import pygmae library for hanling audio playback
import random # import random for generating random choices
import asyncio # import asyncio for handling asynchronous tasks
import edge_tts # import edge_tts for text to speech conversion
import os # import os for interacting with the operating system
from dotenv import dotenv_values       # import dotenv for loading environment variables from a .env file

# load env variables from .env 
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

async def TextToAudioFile(text) -> None:
     file_path = r"Data\speech.mp3"
     if os.path.exists(file_path):
        os.remove(file_path)
         
     communicate = edge_tts.Communicate(text, AssistantVoice,pitch = '+5Hz', rate = '+13%')
     await communicate.save(r'Data\speech.mp3')
     
#function to manage text to speech tts functionality
def TTS(Text, func= lambda r= None: True):
    while True:
        try:
            # convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))
            
            # intialize pygame mixer for audio playback
            
            pygame.mixer.init()

            # load the gnerated speech file into pygame mixer
            pygame.mixer.music.load(r'Data\speech.mp3')
            pygame.mixer.music.play()
            
            # wait for the audio file to finish playing
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)
            return True    
        
        except Exception as e:
            print(f"Error in TTS: {e}")
        
        finally:
            try:
                # call the provided function with flase to singal the end of tts    
                func(False)
                pygame.mixer.music.stop() # stop the audio playback
                pygame.mixer.quit() # quit the pygame mixer
                
            except Exception as e:
                print(f"Error in finally block: {e}")    
 # function to manage Text to speech   with additional responses for long text
def TextToSpeech(Text, func= lambda r= None: True):
   Data = str(Text).split(".")
   
   responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
   
   # if the text is very long , add a response message
   if len(Data) > 4 and len(Text) >= 250:
       TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)

    
   else:
       TTS(Text, func)  
       
#main exectuion loop

if __name__ == "__main__":
    while True:          
        
        TextToSpeech(input("Enter Your Text: "))