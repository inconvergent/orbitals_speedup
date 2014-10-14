#!/usr/bin/python
# -*- coding: utf-8 -*-

import cairo

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
    ctx.set_source_rgba(*self.back)
    ctx.rectangle(0,0,1,1)
    ctx.fill()

    self.sur = sur
    self.ctx = ctx

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
    self.colors = res
    self.n_colors = len(res)

  def connections(self,X,Y,F,A,R):

    from numpy.random import random
    from numpy import sin, cos

    num = len(X)
    one = self.one

    indsx,indsy = F.nonzero()
    mask = indsx >= indsy
    rectangle = self.ctx.rectangle
    fill = self.ctx.fill
    set_source_rgba = self.ctx.set_source_rgba

    colors = self.colors
    n_colors = self.n_colors
    alpha = self.alpha
    grains = self.grains

    for i,j in zip(indsx[mask],indsy[mask]):
      a = A[i,j]
      d = R[i,j]
      scales = random(grains)*d
      xp = X[i] - scales*cos(a)
      yp = Y[i] - scales*sin(a)

      r,g,b = colors[ (i+num+j) % n_colors ]
      set_source_rgba(r,g,b,alpha)

      for x,y in zip(xp,yp):
        rectangle(x,y,one,one)
        fill()

