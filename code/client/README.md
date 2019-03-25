# Client.
Sur les raspberry pi client il y a un script (client.py) avec 2 threads qui tourne.
Un thread qui va se connecter au serveur (via socket), ensuite il va récupérer pour chaque capteur, l'id du capteur le type de la métrique et la valeur(ex: id=1, type="température", value="19").
Et ensuite l'envoyer en json avec en plus l'id du cube dans lequel le capteur est installé.

L'autre thread va attendre que le serveur lui envoit des messages et les interpréter pour réagir en fonction du message.
Par exemple "bonjour" va allumer les leds, et "au revoir" les éteindre.


# Serveur.
Sur le serveur il y a un script python (main_server.py) qui va ouvrir un socket pour recevoir les connections des clients, et sur connection il réouvre un thread pour attendre les messages.
Le script va également se connecter à la base de donnée mise en place à l'avance.
Ensuite lorsqu'il reçoit un message (les données en json) il les insert dans la base donnée, et si besoin il va réagir en envoyant un message au client.
