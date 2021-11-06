from .GrocyAPI import GrocyAPI
from .Product import Product
from .UnitConversion import UnitConversion


class Grocy(GrocyAPI):
    def __init__(self, url, api_key):
        super().__init__(url, api_key)
        self.conversion = UnitConversion(url, api_key)

    def products(self):
        return self.get(self.url + '/api/objects/products')

    def products_custom_key(self, key_field):
        products = {}
        for product in self.products():
            if key_field in product['userfields']:
                product['id'] = int(product['id'])
                products[product['userfields'][key_field]] = product

        return products

    def get_product(self, name, user_field=None):
        for product in self.products():
            product['id'] = int(product['id'])
            if product['name'] == name:
                return product

            if user_field in product['userfields'] and product['userfields'][user_field] == name:
                return product

        raise ValueError('Unknown product name: %s' % name)

    def get_product_obj(self, name, user_field=None):
        product = self.get_product(name, user_field)
        return Product(self, product)

    def get_stock(self, product):
        return self.get(self.url + '/api/stock/products/%d/entries' % product)

    def add_stock(self, product: int, amount: float, price: float, best_before_date=None,
                  shopping_location=None, purchased_date=None, qu_id=None):
        """

        :param product:
        :param amount: Stock unit amount
        :param price: Price per stock unit
        :param best_before_date:
        :param shopping_location:
        :param purchased_date:
        :param qu_id:
        :return:
        """
        data = {
            'amount': amount,
            'best_before_date': best_before_date,
            'transaction_type': 'purchase',
            'price': price,
            'shopping_location_id': shopping_location,
            'purchased_date': purchased_date,
            'qu_id': qu_id
        }

        response = self.session.post(self.url + '/api/stock/products/%d/add' % product, data)
        response.raise_for_status()
        return response.json()
