from apiclient import discovery
import urllib
from datetime import datetime
import httplib2
from GmailWrapper import GmailWrapper
from Subscribers import Subscribers
from TableParser import TableParser

parser = TableParser()
response = urllib.urlopen(
    'http://www.haifa-stadium.co.il/%D7%9E%D7%A9%D7%97%D7%A7%D7%99_%D7%9B%D7%93%D7%95%D7%A8%D7%92%D7%9C')
data = response.read()
parser.feed(data)
games = parser.table

have_game_today = False
time = 0
for game in games:
    day, month = game['date'].split('/', 1)
    if day == str(datetime.now().day) and month == str(datetime.now().month):
        have_game_today = True
        time = game['time']
        break
if have_game_today:
    mail = GmailWrapper()
    mail.get_credentials()

    credentials = mail.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    s = Subscribers()
    for email in s.subscribers:
        msg = mail.create_mail('alexbousso@gmail.com', email, 'Game today',
                               'Unfortunately there\'s a game today in Sami Ofer stadium, starting at '
                               + str(time) + ', so beware of traffic!')
        mail.send_message(service, 'me', msg)
