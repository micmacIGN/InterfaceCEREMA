L'interface CEREMA offre une interface graphique conviviale pour 
MICMAC, l'outil de photogrammétrie libre de l'IGN.

version 5.40 01 avril 2019 :
	modification ergonomie saisies des points GPC, photo suivante/précédente dans fenêtre de saisie
	corrections de bugs
	ajout du drapage pour les option quickmac micmac et BigMac de c3dc
	modification de l'option par défaut de c3dc : BigMac
	
version 5.34 suite aux conseils de Xavier Rolland (26/03/19)
- remplacement global de GPS par GCP = Ground Control Point
- Au retour de saisie des points GCP : fenêtre liste des photos
- l'affichage des coordonnées des points saisis devient optionnel
- la limite du zoom dans la fenêtre de saisie des points est augmentée

Le 25 mars 2019 : ajout d'un tutoriel pour prendre en main MicMac à travers l'interface CEREMA.

Version du 25 mars 2019 : 5.33
- Possibilité de relancer un chantier non terminé en conservant les points homologues.
- ajout d'un item au menu expert : modifier la longueur du préfixe utilisé pour définir plusieurs appareils. 
- suppression pour les anciennes versions des installateurs windows 32 bits et linux.
  Ces installateurs (msi 32 bit pour la version 5.0 ; deb et rpm pour la version 3.14) restent disponibles dans l'historique Github. 

Version du 12 mars 2019 : 5.32
- la recherche d'une nouvelle version sur le web propose la visualisation du fichier "readme.txt" (Outils/véifier la présence...)
- sous windows : avertissement si la longueur d'une ligne de commande dépasse 8191 caractères, risque de plantage 
- correction bug lors de la définition de plusieurs appareils photos, amélioration de la vitesse du traitement 

Version du 8 mars 2019 : 5.31
- Les échelles par défaut de Tapioca sont calculées suivant les photos : 60% de la dimension maxi des photos
- suppresssion des items de menu outils\qualité des photos line et qualité des photos ALL,
  maintient de la qualité des photos sur le dernier traitement
- Ajout d'un controle d'unicité de la scène aprés le premier passage, rapide, de Tapioca MultiScale :
  évite de se lancer dans une recherche approfondie de points homologues si l'échec est prévu
- Ajout de 1 item au menu outils : retirer des photos au chantier
- optimisation de la fonction "Expert/plusieurs appareils"
- l'installateur msi pour Windows installe un item dans le menu démarrer, un raccourci sur le bureau et
  ajoute le répertoire d'installation au path

Plusieurs nouveautés dans la version 5.30 février 2019:
- dans les items 'Outils/Qualité des photos' ajout des photos 'isolées', en disjontion de toutes les autres.
  Ces photos font 'planter' la recherche de l'orientation.
- Suite à la recherche des points homologues vérification de l'unicité de la scène photographiée.
  Plusieurs scènes sans points homologues communs font planter la recherche d'une orientation.
  Cette fonction est ajoutée à l'item 'Outils/Qualité des photos'.
- Lorsque le message MAXLINELENGTH est émis par Tapioca il est affiché et expliqué dans la trace synthétique.
- prise en compte de l'erreur concernant la fonction filedialog sous Mac-Os lors des recherche de programmes (exiftool...).
- Ajout d'un item dans paramètrage : recherche d'une nouvelle version GitHub.

dans les versions 5.2 :
- lancement automatique de campari après GCP_bascul (menu MicMac/options/points gps)
- ajout de la consultation du log mm3d (menu expert)
- mise à jour de dicocamera.xml pour "tous" les appareils photos du lot de données (menu outils)
- ajout d'un chantier à partir d'un répertoire (menu fichier)
- ajout d'un item dans le menu expert : ouverture d'une console pour lancer des commandes "python"

Plusieurs nouveautés dans la version 5.11 : 

- menu MicMac/options : l'onglet "calibration" est renommé : "mise à l'échelle"
- menu MicMac/option/Tapas : les photos pour calibrer l'appareil photo sont, ou pas, indépendantes des photos utilisées pour construire le nuage
- menu outils/nom de l'appareil photo : affichage des dimensions des photos et du numéro de série de l'appareil (si présent dans l'exif)
- Menu Expert, nouveaux item :
  - saisie des points GPS à partir d'un fichier texte (séparateur espace  : nom, x,y,z, dx,dy,dz)
  - possibilité de répartir les photos suivant plusieurs appareils photos 
  - liste des différents appareils photos présents dans le lot de photos
  
Pour plus de détail voir l'item de menu "Aide/historique" ou le code source.


Un installateur msi facilite l'installation de la version 5.33 sous Windows 64 bits.
Sous linux et mac/os : voir la documentation
 
L'application MicMac de l'IGN doit être installée ( https://github.com/micmacIGN ou http://logiciels.ign.fr/?Micmac )