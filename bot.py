# \vaporBot\bot.py
import json
import traceback

import discord
from discord.ext import commands

from PrereqsChecker import PrereqsChecker
from routers.CDRouter import CDRouter
from routers.UIRouter import UIRouter

intents = discord.Intents.default()
intents.message_content = True

with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='v!', intents=intents)

checker = PrereqsChecker()
bot.add_check(checker.apply_all_checks())


async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        guild_id = 773951576456036372
        guild = discord.Object(id=guild_id)
        bot.tree.copy_global_to(guild=guild)  # Copy global commands to the guild.
        await bot.tree.sync(guild=guild)  # Sync commands to the guild.

        print(f"Synced commands to guild {guild_id}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
        traceback.print_exc()


async def setup_hook():
    await bot.add_cog(CDRouter(bot))
    await bot.add_cog(UIRouter(bot))


bot.setup_hook = setup_hook
bot.event(on_ready)  # Use bot.event to register event handlers

bot.run(config["BOT_TOKEN"])
