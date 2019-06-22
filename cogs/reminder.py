import datetime

from discord.ext import commands, tasks

from utils.bot_utils import is_allowed_to_command
from converters.date_helper import DateHelper
from utils.file_serivce import load_reminders, update_reminders
from model.remind import Remind


class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reminders = load_reminders()
        self.check_reminders.start()

    @commands.group()
    async def reminder(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid reminder command passed.')

    @reminder.command()
    @is_allowed_to_command()
    async def add(self, ctx, date: DateHelper, *message: str):
        """Adds new reminder, only leaders are allowed"""
        if not date:
            return

        remind = Remind(date, ' '.join(message))
        self.reminders.append(remind)
        update_reminders(self.reminders)
        await ctx.send('Dodano przypomnienie: ' + str(remind))

    @reminder.command()
    async def list(self, ctx):
        """Show all reminders"""
        message = '\n\n'.join(str(reminder) for reminder in self.reminders)
        await ctx.send('PRZYPOMNIENIA:\n\n' + message)

    @reminder.command()
    @is_allowed_to_command()
    async def remove(self, ctx, id: int):
        """Remove reminder, only leaders are allowed"""

        async for remind in self.reminders:
            if remind.uuid == id:
                self.reminders.remove(remind)
                update_reminders(self.reminders)
                return await ctx.send('Usunieto przypomnienie: ' + str(id))
        await ctx.send('Nie znaleziono przypomnienia: ' + str(id))

    @tasks.loop(seconds=10.0)
    async def check_reminders(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(493171873274789898)
        updated = False
        for remind in self.reminders:
            print(remind.date - datetime.datetime.now())
            print(remind.displayed)
            if (remind.date - datetime.datetime.now()) < datetime.timedelta(days=-1, hours=23,
                                                                            minutes=59):  # remind date is after now
                self.reminders.remove(remind)
                updated = True
            elif remind.displayed == 3 and (remind.date - datetime.datetime.now()) < datetime.timedelta(0, 1800, 0):
                await channel.send(remind.display())
                remind.displayed = remind.displayed - 1
            elif remind.displayed == 2 and (remind.date - datetime.datetime.now()) < datetime.timedelta(0, 900, 0):
                await channel.send(remind.display())
                remind.displayed = remind.displayed - 1
            elif remind.displayed == 1 and (remind.date - datetime.datetime.now()) <= datetime.timedelta(0, 11, 0):
                await channel.send(remind.display())
                self.reminders.remove(remind)
                updated = True
        if updated:
            update_reminders(self.reminders)


def setup(client):
    client.add_cog(Reminder(client))
