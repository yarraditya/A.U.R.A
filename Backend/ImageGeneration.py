import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep

# Load environment variables
load_dotenv()

# Folder path to save and read images
folder_path = r"Data"
os.makedirs(folder_path, exist_ok=True)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_KEY = os.getenv("HuggingFaceAPIKey")
if not API_KEY:
    raise EnvironmentError("HuggingFaceAPIKey not found in environment variables")

headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to open and display generated images
def open_images(prompt):
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(4)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(randint(1, 3))
        except IOError:
            print(f"Error opening image: {image_path}")

# Async function to query the Hugging Face API
async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Async function to generate multiple images
async def generate_images(prompt: str):
    tasks = []

    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 10000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            file_path = os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i}.jpg")
            try:
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
            except Exception as e:
                print(f"Failed to save image {i}: {e}")

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop to check for new prompt requests
def main():
    data_file_path = r"Frontend\Files\ImageGeneration.data"
    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

    while True:
        try:
            if not os.path.exists(data_file_path):
                sleep(1)
                continue

            with open(data_file_path, "r") as f:
                data = f.read().strip()

            if not data:
                sleep(1)
                continue

            prompt, status = map(str.strip, data.split(","))
            if status == "True":
                print("Generating Images...")
                GenerateImages(prompt)
                with open(data_file_path, "w") as f:
                    f.write("False,False")
                break
            else:
                sleep(1)
        except Exception as e:
            print(f"Main loop error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()
