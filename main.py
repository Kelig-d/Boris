import discord
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import requests
import base64
import json
from methods.link_test import linkTest
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('.env/.env')
load_dotenv(dotenv_path=dotenv_path)
client = discord.Client()
keywords = open("keywords/hello.txt","r").readlines()
mots = []
for i in range(0,len(keywords)):
    mots.append(keywords[i][0:len(keywords[i])-1])

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for i in range(0,len(mots)-1):
        if(message.content.startswith(mots[i])):
            await message.channel.send(mots[random.randint(0,len(mots)-1)])
            break
    if message.content.startswith("https://vm.tiktok.com"):
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            link = ""
            driver.get(message.content)
            while link == "":
                try:
                    link = driver.find_element(By.CSS_SELECTOR,'.tiktok-lkdalv-VideoBasic.e1yey0rl4').get_attribute('src')
                except Exception:
                    link = ""
            urllib.request.urlretrieve(link, 'tiktok.mp4')
            await message.delete()
            await message.channel.send(file=discord.File(r'videos/tiktok.mp4'))
    if message.content.startswith("+image"):
        is_valid = False
        link = linkTest(message.content)
        if link:
            link_segments = link[0].split(".")
            image_extension = link_segments[len(link_segments)-1]
            valid_extensions = ["jpg","png","gif","jpeg"]
            for i in range(0,len(valid_extensions)):
                if image_extension == valid_extensions[i]:
                    is_valid = True
                    break
        if message.attachments or (link and is_valid):
            await message.channel.send("Attends que l'image soit analysée")
            if link:
                image_url = link[0]
            else:
                image_url = message.attachments[0].url
                image_segment = image_url.split(".")
                image_extension = image_segment[len(image_segment)-1]
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'whatever')
            opener.retrieve(image_url, 'images/image_to_improve.'+image_extension)
            encoded_image = base64.b64encode(open("images/image_to_improve."+image_extension, "rb").read())
            encoded_image_clean = str(encoded_image)[2:]
            string_json = {
                "data": [
                    'data:image/'+image_extension+';base64,'+encoded_image_clean,
                    'base'
                ]
            }
            
            # string_json = '"data": ["data:image/'+image_extension+";base64,"+str(encoded_image)+'","base"]'
            json_to_send = json.dumps(string_json)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url='https://hf.space/gradioiframe/akhaliq/Real-ESRGAN/api/predict', data=json_to_send, headers= headers)
            json_data = r.json()["data"]
            all_data_string = str(json_data)
            image_data = all_data_string[24:]
            image_result = open('images/image_improved.jpg','w').close()
            image_result = open('images/image_improved.jpg','wb')
            image_result.write(base64.b64decode(image_data))
            await message.delete()
            await message.channel.send("Voici ton image améliorée",file=discord.File(r'images/image_improved.jpg'))

        else:
            await message.channel.send("Tu dois mettre une image avec")


client.run(os.getenv('TOKEN'))