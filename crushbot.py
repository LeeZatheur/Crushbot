# bot.py
import os
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

target_list = []
with open("target_list.json", "r") as json_file:
    print("List file found")
    data = json.load(json_file)
    target_list = data["list"]

print("List of targets: ")
for name in target_list:
    print(name)

def save_list():
    with open("target_list.json", "w") as json_file:
        data = {"list":target_list}
        dump = json.dumps(data)
        json_file.write(dump)
        print("List updated")

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    guild = discord.utils.get(client.guilds, name=GUILD)

    if message.content.startswith("Je crush sur"):
        target_name = message.content.split("Je crush sur ")[1]
        if target_name in target_list:
            target = discord.utils.get(guild.members, name=target_name)
            if target:
                print("Target acquired: " + target_name)
                chan = discord.utils.get(guild.channels, name="crush")
                response ="<@" + f"{target.id}>, quelqu'un crush sur toi"

                await chan.send(response)
            else:
                print("Invalid target: " + target_name)
                response = "Déso je sais pas qui est " + target_name + ". Faut bien qu'iel soit sur le serveuri et inscrit.e à la liste hein"
                await message.channel.send(response)
        else:
             response = "Déso mais " + target_name + " n'est pas dans la liste. Arranges toi pour qu'iel s'inscrive"
         await message.channel.send(response)

    elif message.content == "Dis moi qui crush sur moi":
        author_name = message.author.name
        if author_name not in target_list:
            response = "Ok, t'es ajouté.e a la liste"
            target_list.append(author_name)
            save_list()
            await message.channel.send(response)
        else:
            response = "T'es déjà inscrit.e"
            await message.channel.send(response)
    elif message.content == "Je veux plus savoir qui crush sur moi":
        author_name = message.author.name
        if author_name in target_list:
            response = "Ok, t'es retiré.e a la liste"
            target_list.remove(author_name)
            save_list()
            await message.channel.send(response)
        else:
            response = "T'étais pas inscrit.e"
            await message.channel.send(response)

client.run(TOKEN)
                                                 