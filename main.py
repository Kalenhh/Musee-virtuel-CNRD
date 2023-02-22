#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *


class Myapp(ShowBase) :
	def __init__(self) :
		ShowBase.__init__(self)

		self.widget = []


	def clear(self) :
		for elt in self.widget :
			elt.destroy()

	def close_app(self) :
		self.finalizeExit()


	def show(self,tag,text) :
		self.tag = OnscreenText(text=text,scale=0.15,pos=(0,0.8,0))


app = MyApp()
app.show('first','sdfghjk')
app.run()