"""


"""
from tropicpy.attacks.attacks_utils import *


def kotov_ushakov(A, B, g, U, V, p_min):
    n = A.rows
    data = []

    for i in range(g + 1):
        for j in range(g + 1):
            matrix_min = min_of_matrix_difference((A ** i) * (B ** j), U * TropicalValue((-2) * -1000))
            if matrix_min[0].value <= 0:
                result = {"i": i, "j": j, "minval": matrix_min[0], "inds": matrix_min[1]}
                data.append(result)

    inds = [result["inds"] for result in data]
    C = minimal_set_covers(inds)

    minimal_covers_ij = []
    for cover in C:
        minimal_covers_ij.extend(
            list_cartesian([[[record["i"], record["j"]] for record in data if el == record["inds"]] for el in cover]))

    for ij in minimal_covers_ij:
        result = simplex(make_simplex_matrix(data, g, ij))
        if result:
            polys = [[int(result[i] + p_min) for i in range(g + 1)], [int(result[g + 1 + i] + p_min) for i in range(g + 1)]]
            p1_A = tropical_matrix_0(n)
            p2_B = tropical_matrix_0(n)
            for (el1, el2, i) in zip(polys[0], polys[1], range(g + 1)):
                p1_A += (A ** i) * TropicalValue(el1)
                p2_B += (B ** i) * TropicalValue(el2)

            print("Attack was succesfull!")
            print("p1(A)=\n" + str(p1_A))
            print("p2(B)=\n" + str(p2_B))

            return p1_A * V * p2_B

    return False
