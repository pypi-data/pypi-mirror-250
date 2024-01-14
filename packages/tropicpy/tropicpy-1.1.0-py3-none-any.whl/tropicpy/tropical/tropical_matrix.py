"""


"""

from tropicpy.tropical.tropical_value import *
import random

class TropicalMatrix:
    def __init__(self, values):

        tmp_rows = len(values)
        if tmp_rows == 0:
            tmp_columns = 0
        else:
            tmp_columns = len(values[0])
        tmp_values = []

        for (row, i) in zip(values, range(tmp_rows)):
            if len(row) != tmp_columns:
                raise Exception("Missing values in row no. " + str(i + 1) + ": " + str(row))

        for (row, i) in zip(values, range(tmp_rows)):
            tmp_row = []
            for value in row:
                if correct_tropical_value(value):
                    tmp_row.append(TropicalValue(value))
                elif isinstance(value, TropicalValue) and correct_tropical_value(value.value):
                    tmp_row.append(value)
                else:
                    raise Exception(str(value) + " is not an accurate element of a tropical matrix.")
            tmp_values.append(tmp_row)

        self.rows = tmp_rows
        self.columns = tmp_columns
        self.values = tmp_values

    def __str__(self):
        if len(self.values) == 0:
            return "[]"

        result = ""
        column_widths = []
        for col_no in range(self.columns):
            column_widths += [max(len(str(row[col_no])) for row in self.values)]

        for (row, row_no) in zip(self.values, range(self.rows)):
            result += "["
            for (value, col_no) in zip(row, range(self.columns)):
                result += '{0:^{1}}'.format(str(value), column_widths[col_no] + 2)
            result += "]"
            if row_no != self.rows - 1:
                result += "\n"
        return result

    def __eq__(self, other):
        if isinstance(other, TropicalMatrix):
            if self.rows != other.rows:
                return False
            elif self.columns != other.columns:
                return False

            for (row_a, row_b) in zip(self.values, other.values):
                for (a, b) in zip(row_a, row_b):
                    if a != b:
                        return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        if self + other == self:
            return True
        else:
            return False

    def __add__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Different dimensions of matrices.")

        result = []
        for (row_a, row_b) in zip(self.values, other.values):
            tmp_row = []
            for (a, b) in zip(row_a, row_b):
                tmp_row.append(a + b)
            result.append(tmp_row)
        return TropicalMatrix(result)

    def __mul__(self, other):
        if isinstance(other, TropicalMatrix):
            if self.columns != other.rows:
                raise Exception("Mismatched dimensions of matrices.")

            result = []
            other_columns = []

            for col_no in range(other.columns):
                other_columns.append([row[col_no] for row in other.values])

            for row in self.values:
                tmp_row = []
                for col_no in range(self.columns):
                    times = list(map(TropicalValue.__mul__, row, other_columns[col_no]))
                    tropical_sum = tropical_0
                    for el in times:
                        tropical_sum += el
                    tmp_row.append(tropical_sum)
                result.append(tmp_row)
            return TropicalMatrix(result)
        elif isinstance(other, TropicalValue):
            result = []
            for row in self.values:
                tmp_row = []
                for value in row:
                    tmp_row.append(other * value)
                result.append(tmp_row)

            return TropicalMatrix(result)
        else:
            raise Exception("Cannot perform tropical multiplication for type: " + str(type(other)))

    def __pow__(self, power, modulo=None):
        if isinstance(power, int):
            if power == 0:
                return tropical_matrix_1(self.rows)
            elif power == 1:
                return self
            elif power % 2 == 0:
                return (self * self) ** (power >> 1)
            else:
                return self * ((self * self) ** ((power - 1) >> 1))
        else:
            raise Exception(str(power) + " is not an accurate power.")

    def __matmul__(self, other):
        if isinstance(other, TropicalMatrix):
            return self + other + (self * other)
        else:
            raise Exception("Cannot perform adjoint multiplication for type: " + str(type(other)))

    def __xor__(self, power):
        if power == 1:
            return self
        elif power % 2 == 0:
            return (self @ self) ^ (power >> 1)
        else:
            return self @ ((self @ self) ^ ((power - 1) >> 1))


def semidirect_product_1st(A, B, C, D):
    return (A @ D) + C


def semidirect_product_2nd(A, B, C, D):
    return B @ D


# originally square-and-multiply method
def semidirect_power_1st(A, B, n):
    if n == 1:
        return A
    else:
        I = tropical_matrix_1(A.rows)
        return ((A * (I + B)) + B) * ((I + B) ** (n - 2))


def semidirect_power_2nd(A, B, n):
    return B ^ n


def tropical_matrix_0(n):
    values = []
    for i in range(n):
        values.append([tropical_0] * n)
    return TropicalMatrix(values)


def tropical_matrix_1(n):
    values = []
    for i in range(n):
        tmp_row = [tropical_0] * n
        tmp_row[i] = tropical_1
        values.append(tmp_row)
    return TropicalMatrix(values)


def generate_random_tropical_value(l, u):
    value = random.randint(l, u)
    if random.randint(1, 100) == 1:
        value = inf
    return TropicalValue(value)


def generate_random_tropical_matrix(n, l, u):
    values = []
    for i in range(n):
        tmp_row = []
        for j in range(n):
            tmp_row.append(generate_random_tropical_value(l, u))
        values.append(tmp_row)
    return TropicalMatrix(values)
