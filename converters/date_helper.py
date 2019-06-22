import datetime

from discord.ext import commands

from errors.errors import DateFormatError


class DateHelper(commands.Converter):

    async def convert(self, ctx, argument):
        date_format = '%d/%m/%Y_%H:%M'
        try:
            return datetime.datetime.strptime(argument, date_format)
        except ValueError as ve:
            raise DateFormatError('Invalid date format: ' + date_format)
