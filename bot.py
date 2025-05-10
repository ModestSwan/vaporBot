import json
import discord
from discord.ext import commands

from routers.CDRouter import CDRouter
from PrereqsChecker import PrereqsChecker

intents = discord.Intents.default()
intents.message_content = True

with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='v!', intents=intents)

checker = PrereqsChecker()
bot.add_check(checker.apply_all_checks())

async def on_ready():
    print(f'Bot is online as {bot.user}')

async def setup_hook():
    await bot.add_cog(CDRouter(bot))

bot.setup_hook = setup_hook
bot.event(on_ready) # Use bot.event to register event handlers

bot.run(config["BOT_TOKEN"])