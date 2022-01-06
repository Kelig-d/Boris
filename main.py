#Importations des librairies utilisées dans le main et des fonctions
import discord
import random
from dotenv import load_dotenv
from pathlib import Path
import os
from methods.jokes import GetJoke
from methods.image_improver import ImageImprover
from methods.tiktok_to_video import TiktokToVideo
from methods.get_link import GetLink
import asyncio

#Environment variable import (bot token)
#.env file is in .env folder. It's the python environment
dotenv_path = Path('.env/.env')
load_dotenv(dotenv_path=dotenv_path)

#Discord client creation
client = discord.Client()
#Hello message Processing
keywords = open("keywords/hello.txt","r").readlines()
mots = []
for i in range(0,len(keywords)):
    mots.append(keywords[i][0:len(keywords[i])-1])

help_section = open("help.txt","r",encoding="utf-8")
joke_help = open("joke_help.txt","r",encoding="utf-8")
@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    #Test if the message is not from the bot
    if message.author == client.user:
        return
    #Bot send random word from file to respond to users when they say hello
    for i in range(0,len(mots)-1):
        if(message.content.startswith(mots[i])):
            await message.channel.send(mots[random.randint(0,len(mots)-1)])
            break
    #If a user send tiktok video, the bot will download it and resend in .mp4 format to play it on discord
    if "https" in message.content and "tiktok" in message.content:
        link = GetLink(message.content)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, TiktokToVideo, link[0])
        await message.delete()
        await message.channel.send(file=discord.File(r'videos/tiktok.mp4'))
    #The bot will get the image with this command and improve it with the real ESRGAN via an API 
    if message.content.startswith("+image"):
        is_valid = False
        link = GetLink(message.content)
        if link:
            link_segments = link[0].split(".")
            image_extension = link_segments[len(link_segments)-1]
            valid_extensions = ["jpg","png","gif","jpeg"]
            for i in range(0,len(valid_extensions)):
                if image_extension == valid_extensions[i]:
                    is_valid = True
                    image = ""
                    break
        else:
            link =""
            image = message.attachments[0]
        if message.attachments or (link and is_valid):
            await message.channel.send("Attends que l'image soit analysée")
            ImageImprover(link, image)
            await message.channel.send("Voici ton image améliorée",file=discord.File(r'images/image_improved.jpg'))
        else:
            await message.channel.send("Tu dois mettre une image avec")
    if message.content.startswith("+jokehelp"):
        await message.channel.send(joke_help.read())
    elif message.content.startswith("+j"):
        message_segments = message.content.split(" ")
        try:
            argument = message_segments[1]
            try:
                argument2 = message_segments[2]
            except Exception:
                argument2 = ""
        except Exception:
            argument = ""
            argument2 = ""
        await message.channel.send(GetJoke(argument, argument2))
    if message.content.startswith("+boris help"):
        await message.channel.send(help_section.read())

client.run(os.getenv('TOKEN'))