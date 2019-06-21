import datetime
import uuid


class Remind:
    def __init__(self, date, msg, remind_id=None):
        self.uuid = remind_id if remind_id else str(uuid.uuid4().fields[-1])[:3]
        self.date = date
        self.msg = msg
        self.displayed = self.set_displayed()

    def __repr__(self) -> str:
        return 'ID: ' + str(self.uuid) + ' | ' + str(self.date) + '\n' + self.msg

    def display(self):
        return '@everyone Przypomnienie: ' + str(self.date) + '\n' + self.msg

    def set_displayed(self):
        if (self.date - datetime.datetime.now()) > datetime.timedelta(0, 1800, 0):
            return 3
        elif (self.date - datetime.datetime.now()) > datetime.timedelta(0, 900, 0):
            return 2
        elif (self.date - datetime.datetime.now()) > datetime.timedelta(0, 5, 0):
            return 1
