import discord
from discord.ext import commands, tasks
from typing import Literal
from fetcher.grabber import get_animals

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ID = os.getenv("my_id")
channel_id = os.getenv("channel_id")
me = os.getenv("id")

server = discord.Object(id=ID)

intents = discord.Intents.all()
client = commands.Bot(command_prefix="tfdyukjil114142dsfgsfh", intents=intents)


@client.event
async def on_ready():
    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))


@client.tree.command(name="check-site", description='check spca', guild=server)
async def check_site(ctx, animal: Literal["all", "cats", "dogs", "small animals", "farm animals"], location: Literal["ashburton-centre", "auckland-centre", "hobsonville-center"]):
    get_animals(animal, location)
    with open(f'./{animal}/{location}/difference.txt', 'r') as f:
        difference = f.read()
    if difference == "":
        await ctx.response.send_message(f"No new animals at {location} for {animal}")
    else:
        await ctx.response.send_message(f"New Animals at {location} for {animal}\n{difference}",)

@client.tree.command(name="get-site", description='get animals at spca', guild=server)
async def get_site(ctx, animal: Literal["all", "cats", "dogs", "small animals", "farm animals"], location: Literal["ashburton-centre", "auckland-centre", "hobsonville-center"]):
    get_animals(animal, location)
    await ctx.response.send_message(f"Animals at {location} for {animal}", file=discord.File(f'./{animal}/{location}/new.txt'))

@client.tree.command(name="set-alert", description='Set alert for new animals', guild=server)
async def set_alert(ctx: discord.Interaction, animal_name: str, animal: Literal["all", "cats", "dogs", "small animals", "farm animals"], location: Literal["ashburton-centre", "auckland-centre", "hobsonville-centre"]):
    channel_id = ctx.channel.id
    user = ctx.user

    await ctx.response.send_message(f"Alert set for {animal_name} in {location}. I'll notify you if it becomes available.")
    check_for_new_animals.start(channel_id, user, animal_name, animal, location)  # Start the background task

@tasks.loop(seconds=60)
async def check_for_new_animals(channel_id: int, user: discord.User, animal_name: str, animal: str, location: str):
    channel = client.get_channel(channel_id)
    
    # Call your existing function to get animals
    get_animals(animal, location)
    
    # Check the difference file
    with open(f'./{animal}/{location}/difference.txt', 'r') as f:
        difference = f.read()
    
    # Logic to check if there are any new animals
    if difference == "":
        await channel.send(f"No new animals at {location} for {animal}.")
    else:
        await channel.send(f"New animals at {location} for {animal}:\n{difference}")
        if animal_name in difference:
            await channel.send(f"{user.mention} {animal_name} is available at {location}!")
            check_for_new_animals.stop()  # Stop the loop once the animal is found
    
    

client.run(TOKEN)