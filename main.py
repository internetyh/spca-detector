from bot import client
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

client.run(TOKEN)