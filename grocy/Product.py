from grocy import Grocy


class Product:
    id: int
    stock_unit: int

    stock_amount: float = None
    """
    Number of stock units
    """

    stock_unit_price: float = None
    """
    Price for one stock unit
    """

    def __init__(self, grocy_api: Grocy, product=None):
        self.api = grocy_api
        if product:
            self.id = int(product['id'])
            self.name = product['name']
            self.stock_unit = int(product['qu_id_stock'])
            self.purchase_unit = int(product['qu_id_purchase'])
            self.purchase_unit_factor = float(product['qu_factor_purchase_to_stock'])

    def set_package(self, package_size, package_unit: int, package_price, num_packages=1):
        pieces = package_size * num_packages
        piece_price = (package_price * num_packages) / pieces
        if package_unit != self.stock_unit:
            self.stock_amount = self.api.conversion.convert(self.id, package_unit, self.stock_unit,
                                                            pieces)
            self.stock_amount = round(self.stock_amount, 2)

            self.stock_unit_price = (package_price * num_packages) / self.stock_amount
            self.stock_unit_price = round(self.stock_unit_price, 2)
        else:
            # Purchased unit is the same as stock, no conversion required
            self.stock_amount = round(pieces, 2)
            self.stock_unit_price = round(piece_price, 2)

    def set_total_price(self, total):
        self.stock_unit_price = total / self.stock_amount

    def set_unit_price(self, price):
        self.stock_unit_price = price

    def set_amount(self, amount, unit=None):
        if unit and unit != self.stock_unit:
            raise ValueError('Conversion needed')
        else:
            self.stock_amount = amount
