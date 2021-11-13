class OrderLine:
    barcode: int
    """Product barcode"""
    name: str
    """Product name"""
    price: float
    """Item price"""
    amount: float
    """Line amount"""
    package_size: float
    """Product package size"""
    package_unit: str
    """Product package size unit"""
    total: float
    """Line sum"""
    tax: float
    """Tax amount"""

    def __init__(self, barcode: int = None, name: str = None, price: float = None,
                 amount: float = None, package_size: float = None, package_unit: str = None,
                 total: float = None, tax: float = None):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.amount = amount
        self.package_size = package_size
        self.package_unit = package_unit
        self.total = total
        self.tax = tax

        if not self.price and self.total and self.amount:
            self.price = round(self.total / self.amount, 2)

    def __str__(self):
        return self.name

    def unit_price(self, multiplier=1):
        price = (self.price / self.package_size) * multiplier
        return round(price, 2)
