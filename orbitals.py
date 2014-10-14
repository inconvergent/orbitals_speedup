#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy.random import random, randint
from numpy import zeros, sin, cos

class Orbitals(object):

  def __init__(self,num,stp,farl,nearl,friendship_ratio,
               friendship_initiate_prob,maxfs):

    self.num = num
    self.stp = stp
    self.farl = farl
    self.nearl = nearl
    self.friendship_ratio = friendship_ratio
    self.friendship_initiate_prob = friendship_initiate_prob
    self.maxfs = maxfs

    self.X = zeros(num,'float')
    self.Y = zeros(num,'float')
    self.R = zeros((num,num),'float')
    self.A = zeros((num,num),'float')
    self.F = zeros((num,num),'int')

  def make_friends(self,i):

    cand_num = self.F.sum(axis=1)

    maxfs = self.maxfs
    F = self.F

    if cand_num[i]>=maxfs:
      return

    cand_mask = cand_num<maxfs
    cand_mask[i] = 0
    cand_ind = cand_mask.nonzero()[0]

    cand_dist = self.R[i,cand_ind].flatten()
    cand_sorted_dist = cand_dist.argsort()
    cand_ind = cand_ind[cand_sorted_dist]

    cand_n = len(cand_ind)

    if cand_n<1:
      return

    for k in xrange(cand_n):

      if random()<self.friendship_ratio:

        j = cand_ind[k]
        F[[i,j],[j,i]] = 1
        return

  def init(self, rad):

    from numpy import pi

    for i in xrange(self.num):
      the = random()*pi*2
      phi = random()*pi*2
      x = rad * sin(the)
      y = rad * cos(the)
      self.X[i] = 0.5+x + cos(phi)*rad*0.05
      self.Y[i] = 0.5+y + sin(phi)*rad*0.05

  def step(self):

    from speedup.speedup import pyx_set_distances
    from speedup.speedup import pyx_iteration

    pyx_set_distances(self.X,self.Y,self.A,self.R,self.num)
    pyx_iteration(self.X,self.Y,self.A,self.R,self.F,self.num,
                  self.stp,self.farl,self.nearl)

    if random()<self.friendship_initiate_prob:

      k = randint(self.num)
      self.make_friends(k)

  def get_render_data(self):
    return self.X,self.Y,self.F,self.A,self.R


