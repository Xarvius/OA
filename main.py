import logging
import os

import discord
import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='&')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension('cogs.' + filename[:-3])

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@bot.event
async def on_ready():
    print('-----')
    print('[LOG]Bot created by Wheezy')
    print('[LOG]Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')


@bot.command(pass_context=True)
async def info(ctx):
    """Bot and author info"""
    description_message = 'Specjalnie dla gildii OSTRZA [OA]!'
    embed = discord.Embed(title="SUPER-OSTRZA INFO", description=description_message, color=0x00ff00,
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Autor", value="Wheezy", inline=False)
    embed.add_field(name="Język", value="Python", inline=False)
    embed.add_field(name="Framework", value="Discrod.py", inline=False)
    await ctx.send(embed=embed)


bot.run(os.environ['TOKEN'])
