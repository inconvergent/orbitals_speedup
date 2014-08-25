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
                  int num,
                  float stp,
                  float farl,
                  float nearl):
  cdef float d
  cdef float a
  cdef float dx
  cdef float dy
  cdef float sx
  cdef float sy
  cdef float speed
  cdef int i
  cdef int j

  for i in xrange(num):
    sx = 0.
    sy = 0.
    for j in xrange(num):

      if i == j:
        continue

      d = R[i,j]
      a = A[i,j]
      dx = cos(a)
      dy = sin(a)

      if F[i,j]>0:
        if d<nearl:
          speed = farl-d
          sx += dx*speed
          sy += dy*speed
        else:
          sx -= dx
          sy -= dy
      else:
        if d<farl:
          speed = farl-d
          sx += dx*speed
          sy += dy*speed

    X[i] += sx*stp
    Y[i] += sy*stp

  return

