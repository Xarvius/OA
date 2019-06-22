from discord.ext import commands

from utils import config
from errors.errors import NotAllowed

CONFIG = config.load_config()


def is_allowed_to_command():
    async def predicate(ctx):
        if ctx.author.id not in CONFIG["BOT_PERMISSIONS"]:
            raise NotAllowed()
        return True
    return commands.check(predicate)

