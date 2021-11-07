from grocy.GrocyAPI import GrocyAPI
from grocy import exceptions


class UnitConversion(GrocyAPI):
    def __init__(self, url, api_key):
        super().__init__(url, api_key)
        self.quantities = self.get('/api/objects/quantity_units')

    def get_quantity_dict(self, key_field='abbreviation'):
        data = self.get(self.url + '/api/objects/quantity_units')
        units = {}
        for unit in data:
            unit['id'] = int(unit['id'])
            if key_field in unit['userfields'] and unit['userfields'][key_field]:
                key = unit['userfields'][key_field]
            elif key_field in unit and unit[key_field]:
                key = unit[key_field]
            else:
                key = unit['name']
            units[key] = unit

        return units

    def get_quantity(self, name):
        for unit in self.quantities:
            unit['id'] = int(unit['id'])
            for value in unit.values():
                if value == name:
                    return unit
            for value in unit['userfields'].values():
                if value == name:
                    return unit

        raise exceptions.InvalidUnitException('Unknown unit: %s' % name)

    def get_conversion(self, product: int, unit_from: int, unit_to: int):
        assert isinstance(product, int), 'Product id is not int'
        assert isinstance(unit_from, int)
        assert isinstance(unit_to, int)

        data = self.get(self.url + '/api/objects/quantity_unit_conversions')
        reverse = False
        for conversion in data:
            if not conversion['product_id'] or int(conversion['product_id']) != product:
                continue
            if int(conversion['from_qu_id']) != unit_from or int(conversion['to_qu_id']) != unit_to:
                if int(conversion['from_qu_id']) != unit_to or int(conversion['to_qu_id']) != unit_from:
                    continue
                else:
                    reverse = True

            return float(conversion['factor']), reverse
        raise exceptions.MissingConversionException(
            'No conversion found for product %d from %s to %s' % (product, unit_from, unit_to))

    def convert(self, product_id: int, unit_from: int, unit_to: int, value):
        factor, reverse = self.get_conversion(product_id, unit_from, unit_to)
        if not reverse:
            return value * factor
        else:
            return value / factor

#    def purchase_convert_default(self, product_id: int, value):

