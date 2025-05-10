# \vaporBot\PrereqsChecker.py
from discord.ext import commands

from utils.config_util import get_testing_servers


class PrereqsChecker:

    def testing_environment_check(self):
        async def predicate(ctx):
            return ctx.guild is not None and ctx.guild.id in get_testing_servers()

        return predicate  # Return just the predicate function

    def apply_all_checks(self):
        async def combined_check(ctx):
            checks = [
                await self.testing_environment_check()(ctx),
                # Add more check calls here if needed
            ]
            return all(checks)

        return commands.check(combined_check)
