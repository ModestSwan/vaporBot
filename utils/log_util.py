# \vaporBot\utils\log_util.py
import json
import os
from datetime import datetime

import discord

LOG_FILE_PATH = "./message_logs.json"


def log_command_to_file(user_id, user_name, guild_id, guild_name, channel_id, channel_name, command_message_id,
                        command_content, response, response_message_id):
    log_entry = {
        "command": {
            "timestamp": datetime.utcnow().isoformat(),
            "message_id": command_message_id,
            "user_id": user_id,
            "user_name": user_name,
            "guild_id": guild_id,
            "guild_name": guild_name,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "content": command_content
        },
        "response": {
            "content": response,
            "message_id": response_message_id
        }
    }

    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


async def send_and_log(ctx, content=None, embed=None):
    if content:
        msg = await ctx.send(content)
        response_log = content
    elif embed:
        msg = await ctx.send(embed=embed)
        response_log = {
            "title": embed.title,
            "description": embed.description,
            "fields": [f"{f.name}: {f.value}" for f in embed.fields],
            "image_url": embed.image.url if embed.image else None
        }
    else:
        return None

    command_content = None
    command_message_id = None
    if hasattr(ctx, 'message'):
        command_content = ctx.message.content
        command_message_id = ctx.message.id
    elif isinstance(ctx, discord.ApplicationContext) and ctx.command:
        command_content = f"/{ctx.command.name} {' '.join(f'{option.name}:{option.value}' for option in ctx.selected_options)}"
        command_message_id = ctx.interaction.id  # Interaction ID for slash commands

    log_command_to_file(
        user_id=ctx.author.id,
        user_name=str(ctx.author),
        guild_id=ctx.guild.id if ctx.guild else None,
        guild_name=str(ctx.guild) if ctx.guild else None,
        channel_id=ctx.channel.id,
        channel_name=str(ctx.channel),
        command_message_id=command_message_id,
        command_content=command_content,
        response=response_log,
        response_message_id=msg.id
    )

    return msg
