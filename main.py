#coding:utf-8
# main.py

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import VBase4 , NodePath , TextNode

from direct.gui.OnscreenText import OnscreenText

import struct
import imghdr

def get_image_size(fname):
	'''Determine the image type of fhandle and return its size.
	from draco'''
	with open(fname, 'rb') as fhandle:
		head = fhandle.read(24)
		if len(head) != 24:
			return
		if imghdr.what(fname) == 'png':
			check = struct.unpack('>i', head[4:8])[0]
			if check != 0x0d0a1a0a:
				return
			width, height = struct.unpack('>ii', head[16:24])
		elif imghdr.what(fname) == 'gif':
			width, height = struct.unpack('<HH', head[6:10])
		elif imghdr.what(fname) == 'jpeg':
			try:
				fhandle.seek(0) # Read 0xff next
				size = 2
				ftype = 0
				while not 0xc0 <= ftype <= 0xcf:
					fhandle.seek(size, 1)
					byte = fhandle.read(1)
					while ord(byte) == 0xff:
						byte = fhandle.read(1)
					ftype = ord(byte)
					size = struct.unpack('>H', fhandle.read(2))[0] - 2
				# We are at a SOFn block
				fhandle.seek(1, 1)  # Skip `precision' byte.
				height, width = struct.unpack('>HH', fhandle.read(4))
			except Exception: #IGNORE:W0703
				return
		else:
			return
		return width, height



class Myapp(ShowBase) :

	def __init__(self) :
		ShowBase.__init__(self)
		ShowBase.setBackgroundColor(self,r=255,g=255,b=255,a=0.0)

		self.widget = {}		# liste de widget ex : bouton , barre , input  TRUC FIXES / GUI
		self.texte_liste = {} 	# Chaque element est un paragraphe de texte   TRUC PAS FIXES 

		self.load_menu()

		self.padding = 0.06
		self.k = 1.19
		self.c = 0.06

		self.music_time = 0

		self.taskMgr.add(self.loop,'loop')



	def loop(self,task) :

		is_down = base.mouseWatcherNode.is_button_down

		#print(ShowBase.get_size(self))
		print(self.padding,self.k,self.c)

		delta = 0
		if is_down('m') and self.texte_liste['end_balise']['pos'][1] <= 0 : #descendre
			delta = 0.04
		elif is_down('p') and self.texte_liste['start_balise']['pos'][1] >= 0 : #monter
			delta = -0.04

		if is_down('a') :
			self.c  += 0.001
			self.load_chapter(1)
			

		if is_down('q') :
			self.c -= 0.001
			self.load_chapter(1)
			

		if is_down('z') :
			self.k += 0.01
			self.load_chapter(1)
			

		if is_down('s') :
			self.k -= 0.01
			self.load_chapter(1)
			

		if is_down('e') :
			self.padding += 0.01
			self.load_chapter(1)
			

		if is_down('d') :
			self.padding -= 0.01
			self.load_chapter(1)
			


		if delta != 0 :
			print("mouv")
			for i in self.texte_liste :
				
				curr = self.texte_liste[i]

				if isinstance(curr,DirectButton) :
					curr.setPos(curr.getPos()[0],0,curr.getPos()[2]+delta)
					continue

				elif isinstance(curr,OnscreenImage) :
					curr['pos'] = (curr['pos'][0], 0 , curr['pos'][2]+delta)
					continue

				curr['pos'] = (curr['pos'][0], curr['pos'][1]+delta ,0)  # ONSCREENTEXT


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
			self.show(texte,chap_id)



		# WIDGET GUI PART ------------------------------------------------------------------------------------
		self.widget['barre'] = DirectFrame(frameSize=(-5,5,0.825,2),frameColor=(206/255,6/255,6/255,1))  # 206,6,6,255
		self.widget['go_back_button'] = DirectButton(text="Retour",command=self.load_menu,scale=0.1,pos=(-1,0,0.9),frameSize=(-2,2,-0.5,0.9))


		self.mySound = base.loader.loadSfx(f"sound/{chap_id}.wav")
		self.mySound.setVolume(0.5)

		self.widget["playsound_button"] = DirectButton(text="musique",command=self.musique,
														scale=0.1,pos=(0.8,0,0.9),frameSize=(-2,2,-0.5,0.9))

		self.widget["vol_plus_button"] = DirectButton(text="+",command = lambda : self.mySound.setVolume(self.mySound.getVolume()+0.1) ,
														scale=0.1,pos=(1.1,0,0.9),frameSize=(-0.7,0.7,-0.5,0.9))

		self.widget["vol_moins_button"] = DirectButton(text="-",command =lambda : self.mySound.setVolume(self.mySound.getVolume()-0.1)  ,
														scale=0.1,pos=(0.5,0,0.9),frameSize=(-0.7,0.7,-0.5,0.9))

		# ---------------------------------------------------------------------------------------------------------


	def musique(self) :
		print(self.mySound.status())
		if self.mySound.status() == self.mySound.PLAYING :
			self.music_time = self.mySound.getTime()
			self.mySound.stop()
		else :
			self.mySound.play()
			self.mySound.setTime(self.music_time)
			self.mySound.play()

			self.music_time = 0



	def show(self,text,chap_id) :
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

				
				# ---------------------------------------------------------
				if text[borne1+1] in ['1','2','3','4'] :
					scale = int(text[borne1+1])

					self.affiche(	current_paragraphe,
									para_nbr,
									scale,
									-next_ligne_pos)

					if text[borne1+1] == "3" :
						next_ligne_pos += 1

					next_ligne_pos += self.padding*nbr_ligne + scale*self.c*nbr_ligne


				elif text[borne1+1] == 'i' :  # IMAGE

					path = f"images/{chap_id}{text[borne1+3:borne2]}.png"
					im = get_image_size(path)
				
					next_ligne_pos += im[1]/im[0]*self.k
					self.texte_liste[path] = OnscreenImage(image=path, pos=(0,0,-next_ligne_pos),scale=(1,0,1*im[1]/im[0]))
					next_ligne_pos += im[1]/im[0]*self.k



					# -----------------------------------------------------------------


				

				# ---------------------------------------------------------


				para_nbr += 1
				borne1 , borne2 , borne3 , borne4 = None , None , None , None



		self.texte_liste['end_balise'] = OnscreenText(text='',pos=(0,-next_ligne_pos,0))

		if chap_id < 7 : # NOMBRE DE CHAP MAX
			self.texte_liste['next_chap_button'] = DirectButton(text='Next',pos=(1,0,-next_ligne_pos-0.3),
															command = self.load_chapter,extraArgs=[chap_id+1],
															scale=0.1)

		if chap_id > 1 : # NOMBRE DE CHAP MINI
			self.texte_liste['prev_chap_button'] = DirectButton(text='prev',pos=(-1,0,-next_ligne_pos-0.3),
															command = self.load_chapter,extraArgs=[chap_id-1],
															scale=0.1)


	def affiche(self,texte:str,name:int,scale:int,position:int) :
		"""
		Affiche du texte 
		texte : le texte a afficher
		name : le nom de l'objet contenant le texte
		scale : taille
		position : nombre négatif pour indiquer la position en Y du texte
		"""

		framme = (0,0,0,0)
		if scale > 1 :
			pos = TextNode.ACenter
			posx = 0
		else :
			pos = TextNode.ALeft
			posx = -1

		if scale == 2 :
			framme = (0,0,0,255)

		self.texte_liste[str(name)] = OnscreenText(	text = texte ,
														pos = (	posx ,
																position) ,
														scale = 0.05+scale/100 ,
														align = pos ,
														frame=framme)


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
	
		for i in range(len(string)) :

			c += 1

			if string[i] == " " and c > max_char :
				string = string[:i] + "\n" + string[i+1:]
				c = 0
				nbr_ligne+= 1 

		return string, nbr_ligne


	def load_menu(self) :
		"""
		Affiche le menu principal de l'app
		"""

		self.clear_all()

		

		self.widget['chapitre_button'] = 	DirectButton(text="chapitre",command=self.load_chapter_menu,
										scale=0.1,pos=(0,0,-0.2),frameSize=(-2,2,-0.5,0.9))
		
		self.widget['exit_button'] = 		DirectButton(text="quitter",command=self.close_app,
										scale=0.1,pos=(0,0,-0.6),frameSize=(-2,2,-0.5,0.9))#left right bottom top


		texte = 'CNRD BOUTET'
		self.texte_liste['titre'] = OnscreenText(		text = texte ,
														pos = (	0 ,
																0.5) ,
														scale = 0.05+6/100)

		texte = "Une personne\ndeux personnes\ntrois persernne\nquatre personne"
		self.texte_liste['texte_pres'] = OnscreenText(	text = texte ,
														pos = (	-1 ,
																0) ,
														scale = 0.05+3/100 ,
														align = TextNode.ALeft)
	

	def load_chapter_menu(self) :
		"""
		Menu pour selectionner un chapitre en particuler
		"""

		name = {1:"Exode et Défaite",
				2:"Mise au pas de l'école",
				3:"vichy : un état repressif",
				4:"Résistance",
				5:"Libération",
				6:"Epilogue",
				7:"Sources"}

		self.clear_all()


		for i in range(7) :
			self.widget['button_chap'+str(i+1)] = DirectButton(	text=name[i+1],scale=0.1,pos=(0,0,-0.2*i+0.5),
																frameSize=(-5.8,5.8,-0.5,0.9),
																command=self.load_chapter,extraArgs=[i+1] )

		self.widget['return_button'] = DirectButton(text="Retour",command=self.load_menu,scale=0.1,pos=(-1,0,0.9),frameSize=(-2,2,-0.5,0.9))



	def close_app(self) :
		"""
		Ferme l'app en sécurité
		"""
		self.finalizeExit()



app = Myapp()
app.run()