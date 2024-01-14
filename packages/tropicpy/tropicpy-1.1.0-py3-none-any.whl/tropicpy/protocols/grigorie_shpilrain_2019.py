"""


"""
from tropicpy.tropical.tropical_matrix import *


class GrigorieShpilrain2019:

    def __init__(self, A, B):
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

            self.k = A.rows
            self.A = A
            self.B = B

            self.m = random.getrandbits(int(2 ** 200).bit_length())

            self.U = None
            self.Bm = None
            self._K = None

    def send_message(self):
        self.U = semidirect_power_1st(self.A, self.B, self.m)
        self.Bm = semidirect_power_2nd(self.A, self.B, self.m)
        return self.U

    def set_Key(self, V):
        self._K = (V @ self.Bm) + self.U

    def get_Key(self):
        return self._K

    def check_Key(self, check_K):
        return check_K == self._K
