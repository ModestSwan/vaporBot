# \vaporBot\routers\CDRouter.py
from datetime import datetime

import discord
from dateutil.relativedelta import relativedelta
from discord.ext import commands

from utils.config_util import get_next_patch_number, get_patch_details, get_art_url, get_stream_details
from utils.log_util import send_and_log


class CDRouter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def patchCD(self, ctx, patch_number: float = None):
        if patch_number is None:
            patch_number = get_next_patch_number()

        patch = get_patch_details(patch_number)
        if patch is None:
            return

        description = self.build_patch_description(patch)
        embed = self.build_patch_embed(patch, description)
        await send_and_log(ctx, embed=embed)

    def build_patch_description(self, patch):
        time_left = self.calculate_time_left(patch["timestamp"])
        time_tag = f"<t:{patch['timestamp']}:F>"
        desc = f"{time_tag}\n{time_left}"
        if patch.get("source"):
            desc += f"\n{patch['source']}"
        return desc

    def build_patch_embed(self, patch, description):
        embed = discord.Embed(
            title=f"Patch Countdown - Version {patch['patch_number']}",
            description=description,
            color=0x2b2d31
        )
        url = get_art_url(patch.get("art_id"))
        if url:
            embed.set_image(url=url)
        return embed

    def calculate_time_left(self, target_timestamp):
        target_time = datetime.fromtimestamp(target_timestamp)
        current_time = datetime.now()
        rd = relativedelta(target_time, current_time)

        if rd.years > 0:
            return f"{rd.years} year{'s' if rd.years > 1 else ''}, {rd.months} month{'s' if rd.months > 1 else ''}, {rd.days} day{'s' if rd.days > 1 else ''}"
        if rd.months > 0:
            return f"{rd.months} month{'s' if rd.months > 1 else ''}, {rd.days} day{'s' if rd.days > 1 else ''}, {rd.hours} hour{'s' if rd.hours > 1 else ''}"
        if rd.days > 0:
            return f"{rd.days} day{'s' if rd.days > 1 else ''}, {rd.hours} hour{'s' if rd.hours > 1 else ''}, {rd.minutes} minute{'s' if rd.minutes > 1 else ''}"
        return f"{rd.hours} hour{'s' if rd.hours > 1 else ''}, {rd.minutes} minute{'s' if rd.minutes > 1 else ''}"

    @commands.command()
    async def streamCD(self, ctx):
        data = get_stream_details()
        if data is None:
            return
        next_stream_unix = data.get("timestamp", -1)
        image_url = data.get("image_url", "")
        sources = data.get("source", [])

        if next_stream_unix <= 0:
            await send_and_log(ctx, content="No official announcement yet")
            return

        time_tag = f"<t:{next_stream_unix}:F>"
        time_left = self.calculate_time_left(next_stream_unix)

        description = f"{time_tag}\n{time_left}"
        if sources:
            description += "\n" + "\n".join(sources)

        embed = discord.Embed(
            title="Livestream Countdown - Version 5.7",
            description=description,
            color=0x2b2d31
        )

        if image_url:
            embed.set_image(url=image_url)

        await send_and_log(ctx, embed=embed)
