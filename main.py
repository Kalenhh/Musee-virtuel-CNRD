#coding:utf-8
# main.py

from math import pi, sin, cos , radians

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3 ,WindowProperties, CollisionRay , CollisionNode , CollisionHandlerFloor , CollisionTraverser , NodePath
from direct.gui.DirectGui import *
from pandac.PandaModules import BitMask32

from game.monde import Modele


class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		base.disableMouse()
		props = WindowProperties()
		props.setCursorHidden(True)
		base.win.requestProperties(props)
		
		base.cTrav = CollisionTraverser()
		base.cTrav.setRespectPrevTransform(1)

		self.scene = Modele()


		self.pandaActor = NodePath('pandaActor')

		self.panda = Actor("models/panda-model",
								{"walk": "models/panda-walk4"})

		self.panda.setScale(0.005, 0.005, 0.005)
		self.panda.reparentTo(self.pandaActor)

		self.pandaActor.reparentTo(self.render)
		
		self.pandaActor.setZ(10)


		self.panda.loop("walk")

		self.taskMgr.add(self.move,'move')
		self.taskMgr.add(self.pause_menu,'pause_menu')

		self.camLens.setFov(80)

		# COLLISION ----------------------------------

 				# IMPORTANT




		self.footRay = CollisionRay(0, 0, 1, 0, 0, -1)
		self.playerFootRay = self.pandaActor.attachNewNode(CollisionNode("playerFootCollision"))
		self.playerFootRay.node().addSolid(self.footRay)
		

		self.playerFootRay.node().setFromCollideMask(1)

		self.lifter = CollisionHandlerFloor()
		self.lifter.addCollider(self.playerFootRay, self.pandaActor)
		self.lifter.setOffset(1.0)
		self.lifter.setMaxVelocity(5.0)
		self.lifter.setReach(1.0)


		base.cTrav.addCollider(self.playerFootRay, self.lifter)


		#-----------------------------------------------------------------------------------------------


		#####


		# -------------------------------------------------


	def move(self,task) :

		print(self.pandaActor.getZ(),self.panda.getZ())

		speed = 0.3
		camera_sensi = 25
		jump = 2

		is_down = base.mouseWatcherNode.is_button_down

		if is_down('z') :

			self.pandaActor.setX(   self.pandaActor.getX()+( cos(radians(self.pandaActor.getH()-90))*speed  )  )
			self.pandaActor.setY(   self.pandaActor.getY()+( sin(radians(self.pandaActor.getH()-90))*speed  )  )
		
		if is_down('s') :

			self.pandaActor.setX(   self.pandaActor.getX()-( cos(radians(self.pandaActor.getH()-90))*speed  )  )
			self.pandaActor.setY(   self.pandaActor.getY()-( sin(radians(self.pandaActor.getH()-90))*speed  )  )

		if is_down('q') :
			self.pandaActor.setX(   self.pandaActor.getX()+( cos(radians(self.pandaActor.getH()))*speed  )  )
			self.pandaActor.setY(   self.pandaActor.getY()+( sin(radians(self.pandaActor.getH()))*speed  )  )

		if is_down('d') :
			self.pandaActor.setX(   self.pandaActor.getX()-( cos(radians(self.pandaActor.getH()))*speed  )  )
			self.pandaActor.setY(   self.pandaActor.getY()-( sin(radians(self.pandaActor.getH()))*speed  )  )

		if is_down('j') :
			self.pandaActor.setZ(10)

		x,y = 0,0
		if base.mouseWatcherNode.hasMouse():
			x = round(base.mouseWatcherNode.getMouseX() , 2 )
			y = round(base.mouseWatcherNode.getMouseY() , 2 )
			props = base.win.getProperties()
			base.win.movePointer(0,props.getXSize() // 2,props.getYSize() // 2)
		
		x,y = x*camera_sensi,y*camera_sensi

		self.camera.setPos(self.pandaActor.getX(),self.pandaActor.getY(),self.pandaActor.getZ()+3.5)
		
		self.camera.setH(self.camera.getH()-x)
		self.pandaActor.setH(self.camera.getH()-180)

		self.camera.setP(self.camera.getP()+y)

		return Task.cont

	def closer(self) :
		self.b.destroy()
		self.bert.destroy()
		self.taskMgr.add(self.move,'move')
		self.taskMgr.add(self.pause_menu,'pause_menu')
		props = WindowProperties()
		props.setCursorHidden(True)
		base.win.requestProperties(props)
		return

	def destruire(self) :
		self.finalizeExit()


	def pause_menu(self,task) :

		is_down = base.mouseWatcherNode.is_button_down

		if is_down('p') :
			taskMgr.remove('move')
			props = WindowProperties()
			props.setCursorHidden(False)
			base.win.requestProperties(props)	

			self.b = DirectButton(text='return',command=self.closer,scale=0.1)

			self.bert = DirectButton(text='destroy',command=self.destruire,scale=0.1,pos=(0,0,-0.2))

			self.taskMgr.remove('pause_menu')
			return Task.cont

		return Task.cont

app = MyApp()
app.run()