"""


"""

from tropicpy.attacks.attacks_utils import *


def isaac_kahrobaei(A, B, U, V):
    m = 1

    D = None
    A_now = A

    previous_D = []
    previous_A = [None]

    while semidirect_power_1st(A, B, m) != U:

        additional_previous_D = []

        while D not in additional_previous_D:
            A_before = A_now
            A_now = semidirect_product_1st(A_before, None, A, B)
            additional_previous_D.append(D)
            previous_A.append(A_before)
            D = matrix_difference(A_now, A_before)

        previous_D = previous_D + additional_previous_D

        previous_D.reverse()
        d = len(previous_D) - previous_D.index(D) - 2
        previous_D.reverse()

        rho = len(previous_D) - (d + 1)
        print("d=" + str(d))
        print("rho=" + str(rho))

        if any(is_zero_matrix(prev_D) for prev_D in previous_D) or is_zero_matrix(D):
            m = d + 1
            break

        Y = matrix_difference(U, previous_A[d + 1])
        full_sum = matrix_sum([previous_D[i + 1] for i in range(d, d + rho)])

        for a in range(1, rho + 1):
            partial_sum = matrix_sum([previous_D[i] for i in range(d + 1, d + a + 1)], D.rows)
            diff = matrix_difference(Y, partial_sum)
            if is_zero_modulo(diff, full_sum):
                print("k=" + str(a))
                break

        x = (diff.values[0][0]).value // (full_sum.values[0][0]).value
        print("x=" + str(x))
        m = d + x * rho + a + 1

    print("Attack was succesfull!")
    print("m = " + str(m))
    Bm = semidirect_power_2nd(A, B, m)

    return semidirect_product_1st(V, None, U, Bm)
