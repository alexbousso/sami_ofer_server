import urllib
from TableParser import TableParser

parser = TableParser()

response = urllib.urlopen(
    'http://www.haifa-stadium.co.il/%D7%9E%D7%A9%D7%97%D7%A7%D7%99_%D7%9B%D7%93%D7%95%D7%A8%D7%92%D7%9C')
data = response.read()

parser.feed(data)
