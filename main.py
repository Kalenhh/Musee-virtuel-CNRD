#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import VBase4 , NodePath , TextNode

from direct.gui.OnscreenText import OnscreenText

from os import listdir
from os.path import isfile, join




class Myapp(ShowBase) :

	def __init__(self) :
		ShowBase.__init__(self)
		ShowBase.setBackgroundColor(self,r=255,g=255,b=255,a=0.0)

		self.widget = {}		# liste de widget ex : bouton , barre , input
		self.texte_liste = {} 	# Chaque element est un paragraphe de texte
		
		t1 = OnscreenText("0,0",pos=(0,0,0))
		t2 = OnscreenText("1,0",pos=(1,0,0))
		t3 = OnscreenText("-1,0",pos=(-1,0,0))  # ONSCREENTEXT    ( VERTICALE  ,  HORIZONTALE , INUTILE    )
		t4 = OnscreenText("0,1",pos=(0,1,0))

		self.load_menu()

		self.padding = 0.07
		self.k = 1
		self.c = 100
		self.taskMgr.add(self.loop,'loop')


	def loop(self,task) :

		is_down = base.mouseWatcherNode.is_button_down

		#print(ShowBase.get_size(self))
		print(self.padding,self.k,self.c)

		delta = 0
		if is_down('m') and self.texte_liste['end_balise']['pos'][1] <= 0 : #descendre
			delta = 0.01
		elif is_down('p') and self.texte_liste['start_balise']['pos'][1] >= 0 : #monter
			delta = -0.01

		if is_down('a') :
			self.c  += 0.1
			self.load_chapter(0)
			

		if is_down('q') :
			self.c -= 0.1
			self.load_chapter(0)
			

		if is_down('z') :
			self.k += 1
			self.load_chapter(0)
			

		if is_down('s') :
			self.k -= 1
			self.load_chapter(0)
			

		if is_down('e') :
			self.padding += 0.01
			self.load_chapter(0)
			

		if is_down('d') :
			self.padding -= 0.01
			self.load_chapter(0)
			


		if delta != 0 :
			for i in self.texte_liste :
				
				curr = self.texte_liste[i]

				if isinstance(curr,DirectButton) :
					curr.setPos(0,0,curr.getPos()[2]+delta)
					continue

				curr['pos'] = (curr['pos'][0], curr['pos'][1]+delta ,0)


		return Task.cont



# Clear fonctions -----------------
	def clear_widget(self) :
		for elt in self.widget :
			self.widget[elt].destroy()
		self.widget = {}

	def clear_text(self) :
		for elt in self.texte_liste :
			self.texte_liste[elt].destroy()
		self.texte_liste = {}
		

	def clear_all(self) :
		self.clear_widget()
		self.clear_text()

# --------------------------------

	def load_chapter(self,chap_id) :
		"""
		Charge le layout pour l'affichage d'un chapitre

		"""
		self.clear_all()

		with  open("chapitres/"+str(chap_id)+".txt",'r',encoding='utf-8') as chap :
			texte = chap.read()
			self.show(texte)


		self.widget['barre'] = DirectFrame(frameSize=(-5,5,0.8,2),frameColor=(0,0,0,255))
		self.widget['go_back_button'] = DirectButton(text="Retour",command=self.load_menu,scale=0.1,pos=(-1,0,0.9),frameSize=(-2,2,-0.5,0.9))


	def show(self,text) :
		"""
		borne 1 <
		borne 2 >
				texte
		borne 3 <
		borne 4 >

		"""

		self.texte_liste['start_balise'] = OnscreenText(text='',pos=(0,0,0))

		borne1 , borne2 , borne3 , borne4 = None , None , None , None

		para_nbr = 0

		next_ligne_pos = 0


		for i in range(len(text)) :
			
			if text[i] == '<' and borne1 is None :
				borne1 = i 
				continue
			
			elif text[i] == '>' and borne2 is None :
				borne2 = i
				continue

			elif text[i] == '<' and borne3 is None :
				borne3 = i
				continue

			elif text[i] == '>' and borne4 is None : # Un paragraphe est délimité
				borne4 = i 
					
				if text[borne1+1] != text[borne3+1] :
					raise Exception('Erreur dans le chapitre') # Erreur de mise en forme
				

				current_paragraphe , nbr_ligne = self.partitionner(text[borne2+1:borne3])

				if text[borne1+1] in ['1','2','3','4'] :
					scale = int(text[borne1+1])

					self.affiche(	current_paragraphe,
									para_nbr,
									scale,
									-next_ligne_pos)
				
				elif text[borne1+1] == 'i' :
					self.load_image(text[borne1+3:borne2],-next_ligne_pos,para_nbr+1)
					next_ligne_pos += 0.5*self.k  # TAILLE DE L4IMAGE

					self.texte_liste[str(para_nbr)] = OnscreenText(text="")

					para_nbr += 1
					self.affiche(current_paragraphe,
								para_nbr,
								1,
								-next_ligne_pos)
					self.texte_liste[str(para_nbr)]['pos'] = (	50,
																self.texte_liste[str(para_nbr)]['pos'][1],
																0 )


				next_ligne_pos += self.padding*nbr_ligne + scale/self.c*nbr_ligne



				para_nbr += 1
				borne1 , borne2 , borne3 , borne4 = None , None , None , None

		self.texte_liste['end_balise'] = OnscreenText(text='',pos=(0,-next_ligne_pos,0))



	def affiche(self,texte:str,name:int,scale:int,position:int) :
		"""
		Affiche du texte 
		texte : le texte a afficher
		name : le nom de l'objet contenant le texte
		scale : taille
		position : nombre négatif pour indiquer la position en Y du texte
		"""

		if scale > 1 :
			pos = TextNode.ACenter
			posx = 0
		else :
			pos = TextNode.ALeft
			posx = -1

		self.texte_liste[str(name)] = OnscreenText(	text = texte ,
														pos = (	posx ,
																position) ,
														scale = 0.05+scale/100 ,
														align = pos )


	def partitionner(self,string) :
		"""
		Met le texte dans un certain format
		texte : str raw de UN paragraphe

		sert surtout a partitionner un texte  (pour l'instant)
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


	def load_image(self,path,pos,args) :  # A REFAIRE
		self.texte_liste[str(path)] = DirectButton(image=str(path), pos=(0, 0,pos),scale=0.3,command=self.deplier,extraArgs=[args])
		print(self.texte_liste[str(path)]["frameSize"])

	def deplier(self,para_id) :
		return None





	def load_menu(self) :
		"""
		Affiche le menu principal de l'app
		"""

		self.clear_all()
		self.taskMgr.remove('loop')

		

		self.widget['chapitre_button'] = 	DirectButton(text="chapitre",command=self.load_chapter_menu,
										scale=0.1,pos=(0,0,-0.2),frameSize=(-2,2,-0.5,0.9))
		
		self.widget['exit_button'] = 		DirectButton(text="quitter",command=self.close_app,
										scale=0.1,pos=(0,0,-0.6),frameSize=(-2,2,-0.5,0.9))#left right bottom top
	

	def load_chapter_menu(self) :
		"""
		Menu pour selectionner un chapitre en particuler
		"""

		self.clear_all()

		onlyfiles = [f for f in listdir("chapitres") if isfile(join("chapitres", f))]
		print(onlyfiles)

		for i in range(len(onlyfiles)) :
			self.widget['button_chap'+str(i)] = DirectButton(	text=onlyfiles[i],scale=0.1,pos=(0,0,-0.2*i),
																frameSize=(-2,2,-0.5,0.9),
																command=self.load_chapter,extraArgs=[i] )


	def close_app(self) :
		"""
		Ferme l'app en sécurité
		"""
		self.finalizeExit()



app = Myapp()
app.run()