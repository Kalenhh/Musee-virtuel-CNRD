#coding:utf-8
# main.py

from math import pi, sin, cos , radians

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3 ,WindowProperties, CollisionSphere, CollisionHandlerQueue, CollisionHandlerPusher, CollisionSegment, CollisionRay , CollisionNode , CollisionHandlerFloor , CollisionTraverser , NodePath
from direct.gui.DirectGui import *
from pandac.PandaModules import BitMask32

from game.monde import Modele
from game.guicontrol import hide_mouse


class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		base.disableMouse()

		hide_mouse(True)
		
		base.cTrav = CollisionTraverser()
		base.cTrav.setRespectPrevTransform(1)

		self.scene = Modele()


		self.objNP = NodePath('objNP')

		self.obj = loader.loadModel("design/tableau.gltf")
		self.obj.reparentTo(self.objNP)

		self.objNP.reparentTo(render)


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
		self.taskMgr.add(self.pickertask,'pickertask')

		self.camLens.setFov(80)

		base.setBackgroundColor(r=100,g=100,b=250,a=0.5)

		# COLLISION ----------------------------------

		if True :
			self.footRay = CollisionRay(0, 0, 1, 0, 0, -1)
			self.playerFootRay = self.pandaActor.attachNewNode(CollisionNode("playerFootCollision"))
			self.playerFootRay.node().addSolid(self.footRay)
			

			self.playerFootRay.node().setFromCollideMask(1)
			self.playerFootRay.node().setIntoCollideMask(0)

			self.lifter = CollisionHandlerFloor()
			self.lifter.addCollider(self.playerFootRay, self.pandaActor)
			self.lifter.setOffset(1.0)
			self.lifter.setMaxVelocity(5.0)
			self.lifter.setReach(1.0)


			base.cTrav.addCollider(self.playerFootRay, self.lifter)
		# ------------------------------------------------------------------------------------------------------
			self.myHandler = CollisionHandlerQueue()

			self.pickerNode = CollisionNode('mouseRay')
			self.pickerNP = self.camera.attachNewNode(self.pickerNode)
			self.pickerRay = CollisionSegment(0,0,0,5,0,0)
			self.pickerNode.setIntoCollideMask(0)
			self.pickerNode.addSolid(self.pickerRay)

			self.pickerNode.setFromCollideMask(2)

			self.obj.setCollideMask(2)

			self.obj.setPos(x=0,y=0,z=10)
			
			base.cTrav.addCollider(self.pickerNP, self.myHandler)

			self.pickerNP.show()  # Collision
			# ---------------------------------------------------------------------------------------------------

			self.pusher = CollisionHandlerPusher()

			self.pandafrom = self.pandaActor.attachNewNode(CollisionNode('pusherNode'))
			self.pandafrom.node().addSolid(CollisionSphere(0,0,0,0.5))

			self.pandafrom.node().setFromCollideMask(1)
			self.pandafrom.node().setIntoCollideMask(0)

			self.pusher.addCollider(self.pandafrom,self.pandaActor)

			base.cTrav.addCollider(self.pandafrom,self.pusher)



###
	"""	def myFunction():
		    mpos = base.mouseWatcherNode.getMouse()
		    pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
		    myTraverser.traverse(render)
		    # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
		    if myHandler.getNumEntries() > 0:
		        # This is so we get the closest object.
		        myHandler.sortEntries()
		        pickedObj = myHandler.getEntry(0).getIntoNodePath()
		        pickedObj = pickedObj.findNetTag('myObjectTag')
		        if not pickedObj.isEmpty():
		            handlePickedObject(pickedObj)"""

###
	def pickertask(self,task) :

		#self.pickerRay.setPointA(self.pandaActor.getPos())  # FAUT REGLER CETTE DIABLERIE
		#self.pickerRay.setPointB(self.objNP.getPos())
		self.pickerRay.setFromLens(base.camNode,0,0)		# LAD IABLERIE EST REGLE


		if self.myHandler.getNumEntries() > 0 :
			
			self.myHandler.sortEntries()

			picked = self.myHandler.getEntry(0)
			pol = picked.getSurfacePoint(NodePath(base.camera))


			if pol[1] < 15 :
				print("                 coli")
		else :
			print("non")

		#print(self.pickerRay.getPointA(),self.pickerRay.getPointB())


		return Task.cont


	def move(self,task) :

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

		self.camera.setH(self.camera.getH()-x)
		
		getp = self.camera.getP() + y
		if getp > (-60) and getp < 90 :
			self.camera.setP(getp)

		self.camera.setPos(self.pandaActor.getX(),self.pandaActor.getY(),self.pandaActor.getZ()+3.5)
		self.pandaActor.setH(self.camera.getH()-180)
		return Task.cont

	
	def closer(self) :
		"""
		Fermer le menu
		"""
		self.b.destroy()
		self.bert.destroy()
		self.taskMgr.add(self.move,'move')
		self.taskMgr.add(self.pause_menu,'pause_menu')
		
		hide_mouse(True)

		return

	def destruire(self) :
		"""
		Fermer l'app
		"""
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



app = MyApp()	# Main object
app.run()