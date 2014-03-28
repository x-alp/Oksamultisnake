# -*- coding: utf-8 -*-
################################################################
##					Initialisation.py
################################################################
# Paramètres du jeu
#
# Antoine Courcelles, Marc Cerou,
# André Guimaraes-Duarte, Doina Leca

#List d'initialisation
list_direction=['m1', 'm2', 'm3', 'm4']
list_color=['blue', 'green', 'red', 'yellow']
list_init=[[[10,10],[10,20]],[[100,100],[110,100]],[[200,200],[200,210]],[[300,300],[300,310]]]

#Taille du bonus
lenFood=8
colorFood='red'
#Taille case du serpent
lenSnake=10
colorHead='black'
approxEat=lenSnake

#Taille fenetre
window_width=400
window_height=400

nbRow=3
nbCol=0
nbColSpan=2

# Paramètres réseaux par défaut
numPort=8000
ipConnect="127.0.0.1"

#Pas de temps
pdt=0.05
