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
        log_command_to_file(
            user_id=str(interaction.user.id),
            user_name=str(interaction.user),
            guild_id=str(interaction.guild.id) if interaction.guild else "DM",
            guild_name=str(interaction.guild.name) if interaction.guild else "Direct Message",
            channel_id=str(interaction.channel.id) if interaction.channel else "NA",
            channel_name=str(interaction.channel.name) if hasattr(interaction.channel, 'name') else "NA",
            command_message_id="NA",  # No message ID in slash command interaction
            command_content="/compare_builds",
            response="Modal sent",
            response_message_id="NA"  # Response modal has no message ID
        )
        await interaction.response.send_modal(modal1)
