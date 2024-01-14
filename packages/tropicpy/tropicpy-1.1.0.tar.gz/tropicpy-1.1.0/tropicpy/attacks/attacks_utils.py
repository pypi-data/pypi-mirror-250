"""


"""
from tropicpy.tropical.tropical_matrix import *


def value_difference(a, b):
    if b == tropical_0:
        return False
    elif a == tropical_0:
        return tropical_0
    else:
        return TropicalValue(a.value - b.value)


def matrix_difference(A, B):
    result = []
    for (row_a, row_b) in zip(A.values, B.values):
        tmp_row = []
        for (a, b) in zip(row_a, row_b):
            tmp_row.append(value_difference(a, b))
        result.append(tmp_row)

    return TropicalMatrix(result)


def double_matrix_sum(A, B):
    result = []
    for (row_a, row_b) in zip(A.values, B.values):
        tmp_row = []
        for (a, b) in zip(row_a, row_b):
            tmp_row.append(a * b)
        result.append(tmp_row)

    return TropicalMatrix(result)


def matrix_sum(matrix_table, n=None):
    if not matrix_table:
        return TropicalMatrix([[0] * n] * n)
    R = matrix_table[-1]
    matrix_table.pop()
    for M in matrix_table:
        R = double_matrix_sum(R, M)
    return R


def is_matrix_difference_constant(A, B):
    frst = True
    for (row_a, row_b) in zip(A.values, B.values):
        for (a, b) in zip(row_a, row_b):
            if frst:
                frst = False
                c = value_difference(a, b)
                if not c:
                    continue
            else:
                new_c = value_difference(a, b)
                if new_c:
                    if new_c != c:
                        return False
                    else:
                        c = new_c
    return c


def min_of_matrix_difference(A, B):
    matrix_min = tropical_0
    inds = []
    for (row_a, row_b, i) in zip(A.values, B.values, range(A.rows)):
        for (a, b, j) in zip(row_a, row_b, range(A.columns)):
            c = value_difference(a, b)
            if matrix_min == c:
                inds.append((i, j))
            elif matrix_min + c == c:
                matrix_min += c
                inds = [(i, j)]
    return matrix_min, inds


def is_cover(main_set, cover):
    tmp_main_set = main_set.copy()
    for curr_set in cover:
        for el in curr_set:
            tmp_main_set.remove(el)
    return len(tmp_main_set) == 0


def compress_data(data):
    result = []

    for record in data:
        if record not in result:
            result.append(record)

    return result


def list_union(list_of_lists):
    return list(set(sum(list_of_lists, [])))


def list_concatenation(list_of_lists):
    concatenation = []

    for el in list_of_lists:
        if len(el) > 0:
            concatenation += el

    return concatenation


def list_difference(list_of_lists1, list_of_els2):
    difference = []

    for el in list_of_lists1:
        el_differece = [ind for ind in el if ind not in list_of_els2]
        if len(el_differece) > 0:
            difference.append(el_differece)

    return difference


def list_cartesian(list_of_lists):
    n = len(list_of_lists)

    if n == 1:
        return list_of_lists
    if n == 2:
        tmp_cartesian = []
        for el1 in list_of_lists[0]:
            tmp_cartesian.extend([[el1, el2] for el2 in list_of_lists[1]])
        return tmp_cartesian
    else:
        tmp_cartesian = []
        for el1 in list_of_lists[0]:
            tmp_cartesian.extend(list_concatenation([[el1], el2]) for el2 in list_cartesian(list_of_lists[1:]))
        return tmp_cartesian


def minimal_set_covers(data):
    if len(data) == 0:
        return [[]]

    minimal_cover = []

    sets = compress_data(data)

    for curr_set in sets:
        other_sets_union = list_union([other_cover for other_cover in sets if other_cover != curr_set])
        l = [ind for ind in curr_set if ind not in other_sets_union]
        if len([ind for ind in curr_set if ind not in other_sets_union]) != 0:
            minimal_cover.append(curr_set)

    minimal_cover_union = list_union(minimal_cover)

    uncovered_elements = list_difference(sets, minimal_cover_union)

    if len(uncovered_elements) > 0:
        uncovered_elements.sort(reverse=True, key=(lambda x: len(x)))
        L = minimal_set_covers(list_difference(uncovered_elements, uncovered_elements[0]))
        I = list_concatenation([[[uncovered_elements[0], l] for l in L], [minimal_set_covers(uncovered_elements[1:])]])
        return [list_concatenation([i, minimal_cover]) for i in I]

    return [minimal_cover]


def make_simplex_matrix(data, g, ij):
    matrix = [[0 for i in range(2 * (g + 1) + (g + 1) ** 2 + 1)] for j in range((g + 1) ** 2 + 1)]

    for i in range(g + 1):
        for j in range(g + 1):
            matrix[i * (g + 1) + j][i] = 1
            matrix[i * (g + 1) + j][g + 1 + j] = 1

    for record in data:
        matrix[record["i"] * (g + 1) + record["j"]][2 * (g + 1) + (g + 1) ** 2] = record["minval"].value * (-1)

    for i in range((g + 1) ** 2):
        matrix[i][2 * (g + 1) + i] = -1

    for inds in ij:
        matrix[inds[0] * (g + 1) + inds[1]][2 * (g + 1) + inds[0] * (g + 1) + inds[1]] = 0

    for i in range(len(matrix[0])):
        tmp_sum = 0
        for j in range(len(matrix) - 1):
            tmp_sum += matrix[j][i]
        matrix[(g + 1) ** 2][i] = tmp_sum * (-1)

    return matrix


def find_pivot_column(matrix, matrix_rows, matrix_cols):
    best = 0
    best_i = False
    for i in range(matrix_cols - 1):
        t = matrix[matrix_rows - 1][i]
        if t < best:
            best = t
            best_i = i
    return best_i


def find_pivot_row(matrix, column, matrix_rows, matrix_cols):
    best_i = False
    best = float(inf)
    for i in range(matrix_rows - 1):
        a = matrix[i][column]
        b = matrix[i][matrix_cols - 1]
        if a > 0 and b / a < best:
            best_i = i
            best = b / a
    return best_i


def recalc(simplex_matrix, pivot_row, pivot_col, bs, ns, simplex_matrix_rows, simplex_matrix_cols):
    tmp = ns[pivot_col]
    ns[pivot_col] = bs[pivot_row]
    bs[pivot_row] = tmp

    for i in range(simplex_matrix_rows):
        for j in range(simplex_matrix_cols):
            if i != pivot_row and j != pivot_col:
                simplex_matrix[i][j] = simplex_matrix[i][j] - simplex_matrix[i][pivot_col] * simplex_matrix[pivot_row][
                    j] / simplex_matrix[pivot_row][pivot_col]

    for i in range(simplex_matrix_rows):
        if i != pivot_row:
            simplex_matrix[i][pivot_col] = -simplex_matrix[i][pivot_col] / simplex_matrix[pivot_row][pivot_col]

    for j in range(simplex_matrix_cols):
        if j != pivot_col:
            simplex_matrix[pivot_row][j] = simplex_matrix[pivot_row][j] / simplex_matrix[pivot_row][pivot_col]

    simplex_matrix[pivot_row][pivot_col] = 1 / simplex_matrix[pivot_row][pivot_col]


def simplex(simplex_matrix):
    simplex_matrix_rows = len(simplex_matrix)
    simplex_matrix_cols = len(simplex_matrix[0])
    bs = list(range(simplex_matrix_cols - 1, simplex_matrix_cols + simplex_matrix_rows - 2))
    ns = list(range(simplex_matrix_cols - 1))
    while True:
        pivot_col = find_pivot_column(simplex_matrix, simplex_matrix_rows, simplex_matrix_cols)
        if type(pivot_col) == bool and not pivot_col:
            break
        pivot_row = find_pivot_row(simplex_matrix, pivot_col, simplex_matrix_rows, simplex_matrix_cols)
        if type(pivot_col) == bool and not pivot_row:
            return False
        recalc(simplex_matrix, pivot_row, pivot_col, bs, ns, simplex_matrix_rows, simplex_matrix_cols)

    if simplex_matrix[simplex_matrix_rows - 1][simplex_matrix_cols - 1] != 0:
        return False

    result = [0.0] * (max(bs) + 1)

    for i in range(len(bs)):
        result[bs[i]] = simplex_matrix[i][simplex_matrix_cols - 1]
    return result


def is_zero_modulo(A, B):
    for (row_a, row_b) in zip(A.values, B.values):
        for (a, b) in zip(row_a, row_b):
            if a.value % b.value != 0:
                return False
    return True


def is_zero_matrix(A):
    if not isinstance(A, TropicalMatrix):
        return False
    for row_a in A.values:
        for a in row_a:
            if a.value != 0:
                return False
    return True
