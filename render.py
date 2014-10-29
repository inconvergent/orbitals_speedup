#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo
import gtk, gobject
from speedup.speedup import pyx_connections


class Render(object):

  def __init__(self,color_path,back,alpha,grains,size):

    self.color_path = color_path
    self.size = size
    self.back = back
    self.grains = grains
    self.one = 1./size
    self.alpha = alpha

    self.__init_cairo()
    self.__get_colors(color_path)

  def __init_cairo(self):

    sur = cairo.ImageSurface(cairo.FORMAT_ARGB32,self.size,self.size)
    ctx = cairo.Context(sur)
    ctx.scale(self.size,self.size)
    self.sur = sur
    self.ctx = ctx

    self.clear_canvas()

  def clear_canvas(self):

    self.ctx.set_source_rgba(*self.back)
    self.ctx.rectangle(0,0,1,1)
    self.ctx.fill()

  def __get_colors(self,f):

    import Image
    from numpy.random import shuffle

    scale = 1./255.
    im = Image.open(f)
    w,h = im.size
    rgbim = im.convert('RGB')
    res = []
    for i in xrange(0,w):
      for j in xrange(0,h):
        r,g,b = rgbim.getpixel((i,j))
        res.append((r*scale,g*scale,b*scale))

    shuffle(res)
    self.colors = tuple(res)
    self.n_colors = len(res)

  def connections_pyx(self,X,Y,F,A,R):

    # this is rather hacky. connections is better code, but this is
    # about twice as fast (on the configurations i tested), which is useful
    # for animations

    rectangle = self.ctx.rectangle
    fill = self.ctx.fill
    set_source_rgba = self.ctx.set_source_rgba
    from numpy.random import random

    num = len(X)

    pyx_connections(X,Y,F,A,R,num,self.one,self.colors,self.n_colors,self.alpha,
                    self.grains,fill,rectangle,set_source_rgba,random)

  def circles(self,X,Y,F,A,R,r):

    from numpy import pi

    #r = self.one*7.

    arc = self.ctx.arc
    fill = self.ctx.fill

    fnum = F.sum(axis=0)

    for x,y,f in zip(X,Y,fnum):
      arc(x,y,r,0,pi*2.)
      fill()

  def connections_lines(self,X,Y,F,A,R):

    move_to = self.ctx.move_to
    line_to = self.ctx.line_to
    stroke = self.ctx.stroke

    indsx,indsy = F.nonzero()
    mask = indsx >= indsy

    for i,j in zip(indsx[mask],indsy[mask]):
      move_to(X[i],Y[i])
      line_to(X[j],Y[j])
      stroke()

  def connections(self,X,Y,F,A,R):

    from numpy.random import random
    from numpy import sin, cos

    num = len(X)
    one = self.one

    rectangle = self.ctx.rectangle
    fill = self.ctx.fill
    set_source_rgba = self.ctx.set_source_rgba

    colors = self.colors
    n_colors = self.n_colors
    alpha = self.alpha
    grains = self.grains

    indsx,indsy = F.nonzero()
    mask = indsx >= indsy

    for i,j in zip(indsx[mask],indsy[mask]):
      a = A[i,j]
      d = R[i,j]
      scales = random(grains)*d
      xp = X[i] - scales*cos(a)
      yp = Y[i] - scales*sin(a)

      r,g,b = colors[ (i*num+j) % n_colors ]
      set_source_rgba(r,g,b,alpha)

      for x,y in zip(xp,yp):
        rectangle(x,y,one,one)
        fill()

class Animate(Render):

  def __init__(self,color_path,back,alpha,grains,size, step):

    Render.__init__(self, color_path, back,alpha, grains, size)

    window = gtk.Window()
    window.resize(self.size, self.size)

    self.step = step

    window.connect("destroy", self.__destroy)
    darea = gtk.DrawingArea()
    darea.connect("expose-event", self.expose)
    window.add(darea)
    window.show_all()

    self.darea = darea
    self.steps = 0

    gobject.idle_add(self.step_wrap)

  def __destroy(self,*args):

    gtk.main_quit(*args)

  def expose(self,*args):

    cr = self.darea.window.cairo_create()
    cr.set_source_surface(self.sur,0,0)
    cr.paint()

  def step_wrap(self):

    res = self.step(self)
    self.steps += 1
    self.expose()

    return res

