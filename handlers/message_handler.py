from enums import flag as f
from enums import good as g
import flag
import re
import json


class MessageHandler:
    res = []
    item_price = None
    file_path = 'data/item_price.json'
    new_message = ''

    def __init__(self, message: str):
        self.message = message
        self.prepare_message()
        self.make_new_message()
        print(1223)

    def read_item_price(self):
        file = open(self.file_path)
        self.item_price = json.load(file)

    def prepare_message(self):
        lines = self.message.splitlines()
        lines = list(filter(None, lines))
        for line in lines:
            self.res.append(LineHandler(line, self.item_price))

    def make_new_message(self):
        for item in self.res:
            if item.new_line != '':
                self.message = self.message.replace(item.line, item.new_line)


class LineHandler:
    status = False

    price = None
    country = None
    good = None
    manufacturer = None
    item_price = None
    new_line = ''
    margin = 1500

    def __init__(self, line: str, item_price: dict):
        self.line = line
        self.item_price = item_price
        self.find_price()
        self.make_new_price()
        #self.find_flag()
        #self.find_manufacturer()

    def find_flag(self):
        for item in f.Flag:
            flag_item = flag.flag(item.value)
            if re.search(flag_item, self.line):
                self.country = item.name
                break

    def find_price(self):
        numbers = re.findall(r'\d+', self.line)
        numbers = list(map(int, numbers))
        if numbers:
            self.price = max(numbers)

    def make_new_price(self):
        if self.price:
            new_price = self.price + self.margin
            self.new_line = self.line.replace(str(self.price), str(new_price))
            self.status = True

    def find_manufacturer(self):
        for man in g.Manufacturer:
            for keyword in man.value:
                if re.search(keyword, self.line):
                    self.manufacturer = man.name


