import discord
from discord.ext import commands
from typing import Literal
from fetcher.grabber import get_animals

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ID = os.getenv("my_id")
channel_id = os.getenv("channel_id")

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
        await ctx.response.send_message(f"New Animals at {location} for {animal}", file=discord.File(f'./{animal}/{location}/difference.txt'))

@client.tree.command(name="get-site", description='get animals at spca', guild=server)
async def get_site(ctx, animal: Literal["all", "cats", "dogs", "small animals", "farm animals"], location: Literal["ashburton-centre", "auckland-centre", "hobsonville-center"]):
    get_animals(animal, location)
    await ctx.response.send_message(f"Animals at {location} for {animal}", file=discord.File(f'./{animal}/{location}/new.txt'))

client.run(TOKEN)