import discord
from discord.ext import commands
from datetime import datetime
from typing import Literal
import random

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="tfdyukjil114142dsfgsfh", intents=intents)


@client.event
async def on_ready():
    for server in client.guilds:
        await client.tree.sync(guild=discord.Object(id=server.id))


# keep_alive()
client.run(TOKEN)
