#coding:utf-8
# Monde

from pandac.PandaModules import BitMask32


class Modele :
	"""
	Classe de définition du monde
	"""
	def __init__(self) :

		self.scene = loader.loadModel("design/test.gltf")

		self.scene.setTwoSided(True)
		self.scene.setScale(2)

		self.scene.reparentTo(render)
		self.scene.setCollideMask(1)

		self.scene.setPos(-8, 42, 0)

