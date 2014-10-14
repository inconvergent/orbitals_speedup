#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import sin, cos, pi
from numpy.random import random

from itertools import count

from speedup.speedup import pyx_set_distances
from speedup.speedup import pyx_iteration

#np.random.seed(1)

COLOR_PATH = '../colors/dark_cyan_white_black.gif'
#COLOR_PATH = '../colors/shimmering.gif'

PI = pi
TWOPI = pi*2.

SIZE = 1080 # size of png image
NUM = 200 # number of nodes
MAXFS = 10 # max friendships pr node

BACK = [1,1,1,1] # background color
GRAINS = 5
ALPHA = 0.05 # opacity of drawn points

ONE = 1./SIZE
STP = ONE/15.

RAD = 0.26 # radius of starting circle
FARL  = 0.13 # ignore "enemies" beyond this radius
NEARL = 0.02 # do not attempt to approach friends close than this

UPDATE_NUM = 1000

FRIENDSHIP_RATIO = 0.1 # probability of friendship dens
FRIENDSHIP_INITIATE_PROB = 0.1 # probability of friendship initation attempt

FILENAME = './img/ff_c_num{:d}_fs{:d}_near{:2.4f}_far{:2.4f}_pa{:2.4f}_pb{:2.4f}'\
           .format(NUM,MAXFS,NEARL,FARL,\
                   FRIENDSHIP_RATIO,FRIENDSHIP_INITIATE_PROB)
FILENAME = FILENAME + '_itt{:05d}.png'

print
print 'SIZE', SIZE
print 'NUM', NUM
print 'STP', STP
print 'ONE', ONE
print
print 'MAXFS', MAXFS
print 'GRAINS', GRAINS
print 'COLOR_PATH', COLOR_PATH
print 'RAD', RAD
print 'FRIENDSHIP_RATIO', FRIENDSHIP_RATIO
print 'FRIENDSHIP_INITIATE_PROB', FRIENDSHIP_INITIATE_PROB
print

def make_friends(i,f,r, friendship_ratio, maxfs):

  cand_num = f.sum(axis=1)

  if cand_num[i]>=maxfs:
    return

  cand_mask = cand_num<maxfs
  cand_mask[i] = 0
  cand_ind = cand_mask.nonzero()[0]

  cand_dist = r[i,cand_ind].flatten()
  cand_sorted_dist = cand_dist.argsort()
  cand_ind = cand_ind[cand_sorted_dist]

  cand_n = len(cand_ind)

  if cand_n<1:
    return

  for k in xrange(cand_n):

    if random()<friendship_ratio:

      j = cand_ind[k]
      f[[i,j],[j,i]] = 1
      return

def init(xx,yy,rad):

  from numpy import pi

  for i in xrange(NUM):
    the = random()*pi*2
    phi = random()*pi*2
    x = rad * sin(the)
    y = rad * cos(the)
    xx[i] = 0.5+x + cos(phi)*rad*0.05
    yy[i] = 0.5+y + sin(phi)*rad*0.05

def step(xx,yy,aa,rr,ff,stp,farl,nearl,friendship_ratio,
         friendship_initiate_prob,maxfs):

  from numpy.random import randint

  num = len(xx)

  pyx_set_distances(xx,yy,aa,rr,num)
  pyx_iteration(xx,yy,aa,rr,ff,num,stp,farl,nearl)

  if random()<friendship_initiate_prob:

    k = randint(num)
    make_friends(k,ff,rr,friendship_ratio, maxfs)


def main():

  from numpy import zeros
  from time import time

  from render import Render

  render = Render(COLOR_PATH,BACK,ALPHA,GRAINS,SIZE)

  X = zeros(NUM,'float')
  Y = zeros(NUM,'float')
  R = zeros((NUM,NUM),'float')
  A = zeros((NUM,NUM),'float')
  F = zeros((NUM,NUM),'int')

  init(X,Y,RAD)

  render_connections = render.connections

  tcum = 0

  for itt in count():

    t1 = time()

    step(X,Y,A,R,F,STP,FARL,NEARL,FRIENDSHIP_RATIO,
         FRIENDSHIP_INITIATE_PROB,MAXFS)

    render_connections(X,Y,F,A,R)

    t2 = time()

    tcum += t2-t1

    if not (itt+1)%100:

      print itt, tcum
      tcum = 0

    if not (itt+1)%UPDATE_NUM:

      fn = FILENAME.format(itt+1)
      print fn
      render.sur.write_to_png(fn)


if __name__ == '__main__' :

  if False:

    import pstats, cProfile
    fn = './profile/profile'
    cProfile.run('main()',fn)
    p = pstats.Stats(fn)
    p.strip_dirs().sort_stats('cumulative').print_stats()

  else:

    main()

