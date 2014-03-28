# -*- coding: utf-8 -*-

################################################################
##					Player.py
################################################################
# Classe Player : nécessite initialisation.py
#
# Antoine Courcelles, Marc Cerou,
# André Guimaraes-Duarte, Doina Leca

import random
from Initialisation import*

class Player:

	def __init__(self, name, id_player, color, coord_init):
		
		self.name=name
		self.id_player=id_player
		self.color=color
		self.score=0
		self.direction=random.sample(list_direction, 1)[0]
	
		self.coordinates=[]
		self.coordinates.append(coord_init[0])
		self.coordinates.append(coord_init[1])

# met à jour le mouvement du serpent
	def movement(self): 
		new=[]

		if self.direction=='m1':  # up
			new.append(self.coordinates[0][0])
			new.append(self.coordinates[0][1]-lenSnake)


		elif self.direction=='m2': # rigth
			new.append(self.coordinates[0][0]+lenSnake)
			new.append(self.coordinates[0][1])
	
		elif self.direction=='m3': # down
			new.append(self.coordinates[0][0])
			new.append(self.coordinates[0][1]+lenSnake)
		
		else:	# left
			new.append(self.coordinates[0][0]-lenSnake)
			new.append(self.coordinates[0][1])
			
		self.coordinates.pop(-1)
		self.coordinates.insert(0, new)
	
# met à jour la direction du joueur
	def majDirection(self, newDirection):
		if newDirection!=self.direction:
			if not (newDirection=='m3' and self.direction=='m1') and not (newDirection=='m1' and self.direction=='m3'):
				if not (newDirection=='m2' and self.direction=='m4') and not (newDirection=='m4' and self.direction=='m2'):		
					self.direction=newDirection

# met à jour le score : ajout d'une case
	def majScore(self):
		self.score+=1
		new=[]

		if self.direction=='m1':  # up
			new.append(self.coordinates[-1][0])
			new.append(self.coordinates[-1][1]+lenSnake)

		elif self.direction=='m2': # rigth
			new.append(self.coordinates[-1][0]-lenSnake)
			new.append(self.coordinates[-1][1])
	
		elif self.direction=='m3': # down
			new.append(self.coordinates[-1][0])
			new.append(self.coordinates[-1][1]-lenSnake)
		
		else:	# left
			new.append(self.coordinates[-1][0]+lenSnake)
			new.append(self.coordinates[-1][1])
		
		self.coordinates.append(new)

# Gere le tor : on reste dans le cadre de la fenetre
	def stayHere(self):
		head=self.coordinates[0]

		if head[0] > window_height:
			head[0]=0
		elif head[0] < 0:
			head[0]=window_height
		
		if head[1] > window_width:
			head[1]=0
		elif head[1]< 0:
			head[1]=window_width


# Gere le game over du joueur : ne pas se mordre la queue, return 1 == GO
	def gameOver_lonely(self):
		head=self.coordinates[0]	
	
		for i in range(1, len(self.coordinates)):
			if head==self.coordinates[i]:
				return 1




