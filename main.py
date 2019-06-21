import asyncio
import os

import discord
from discord import InvalidArgument
import datetime
from discord.ext import commands

import config
from discord.utils import get

from file_serivce import load_reminders, update_reminders
from on_message_handler import voice_binds
from remind import Remind

CONFIG = config.load_json('config.json')
binds = config.load_json('binds.json')
players = {}
server = {}
reminders = load_reminders()

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


@bot.command(pass_context=True)
async def remind_add(ctx):
    """Adds new reminder, only leaders are allowed"""
    if not check_user_permissions(ctx.message.author.id):
        pass
    date_format = '%d/%m/%Y %H:%M'
    message = ctx.message.content
    data = message.split(' ')

    if len(data) < 4:
        await bot.send_message(ctx.message.channel, "Niepoprawna ilosc parametrow: data godzina wiadomosc")
        return

    date_str = data[1] + ' ' + data[2]
    try:
        date_obj = datetime.datetime.strptime(date_str, date_format)
    except ValueError as ve:
        await bot.send_message(ctx.message.channel, "Niepoprawny format daty, poprawny format to: " + date_format)
        return

    message = ' '.join(data[3:])

    remind = Remind(date_obj, message)
    reminders.append(remind)
    update_reminders(reminders)
    await bot.send_message(ctx.message.channel, 'Dodano przypomnienie: ' + str(remind))


@bot.command(pass_context=True)
async def remind_list(ctx):
    """Show all reminders"""
    message = '\n\n'.join(str(reminder) for reminder in reminders)
    await bot.send_message(ctx.message.channel, 'PRZYPOMNIENIA:\n\n' + message)


@bot.command(pass_context=True)
async def remind_remove(ctx):
    """Remove reminder, only leaders are allowed"""
    if not check_user_permissions(ctx.message.author.id):
        pass
    id = ctx.message.content.split(' ')[1]
    for remind in reminders:
        if remind.uuid == id:
            reminders.remove(remind)
            update_reminders(reminders)
            await bot.send_message(ctx.message.channel, 'Usunieto przypomnienie: ' + id)
            return
    await bot.send_message(ctx.message.channel, 'Nie znaleziono przypomnienia: ' + id)


async def check_reminders():
    await bot.wait_until_ready()
    channel = bot.get_channel("493171873274789898")
    while not bot.is_closed:
        updated = False
        for remind in reminders:
            # print(remind.date - datetime.datetime.now())
            # print(remind.displayed)
            if remind.date < datetime.datetime.now():  # remind date is after now
                reminders.remove(remind)
                updated = True
            elif remind.displayed == 3 and (remind.date - datetime.datetime.now()) < datetime.timedelta(0, 1800, 0):
                await bot.send_message(channel, remind.display())
                remind.displayed = remind.displayed - 1
            elif remind.displayed == 2 and (remind.date - datetime.datetime.now()) < datetime.timedelta(0, 900, 0):
                await bot.send_message(channel, remind.display())
                remind.displayed = remind.displayed - 1
            elif remind.displayed == 1 and (remind.date - datetime.datetime.now()) < datetime.timedelta(0, 5, 0):
                await bot.send_message(channel, remind.display())
                reminders.remove(remind)
                updated = True
        if updated:
            update_reminders(reminders)
        await asyncio.sleep(5)


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


@bot.command(pass_context=True)
async def clear(ctx):
    channel = ctx.message.channel
    async for msg in bot.logs_from(channel):
        if not msg.pinned:
            await bot.delete_message(msg)


bot.loop.create_task(check_reminders())
bot.run(os.environ['TOKEN'])
