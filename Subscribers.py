import pickle
import re
import os.path


class Subscribers:
    subscribers = []

    def __init__(self):
        if not (os.path.exists('subscribers') and os.path.isfile('subscribers')):
            self.subscribers = []
            return
        subscribers_file = open('subscribers', 'rb')
        self.subscribers = pickle.load(subscribers_file)
        subscribers_file.close()

    def __serialize__(self):
        subscribers_file = open('subscribers', 'wb')
        pickle.dump(self.subscribers, subscribers_file)
        subscribers_file.close()

    @staticmethod
    def __check_if_email__(email):
        if not isinstance(email, str):
            raise ValueError('email must be a str, but received: {0}'.format(type(email)))
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('email is not a valid e-mail, received: {0}'.format(email))

    def add(self, email):
        """
        Adds an e-mail to the list of subscribers.
        :type email: str
        :param email: The e-mail to add
        :return: Raises ValueError if email is not an instance of str or if email is not a valid e-mail.
        """
        self.__check_if_email__(email)
        if email in self.subscribers:
            raise Exception('{0} is already subscribed'.format(email))
        self.subscribers.append(email)
        self.__serialize__()

    def remove(self, email):
        self.__check_if_email__(email)
        self.subscribers.remove(email)
        self.__serialize__()

    def get_emails(self):
        return self.subscribers
