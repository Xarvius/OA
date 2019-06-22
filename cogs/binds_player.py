import json

import discord
from discord.ext import commands

from utils.bot_utils import is_allowed_to_command


class BindsPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.player = None
        self.binds = self._load_binds()

    @commands.group()
    async def player(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid reminder command passed.')

    @player.command()
    @is_allowed_to_command()
    async def join(self, ctx):
        if self.player:
            await ctx.send("You have to disconnect player first")
        channel = ctx.author.voice.channel
        self.player = await channel.connect()

    @player.command()
    @is_allowed_to_command()
    async def leave(self, ctx):
        if not self.player:
            pass
        await self.player.disconnect()
        self.player = None

    @player.command()
    @is_allowed_to_command()
    async def play(self, ctx, command):
        if not self.player:
            return await ctx.send("You have to connect player first")

        if self.player.is_playing():
            self.player.stop()

        music_name = self._find_bind_in_binds(command)
        if not music_name:
            return await ctx.send('Bind not found.')
        self.player.play(discord.FFmpegPCMAudio(music_name))

    def _find_bind_in_binds(self, bind_name):
        found = False
        for key in self.binds.keys():
            if key == bind_name:
                found = True
                break

        if not found:
            return
        return './sounds/' + self.binds[bind_name]

    def _load_binds(self):
        with open('./utils/binds.json', encoding='utf-8') as binds:
            binds = json.load(binds)
        return binds


def setup(client):
    client.add_cog(BindsPlayer(client))
