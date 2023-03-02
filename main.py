#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import VBase4



class Myapp(ShowBase) :
	def __init__(self) :
		ShowBase.__init__(self)
		ShowBase.setBackgroundColor(self,r=255,g=255,b=255,a=0.0)

		self.widget = []
		self.myframe = DirectScrolledFrame(canvasSize=(-2, 2, -2, 2), frameSize=(-.5, .5, -.5, .5))
		self.myframe.setPos(0, 0, 0)


	def clear(self) :
		for elt in self.widget :
			elt.destroy()

	def close_app(self) :
		self.finalizeExit()


	def show(self,tag,text) :
		self.tag = DirectLabel(parent=self.myframe,text=text,scale=0.15,pos=(0,0.8,0))


app = Myapp()
app.show('first','sdfghjk')
app.run()