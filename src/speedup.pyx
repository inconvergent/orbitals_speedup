# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np
cimport numpy as np
cimport cython

cdef double PI = np.pi

#from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from libc.math cimport pow
from libc.math cimport cos
from libc.math cimport sin
from libc.math cimport atan2

int = np.int
ctypedef np.int_t int_t
double = np.double
ctypedef np.double_t double_t

cdef inline double norm(double a, double b):
  cdef double dd = sqrt(pow(a,2)+pow(b,2))
  return dd

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def pyx_set_distances(np.ndarray[double, mode="c",ndim=1] X,
                      np.ndarray[double, mode="c",ndim=1] Y,
                      np.ndarray[double, mode="c",ndim=2] A,
                      np.ndarray[double, mode="c",ndim=2] R,
                      int num):
  cdef double dx
  cdef double dy
  cdef double x
  cdef double y
  cdef double a

  for i in xrange(num):
    x = X[i]
    y = Y[i]
    for j in xrange(i,num):
      if i==j:
        A[i,j] = 0.
        R[i,j] = 0.
        continue

      dx = x-X[j]
      dy = y-Y[j]
      d = norm(dx,dy)

      A[i,j] = atan2(dy,dx)
      A[j,i] = atan2(-dy,-dx)
      R[i,j] = d

      R[j,i] = d

  return

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def pyx_iteration(np.ndarray[double, mode="c",ndim=1] X,
                  np.ndarray[double, mode="c",ndim=1] Y,
                  np.ndarray[double, mode="c",ndim=2] A,
                  np.ndarray[double, mode="c",ndim=2] R,
                  np.ndarray[long, mode="c",ndim=2] F,
                  np.ndarray[double, mode="c",ndim=1] SX,
                  np.ndarray[double, mode="c",ndim=1] SY,
                  int num,
                  float stp,
                  float farl,
                  float nearl):
  cdef float d
  cdef float a
  cdef float dx
  cdef float dy
  cdef int i
  cdef int j

  SX[:] = 0.
  SY[:] = 0.

  for i in xrange(num):
    for j in xrange(num):

      if i == j:
        continue

      d = R[i,j]
      a = A[i,j]
      dx = cos(a)
      dy = sin(a)

      if F[i,j]>0:
        if d<nearl:
          SX[j] -= dx*(farl-d)
          SY[j] -= dy*(farl-d)
        else:
          SX[j] += dx
          SY[j] += dy
      else:
        if d<farl:
          SX[j] -= dx*(farl-d)
          SY[j] -= dy*(farl-d)

  for i in xrange(num):
    X[i] += SX[i]*stp
    Y[i] += SY[i]*stp

  return

