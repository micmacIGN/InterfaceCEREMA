## Version 5.32 (12 mars 2019)
- la recherche d'une nouvelle version sur le web propose la visualisation du fichier "readme.txt" (Outils/véifier la présence...)
- sous windows : avertissement si la longueur d'une ligne de commande dépasse 8191 caractères, risque de plantage 
- correction bug lors de la définition de plusieurs appareils photos, amélioration de la vitesse du traitement 

## Version 5.31 (8 mars 2019)
- Les échelles par défaut de Tapioca sont calculées suivant les photos : 60% de la dimension maxi des photos
- suppresssion des items de menu outils\qualité des photos line et qualité des photos ALL,
  maintient de la qualité des photos sur le dernier traitement
- Ajout d'un controle d'unicité de la scène aprés le premier passage, rapide, de Tapioca MultiScale :
  évite de se lancer dans une recherche approfondie de points homologues si l'échec est prévu
- Ajout de 1 item au menu outils : retirer des photos au chantier
- optimisation de la fonction "Expert/plusieurs appareils"
- l'installateur msi pour Windows installe un item dans le menu démarrer, un raccourci sur le bureau et
  ajoute le répertoire d'installation au path

## Version 5.30 (février 2019)
- dans les items 'Outils/Qualité des photos' ajout des photos 'isolées', en disjontion de toutes les autres.
  Ces photos font 'planter' la recherche de l'orientation.
- Suite à la recherche des points homologues vérification de l'unicité de la scène photographiée.
  Plusieurs scènes sans points homologues communs font planter la recherche d'une orientation.
  Cette fonction est ajoutée à l'item 'Outils/Qualité des photos'.
- Lorsque le message MAXLINELENGTH est émis par Tapioca il est affiché et expliqué dans la trace synthétique.
- prise en compte de l'erreur concernant la fonction filedialog sous Mac-Os lors des recherche de programmes (exiftool...).
- Ajout d'un item dans paramètrage : recherche d'une nouvelle version GitHub.

## Version 5.2
- lancement automatique de campari après GCP_bascul (menu MicMac/options/points gps)
- ajout de la consultation du log mm3d (menu expert)
- mise à jour de dicocamera.xml pour "tous" les appareils photos du lot de données (menu outils)
- ajout d'un chantier à partir d'un répertoire (menu fichier)
- ajout d'un item dans le menu expert : ouverture d'une console pour lancer des commandes "python"

## Version 5.11

- menu MicMac/options : l'onglet "calibration" est renommé : "mise à l'échelle"
- menu MicMac/option/Tapas : les photos pour calibrer l'appareil photo sont, ou pas, indépendantes des photos utilisées pour construire le nuage
- menu outils/nom de l'appareil photo : affichage des dimensions des photos et du numéro de série de l'appareil (si présent dans l'exif)
- Menu Expert, nouveaux item :
  - saisie des points GPS à partir d'un fichier texte (séparateur espace  : nom, x,y,z, dx,dy,dz)
  - possibilité de répartir les photos suivant plusieurs appareils photos 
  - liste des différents appareils photos présents dans le lot de photos
