#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

#np.random.seed(1)

COLOR_PATH = '../colors/dark_cyan_white_black.gif'
#COLOR_PATH = '../colors/shimmering.gif'

SIZE = 1080 # size of png image
NUM = 200 # number of nodes
MAXFS = 10 # max friendships pr node

BACK = [1,1,1,1] # background color
GRAINS = 10
ALPHA = 0.05 # opacity of drawn points

STP = 0.0001

RAD = 0.26 # radius of starting circle
FARL  = 0.13 # ignore "enemies" beyond this radius
NEARL = 0.02 # do not attempt to approach friends close than this

UPDATE_NUM = 35

FRIENDSHIP_RATIO = 0.1 # probability of friendship dens
FRIENDSHIP_INITIATE_PROB = 0.1 # probability of friendship initation attempt

print
print 'SIZE', SIZE
print 'NUM', NUM
print 'STP', STP
print
print 'MAXFS', MAXFS
print 'GRAINS', GRAINS
print 'COLOR_PATH', COLOR_PATH
print 'RAD', RAD
print 'FRIENDSHIP_RATIO', FRIENDSHIP_RATIO
print 'FRIENDSHIP_INITIATE_PROB', FRIENDSHIP_INITIATE_PROB
print


def main():

  #from time import time
  from render import Animate
  from orbitals import Orbitals
  from time import time


  orbitals = Orbitals(NUM,STP,FARL,NEARL,FRIENDSHIP_RATIO,
                      FRIENDSHIP_INITIATE_PROB,MAXFS)
  orbitals.init(RAD)

  def step_wrap(render):

    t1 = time()
    for i in xrange(UPDATE_NUM):
      orbitals.step()
      render.connections(*orbitals.get_render_data())
    t2 = time()

    print render.steps, t2-t1

    return True

  render = Animate(COLOR_PATH,BACK,ALPHA,GRAINS,SIZE, step_wrap)

  gtk.main()


if __name__ == '__main__' :

  if False:

    import pyximport
    pyximport.install()
    import pstats, cProfile

    fn = './profile/profile'
    cProfile.runctx("main()", globals(), locals(), fn)
    p = pstats.Stats(fn)
    p.strip_dirs().sort_stats('cumulative').print_stats()

  else:

    main()

