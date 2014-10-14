#!/usr/bin/python
# -*- coding: utf-8 -*-

#np.random.seed(1)

COLOR_PATH = '../colors/dark_cyan_white_black.gif'
#COLOR_PATH = '../colors/shimmering.gif'

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
           .format(NUM,MAXFS,NEARL,FARL,
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


def main():

  from time import time
  from itertools import count

  from render import Render
  from orbitals import Orbitals

  render = Render(COLOR_PATH,BACK,ALPHA,GRAINS,SIZE)

  orbitals = Orbitals(NUM,STP,FARL,NEARL,FRIENDSHIP_RATIO,
                      FRIENDSHIP_INITIATE_PROB,MAXFS)
  orbitals.init(RAD)

  render_connections = render.connections

  tcum = 0

  for itt in count():

    t1 = time()

    orbitals.step()
    render_connections(*orbitals.get_render_data())

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

  if True:

    import pstats, cProfile
    fn = './profile/profile'
    cProfile.run('main()',fn)
    p = pstats.Stats(fn)
    p.strip_dirs().sort_stats('cumulative').print_stats()

  else:

    main()

