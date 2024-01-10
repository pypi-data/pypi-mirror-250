"""
all functions whose name contains _problem
will be tested by test_problems.py

they should define
- data: a numpy array
- and either
    - solutions: a set of tuples describing all the solutions
    - or first_solutions: a set of tuples describing the first expected solutions
"""

import numpy as np
import pandas as pd

DTYPE_FOR_ARRAY = bool


def knuth_original_problem():
    to_cover = np.array(
        [
            [0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 1],
        ]
    )
    return dict(
        data=to_cover,
        solutions={
            (0, 3, 4),
        },
    )


# https://en.wikipedia.org/wiki/Exact_cover#Detailed_example
def detailed_wikipedia_problem():
    sets = [
        {1, 4, 7},
        {1, 4},  # <- 1
        {4, 5, 7},
        {3, 5, 6},  # <- 3
        {2, 3, 6, 7},
        {2, 7},  # <- 5
    ]
    return dict(
        data=np.array(
            [[1 if i in s else 0 for i in range(1, 8)] for s in sets],
            dtype=DTYPE_FOR_ARRAY,
        ),
        solutions={(1, 3, 5)},
    )


def bruteforce_problem1():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions={(0, 1, 2), (3, 4, 5)}
    )


def bruteforce_problem2():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions={
            (0, 1, 2),
            (0, 1, 8),
            (0, 7, 2),
            (0, 7, 8),
            (4, 5, 3),
            (6, 1, 2),
            (6, 1, 8),
            (6, 7, 2),
            (6, 7, 8),
        },
    )


def bruteforce_problem3():
    to_cover = [
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
        [1, 0, 0, 1, 0, 0, 1, 0],  # <- sol1
        [0, 1, 0, 0, 1, 0, 0, 1],  # <- sol1
        [0, 0, 1, 0, 0, 1, 0, 0],  # <- sol1
        [0, 0, 0, 1, 0, 0, 0, 0],  # <- sol2
        [1, 0, 1, 0, 1, 0, 0, 1],  # <- sol2
        [0, 1, 0, 0, 0, 1, 1, 0],  # <- sol2
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions={
            (0, 1, 2),
            (0, 1, 8),
            (0, 7, 2),
            (0, 7, 8),
            (4, 5, 3),
            (4, 5, 9),
            (4, 11, 3),
            (4, 11, 9),
            (6, 1, 2),
            (6, 1, 8),
            (6, 7, 2),
            (6, 7, 8),
            (10, 5, 3),
            (10, 5, 9),
            (10, 11, 3),
            (10, 11, 9),
        },
    )


def bruteforce3_with_odd_zero_rows_problem():
    p = bruteforce_problem3()
    d, s = p['data'], p['solutions']
    r, c = d.shape
    # add same area of 0s on the right hand side of d
    d1 = np.hstack((d, np.zeros(d.shape, dtype=d.dtype)))
    # reshape it - each gets folded in 2
    # so we end up with all the odd rows being 0
    d2 = d1.reshape((-1, c))
    # non empty rows are now 0 2 4, so twice the original index
    s = { tuple(map(lambda i: i*2, t)) for t in s }
    return dict(data=d2, solutions=s)

def bruteforce3_with_odd_zero_rows_problem():
    p = bruteforce_problem3()
    d, s = p['data'], p['solutions']
    r, c = d.shape
    # add same area of 0s on the left hand side of d
    d1 = np.hstack((np.zeros(d.shape, dtype=d.dtype), d))
    # reshape it - each gets folded in 2
    # so we end up with all the even rows being 0
    d2 = d1.reshape((-1, c))
    # non empty rows are now 1 3 5, so twice the original index + 1
    s = { tuple(map(lambda i: i*2+1, t)) for t in s }
    return dict(data=d2, solutions=s)


# problem originally based on solving the trivial problem
# of arranging 2 identical triminos on a 3x3 board

#    +--+
#    |  |
# +--+--+
# |  |  |
# +--+--+

# +--+--+--+
# |xx|  |xx|
# +--+--+--+
# |  |  |  |
# +--+--+--+
# |xx|  |  |
# +--+--+--+


# this problem has 2 solutions
# (5, 13) and (6, 12)
def small_trimino_problem():
    to_cover = [
        [1, 0, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0],  # <- 5
        [1, 0, 0, 0, 0, 1, 1, 1],  # <- 6
        [0, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 1],
        [0, 1, 1, 1, 1, 0, 0, 0],  # <- 12
        [0, 1, 0, 0, 0, 1, 1, 1],  # <- 13
    ]
    return dict(
        data=np.array(to_cover, dtype=DTYPE_FOR_ARRAY),
        solutions={(5, 13), (6, 12)},
    )


def small_trimino_problem_from_file():
    return dict(
        data=np.load("tests/data/small_trimino.npy"),
        solutions={(5, 13), (6, 12)},
    )


def pentomino_chessboard_problem():
    to_cover = pd.read_csv("tests/data/pentominos-chessboard.csv", sep=" ").to_numpy()
    return dict(
        data=to_cover,
        first_solutions=[
            [26, 172, 213, 444, 1545, 1284, 963, 720, 1380, 1118, 496, 1482, 1101],
            [26, 172, 350, 496, 1162, 1545, 729, 1492, 1429, 1110, 1278, 856, 311],
            [26, 172, 350, 496, 1263, 1468, 728, 339, 1193, 1523, 1406, 1105, 900],
            [26, 172, 350, 978, 1263, 1173, 582, 276, 1423, 906, 1499, 794, 1545],
            [26, 172, 350, 978, 1263, 1173, 1468, 728, 339, 1399, 933, 617, 1551],
            [26, 172, 490, 421, 755, 1218, 1347, 1288, 965, 300, 978, 1528, 1452],
            [26, 172, 490, 421, 755, 1268, 898, 978, 1452, 1383, 1239, 346, 1541],
            [26, 172, 490, 1545, 700, 1037, 430, 1143, 1366, 1492, 1283, 961, 300],
            [26, 172, 490, 1545, 978, 676, 430, 1143, 1366, 1492, 1283, 961, 300],
            [26, 172, 689, 444, 1493, 1104, 1189, 1259, 855, 1530, 1407, 622, 340],
            [26, 172, 689, 1268, 912, 645, 483, 1500, 328, 1062, 1312, 1121, 1522],
            [26, 172, 689, 1268, 912, 645, 483, 1551, 328, 1312, 1121, 1464, 1080],
            [26, 172, 842, 421, 755, 547, 1541, 346, 1239, 1277, 1332, 978, 1452],
            [26, 172, 974, 1162, 1545, 811, 1266, 1382, 1500, 611, 729, 469, 343],
            [26, 172, 1304, 645, 1509, 1500, 276, 702, 1051, 959, 369, 1280, 1143],
            [26, 172, 1304, 1493, 341, 444, 782, 610, 1110, 1509, 1271, 907, 1131],
            [26, 172, 1304, 1545, 855, 985, 726, 300, 610, 485, 1492, 1275, 1143],
            [26, 172, 1434, 444, 645, 214, 830, 1333, 1275, 1212, 1542, 771, 1062],
            [26, 172, 1434, 444, 645, 214, 830, 1333, 1275, 1212, 1542, 790, 1110],
            [26, 172, 1434, 1268, 421, 1414, 925, 1193, 515, 218, 699, 1079, 1551],
        ])


# not enabled for now
# def pentomino_5_12_problem():
def pentomino_5_12_problem():
    to_cover = pd.read_csv("tests/data/pentominos-5-12.csv").to_numpy()
    return dict(
        data=to_cover,
        first_solutions=[
            [1555, 350, 140, 286, 1244, 1357, 1143, 637, 1875, 1541, 1804, 870],
            [1555, 350, 140, 669, 1368, 1244, 1053, 258, 952, 1935, 1511, 1698],
            [1555, 350, 140, 669, 1368, 1244, 1053, 258, 1804, 1875, 1511, 826],
            [1555, 350, 140, 821, 1244, 257, 706, 1127, 1793, 1541, 1861, 1339],
            [1555, 350, 140, 821, 1244, 609, 259, 1063, 1696, 1451, 1895, 1373],
            [1555, 350, 140, 821, 1244, 1409, 289, 1891, 1511, 1614, 581, 1127],
            [1555, 350, 140, 821, 1244, 1705, 1063, 672, 291, 1481, 1383, 1865],
            [1555, 350, 140, 1100, 255, 771, 1479, 1696, 647, 1825, 1373, 1229],
            [1555, 350, 140, 1100, 255, 1418, 1195, 637, 1875, 1541, 1804, 870],
            [1555, 350, 140, 1100, 255, 1418, 1696, 1299, 647, 1825, 1552, 861],
            [1555, 350, 140, 1100, 255, 1713, 1548, 928, 732, 1273, 1412, 1825],
            [1555, 350, 140, 1100, 549, 771, 1790, 1510, 258, 1825, 1373, 1229],
            [1555, 350, 140, 1100, 1467, 1225, 730, 1705, 827, 1823, 251, 1352],
            [1555, 350, 140, 1100, 1467, 1225, 730, 1705, 1372, 251, 1923, 797],
            [1555, 350, 140, 1100, 1467, 1225, 1369, 609, 1613, 251, 1834, 827],
            [1555, 350, 140, 1100, 1467, 1225, 1369, 1705, 251, 705, 1834, 827],
            [1555, 350, 140, 1693, 1244, 662, 907, 1842, 291, 1471, 1097, 1383],
            [1555, 350, 140, 1693, 1244, 662, 907, 1842, 291, 1471, 1147, 1363],
            [1555, 350, 140, 1693, 1244, 1092, 1851, 673, 1372, 251, 1442, 869],
            [1555, 350, 140, 1693, 1244, 1092, 1851, 673, 1372, 251, 1531, 983],
    ])
