# \vaporBot\routers\DefaultRouter.py
import discord
from discord.ext import commands

from utils.log_util import send_and_log


class DefaultRouter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        helpDesc = '''

        {bold}Commands{bold}:
        {bold}v!patchCD{bold} : Countdown till the next Genshin version update
        {bold}v!patchCD <version_number>{bold} : Countdown till the specific Genshin version update. Usage example: v!patchCD 5.8
        {bold}v!streamCD{bold} : Countdown till the next Genshin livestream
        {bold}/comparebuilds{bold} : Compare different builds based on atk/bonusDmg/critRate/critDmg

        '''.format(bold='**')
        embed = discord.Embed(title="Bot Stuff", description=helpDesc, color=0x2b2d31)
        embed.set_image(url="https://i.ibb.co/nkM4NHD/ezgif-com-crop-2.gif")
        await send_and_log(ctx, embed=embed)
