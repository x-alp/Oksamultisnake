# -*- coding: utf-8 -*-

################################################################
##					Client.py
################################################################
# A lancer : python Client.py :> utilisation des paramètres par defaut
#	ip =127.0.0.1 port = 8000
#	sinon : python Client.py [-p port] [-ip ip]
#
# Antoine Courcelles, Marc Cerou,
# André Guimaraes-Duarte, Doina Leca

from Tkinter import *
from random import randrange
from socket import*
import sys
import threading
import time


# Paramètres réseaux par défaut
numPort=8000
ipConnect="127.0.0.1"


# Utilisation des paramètres non par défaut
if len(sys.argv)>1:
	for i in range(len(sys.argv)):
		if sys.argv[i]=='-ip':
			ipConnect=str(sys.argv[i+1])
		elif sys.argv[i]=='-p':
			numPort= int(sys.argv[i+1])


# Variable bool
global inMove
inMove=0
global inGame
inGame=0

#variable Thread
global listThreads
listThreads=[]


class Client:

	def __init__(self, pseudo):
		self.client=socket(AF_INET, SOCK_STREAM)
		self.client.connect((ipConnect, numPort))
		
		self.pseudo=pseudo
		self.client.sendall(pseudo)


# Initialisation détails graphique
		data=self.client.recv(10224)
		listDetailsGame=data.split(';')

		self.lenFood=int(listDetailsGame[0])
		self.colorFood=str(listDetailsGame[1])
		self.lenSnake=int(listDetailsGame[2])
		self.colorHead=str(listDetailsGame[3])
		self.window_width=int(listDetailsGame[4])
		self.window_height=int(listDetailsGame[5])

		self.nbRow=int(listDetailsGame[6])
		self.nbCol=int(listDetailsGame[7])
		self.nbColSpan=int(listDetailsGame[8])

# Choix de Jeu
		choice=raw_input(self.client.recv(10224))
		self.client.sendall(choice)
		
		rep=self.client.recv(10224)
		while rep!="GAMEON":
			rep=self.client.recv(10224)
		
		self.client.sendall("GO")

# Initialisation paramètres partie
		data=self.client.recv(10224)
		listDetails=data.split(';')		

		self.player_Color=str(listDetails[0])
		self.player_Name=str(listDetails[4])
		self.player_Number=int(listDetails[3])
		
		self.score=0

# Création graphique
		self.window=Tk()
		self.window.title("Oksa multisnake")
		self.can=Canvas(self.window, width = self.window_width, height = self.window_height , bg = 'gray')
		self.can.grid(row=self.nbRow,column=self.nbCol,columnspan=self.nbColSpan)

		Label(self.window, text='Nombre de joueur : '+str(self.player_Number)).grid(row=0, column=0)
		Label(self.window, text='Pseudo : '+str(self.player_Name)+" Couleur : "+self.player_Color).grid(row=1, column=0)
		Label(self.window, text='Score : '+str(self.score)).grid(row=0, column=1)




# Lance le jeu
	def startGame(self):
		Label(self.window, text='JEU EN COURS').grid(row=2, column=0)

		threadGO=threading.Thread(target=self.listenStart, name="threadGo")
		listThreads.append(threadGO)
		threadGO.start()

		self.bindCommand()
		self.window.mainloop()
		

################################################################
##					Fonctions affichage 

# Affichage des bonus
	def displayBonus(self,listCoord):
		for bonus in listCoord:
			self.can.create_oval(bonus[0],bonus[1], bonus[0]+self.lenFood, bonus[1]+self.lenFood, fill=self.colorFood)

# Affichage des serpents
	def displaySnake(self, listSnake):
		j=0
		for snake in listSnake:
			self.can.create_rectangle(snake[1][0], snake[1][1], snake[1][0]+self.lenSnake, snake[1][1]+self.lenSnake, fill=self.colorHead)
			for i in range(2,len(snake)):
				self.can.create_rectangle(snake[i][0], snake[i][1], snake[i][0]+self.lenSnake, snake[i][1]+self.lenSnake, fill=snake[0])
			
			# mise à jour du score : en fonction de la taille de notre serpent	
			if snake[0]==self.player_Color:
				self.score=len(snake)-2
			j+=1


################################################################
##					Fonctions Mouvement et Echange Réseau

#Lien touches clavier -> fonctions
	def bindCommand(self):
		self.can.bind_all('<Up>', self.move_up)
		self.can.bind_all('<Down>', self.move_down)
		self.can.bind_all('<Left>', self.move_left)
		self.can.bind_all('<Right>', self.move_right)
		self.can.bind_all('<space>', self.move_start)
		self.can.bind_all('p', self.move_stop)
		
	def move_stop(self, evt):
		global inMove
		global inGame
		
		# reprise de la pause
		if not inGame:
			Label(self.window, text='JEU EN COURS').grid(row=2, column=0)
			Label(self.window, text='').grid(row=3, column=0)
			self.sendEvt('p0')
			inGame=1	
		
		# pause
		else:
			Label(self.window, text='JEU EN PAUSE').grid(row=2, column=0)
			Label(self.window, text='JEU EN PAUSE').grid(row=3, column=0)
			self.sendEvt('p0')
			inGame=0
			

	def move_start(self, evt):
		global inMove
		
		# Début du jeu
		if inMove==0:
			Label(self.window, text='JEU EN COURS').grid(row=2, column=0)
			Label(self.window, text='').grid(row=3, column=0)
			self.sendEvt('s0')
			inMove=1		
	
		# Fin du jeu
		else:
			self.sendEvt('q0')
			inMove=0
			listThreads[-1].join()
			listThreads[0].join()
			self.window.destroy()	
			

	def move_up(self, evt):
		self.sendMvt('m1')

	def move_right(self, evt):
		self.sendMvt('m2')

	def move_down(self, evt):
		self.sendMvt('m3')

	def move_left(self, evt):
		self.sendMvt('m4')

################################################################
##					Fonction JEU

# Receptionne les données et lance l'affichage
	def game(self):
		global inMove
		global inGame
		inMove=1
		inGame=1
		

		while inMove:
			data=self.client.recv(10224)
			listData=data.split('_')

			if listData[0]=="data" and verifBadReception(listData[1:], 'data'):
				self.can = Canvas(self.window, width = self.window_width, height = self.window_height , bg = 'gray')
				self.can.grid(row=self.nbRow,column=self.nbCol,columnspan=self.nbColSpan)

				listBonus=parseDataBonus(listData[1])
				self.displayBonus(listBonus)
				listSnake=parseDataSnake(listData[2])
				self.displaySnake(listSnake)
				
				Label(self.window, text='\n  Score : '+str(self.score)).grid(row=0, column=1)

			elif listData[0]=="stop":
				Label(self.window, text=str(listData[1])).grid(row=3, column=0)	


################################################################
##					Fonctions réseau
################################################################


#Envoie le mouvement au serveur
	def sendMvt(self, evt):
		dataToSend="mvt_"+evt
		self.client.sendall(dataToSend)

#Envoie l'évement au serveur	
	def sendEvt(self, evt):
		dataToSend="evt_"+evt
		self.client.sendall(dataToSend)

#Lance le jeu quand reception de start
	def listenStart(self):
		data=self.client.recv(10224)
		if data=="START":
			threadGame=threading.Thread(target=self.game, name="threadGame")
			listThreads.append(threadGame)
			threadGame.start()


################################################################
##					Fonctions parsing
################################################################

# Verifie l'intégrité des données
def verifBadReception(liste, motif):
	for sousListe in liste:
		if motif in sousListe:
			return 0
	return 1

# Chaine de caractères -> liste Bonus, template "x,y;x1,y1;x2,y2"
def parseDataBonus(data): 
	listBonus=[]
	
	for obj in data.split(';'):
		listBonus.append(map(int, obj.split(',')))

	return listBonus

# Chaine de caractères -> liste Snake; template : "color/tx,ty:x,y:x1,y1:x2,y2;tx,ty,x,y,x1,y1,x2,y2"
def parseDataSnake(data): 
	listSnake=[]

	for obj in data.split(';'):
		listInter=[]
		listInterR=obj.split('/')
		listInter.append(listInterR[0])
		for coord in listInterR[1].split(','):
			listInter.append(map(int,coord.split(':')))
		listSnake.append(listInter)
	
	return listSnake

# Chaine de caractères -> liste details
def parseDetails(data):	
	listDetails=[]

	for obj in data.split(';'):
		listDetails.append(obj)

	return listDetails	
	
# Fonction debug 
def displayThread():
	global listThreads
	
	print 'Nb Thread : ',len(listThreads)	
	for t in listThreads:
		print t.name, 'actif : ',t.isAlive()
		
	
################################################################
##					MAIN
################################################################

msg="Bienvenue sur notre super Jeu\n"
msg+="Quel est votre pseudo ?\n"
pseudo=raw_input(msg)		

objet_client=Client(pseudo)
objet_client.startGame()
rep=int(raw_input("La partie est finie !\nVoulez-vous rejouez ?\n0) Non\n1) Oui\n"))
while rep:
	del(objet_client)
	objet_client=Client(pseudo)
	objet_client.startGame()
	rep=int(raw_input("La partie est finie !\nVoulez-vous rejouez ?\n0) Non\n1) Oui\n"))


