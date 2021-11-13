import datetime
import os
import unittest

import shopping
from suppliers import OdaWeb


class TestOdaWeb(unittest.TestCase):
    def setUp(self) -> None:
        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, 'test_data', 'Bestilling evndg9 - Oda.html')) as fp:
            html = fp.read()
        oda = OdaWeb(html)
        self.order = oda.get_order()

    def test_parse_order(self):
        self.assertEqual('evndg9', self.order.identifier)
        self.assertEqual(datetime.date(2021, 11, 7), self.order.date)
        self.assertIsInstance(self.order.lines[0], shopping.OrderLine)

    def test_line(self):
        line = self.order.lines[1]
        self.assertEqual(1.0, line.amount)
        self.assertEqual(27.90, line.price)
        self.assertEqual('l', line.package_unit)

    def test_line_amount(self):
        line = self.order.lines[4]
        self.assertEqual(3.0, line.amount)
        self.assertEqual(59.90, line.price)
        self.assertEqual(179.71, line.total)
        self.assertEqual(525, line.package_size)
        self.assertEqual('g', line.package_unit)
        self.assertEqual(114.10, line.unit_price(1000))

    def test_line_amount2(self):
        line = self.order.lines[0]
        self.assertEqual(1.0, line.amount)
        self.assertEqual(67.90, line.price)
        self.assertEqual(67.90, line.total)
        self.assertEqual('stk', line.package_unit)
        self.assertEqual(16, line.package_size)
