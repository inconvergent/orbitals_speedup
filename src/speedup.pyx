# -*- coding: utf-8 -*-
# cython: profile=True

from __future__ import division

import numpy as np
cimport numpy as np
cimport cython

cdef float PI = np.pi

#from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from libc.math cimport cos
from libc.math cimport sin
from libc.math cimport atan2


# hack ahead ...

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
def pyx_connections(np.ndarray[double, mode="c",ndim=1] X,
                    np.ndarray[double, mode="c",ndim=1] Y,
                    np.ndarray[long, mode="c",ndim=2] F,
                    np.ndarray[double, mode="c",ndim=2] A,
                    np.ndarray[double, mode="c",ndim=2] R,
                    long num,
                    double one,
                    tuple colors,
                    long n_colors,
                    double alpha,
                    long grains,
                    fill,
                    rectangle,
                    set_source_rgba,
                    random):
  cdef int i
  cdef int j
  cdef int k
  cdef float a
  cdef float d
  cdef float s
  cdef float x
  cdef float y
  cdef tuple rgb


  cdef np.ndarray[double, mode="c",ndim=1] rnd

  for i in xrange(num):
    for j in xrange(i+1,num):

      if F[i,j]<1:
        continue

      a = A[i,j]
      d = R[i,j]

      rnd = random(grains)

      rgb = colors[ (i*num+j) % n_colors ]
      set_source_rgba(rgb[0],rgb[1],rgb[2],alpha)

      for k in xrange(grains):
        s = rnd[k]
        x = X[i] - d*s*cos(a)
        y = Y[i] - d*s*sin(a)
        rectangle(x,y,one,one)
        fill()

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def pyx_set_distances(np.ndarray[double, mode="c",ndim=1] X,
                      np.ndarray[double, mode="c",ndim=1] Y,
                      np.ndarray[double, mode="c",ndim=2] A,
                      np.ndarray[double, mode="c",ndim=2] R,
                      int num):

  cdef int i
  cdef int j
  cdef float dx
  cdef float dy
  cdef float x
  cdef float y
  cdef float a

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
      d = sqrt(dx*dx + dy*dy)

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
                  long num,
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

