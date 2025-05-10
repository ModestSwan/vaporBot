# \vaporBot\routers\UIRouter.py
import discord
from discord import app_commands
from discord.ext import commands

from ui.number_input_modal import Build1DetailsModal
from utils.log_util import log_command_to_file


class UIRouter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="compare_builds", description="Opens a modal to enter four numbers")
    async def slash_compare_builds(self, interaction: discord.Interaction):
        modal1 = Build1DetailsModal()
        log_command_to_file(str(interaction.user), str(interaction.guild), str(interaction.channel), "/compare_builds",
                            "NA")
        await interaction.response.send_modal(modal1)
