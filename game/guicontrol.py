#coding:utf-8
# Controle des éléments GUI

from panda3d.core import WindowProperties
from direct.gui.DirectGui import *


def hide_mouse(var) :
	"""
	Affiche le curseur ; True -> affiche , False -> cache
	"""

	assert isinstance(var,bool)
	
	props = WindowProperties()
	props.setCursorHidden(var)
	base.win.requestProperties(props)

class PauseMenu :

	def __init__(self) :

		hide_mouse(False)

		self.b_return = DirectButton(text='return',command=self.close_menu,scale=0.1)
		self.b_quit = DirectButton(text='destroy',command='destruire',scale=0.1,pos=(0,0,-0.2))
		self.b_config = DirectButton(text='config',command='config_menu',scale=0.1,pos=(0,0,-0.3))


	def close_menu(self) :
		"""
		Fermer le menu
		"""

		self.b_return.destroy()
		self.b_quit.destroy()
		self.b_config.destroy()
			
		hide_mouse(True)


	def destruire(self) :
		"""
		Fermer l'app
		"""
		self.finalizeExit()

	def config_menu(self) :
		"""
		Menu de parametre de configuration ex : vitesse de déplacement , FOV
		"""
		self.taskMgr.remove('move')
		self.taskMgr.remove('pause_menu')

		self.butt = DirectSlider(pos=(0,0,0.2),range=(0.1,2))

def onscreen() :
	return None