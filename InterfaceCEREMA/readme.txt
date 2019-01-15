L'interface CEREMA offre une interface graphique conviviale pour 
MICMAC, l'outil de photogrammétrie libre de l'IGN.

Version 5.11 le 21 décembre 2018 : utiliser le source aperodedenis.py 

Plusieurs nouveautés dans la version 5.11 : 

- menu MicMac/options : l'onglet "calibration" est renommé : "mise à l'échelle"
- menu MicMac/option/Tapas : les photos pour calibrer l'appareil photo sont, ou pas, indépendantes des photos utilisées pour construire le nuage
- menu outils/nom de l'appareil photo : affichage des dimensions des photos et du numéro de série de l'appareil (si présent dans l'exif)
- Menu Expert, nouveaux item :
  - saisie des points GPS à partir d'un fichier texte (séparateur espace  : nom, x,y,z, dx,dy,dz)
  - possibilité de répartir les photos suivant plusieurs appareils photos 
  - liste des différents appareils photos présent dans le lot de photos
  
 et sous la  version 5.2 :
- lancement automatique de campari après GCP_bascul s'il y a les bons paramètres.
- ajout dans le menu expert de la consultation du log mm3d
- mise à jour de dico camera pour "tous" les appareils photos du lot de données


Des installateurs facilitent l'installation des anciennes versions :

Version 5 sous windows (msi)
Version 3 sous Linux (deb et rpm)

Un installateur pour la version 5.2 sous windows ewst en préparation.

Sous mac : voir la documentation
 
L'application MicMac de l'IGN doit être installée ( https://github.com/micmacIGN ou http://logiciels.ign.fr/?Micmac )