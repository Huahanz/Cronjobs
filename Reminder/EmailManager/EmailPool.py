from random import choice


class EmailPool:
    def __init__(self):
        pass

    def get_email_sender(self):
        sender_list = self.get_all_email_sender()
        sender = choice(sender_list)
        return sender

    def get_all_email_sender(self):
        all_list = []
        all_list.append(['huahanzh@gmail.com', 'testemail123'])
#        all_list.append(['nasdaqstock.cronjobs@gmail.com', 'emailtest012'])
        return all_list
