from discord.ext import commands

from errors.errors import NotAllowed, DateFormatError


class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        elif isinstance(error, NotAllowed):
            return await ctx.send('You are not allowed to use this command.')

        elif isinstance(error, DateFormatError):
            return await ctx.send(error)

        raise error


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
