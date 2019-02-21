L'interface CEREMA offre une interface graphique conviviale pour 
MICMAC, l'outil de photogrammétrie libre de l'IGN.

Version du 21 février 2019 : V 5.30

Plusieurs nouveautés dans la version 5.11 : 

- menu MicMac/options : l'onglet "calibration" est renommé : "mise à l'échelle"
- menu MicMac/option/Tapas : les photos pour calibrer l'appareil photo sont, ou pas, indépendantes des photos utilisées pour construire le nuage
- menu outils/nom de l'appareil photo : affichage des dimensions des photos et du numéro de série de l'appareil (si présent dans l'exif)
- Menu Expert, nouveaux item :
  - saisie des points GPS à partir d'un fichier texte (séparateur espace  : nom, x,y,z, dx,dy,dz)
  - possibilité de répartir les photos suivant plusieurs appareils photos 
  - liste des différents appareils photos présents dans le lot de photos
  
dans les versions 5.2 :
- lancement automatique de campari après GCP_bascul (menu MicMac/options/points gps)
- ajout de la consultation du log mm3d (menu expert)
- mise à jour de dicocamera.xml pour "tous" les appareils photos du lot de données (menu outils)
- ajout d'un chantier à partir d'un répertoire (menu fichier)
- ajout d'un item dans le menu expert : ouverture d'une console pour lancer des commandes "python"

dans la version 5.30 :
- dans les items 'Outils/Qualité des photos' ajout des photos 'isolées', en disjontion de toutes les autres.
  Ces photos font 'planter' la recherche de l'orientation.
- Suite à la recherche des points homologues vérification de l'unicité de la scène photographiée.
  Plusieurs scènes sans points homologues communs font planter la recherche d'une orientation.
  Cette fonction est ajoutée à l'item 'Outils/Qualité des photos'.
- Lorsque le message MAXLINELENGTH est émis par Tapioca il est affiché et expliqué dans la trace synthétique.
- prise en compte de l'erreur concernant la fonction filedialog sous Mac-Os lors des recherche de programmes (exiftool...).
- Ajout d'un item dans paramètrage : recherche d'une nouvelle version GitHub.


Des installateurs facilitent l'installation de certaines versions :

Version 5.3 sous windows 64 bits
Version 5.0 sous windows 32 bits
Version 3 sous Linux (deb et rpm)

Sous mac : voir la documentation
 
L'application MicMac de l'IGN doit être installée ( https://github.com/micmacIGN ou http://logiciels.ign.fr/?Micmac )