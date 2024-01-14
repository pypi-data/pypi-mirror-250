"""


"""
from tropicpy.tropical.tropical_matrix import *


class GrigorieShpilrain2014:

    def __init__(self, A, B, g, p_min, p_max):
        if not isinstance(A, TropicalMatrix):
            raise Exception(str(A) + " is not an appropriate value.")
        elif not isinstance(B, TropicalMatrix):
            raise Exception(str(B) + " is not an appropriate value.")
        else:
            if A.rows != B.rows or A.columns != B.columns:
                raise Exception("Matrices A and B are of different dimensions.")
            elif A.rows != A.columns:
                raise Exception("Matrix A is not a square matrix.")
            elif B.rows != B.columns:
                raise Exception("Matrix B is not a square matrix.")
            elif A * B == B * A:
                raise Exception("Matrices A and B do not satisfy the condition A*B!=B*A.")

            self.n = A.rows
            self.A = A
            self.B = B
            self.g = g

            tmp_p1 = []
            tmp_p2 = []
            for i in range(g + 1):
                tmp_p1.extend([generate_random_tropical_value(p_min, p_max)])
                tmp_p2.extend([generate_random_tropical_value(p_min, p_max)])

            self._p1 = tmp_p1
            self._p2 = tmp_p2

            result1 = tropical_matrix_0(self.n)
            result2 = tropical_matrix_0(self.n)
            for (el1, el2, i) in zip(self._p1, self._p2, range(self.g + 1)):
                result1 += (self.A ** i) * el1
                result2 += (self.B ** i) * el2

            self._p_1_A = result1
            self._p_2_B = result2

            self.m = None
            self._K = None

    def send_message(self, prnt=False):
        self.m = self._p_1_A * self._p_2_B
        if prnt:
            print("Message:\n" + str(self.m))
        return self.m

    def set_Key(self, v):
        self._K = self._p_1_A * v * self._p_2_B

    def get_Key(self):
        return self._K

    def check_Key(self, check_K):
        return check_K == self._K
