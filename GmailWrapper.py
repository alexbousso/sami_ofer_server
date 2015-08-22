import base64
from email.mime.text import MIMEText
from googleapiclient import errors
import os
import httplib2
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import argparse


class GmailWrapper:
    def __init__(self):
        try:
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        self.SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Sami Ofer Project'

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('.')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail_send.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    @staticmethod
    def create_mail(sender, to, subject, message_text):
        """
        Create a message for an email.

        :param sender: Email address of the sender.
        :param to: Email address of the receiver.
        :param subject: The subject of the email message.
        :param message_text: The text of the email message.
        :returns : An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    @staticmethod
    def send_message(service, user_id, message):
        """
        Send an email message.

        :param service: Authorized Gmail API service instance.
        :param user_id: User's email address. The special value "me"
        :param message: Message to be sent.
        :returns : Sent message
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print 'Message Id: %s' % message['id']
            return message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


def main():
    gmail = GmailWrapper()

    credentials = gmail.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = gmail.create_mail('alexbousso@gmail.com', 'alexbousso@gmail.com', 'Hello',
                                'Hello World!')
    gmail.send_message(service, 'me', message)

if __name__ == '__main__':
    main()
