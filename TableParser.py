from HTMLParser import HTMLParser


class TableParser(HTMLParser):
    table = []

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.in_td = False
        self.tr_count = 0
        self.table = []
        self.item = {'date': None, 'time': None}  # TODO needs refactor!

    def handle_starttag(self, tag, attributes):
        if tag == 'td':
            self.in_td = True
        elif tag == 'tr':
            self.tr_count = 0
            if type(self.item['date']) is str:
                self.table.append(self.item)
            self.item = {'date': None, 'time': None}  # TODO needs refactor!
        elif tag == 'table':
            self.in_table = True

    def handle_data(self, data):
        if self.in_table:
            if self.in_td:
                self.tr_count += 1
                if self.tr_count <= 2:
                    if self.tr_count == 1:
                        self.item['date'] = data
                    else:
                        self.item['time'] = data
                    # print data

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
        elif tag == 'table':
            self.in_table = False
