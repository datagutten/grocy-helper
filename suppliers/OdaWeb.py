import re
from datetime import datetime

import lxml.html

from shopping import Order, OrderLine


def get_float(text):
    return float(text.strip().replace(',', '.'))


def get_amount(text):
    text = text.replace('vask', 'stk')
    matches = re.match(r'(.+)\s([0-9,]+)\s(k?g|stk|[md]?l|pk)', text)
    if matches:
        product_name = re.sub(r'\s[0-9]+ x [0-9,]+.+', '', matches.group(1))
        if product_name[-1] == ',':
            product_name = product_name[:-1]
        unit = matches.group(3).replace('pk', 'stk')
        return product_name, get_float(matches.group(2)), unit
    else:
        return text, None, None


class OdaWeb:
    order: Order

    def __init__(self, html):
        self.data = lxml.html.fromstring(html)
        self.get_order()
        self.parse_order_lines()

    def get_order(self) -> Order:
        date = self.parse_date()
        identifier = self.get_table_cell('Bestilling')
        self.order = Order(date=date.date(), identifier=identifier)
        return self.order

    def get_table_cell(self, header):
        element = self.data.find('.//th[.="%s"]/../td' % header)
        return element.text.strip()

    def parse_date(self) -> datetime:
        order_date_string = self.get_table_cell('Bestilt')
        order_date = datetime.strptime(order_date_string, '%d. %B %Y %H:%M')
        delivery_date_string = self.get_table_cell('Leveringstid')
        delivery_date_string = re.sub(r'.+, ([0-9]\.+.+) - [0-9]{2}:[0-9]{2}',
                                      r'%d \1' % order_date.year, delivery_date_string)
        delivery_date = datetime.strptime(delivery_date_string, '%Y %d. %B, %H:%M')
        return delivery_date

    def parse_order_lines(self):
        lines = self.data.findall('.//tr[@class="order-line "]')
        for line in lines:
            description = line.find('.//div[@class="product-description"]/.').text.strip()
            fields = line.findall('.//td[@class="text-right"]')
            name, package_size, package_unit = get_amount(description)

            line_obj = OrderLine(name=name,
                                 amount=get_float(fields[0].text),
                                 total=get_float(fields[2].text),
                                 tax=get_float(fields[1].text.strip()[:-1]),
                                 package_size=package_size,
                                 package_unit=package_unit
                                 )

            self.order.add_line(line_obj)
        return self.order.lines
