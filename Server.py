# -*- coding: utf-8 -*-

################################################################
##					Server.py
################################################################
# A lancer : python Server.py :> utilisation des paramètres par defaut
#	ip =127.0.0.1 port = 8000
#	sinon : python Server.py [-p port] [-ip ip]
#
# Antoine Courcelles, Marc Cerou,
# André Guimaraes-Duarte, Doina Leca


from socket import*
import sys
import threading
import time
from Game import*


# Utilisation des paramètres non par défaut
if len(sys.argv)>1:
	for i in range(len(sys.argv)):
		if sys.argv[i]=='-ip':
			ipConnect=str(sys.argv[i+1])
		elif sys.argv[i]=='-p':
			numPort= int(sys.argv[i+1])


# Création du server
global server
server=socket(AF_INET, SOCK_STREAM)
server.bind(("", numPort))
server.listen(3)

# Liste des Threads
global listThreads
listThreads=[]

# Objet jeu
global objet_jeu
# Variable bool
global inGame
inGame=0

global dicoScore
dicoScore={}

#variable de fin
global stopSendGame
stopSendGame=True

global stopRecptDirection
stopRecptDirection=True

global stopBoolServ
stopBoolServ = True



################################################################
##					FONCTION RESEAUX
################################################################

# Envoie à tous les clients les scores de la partie
def sendScore():
	msg='stop_Partie Terminée\nVoici les scores :\n'
	for pseudo, liste in dicoScore.iteritems():
		msg+=pseudo+' : '+str(liste[1])+'\n'
	broadcast(msg)
	

# Envoie à tous les clients le message
def broadcast(msg):
	listeClient=[elem[0] for elem in dicoScore.values()]
	for player in listeClient:
		player.sendall(msg)
		
# Receptionne et met à jour les changements de direction des joueurs (fct multithreadée)
def recptDirection(player):
	global inGame
	global stopRecptDirection
	global stopSendGame
	global threadGame
	global objet_jeu
		

	while stopRecptDirection:
		data=player.id_player.recv(10224)
		listData=data.split('_')
		
		if listData[0]=="evt":
			# Debut du jeu
			if listData[1]=="s0" and not threadGame.isAlive():
				broadcast("START")
				threadGame.start()
				inGame=1	

			# Arret de la partie
			elif listData[1]=="q0":				
				stopSendGame=False
				threadGame.join()
				stopRecptDirection=False
			
			# debut pause
			elif listData[1]=="p0" and inGame and threadGame.isAlive():
				inGame=0
				stopSendGame=False
				threadGame.join()				
				
			# reprise pause
			elif listData[1]=="p0" and not inGame:
				inGame=1
				stopSendGame=True
				threadGame=threading.Thread(target=sendGame, name="threadNewGame")
				listThreads.append(threadGame)
				threadGame.start()
		
		# mise à jour de la direction du joueur
		elif listData[0]=="mvt":			
			player.majDirection(listData[1])

		
# Envoi au début du jeu les détails de la partie
def sendDetail():
	for player in objet_jeu.listPlayer:
		msg=player.color+';'+str(window_width)+';'+str(window_height)+';'+str(len(objet_jeu.listPlayer))+';'+player.name
		player.id_player.sendall(msg)

# Envoi les paramètres généraux
def sendVar(client):
	msg=str(lenFood)+';'+colorFood+';'+str(lenSnake)+';'+str(colorHead)+';'+str(window_width)+';'+str(window_height)+';'
	msg+=str(nbRow)+';'+str(nbCol)+';'+str(nbColSpan)
	client.sendall(msg)

# Envoie et met à jour à tous les pas de temps les coordonnées 
def sendGame():
	global inGame
	global stopSendGame
	global objet_jeu

	repJeu=objet_jeu.play()
	while repJeu and stopSendGame: # on boucle tant qu'il n'y a pas de game over

		dataToSend="data_"+objet_jeu.prepareListFood()+"_"+objet_jeu.prepareListSnake()		
		for player in objet_jeu.listPlayer: 
			player.id_player.sendall(dataToSend)
			dicoScore[player.name][1]=player.score
		
		repJeu=objet_jeu.play()			
		time.sleep(pdt)
	
	# si Game Over, on affiche la partie	
	if not repJeu:
		sendScore()

	inGame=0
	
# Fonction principale	
def playGame():
	global inGame
	global objet_jeu
	
	print "Debut partie"
	
	# Initialisation des clients
	while not inGame:

		(client, adr)=server.accept()

		pseudo=str(client.recv(10224))
		dicoScore[pseudo]=[client,0]

		sendVar(client)

		msg="Vous êtes : "+str(len(dicoScore))+" actuellement sur le jeu\n"
		msg+="Que voulez-faire ?\n1) Jouez comme ça\n2) Attendre un copain\n"

		client.sendall(msg)
		choice=int(client.recv(10224))
		if choice==1:
			inGame=1
		elif choice==2:
			client.sendall("On attend un copain !")

	
	listeClient=[elem[0] for elem in dicoScore.values()]
	objet_jeu=Game(len(dicoScore), listeClient, dicoScore.keys())
	for client in listeClient:
		client.sendall("GAMEON")

	for client in listeClient:
		confirm=client.recv(10224)

	if confirm=="GO":	
		sendDetail()

		global threadGame
		threadGame=threading.Thread(target=sendGame, name="threadGame")
		listThreads.append(threadGame)

		for i in range(len(objet_jeu.listPlayer)):
			nameT='threadRcpt'+str(i)
			t=threading.Thread(target=recptDirection, args=(objet_jeu.listPlayer[i],), name=nameT)
			listThreads.append(t)
			t.start()
		
		# Garde le thread actif
		z=0
		while stopRecptDirection:
			z+=1
	
		print "Fin partie"

# Fonction debug 
def displayThread():
	global listThreads
	
	print 'Nb Thread : ',len(listThreads)	
	for t in listThreads:
		print t.name, 'actif : ',t.isAlive()
	

################################################################
##					MAIN SERVER
################################################################

global threadPartie
threadPartie=threading.Thread(target=playGame, name="threadPartie")
listThreads.append(threadPartie)
threadPartie.start()

while stopBoolServ:	

	threadPartie.join()
	
	if not threadPartie.isAlive() and inGame==0:	
		dicoScore.clear()
		del(objet_jeu)
		
		stopSendGame=True	
		stopRecptDirection=True

		threadPartie=threading.Thread(target=playGame, name="threadPartie")
		threadPartie.start()
	
	
	
	
	
