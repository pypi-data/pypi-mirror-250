#! /usr/bin/env python
"""Python wrapper for Fortran confluent hypergeometric functions"""

# Python imports
import os
import ctypes as ct

# Module imports
import numpy as np

fortlib = ct.CDLL(os.path.join(os.getcwd(), 'special_functions.so'))


def gammaln(x):
    """Computes ln(gamma(x))."""

    N = ct.c_int(x.size)
    x = np.asfortranarray(x, dtype=np.float64)
    x_ptr = x.ctypes.data_as(ct.POINTER(ct.c_double))
    lg = np.asfortranarray(np.ones_like(x))
    lg_ptr = lg.ctypes.data_as(ct.POINTER(ct.c_double))

    fortlib.gammaln(x_ptr, lg_ptr, N)

    return lg


def hyp1f1(a, b, z):
    """Confluent hypergeometric function."""

    N = ct.c_int(a.size)
    kf = ct.c_int(1)
    a_c = np.asfortranarray(a, dtype=np.float64)
    b_c = np.asfortranarray(b, dtype=np.float64)
    zr = np.asfortranarray(z, dtype=np.float64)
    zc = np.asfortranarray(np.zeros_like(z), dtype=np.float64)

    chgr = np.asfortranarray(np.zeros_like(z), dtype=np.float64)
    chgc = np.asfortranarray(np.zeros_like(z), dtype=np.float64)

    fortlib.hyp1f1(
        a_c.ctypes.data_as(ct.POINTER(ct.c_double)),
        b_c.ctypes.data_as(ct.POINTER(ct.c_double)),
        zr.ctypes.data_as(ct.POINTER(ct.c_double)),
        zc.ctypes.data_as(ct.POINTER(ct.c_double)),
        chgr.ctypes.data_as(ct.POINTER(ct.c_double)),
        chgc.ctypes.data_as(ct.POINTER(ct.c_double)),
        N,
        kf,
    )

    return chgr


def hyp1f1ln(a, b, z):
    """Logarithm of confluent hypergeometric function."""

    N = ct.c_int(a.size)
    kf = ct.c_int(0)
    a_c = np.asfortranarray(a, dtype=np.float64)
    b_c = np.asfortranarray(b, dtype=np.float64)
    zr = np.asfortranarray(z, dtype=np.float64)
    zc = np.asfortranarray(np.zeros_like(z), dtype=np.float64)

    chgr = np.asfortranarray(np.zeros_like(z), dtype=np.float64)
    chgc = np.asfortranarray(np.zeros_like(z), dtype=np.float64)

    fortlib.hyp1f1(
        a_c.ctypes.data_as(ct.POINTER(ct.c_double)),
        b_c.ctypes.data_as(ct.POINTER(ct.c_double)),
        zr.ctypes.data_as(ct.POINTER(ct.c_double)),
        zc.ctypes.data_as(ct.POINTER(ct.c_double)),
        chgr.ctypes.data_as(ct.POINTER(ct.c_double)),
        chgc.ctypes.data_as(ct.POINTER(ct.c_double)),
        N,
        kf,
    )

    return chgr


if __name__ == "__main__":

    print("ln(gamma(x)):")
    gammaln_known = np.array([
        0, 0, 0.693147, 1.791759, 3.178054, 4.787492, 6.579251, 8.525161,
    ])
    x = np.arange(0, gammaln_known.size).reshape(1, -1) + 1
    glx = gammaln(x)
    print("Input\tKnown\t\tPredicted\n")
    for i in range(x.size):
        print(f"{x[0, i]}:\t{gammaln_known[i]:.6f}\t{glx[0, i]:.6f}")

    print("\nhyp1f1(a, b, z):")
    a = np.array([1, 10, 10, 100, 12]).reshape(1, -1)
    b = np.array([1, 1, 10, 10, 14]).reshape(1, -1)
    z = np.array([1, 10, 10, 1, 0.4]).reshape(1, -1)
    hyp1f1_known = np.array([
        2.718282,
        8514625477,
        22026.47,
        2486.218,
        1.409877,
    ])
    hgfv = hyp1f1(a, b, z)
    print("Input\t\tKnown\t\tPredicted\n")
    for i in range(a.size):
        print(f"({a[0, i]},{b[0, i]},{z[0, i]}):\t{hyp1f1_known[i]:.9}\t{hgfv[0,i]:.9}")

    print("\nhyp1f1ln(a, b, z):")
    hyp1f1ln_known = np.array([
        1,
        22.86505,
        10,
        7.818518,
        0.3435025,
    ])
    lhgfv = hyp1f1ln(a, b, z)
    print("Input\t\tKnown\t\tPredicted\n")
    for i in range(a.size):
        print(f"({a[0, i]},{b[0, i]},{z[0, i]}):\t{hyp1f1ln_known[i]:.7f}\t{lhgfv[0,i]:.7f}")
