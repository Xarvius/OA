import datetime

from model.remind import Remind

filename = 'remind_db.txt'
date_format = '%Y-%m-%d %H:%M:%S'


def load_reminders():
    reminders = []
    with open(filename) as file:
        for line in file.readlines():
            data = line.split('|')
            id = int(data[0])
            date = datetime.datetime.strptime(data[1], date_format)
            message = data[2]
            remind = Remind(date, message, id)
            reminders.append(remind)
        print('loaded reminders')
    return reminders


def update_reminders(reminders):
    with open(filename, 'w+') as file:
        file_content = []
        for remind in reminders:
            to_file = str(remind.uuid) + '|' + str(remind.date) + '|' + remind.msg
            file_content.append(to_file)
        file.write('\n'.join(file_content))
        file.truncate()
