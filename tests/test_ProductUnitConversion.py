import unittest

from grocy import Grocy, exceptions


class TestProduct(unittest.TestCase):
    url = 'http://localhost:9283'
    api_key = 'KykIDhjC2cR3rVjJr2yQVvNmBxAOm7OL5fnHLI0gUkkOj49xyY'

    def setUp(self) -> None:
        self.grocy = Grocy(self.url, self.api_key)

    def test_unit_price1(self):
        product = self.grocy.get_product_obj('Pepsi Max')
        product.set_package(6, 2, 94.70, 1)
        self.assertEqual(15.78, product.stock_unit_price)

        product.set_package(9, 4, 94.70, 1)
        self.assertEqual(15.78, product.stock_unit_price)
        self.assertEqual(6, product.stock_amount)

    def test_unit_price2(self):
        product = self.grocy.get_product_obj('Maxboller')
        with self.assertRaises(exceptions.MissingConversionException, msg='No conversion found for product 10 from 5 to 2'):
            product.set_package(420, 5, 59.40, 1)

        # self.assertEqual(1, product.stock_amount)
        # self.assertEqual(59.40, product.stock_unit_price)

    def test_default_conversion(self):
        product = self.grocy.get_product_obj('Lefsegodt')
        product.set_default_package(18.40, 1)

        self.assertEqual(6, product.stock_amount)
        self.assertEqual(3.07, product.stock_unit_price)

    def test_unit_price3(self):
        product = self.grocy.get_product_obj('Eplejuice')
        product.set_package(1.75, 4, 34.90, 4)
        self.assertEqual(7, product.stock_amount)
        self.assertEqual(19.94, product.stock_unit_price)

    def test_unit_price4(self):
        product = self.grocy.get_product_obj('Eplejuice')
        product.set_package(1, 3, 139.61/4, 4)
        self.assertEqual(7, product.stock_amount)
        self.assertEqual(19.94, product.stock_unit_price)

    def test_invalid_conversion(self):
        product = self.grocy.get_product_obj('Eplejuice')
        with self.assertRaises(exceptions.MissingConversionException, msg='No conversion found for product 1 from 5 to 4'):
            product.set_package(1, 5, 139.61/4, 4)

    def test_get_quantity_unit(self):
        unit = self.grocy.conversion.get_quantity('l')
        self.assertEqual('liter', unit['name'])

        unit = self.grocy.conversion.get_quantity('stk')
        self.assertEqual('stk', unit['name'])

        unit = self.grocy.conversion.get_quantity('pakke')
        self.assertEqual(3, unit['id'])

    def test_get_invalid_quantity_unit(self):
        with self.assertRaises(exceptions.InvalidUnitException, msg='Unknown unit: kilogram'):
            self.grocy.conversion.get_quantity('kilogram')

    def test_get_quantity_dict_abbreviation(self):
        values = self.grocy.conversion.get_quantity_dict()
        self.assertIn('l', values.keys())

    def test_get_quantity_dict_name_plural(self):
        values = self.grocy.conversion.get_quantity_dict('name_plural')
        self.assertIn('gram', list(values.keys()))

    def test_get_quantity_dict_name(self):
        values = self.grocy.conversion.get_quantity_dict(None)
        self.assertIn('liter', list(values.keys()))


if __name__ == '__main__':
    unittest.main()
