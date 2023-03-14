#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import VBase4 , NodePath

from direct.gui.OnscreenText import OnscreenText




class Myapp(ShowBase) :

	def __init__(self) :
		ShowBase.__init__(self)
		ShowBase.setBackgroundColor(self,r=255,g=255,b=255,a=0.0)

		self.widget = []		# liste de widget ex : bouton , barre , input
		self.texte_liste = {} 	# Chaque element est une ligne de texte

		self.taskMgr.add(self.loop,'loop')

		t1 = OnscreenText("0,0",pos=(0,0,0))
		t2 = OnscreenText("1,0",pos=(1,0,0))
		t3 = OnscreenText("-1,0",pos=(-1,0,0))
		t4 = OnscreenText("0,1",pos=(0,1,0))

		self.load_menu()

# Clear fonctions -----------------
	def clear_widget(self) :
		for elt in self.widget :
			elt.destroy()
		self.widget = []

	def clear_text(self) :
		for elt in self.texte_liste :
			self.texte_liste[elt].destroy()
		self.texte_liste = {}
		

	def clear_all(self) :
		self.clear_widget()
		self.clear_text()

# --------------------------------

	def show(self,text,position=0) :
		borne1 = None
		borne2 = None
		chap_nbr = 0

		for i in range(len(text)-2) :
			if text[i] =='<' and text[i+2] == '>' :


				if borne1 is None :
					borne1 = i +3 
				elif borne2 is None :
					borne2 = i-1
					
					if text[borne1-2] != text[borne2+2] :
						raise Exception("erreur dans le chapitre")
					else :

						formated_text = self.format(text[borne1:borne2+1])
						chap_nbr += 1
						
						for o in range(len(formated_text)) :

							self.texte_liste[str(chap_nbr)+str(o)] = OnscreenText(	
																					text=formated_text[o],
																					pos=(	
																							0,
																							-len(self.texte_liste)/10,
																							0
																						),
																					scale= 0.05+int(text[borne1-2])/100)
							print(self.texte_liste[str(chap_nbr)+str(o)]['frameSize'])

						self.texte_liste[str(chap_nbr)+"n"] = OnscreenText(text="",pos=(0,-len(self.texte_liste)/10,0))
						borne1 , borne2 = None , None

	def format(self,texte) :
		"""
		Met le texte dans un certain format
		texte : str raw de UN paragraphe
		scale : taille du texte -> pour ajuster le nombre de caractere par ligne selon la taille de la fenetre bh ui

		le texte formaté doit tenir dans le cadre visible 

		sert surtout a partitionner un texte en chaine plus petite (pour l'instant)
		"""

		nbr_cara = 70
		formated_text = []

		texte = texte.replace('\n',' ')


		c = 0
		i = 0
		
		while True :
			if len(texte) < nbr_cara :
				formated_text.append(texte)
				break
			elif i > nbr_cara and texte[i] == ' ' :
				formated_text.append(texte[:i])
				texte = texte[i:]
				i = 0
			i += 1

		return formated_text # liste de ligne de longueur inferieure à 'nbr_cara'

	def loop(self,task) :

		is_down = base.mouseWatcherNode.is_button_down

		#print(ShowBase.get_size(self))

		delta = 0
		if is_down('m') :
			delta = 0.01
		elif is_down('p') :
			delta = -0.01

		if delta != 0 :
			for i in self.texte_liste :

				self.texte_liste[i]['pos'] = (self.texte_liste[i]['pos'][0], self.texte_liste[i]['pos'][1]+delta ,0)

		return Task.cont

	def load_menu(self) :
		self.clear_all()
		
		start_button = 		DirectButton(text="Lire",command=self.load_chapter,extraArgs=[1],
										scale=0.1,pos=(0,0,0),frameSize=(-2,2,-0.5,0.9))

		chapitre_button = 	DirectButton(text="chapitre",command=self.load_chapter_menu,
										scale=0.1,pos=(0,0,-0.2),frameSize=(-2,2,-0.5,0.9))
		
		param_button = 		DirectButton(text="param",command=self.load_param_menu,
										scale=0.1,pos=(0,0,-0.4),frameSize=(-2,2,-0.5,0.9))
		
		exit_button = 		DirectButton(text="quitter",command=self.close_app,
										scale=0.1,pos=(0,0,-0.6),frameSize=(-2,2,-0.5,0.9))#left right bottom top
	
		self.widget.append(start_button)
		self.widget.append(chapitre_button)
		self.widget.append(param_button)
		self.widget.append(exit_button)

	def load_chapter_menu(self) :
		"""
		Menu pour selectionner un chapitre en particuler
		"""
		self.clear_all()
		self.load_chapter(1)

	def load_chapter(self,chap_id) :
		"""
		affiche un chapitre
		"""
		self.clear_all()

		self.widget.append(go_back_button:=DirectButton(text="Retour",command=self.load_menu,scale=0.1,pos=(-1,0,0),frameSize=(-2,2,-0.5,0.9)))

		with  open(str(chap_id)+".txt",'r') as chap :
			texte = chap.read()
			self.show(texte)

	def load_param_menu(self) :
		"""
		Menu pour changer les parametres
		"""
		self.clear_all()






	def close_app(self) :
		self.finalizeExit()



app = Myapp()
app.run()