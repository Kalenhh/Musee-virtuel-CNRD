#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import VBase4 , NodePath , TextNode

from direct.gui.OnscreenText import OnscreenText




class Myapp(ShowBase) :

	def __init__(self) :
		ShowBase.__init__(self)
		ShowBase.setBackgroundColor(self,r=255,g=255,b=255,a=0.0)

		self.widget = []		# liste de widget ex : bouton , barre , input
		self.texte_liste = {} 	# Chaque element est un paragraphe de texte

		self.padding = 0.07

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
		self.nbr_ligne = 0
		

	def clear_all(self) :
		self.clear_widget()
		self.clear_text()

# --------------------------------

	def show(self,text) :
		borne1 = None
		borne2 = None
		chap_nbr = 0

		next_ligne_pos = 0

		for i in range(len(text)-2) :
			if text[i] =='<' and text[i+2] == '>' :


				if borne1 is None :
					borne1 = i +3 
				elif borne2 is None :
					borne2 = i-1
					
					if text[borne1-2] != text[borne2+2] :
						raise Exception("erreur dans le chapitre")
					else :

						formated_text,nbr_ligne2 = self.format(text[borne1:borne2+1])
						chap_nbr += 1
						
						if int(text[borne1-2]) > 1 :
							pos = TextNode.ACenter
							posx = 0
						else :
							pos = TextNode.ALeft
							posx = -1

						self.texte_liste[str(chap_nbr)] = OnscreenText(	text = formated_text ,
																		pos = (	posx ,
																				-next_ligne_pos) ,
																		scale = 0.05+int(text[borne1-2])/100 ,
																		align = pos )
						
						next_ligne_pos += self.padding*nbr_ligne2+int(text[borne1-2])/100*nbr_ligne2

						borne1 , borne2 = None , None
		
		for i in range(int(round(self.nbr_ligne,0))) :
			self.texte_liste[i] = OnscreenText(text="-----------",pos=(-1,-i/10))


	def load_image(self,path) :  # A REFAIRE
		self.texte_liste[str(path)+str(len(self.texte_liste))] = DirectButton(image=str(path), pos=(0, 0,-self.nbr_ligne/10),scale=0.3)



	def format(self,string) :
		"""
		Met le texte dans un certain format
		texte : str raw de UN paragraphe
		scale : taille du texte -> pour ajuster le nombre de caractere par ligne selon la taille de la fenetre bh ui

		le texte formaté doit tenir dans le cadre visible 

		sert surtout a partitionner un texte en chaine plus petite (pour l'instant)
		"""
		
		string = string.replace('\n',' ')
		
		formated_text = ""
		max_char = 70
		c = 0 

		nbr_ligne = 0

		for i in string :
			if len(string) <= max_char :
				formated_text+=string+"\n"
				nbr_ligne += 1
				break
			if c > max_char and string[c] == ' ' :  
				formated_text += string[:c]+"\n"
				string = string[c:]
				c = 0 
				nbr_ligne+= 1
			c+= 1

		return formated_text , nbr_ligne

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
				
				curr = self.texte_liste[i]
				if isinstance(curr,OnscreenImage) :
					curr['pos'] = (curr['pos'][0],0, curr['pos'][2]+delta)
					continue
				elif isinstance(curr,DirectButton) :
					curr.setPos(0,0,curr.getPos()[2]+delta)
					continue

				curr['pos'] = (curr['pos'][0], curr['pos'][1]+delta ,0)

		if is_down('t') :
			self.padding += 0.01 
			self.load_chapter(1)
		if is_down('g') :
			self.padding -= 0.01
			self.load_chapter(1)

		print(self.padding)
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

		self.texte_liste['go_back_button'] = DirectButton(text="Retour",command=self.load_menu,scale=0.1,pos=(-1,0,0),frameSize=(-2,2,-0.5,0.9))

		with  open(str(chap_id)+".txt",'r',encoding='utf-8') as chap :
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