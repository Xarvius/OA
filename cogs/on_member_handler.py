import datetime

import discord
from discord.ext import commands
from discord.utils import get

from utils import config


class MemberHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = config.load_config()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg_priv = self.config["MESSAGE"]["msg_priv"]
        await member.send(msg_priv)
        role = get(member.guild.roles, name="Gość")
        return await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) != len(after.roles):
            for role in before.roles:
                if role.name == 'Okres Próbny':
                    return
            for role in after.roles:
                if role.name == 'Okres Próbny':
                    msg = self.config["MESSAGE"]["msg_trial"]
                    await after.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.client.get_channel(self.config["log_channel_name"])
        descriptionmsg = '%s wyszedł z serwera.' % member.mention
        embed = discord.Embed(title="WYJŚCIE Z SERWERA [LOG]", description=descriptionmsg, color=0x00ff00,
                                  timestamp=datetime.datetime.utcnow())
        embed.set_author(name=member, url=embed.Empty, icon_url=member.avatar_url)
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MemberHandler(bot))
