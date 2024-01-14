"""


"""
from tropicpy.tropical.tropical_utils import *

inf = "inf"


class TropicalValue(object):
    def __init__(self, value):
        if value == inf or value == float(inf):
            self.is_num = False
            self.value = float(inf)
        elif is_number(value):
            self.is_num = True
            self.value = value
        else:
            raise Exception(str(value) + " is not an accurate tropical value.")

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return TropicalValue(min(self.value, other.value))

    def __mul__(self, other):
        return TropicalValue(self.value + other.value)

    def __pow__(self, power, modulo=None):
        return self.value * power


tropical_0 = TropicalValue(inf)
tropical_1 = TropicalValue(0)


def correct_tropical_value(value):
    try:
        TropicalValue(value)
    except:
        return False
    else:
        return True
