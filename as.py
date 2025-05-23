import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep

# function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    
    #generate the filenames for the images 
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in Files :
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            
            img = Image.open(image_path)
            print(f"Opening image:{image_path}")
            img.show()
            sleep(randint(1,3))
            
        except IOError:
            print(f"Error opening image: {image_path}")
            

#API details for the hugging face stable diffusion model 
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {os.getenv('HuggingFaceAPIKey')}"}




        

#async function to send a query to the hugging face api
async def query(payload):
    response = await asyncio.to_thread(requests.post ,API_URL, headers=headers, json=payload)
    return response.content
# async function to generate images based on given prompt

async def generate_images(prompt: str):
    tasks = []

    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness = maximum , Ultra High details , high resolution, seed = {randint(0, 10000)}",
        
        }    
        task = asyncio.create_task(query(payload))
        tasks.append(task)
        
        # wait for all task to complete 
        image_bytes_list = await asyncio.gather(*tasks)
        
        # save the generated images to files
        for i , image_bytes in enumerate(image_bytes_list):
            with open(fr"Data\{prompt.replace(' ', '_')}{i}.jpg", "wb") as f:
                f.write(image_bytes)
# Wrapper function to generate and open images
def GenerateImages(prompt : str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)        
    
    
while True:
    
     try: 
         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
             Data : str = f.read()
             
         Prompt, Status = Data.split(",")
         
         # if the stauts indicate an images generation request
         if Status == "True":
          print("Generating Images...")
          ImageStatus = GenerateImages(prompt = Prompt)
          
          with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
              f.write("False, False")
              break
         else: 
             sleep(1)
     except :
         pass