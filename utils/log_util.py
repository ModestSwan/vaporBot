# \vaporBot\utils\log_util.py
import json
import os
from datetime import datetime

LOG_FILE_PATH = "./message_logs.json"


def log_command_to_file(user, guild, channel, command, response):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "guild": guild,
        "channel": channel,
        "command": command,
        "response": response
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

    log_command_to_file(
        user=str(ctx.author),
        guild=str(ctx.guild),
        channel=str(ctx.channel),
        command=ctx.message.content,
        response=response_log
    )

    return msg
