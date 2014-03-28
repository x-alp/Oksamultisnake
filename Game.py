# -*- coding: utf-8 -*-
################################################################
##					Game.py
################################################################
# Classe Game: nécessite Player.py
#
# Antoine Courcelles, Marc Cerou,
# André Guimaraes-Duarte, Doina Leca


from Player import*

class Game:

	def __init__(self, nbPlayer, listPlayer, listName):
		self.listPlayer=[]
		self.nbPlayer=nbPlayer

		# création des bonus
		self.nbFood=1
		if nbPlayer>1:
			self.nbFood=nbPlayer-1

		self.listFood=[]

		for i in range(self.nbFood):
			new=[]
			new.append(random.randint(0, window_width))
			new.append(random.randint(0, window_height))
			self.listFood.append(new)

		# création des joueurs
		for i in range(nbPlayer):
			self.listPlayer.append(Player(listName[i], listPlayer[i], list_color[i], list_init[i]))
		

# Gère le Game over : si un joueur en mange un autre, return objet player fautif
	def gameOver_player(self):
		for player in self.listPlayer:
			head=player.coordinates[0]
			
			for player2 in self.listPlayer:
				if player!=player2:
					for case in player2.coordinates:
						if head==case:
							return player

		return 0

# Affichage du GAME OVER et du joueur en question
	def gameOver_stop(self, name, score):
		print "GAME OVER Joueur : "+str(name)+" Score : "+str(score)

# Met à jour le score du joueur s'il a mangé un bonus
	def upScore(self):
		for player in self.listPlayer:
			head=player.coordinates[0]

			for food in self.listFood:
				 #gere l'approximation head!=food
				if ((food[0]>head[0]-approxEat and food[0]<head[0]+approxEat) 
						and (food[1]>head[1]-approxEat and food[1]<head[1]+approxEat)):
						
					player.majScore()
					self.listFood.pop(self.listFood.index(food))
					new=[]
					new.append(random.randint(0, window_width))
					new.append(random.randint(0, window_height))
					self.listFood.append(new)
					break

# Jeu : met à jour le mouvement + score
# supprime le joueur s'il fait un GO
	def play(self):
		for player in self.listPlayer:
			game_over=0	
			player.movement()
			player.stayHere()
			self.upScore()
			
			if player.gameOver_lonely():
				self.gameOver_stop(player.name, player.score)
				self.listPlayer.pop(self.listPlayer.index(player))
				del(player)
				game_over=1
				
			player_GO=self.gameOver_player()
			if player_GO:
				self.gameOver_stop(player_GO.name, player.score)
				self.listPlayer.pop(self.listPlayer.index(player_GO))
				del(player_GO)
				game_over=1
			
			if game_over and len(self.listPlayer)==0:
				return 0

		return 1

# Formatage coordonnées Snake pour le reseau
	def prepareListSnake(self):
		listSnake=''
		
		for player in self.listPlayer:
			listSnake+=str(player.color)+'/'
			
			for case in player.coordinates:
				listSnake+=str(case[0])+':'+str(case[1])+','
				
			listSnake=listSnake[:-1]+';'
			
		listSnake=listSnake[:-1]
		return listSnake

# Formatage coordonnées Bonus pour le reseau
	def prepareListFood(self): 
		listFood=''
		
		for case in self.listFood:
			listFood+=str(case[0])+','+str(case[1])+';'
			
		listFood=listFood[:-1]
		return listFood
		
