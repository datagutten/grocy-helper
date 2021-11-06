import unittest

from grocy import Grocy


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
        with self.assertRaises(ValueError, msg='No conversion found for product 10 from 5 to 2'):
            product.set_package(420, 5, 59.40, 1)

        # self.assertEqual(1, product.stock_amount)
        # self.assertEqual(59.40, product.stock_unit_price)

    def test_unit_price3(self):
        product = self.grocy.get_product_obj('Eplejuice')
        product.set_package(1.75, 4, 34.90, 4)
        self.assertEqual(7, product.stock_amount)
        self.assertEqual(19.94, product.stock_unit_price)


if __name__ == '__main__':
    unittest.main()