"""

"""

from tropicpy.tropical.tropical_matrix import *


def rudy_monico(A, B, U, V):
    r = 1
    tmp_A = semidirect_power_1st(A, B, r)
    while U <= tmp_A:
        r *= 2
        tmp_A = semidirect_power_1st(A, B, r)
    print("Upper bound found: \n" + str(r))
    upper = r
    lower = upper >> 1
    while upper >= lower:
        middle = (lower + upper) >> 1
        tmp_A = semidirect_power_1st(A, B, middle)
        if tmp_A == U:
            print("Attack was succesful!")
            break
        elif tmp_A <= U:
            upper = middle - 1
        else:
            lower = middle + 1

    print("m=" + str(middle))
    Bm = semidirect_power_2nd(A, B, middle)
    return semidirect_product_1st(V, None, U, Bm)
