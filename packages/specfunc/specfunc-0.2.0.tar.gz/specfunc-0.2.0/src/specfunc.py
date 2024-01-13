#! /usr/bin/env python
"""Python wrapper for special functions implemented in Fortran """

# Python imports
import os
import ctypes as ct

# Module imports
import numpy as np

fortlib = ct.CDLL(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'special_functions.so')
)


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
