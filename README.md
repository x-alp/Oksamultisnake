*Oksa multisnake* est un jeu du snake multijoueur écrit en Python. Il est basé sur l'architecture Client-Serveur.

L'objectif du jeu est sans fin, le joueur doit essayer de manger le plus de bonus possible tout en évitant de se manger lui même ou de se faire manger par les autres joueurs.


Dépendances
-----------

Le jeu est nécessite Python et les modules normalement déjà présent tel que :

* Tkinter pour l'affichage graphique,
* Threading
* Socket

Les tests ont été réalisés avec Python 2.7.3 sous Debian 7 et OpenSuse 12.

Test
----

*Lancement du serveur

>$ python Server.py [-p port] [-ip ip]

*Lancement du client

> $python Client.py [-p port] [-ip ip]

Sans paramètres, le script utilisera les paramètres par défaut (port : 8000 et ip : 127.0.0.1).

L'ensembles des variables d'initialisation (taille graphique, ip,...) sont définies dans le fichier Initialisation.py
Celui ci est utilisé par tous les scripts et doit donc correspondre pour le Server et le Client.

Commandes utilisateur
---------------------

* `<space>` Lance et arrête la partie
* `<p>` : Pause
* flèches directrices pour les changements de direction

A améliorer
-----------

*Affichage graphique
*Arrêt propre du serveur

Licence
-------

Le code d'*Oksa multisnake* est sous licence GPL v3. Pour plus de détails concernant les termes de cette licence, consultez la page dédié.

Credits
-------

Antoine Courcelles
http://goldenbear.no-ip.biz/
