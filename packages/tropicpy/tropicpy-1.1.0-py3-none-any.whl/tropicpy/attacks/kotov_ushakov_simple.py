"""


"""
from tropicpy.attacks.attacks_utils import *


def kotov_ushakov_simple(A, B, g, U, V):
    for i in range(1, g + 1):
        for j in range(1, g + 1):
            print("T_" + str(i) + str(j) + "=\n" + str(matrix_difference(U, (A ** i) * (B ** j))))
            c = is_matrix_difference_constant(U, (A ** i) * (B ** j))
            if c:
                print("Attack was succesfull!")
                print("c = " + str(c))
                print("i = " + str(i))
                print("j = " + str(j))

                return ((A ** i) * c) * V * (B ** j)
    return False
