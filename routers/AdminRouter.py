# \vaporBot\routers\AdminRouter.py
import json
import os

import discord
from discord.ext import commands

from utils.log_util import LOG_FILE_PATH


class AdminRouter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deletelastbotmsgs")
    @commands.is_owner()
    async def delete_last_bot_messages(self, ctx, count: int):
        """Deletes the last x messages sent by the bot in this channel (based on responses in logs)."""
        if count <= 0:
            print("Admin Command: delete_last_bot_messages - Invalid count provided.")
            return

        deleted_count = 0
        messages_to_delete = []

        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                    # Iterate through logs and get response message IDs where the response was sent in this channel
                    for entry in reversed(logs):
                        response_info = entry.get('response', {})
                        command_info = entry.get('command', {})
                        response_message_id = response_info.get('message_id')
                        channel_id = command_info.get('channel_id')

                        if response_message_id and channel_id == ctx.channel.id:
                            try:
                                message = await ctx.channel.fetch_message(response_message_id)
                                if message.author == self.bot.user:
                                    messages_to_delete.append(message)
                                    deleted_count += 1
                                    if deleted_count >= count:
                                        break
                            except discord.NotFound:
                                print(
                                    f"Admin Command: delete_last_bot_messages - Logged response ID {response_message_id} not found in channel {ctx.channel.id}.")
                            except discord.HTTPException as e:
                                print(
                                    f"Admin Command: delete_last_bot_messages - Error fetching message {response_message_id}: {e}")
                                return
                except json.JSONDecodeError:
                    print("Admin Command: delete_last_bot_messages - Error reading log file.")
                    return
        else:
            print("Admin Command: delete_last_bot_messages - Log file not found.")
            return

        if messages_to_delete:
            try:
                await ctx.channel.delete_messages(messages_to_delete)
                print(
                    f"Admin Command: delete_last_bot_messages - Successfully deleted {deleted_count} messages in channel {ctx.channel.id}.")
            except discord.HTTPException as e:
                print(f"Admin Command: delete_last_bot_messages - Error occurred while deleting messages: {e}")
        else:
            print(
                f"Admin Command: delete_last_bot_messages - Could not find {count} recent messages sent by the bot in channel {ctx.channel.id} logs.")


def setup(bot):
    bot.add_cog(AdminRouter(bot))
