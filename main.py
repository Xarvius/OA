import datetime
import os

import discord
from discord import InvalidArgument

from discord.ext import commands

import config
from discord.utils import get
from on_message_handler import voice_binds

CONFIG = config.load_json('config.json')
binds = config.load_json('binds.json')
players = {}
server = {}
token = os.environ['TOKEN']

bot = commands.Bot(command_prefix='&')


@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='Guild Wars 2'))
    print('-----')
    print('[LOG]Bot created by Wheezy')
    print('[LOG]Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')


@bot.event
async def on_member_join(member):
    msg_priv = CONFIG["MESSAGE"]["msg_priv"]
    await bot.send_message(member, msg_priv)
    role = get(member.server.roles, name="Gość")
    await bot.add_roles(member, role)
    return


@bot.event
async def on_member_update(before, after):
    if len(before.roles) != len(after.roles):
        for role in before.roles:
            if role.name == 'Okres Próbny':
                return
        for role in after.roles:
            if role.name == 'Okres Próbny':
                msg = CONFIG["MESSAGE"]["msg_trial"]
                await bot.send_message(after, msg)


@bot.command(pass_context=True)
async def info(ctx):
    """Bot and author info"""
    description_message = 'Specjalnie dla gildii OSTRZA [OA]!'
    embed = discord.Embed(title="SUPER-OSTRZA INFO", description=description_message, color=0x00ff00,
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Autor", value="Wheezy", inline=False)
    embed.add_field(name="Język", value="Python", inline=False)
    embed.add_field(name="Framework", value="Discrod.py", inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def join(ctx):
    """CREATES NEW VOICE CLIENT, JOINS PLAYER's CHANNEL (liders)"""
    if not check_user_permissions(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, "Nie masz mocy by mną sterować.")
        return
    channel = ctx.message.author.voice.voice_channel
    server[0] = ctx.message.server
    try:
        await bot.join_voice_channel(channel)
    except InvalidArgument:
        await bot.send_message(ctx.message.channel, "Musisz wejsc na kanal glosowy zeby wlaczyc bota")


@bot.command(pass_context=True)
async def leave(ctx):
    """LEAVES THE CHANNEL (liders)"""
    if not check_user_permissions(ctx.message.author.id):
        await bot.send_message(ctx.message.channel, "Nie masz mocy by mną sterować.")
        return
    current_server = ctx.message.server
    voice_client = bot.voice_client_in(current_server)
    await voice_client.disconnect()


@bot.event
async def on_member_remove(member):
    log_channel = get_log_channel(member.server)
    descriptionmsg = '%s wyszedł z serwera.' % member.mention
    embed = discord.Embed(title="WYJŚCIE Z SERWERA [LOG]", description=descriptionmsg, color=0x00ff00,
                          timestamp=datetime.datetime.utcnow())
    embed.set_author(name=member, url=embed.Empty, icon_url=member.avatar_url)
    await bot.send_message(log_channel, embed=embed)


@bot.event
async def on_message(message):
    if check_user_permissions(message.author.id) and len(message.content) <= 7:
        await voice_binds(message, binds, bot, players, server)
    await bot.process_commands(message)


def check_user_permissions(user_id):
    if user_id in CONFIG["BOT_PERMISSIONS"]:
        return True
    return False


def get_log_channel(msg_server):
    text_channels = [chan for chan in msg_server.channels if chan.type == discord.ChannelType.text]
    for chan in text_channels:
        if chan.name == CONFIG["log_channel_name"]:
            return chan
    return


bot.run(token)
