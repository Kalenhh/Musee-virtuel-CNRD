#coding:utf-8
# Controle des éléments GUI

from panda3d.core import WindowProperties

def hide_mouse(var) :
	"""
	Affiche le curseur ; True -> affiche , False -> cache
	"""

	assert isinstance(var,bool)
	
	props = WindowProperties()
	props.setCursorHidden(var)
	base.win.requestProperties(props)

