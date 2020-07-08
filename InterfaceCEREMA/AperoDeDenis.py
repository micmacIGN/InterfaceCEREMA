#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 0008 -- Style Guide for Python Code

# Version python 3 ou plus
# est-il possible de relancer Malt en conservant le niveau de zoom déjà atteint ??? pas sur, sauf en passant par Micmac

# Version 2.35 :
# le 26 avril 2016
# - affichage des heures avec les secondes
# - Controle que le nom du répertoire bin de micmac ne comporte pas d'espace.
#v 2.41
# correction d'un bogue sur la suppression des points GCP
# autorise 30 points GCP
# 2.42
# suppression bogue suppression de points GCP multiples
# gcpbascule après tapas ET toujours avant malt
# 2.43
# les conséquences du choix de nouvelles photos sont modifiées de trois façons :
# - si des emplacements de points GCP doivent être supprimés alors il y a demande à l'utilisateur
# - le nettoyage du chantier est moins brutal : les fichiers exp (exports) et ply sont conservés.
# - le chantier est enregistré avant de rendre la main (si l'utilisateur ne validait pas un enregistrement ultérieur le chantier devenait inaccessible)
# ajout de import tkinter.messagebox pour le message d'avertissement si AperoDeDenis est dèjà lancé sous windows
# 2.44
# Accepte les virgules comme séparateur décimal pour les points GCP : remplacement des virgules saisies dans les coordonnées GCP par des points
# 2.45
# accepte la virgule pour la distance de la calibration métrique (remplace virgule par point)
# nouveau bouton : lance la calibration GCP
#
# ajout de tawny après Malt, avec saisie libre des options (mosaiquage du résultat de malt/ortho)
# 2.50
# Active/désactive le tacky message de lancement
# 2.6
# saisie de l'incertitude sur la position des points GCP
# 2.61
# correction d'un bogue de compatibilité ascendante (changement de structure de la liste des points GCP. Le 14/09/2016

# a faire : corriger le mode d'obtention de ALL ou Line dans le calcul des indices de qualité
# toutes les focales : la commande explore les sous-répertoires comportant la chaine JPG !!!
# v 3.00 : bilingue (début novembre 2016)
# V 3.10 : sélection des meilleures photos
# v 3.11 : sélection des meilleurs images pour créer un nouveau chantier
# v 3.12 : correction bogue affichage GCP
# v 3.13 : recherche exiftool et convert sous binaire-aux\windows ffmpeg absent sous bin;
#          possibilité de saisir une unité avec la distance
#          controle des photos supprimé si lanceMicMac après Tapas.
# v 3.14 : correction d'une régression de la v 3.13 lors de la restauration des paramètres (dûe à l'ajout de self.ffmpeg dans la sauvegarde).
# v 3.20 : les photos autour de la maitresse pour Malt ne sont plus "autour" mais choisies parmi les meilleures en correspondances
#          Ajout d'un choix pour Malt : AperoDeDenis, l'interface recherche les maitresses et les photos correspondantes
#          ajout filtre pour afficher l'erreur max sur gcpbascule (erreur positionnement des points GCP.
#          controle affiné des points GCP : on indique ceux qui ne sont placés sur une seule photo et on vérifie la présence de 3 points sur 2 photos
#          après plantage durant malt ou fusion : on renomme les JPG et les PLY lors du rédémarrage (reste pb semblable pour calibration intrinsèque)
#          suppression d'un point GCP sur une photo (avant : suppression de tous les points)
#          Affichage dans l'état du chantier des points GCP positionnés sur une seule photo
#          Non mise dans le xml des points GCP positionnés une seule fois.
#          Si le controle des points GCP est négatif alors les fichiers xml ne sont pas créés
# 3.30
# 1) créer une mosaique  après tapas sur toutes les photos : "Tarama" ".*.JPG" "Arbitrary"
# 2) la mosaïque est un tif : sour le répertoire TA : TA_LeChantier.tif
# 3) saisir un masque sur la mosaïque créée : par l'outil de saisie de masque, la masque doit s'appeler : 
# Les masques sont pris en compte par défaut ou si l’option DirTA = "TA" et UseTA=1 de Malt sont actives. (UseTA = 1 par défaut)
# Par défaut l’ajout est _Masq, qui peut être modiﬁée avec l’option MasqIm de Malt. ( "_Masq" après le nom)
# un fichier xml accompagne le masque (créé par MicMac ?)
# voir description : http://jmfriedt.free.fr/lm_sfm.pdf
# 4) Lancer Malt option Ortho : "C:/MicMac6706/bin\mm3d.exe" "Malt" "Ortho" ".*.JPG" "Arbitrary" "NbVI=2" "ZoomF=4" DirTA=TA
# 5) Lancer Tawny pour créer une mosaïque sur le résultat de malt : "mm3d" "Tawny" "Ortho-MEC-Malt/" :
#    ce qui donne la mosaique Orthophotomosaic.tif sous le répertoire "Ortho-MEC-Malt/"
# 6) lancer Nuage2Ply pour obtenir le ply sous le répertoire Mec-Malt : NuageImProf_STD-MALT_Etape_7.ply
# C:\Python340\MesScripts\AperoDeDenis\vaches noires\micmac_17>mm3d Nuage2Ply Mec-Malt/NuageImProf_STD-MALT_Etape_7.xml  Attr=Ortho-MEC-Malt/Orthophotomosaic.tif
# 7) vérifier si une nouvelle version est disponible
# 8) faire un masque "inverse" ou multiple ok
# 9) ouvrir les mosaiques par menu
# menu expert : exécuter une ligne de commande
# correction : self.e au lieu de e dans MyDialog
# version 3.31
# copier les points GCP d'une chantier dans un autre (en corrigeant ce qu'il faut, menu expert)
# version 3.32 : 2 corrections mineures (lignes 3854 supprimée et 3953 orthographe)
# Version 3.33 : correction comptage des points GCP et des points GCP avec les mêmes coordonnées ( définition de listePointsActifs  revue)
# Version 3.34 : janvier 2018
# correction de : e remplacé par self.e dans MyDialog (fixe le problème du renommage des chantiers)
# ajout de self.pasDeFocales = False après la mise à jour des exifs. (fixe le problème du message erroné concerné les focales manquantes)
# modification de l'icone de la fenêtre = l'icone du cerema remplace le graindsel.
# possibilité de choisir le ménage : suppression totale ou conservation des résultats seuls
# Affichage du gain de place en MO après le ménage
# affichage de la taille du dossier en MO dans l'affichage de l'état du chantier
# test de la présence de sous répertoire dans afficheetat :
# si etatDuChantier>2 et pas de sous-répertoire alors etatDuChantier remis à 2 et
# message "chantier nettoyé" affiché
# la version 3.34 est rebaptisée 5.0 (suppression de l'item "indice surfacique")
# Version 5.1 : 4 décembre 2018 : ajout du widget pour éliminer les photos ayant servis à la calibration de l'appareil photo
# ajout d'un item dans le menu expert : copier les coordonnées des points GCP à partir d'un fichier texte
# modification des onglets Malt et C3DC, réunis dans un même onglet "Densification"
# renommage de l'onglet "calibration" en "mise à l'échelle"
# Version 5.2 janvier 2019 : 
# correction bug sur l'affichage des photos pour calibration après Tapas
# ajout des paramètres pour Campari dans la fenêtre des options/points GCP
# lancement automatique de campari après GCP_bascul s'il y a les bons paramètres.
# ajout dans le menu expert de la consultation du log mm3d
# mise à jour de dico camera pour "tous" les appareils photos du lot de données
# fix bug sur mise à jour de l'exif mal pris en compte, suppression des variables pasDeFocales et uneseulefocale.
# ajout de l'item " ajout d'un chantier à partir d'un répertoire" dans le menu fichier
# version 5.21 janvier 2019
# python 3.5 nécessaire pour renommer un chantier (commonpath)
# ajout possibilité de passer une commande "python" dans le menu expert
# Modification de l'option "Autocal" de Tapas : Figee (au lieu de Autocal) : permet de 'figer' la calibration initiale
# version 5.22 11 février 2019
# fix 2 issues :
#  - suppression du l'annonce d'une nouvelle version sur internet (incorrecte)
#  - suppression d'un bug concernant les tags de l'exif suite au renommage d'un chantier, bug de la version 5.1
# version 5.30 21 février 2019 :
#  - dans les items "qualité des photos" ajout des photos "isolées", en disjontion de toutes les autres.
#    Ces photos font "planter" le traitement tapas
#  - Ajout d'un fonction vérifiant le nombre de scènes disjointes en terme de points homologues.
#    lorsqu'il y a plusieurs scènes l'orientation est impossible : arrêt de micmac aprés tapioca.
#  - Lorsque le message MAXLINELENGTH est émis par Tapioca il est affiché et expliqué dans la trace synthétique
#  - Ajout de cette fonction dans l'item "outils/qualité des photos du dernier traitement"
#  - prise en compte de l'issue concernant la fonction filedialog sous Mac-Os lors des recherche de programmes (exiftool...)
#  - suppression des lignes de codes inutilisées concernant les indices surfaciques
#  - Ajout d'un item dans paramètrage : recherche d'une nouvelle version GitHub
#  - la recherche systématique d'une nouvelle version est réactivée (désactivée en version 5.22
# 5.31 : 25/2
#  - Les échelles par défaut de Tapioca sont calculées suivant les photos : 60% de la dimension maxi des photos (qui semble être un optimum)
#  - l'instruction commonpath nécessitant la version 3.5 de python est mise en "try", la version 3.5 de python n'est plus obigatoire
#  - fix sur la qualité des photos si pas de points homologues, idem après Tapioca
#  - modif du filtre qualité des photos : affichage écran de la trace
#  - suppresssion des items de menu outils\qualité des photos line et qualité des photos ALL,
#    maintient de la qualité des photos sur le dernier traitement
#  - Ajout d'un controle d'unicité de la scène aprés le premier passage, rapide, de Tapioca MultiScale :
#    évite de se lancer dans une recherche approfondie de points homologues si l'échec est prévu
#  - Ajout de 1 item au menu outils : retirer des photos au chantier
#  - modification de la fonction "Expert/plusieurs appareils" :
#    la modification du tag model de l'exif est faite à partir du préfixe du nom de fichier, sur 3 caractères
#    la modification a lieu après accord de l'utilisateur, sans autre condition
#    la modification est faite une seule fois, non cumulative
#  - fonction "encadre" : la valeur par défaut du paramètre nouveauDepart passe de 'oui' à 'non'
#    les appels à la fonction encadre sont modifiés en conséquence
# 5.32 : le 11 mars
#  - l'item de menu "rechercher la présence d'une nouvelle version sur GitHub" est désormais placé dans le menu Outils.
#    cet item propose de visualiser la page web de téléchargement ou le readme.txt sur GitHub.
#  - correction d'un bug : la modification des tag "model" des exif met à jour la variable self.lesTagsExifs
#  - accélération importante du traitement de la modification des tag "model"
#  - ajout d'une verrue dans lanceCommande pour essayer de traiter la cas d'une ligne de commande dont la longueur serait supérieure à 8191 sous Windows
# 5.33 : le 12 mars
#  - correction faute de casse : photosavecdistance en photosAvecDistance ligne 3851
#  - modification en cas de nouvelle photos sur un chantier en cours : réinitalise toutes les valeurs par défaut
#  - écriture dans la trace de l'état du chantier si erreur, des demandes de déblocage du chantier
#  - remplace os.chdir par oschdir !
#  - ajout d'un item au menu expert : modification possible de la longueur du préfixe pour définir plusieurs appareils
#  - menu MicMac/lancer MicMac : possibilité de relancer l'orientation (Tapas)  en gardant les points homologues (Tapioca)
#    SI le chantier est arrété après Tapas ou non terminé correctement
# version 5.34 suite aux conseils de Xavier Rolland (26/03/19)
# - remplacement global de GCP par GCP (sauf définition dans l'aide)
# - Au retour de saisie des points GCP : fenêtre liste des photos
# - l'affichage des coordonnées en pixels devient optionnel
# - la limite du zoom dans la fenêtre de saisie des points GCP est augmentée
# version 5.40 30 mars 2019
# - amélioration ergonomie saisie des points gcp : flèches : photo suivante/précédente dans la fenêtre
# - correction 1 issue : repertoire_script erroné si lancement par raccourci windows
# Attention : version 3.3 de python nécesssaire ! (replace)
# - Correction d'un bug : le choix abandon sur la saisie d'un plan (horizontal ou vertical) était = choix valider !!
# - lors de l'import des points gps d'un autre chantier ou de la lecture d'un fichier de points :
#   lance la génération de dico-appuis.xml et mesure-appui.xml
# - ajout dans la trace synthétique et dans la trace complète d'informations sur l'écart de positionnement des points GCP
# - ajout du mode C3DC dans l'afficheEtat
# - les fichiers logocerema.gif logoIgn.gif, flechedroite.gif et flechegauche.gif disparaissent, ils sont inclus dans dans le code
# - message complété par des conseils si la densification échoue
# - ajout du drapage pour les options de c3dc : BigMac QuickMac et MicMac
# - changement d'une option par défaut : C3DC bigmac (avec drapage)
# Version 5.41 :
# - suppression d'un bug dans "du ménage" : le nettoyage des chantiers, s'effectuait uniquement sur le chantier en cours, même s'il n'éatait pas choisi !
# - affichage de la liste des répertoires supprimés aprés nettoyage par du ménage.
# - en cas d'absence de répertoire locale et de lancement par le script (sans exe) il y avait plantage (__cached__ non instancié)
# - SI répertoire locale absent alors on informe direct que la version bilingue n'est pas installée (avent : info après avoir choisi la langue)
# - l'item renommer un chantier remplacé par "Enregistrer sous..." avec un fonctionnement standard (sauf changeùent d'unité disque)
# - Si du ménage a été fait le chantier est indiqué comme nettoyé lors de l'ouverture suivante, avec indication dans la trace
# Version 5.42 6 avril 2019
# correction option aperodedenis de Malt lorsqu'il y a des photos pour calibration uniquement
# corrction écriture de la trace
# Version 5.43
# - Propose à l'utilisateur sous Windows de lancer plusieurs instance d'AperoDeDenis, nouveau dossier si oui
#   modifications diverses pour éviter les collisions entre plusieurs instance lors de la création d'un chantierZ
# - la class MyDialog_OK_KO devient opérationnelle, avec 1 ou 2 boutons, modale.
# - suppression de la sauvegarde des chantiers "vide"
# - module "choisirUnChantier" utilisé pour demander un répertoire : devient modal !
# - l'aide "quelques conseils est séparé en 3 : prises de vue, Options et si MicMac ne trouve pas d'orientation/nuage dense
# - ajout dataIcone = tkinter.PhotoImage(data=iconeTexte) dans initialiser langue (sinon plante à la première install)
# - modif des fleches droite et gauche
# - suppression du test systématique de présence d'une nouvelle version sur GitHub
# - correction du test de présence d'une nouvelle version (nécessite que le readme.txt contiennent " V N.NN" pour la seule version en cours 
# Version 5.44 :
# - modif du message si nouvelle version sur gitHub
# - modif message si tapioca ne trouve pas de points homologues : trop de photos !
# - ajout de la fonction "recherche" dans les textes affichés par texte201 (trace, aide) ; Ctrl F et  F3
# - la recopie des points GCP d'un autre chantier ne se fait que pour les points "actifs"
# - Aprés recopie des points GCP d'un autre chantier ou à partir d'un fichier le chantier est enregistré
# - Un message est mis dans la trace aprés recopie de points GCP
# - le ménage dans un chantier ne supprime plus les éventuels chantiers présents dessous
# - affiche le résultat des commandes systèmes dans une fenêtre texte (menu expert/commande système)
# - aprés un échec dans Tapas le choix "option" propose de conserver les points homologues (= item 'lancer micmac')
#   ce qui permet de relancer Tapas sans tapioca !

# Version 5.45
# - modif ajoutChantier depuis un répertoire : controle présence du répertoire parmi les chantiers (refus) puis du nom du chantier parmi les noms de chantier (pose la question)
#   avant : confusion et possibilité d'enregistrer deux fois le même chantier sous le même chemin
# - enregistrer sous : plus robuste, le répertoire ne doit pas pré-exister, le chantier non plus.
#   changement d'unité disque possible : désormais on recopie le dossier en gardant l'ancien dans ce cas
# - tapas, calibration : sécurisation du changement d'extension des photos. Message et abandon si erreur.
#   Avant cette modification un trop grand nombre de photos sous windows pouvait faire planter le traitement sans laisser de trace.
# - Ajout de l'item "renommer le chantier" (beaucoup plus simple à utiliser que "enregistrer sous", plus rapide, mais limité à la même unité disque)
#   Cet item avait été supprimé dans la version 5.41
# - sécurisation des import de points GCP depuis un autre chantier ou un fichier.
#   notamment l'import devient impossible s'il y a déjà des points GCP définis

# Version 5.46
# - choix de nouvelles photos puis abandon : le chantier est rechargé (avant il fallait le réouvrir)
# - choix de nouvelles photos : le répertoire pour choisir est celui des photos du chantier en cours
# - modification importante de la procédure lanceTapas
# - suppression de la variable self.nePasLancerTapas (à priori : sert à rien)
# - suppression de la référence à la valeur 6 de self.etatDuChantier (valeur jamais instanciée)
# - Ajout de l'item Expert\Personnaliser les paramètres des modules MicMac
# - AJout d'un item : Outils/Qualité des points GCP
# version 5.47
# - correction bug initialisation dicoperso
# - copie point GCP : on efface systématiquement les anciens points GCP (suppression de la boite de dialogue posant la question)
# - on enregistre systématiquement les options si l'onglet est ouvert et qu'il faut le fermer au lieu de poser la question
# - ajout d'une tempo dans la fonction "plusieurs appareils" (pour laisser le temps à exiftool)
# - vérification des ajout/suppression de photos avant de lancer micmac. Blocage si c'est le cas.
# - un nouveau choix de photos ne crée plus un nouveau chantier

# version 5.48
# - Charger la calibration d'un autre chantier
# - ouvrir un chantier avec filtre (ne proposer que les chantier avec présence de gcp ou de calibration)

# Version 5.49
# 1) récupérer les coordonnées gps des appareil drone dji et les intégrer par oriconvert puis centerBascule:
#    exiftool.exe -filename -gpslatitude -gpslongitude -AbsoluteAltitude -relativealtitude -gimbalyawdegree -gimbalpitchdegree -gimbalrolldegree -n -T . > out.txt
#    Par défaut les nuages de points sont créés dans un référentiel local. Les coordonnées GPS du point origine sont inscrites dans la trace.
#    Les composantes X et Y en Lambert93 sont inscrites dans la trace : elle définissent la translation entre le repère local et le Lambert 93.
#    3 items du menu expert permettent de choisir l'utilisation des coordonnées GPS du drone : inutilisées, repére local, repère géocentrique
# ajout dans initialisevaleurs par défaut : (sinon les valeurs se conservent du chantier précédent)
#        self.choixCalibration.set("sans")
#        self.chantierOrigineCalibration =str()                          # si calibration copiée depuis un autre chantier
# suppression des fichiers créés par exiftool lors de la modif de l'exif
# ajout d'un item au menu expert : copier les points homologues d'un autre chantier
#   ne sont proposés que les chantiers ayant des photos compatibles (sur ensemble du chantier en cours) et des points homologues
#   copie aussi les paramètres de tapioca.
# recherche des tags dans les exifs : vitesse très accélérée, au moins 10 fois (tous les tags récupérés en une fois lors du choix des photos) 
# fait : le ménage ne doit pas supprimer TOUS les sous répertoires : certains peuvent contenir des chantiers !! limiter à une liste de noms
# retirer des photos : corrigé pour les maitresses, les masques et les mises à l'échelle
# proposer à l'utilisateur de lancer le traitement sur le plus grand groupe si plusieurs scènes
# suppression du choix "aperodedenis" comme mode pour malt (variante de geoimage; mais les bouts de code restent en placent)
# le traitement est bloqué si une maitresse pour geoimage, une photo utilisée pour la mise à l'échelle ou les points GPS
#  est une photo pour calibration intrinsèque non utilisée pour le traitement
# remise en service de la recherche systématique d'une nouvelle version sur github
# finOptionsOk lance afficheEtat : modifier pour le rendre optionnel (sinon : 2 affichages successifs d'afficheEtat lors du choix de photos avec GPS drone)
#                                  ajout d'un argument nommé
# vérification que l'utilisateur ne retire pas "toutes" les photos 

# version 5.50 :
# 1) Améliorations :
# - Menu expert : ajout de 3 sous menu :
#        - "importer des points homologues ... exporter MNT",
#        -  navigation GPS (drones)
#        -  plusieurs appareils photos
# - menu expert/Navigation GPS : ajout des choix EPSG, wgs84 et lambert93 et "ne pas prendre en compte les données GPS"
# - menu expert : ajout d'un item pour exporter les fichiers ply et les fichiers ascii de type X,Y,Z au format MNT de l'IGN et de GRASS.
# - Option/mise à l'échelle : l'onglet est désormais visible en modif de densification
# - Option/orientation : possibilité de ne pas calculer le nuage non dense (si inutile et cela prend du temps)
# - Option densification/Malt : le nuage de point généré par Malt est désormais au choix de l'utilisateur : nuage ou maillage
# - affichage de l'erreur provoquée par l'éxécution/évaluation d'une commande python (menu expert)

# 2) Corrections de bogues :
# 'self.mm3d' au lieu de 'mm3d" ligne 7127
# 'self.restauPerso' au lieu de self.initPerso ligne 9272
# les variables suivantes étaient initialisées dans l'initialisation des constantes et non par dans l'initialisation des valeurs par défaut :
# self.incertitudePixelImage, self.incertitudeCibleGPS et les variables pour la GOPRO
# remplacement de campari par Campari lors de l'appel à Campari (l'appel ne fonctionnait pas)
# - remplacer UrbanMne par UrbanMNE ligne 7371 (lanceCommande Malt plantait)

# 3) modifs cosmetiques ou correction d'anomalies :
# 'importer' au lieu de 'copier' ligne 1306
# écriture des traces en début de traitement micmac ligne 6815
#     (efface les lignes restant à écrire, qui sinon pouvaient être écrites plusieurs fois) : ecritureTraceMicMac())
# amélioration de la prise en compte des scènes multiples découvertes par Tapioca
# modif su message aprés choix des N meilleures photos : suppressio nde tous les résultats;
# modif libellé ligne 9535 (les chantiers)
# modif libellé suppression chantier (lignes 9505) : précision sur la suppression des sous répertoires
# modification libellé entête bdd nettoyage/suppression de fichiers
# ajout de "BEGIN STEP" dans les filtres c3dc et malt,avant begin Bloc. Uniquement lorsque la valeur change
# ecrire dans le fichier trace si la chaine devient trop longue (1 MO)
# modif du message si on modifie le choix des photos pour un chantier, et indication dans la trace
# modif message dans afficheetat : "drapage demandé" au lieu de "tawny lancé après malt"
# retirer des photos : l'utilisateur doit maisser au moins 2 photos (et non paas 1)
# commencé : importation d'une orientation (menu expert, début de modif)
# écriture des fichiers trace avant leur affichage : ils seront vus en étant à jour
# suppression des écritures multiples des traces dans elle même (survenant après demande d'affichage ligne 4264)
# Si un nouveau chantier est créé mais vide on le sauve pour la session suivante (début de def sauveParamChantier)
# après du choix du répertoire bin :
# - exécution de sauveParamMicmac pour mémoriser le mercurial de MicMac
# - affichage du mercurial de MicMac
# ajout de self.mercurialMicMac dans les paramètres suvegardés par sauveParamMicmac
# suppression du message d'avertissement (redondant) si le répertoire du chantier précéent n'est pas trouvé 


# version 5.51
# ajout d'un item dans le menu édition : info sur un ply : affiche le nombre de points, la surface, les valeurs maxi et mini de x,y, z
# ajout d'un item de menu : outils_métiers, pour la comparaison de 2 MNT issu des nuages
# ajout d'un item dans le menu outils_métiers : écriture du fichier XYZ contenant les coordonnées des points d'un PLY
# nouveau modele3d : ne pas renommer l'ancien, incrémenter le n°
# version 5.511
# corection cas particulier fichier PLY sans nombre de face (nombre_faces non initialisé)

# 2 questions de Thierry mercier : 
# 1) tarama est-il une ortho photo ? Non, c'est atwny qui fait l'ortho photo
# 2) Ajouter dans la doc le mode d'emploi pour diviser en plusieurs lots un seul jeu de beaucoup de photos

# version 5.52
# ajout de la taille du chantier dans les param sauvés du chantier
# affichage de la taille du chantier dans la liste des chantiers à ouvrir (faudrait aussi dans la liste du ménage à faire)
# Du ménage : Ajout d'un mécanisme pour conserver les fichiers résultats qui se trouvent dans l'arborescence, liste : resultatAConserver (Orthomasaique Tawny)
# construction masque 3D : sur aperiCloud seulement, pas prévu sur modele3D, possible manuellement (correction de la V 5.51)
# remarque : l'option tawny de malt n'est jamais utilisée
# modification du paramètre "centrer la scène sur " de SaisieMasqQT pour y mettre le baricentre si c'est l'origine (dans la base de registre)
# Ajout "copier la calibration d'un autre chantier dans le menu expert
# ajouté de la calibration dans le menu expert copier homol, orient, tarama, calibration !
# correction de la vérification de la version sur GitHub, paramètre pour supprimer la vérif automatique au lancement
# les fichiers ply dense portent les noms V1, V2...
# traduction de l'ensemble en anglais, allemand, italien(à revoir), espagnol(à revoir) et chinois, et arabe
# amélioration message pour renommer un chantier et enregistrer sous

# proposer de laisser un coeur libre (NbProc pour Malt) et le gpu pour C3DC (UseGpu) Possible avec les options personnalisées
# vérifier : sélection des meilleures photos : ne cherche pas s'il y a des coordonnées gps
# meilleures photos : tester puis utiliser oriconvert
# si choix des N meilleures photos essayer de garder les points homologues
# si l'utilisateur ferme l'appi par la croix au milieu de Malt alors le subprocess continue : les mm3d s'enchaînent...
# proposer un item "du ménage pour la suppression de tous les chantiers "vides" ou sans fichier param.
# si l'utilisateur modifie le référentiel gps du drone considérer que les options ont été modifiées (ne pas le redemander)

# en prévision :
# renommer un chantier : donner accès à la boite de dialogue de choix d'un répertoire

# prendre en compte les ply mesh binaire pour conversion en mnt
# bug en cours :
# parfois rodolphe lance des traitements interminables (qui ont planté sans commentaire ni fin : a examiner de près)
# version 5.40 : aprés plantage tapas, puis rechargement des photos, le bouton "plan horizontal" devient inactif (cf rodolphe)
# reprise de Tapioca aprés avoir généré un nuage dense : les photos de calibrations ne sont pas restaurées.
# bug bizarre le 16 mai 2019 matin version 2.46 : le fichier des paramètres du chantier micmac_30 vient écraser celui du chantier micmac 26 ????
# l'enregistrement des options par défaut à partir du chantier en cours  n'est pas complet
# pb avec un mac 
# reste a faire :
#   contrairement à la situation actuelle où ils sont renommés à chaque nouvelle densification
# vérifier pourquoi la ligne 9217 (remove) plante parfois ! (mise en try)
# gérer les ajouts de chantier si plusieurs instances (et les suppressions) et les modifs de paramètres...
# choix abandon = valider pour la saisie des lignes horizontale et verticale, a corriger
# présenter à l'utilisateur les écarts sur les points gcp (bascule et campari) mieux que dans la trace
# ajouter des indications pour aider à choisir le type de densification Malt ou 3dc
# le message "débloquer le chantier suite à lancer MicMac est parfois invalide : l chantier est déjà débloqué" !
# si l'absence de nuage dense est susceptible de correction alors donner le conseil à l'utilisateur (exemple : voir les conseils de l'aide)
# revoir les pack dans l'apropos (mal placés)
# il faudrait écrire dans la trace au fur et à mesure (on l'aurait si plantage...) voir :
    # def effaceBufferTrace(self):
        # commentaire le 1/4/2019 : à vérifier

############# Risque : on redéfinit photosAvecChemin et photosSansChemin en gardant le nom !!!! A modifier ligne 5615
# avec geomimage il y a deux affichage du modéle 3 D s'il y a plusieurs maitresses ! (pas encore compris pourquoi !)
# faire en sorte que le filtre tapas renvoie une solution si message Not Enouh Equation in ElSeg3D::L2InterFaisceaux
# généraliser le truc ci dessus à d'autre messages
#bug annulé ou corrigé :
# version 5.43 : aprés saisie de points gps l'affiche etat ne trouve pas de points gps (contrairement à la version 5.1 sur le même chantier bascule à 5.2 ?)
#               en fait : les points GCP sans coordonnées sont ignorés depuis la version 5.21 (?)
# encore décomposé l'aide en cas de plantage : orientation <> densification
# vérifier si l'ajout d'un chantier à partir d'un répertoire récupére bien les options : oui

# parfois tapas plante et rien ne se passe : on attend toujours ! Sans doute à cause du renommage foireux si beaucoup de photos.
# améliorer en version 5.45
# regrouper tout les affichages des texte201 (pour nettoyer le code aprés l'ajout de la recherche ctrl F et ctrl shift F
# lorsqu'il y a un nouveau choix de photos il ne faut pas supprimer tous les répertoires sous le répertoire de travail (idem suppression de photos)

# soucis avec cx_freese :
# des modules, des fichiers, des répertoires peuvent manquer : il faut les ajouter par include_file ou include
# il peut y avoir des problèmes de "CASSE" ie tkinter est importé come Tkinter : cela plante
# on peut alors l'exclure par exclude pour qu'il ne soit pas importé automatiquement puis l'inclure explicitement
# dans scipy, numpy il peut arriver aussi des pb de casse dans des dll
# utiliser l'outil "compare repertoires.py" pour comparer un répertoire qui marche et un qui ne marche pas...
# pour scipy il y avait des pb, voir pymeri, et ici on trouve un écart de casse sur 2 dll de scipy extradll,
# la correction corrige le plantage qui arrive lors de l'écriture d'un ply en MNT.
# ecartmajusc2moins1= 2 {'LIBWRAP_DUM.37XXVKIHM5ANYBLPIHFVIOO3H5TQVGWB.GFORTRAN-WIN_AMD64.DLL', 'LIBDCSRCH.I2AOPDCXAPDRFNPWY55H5UE7XZSU5CVN.GFORTRAN-WIN_AMD64.DLL'}


from tkinter import *                       # gestion des fenêtre, des boutons ,des menus
import tkinter.filedialog                   # boite de dialogue "standards" pour demande fichier, répertoire
import tkinter.messagebox                   # pour le message avertissant que AperoDeDenis est déjà lancé
import tkinter.ttk as ttk                   # amélioration de certains widgets de tkinter : le comportement est géré indépendamment de l'apparence : c'est mieux ! mais différent !
import pickle                               # pour la persistence
import os.path                              # pour les noms de fichier
import os                                   # gestion du système, des path 
import shutil                               # copie des fichiers, gestions répertoires
import time
import sys                                  # info système
import subprocess                           # appel des procédures MicMac
import signal
import traceback                            # uniquement pour pv : affiche les propriétés des variables (qui sert pour débug)
from   PIL import Image                     # pour travailler sur les images, définir le masque, placer les points GCP : PIL
from   PIL import ImageTk
from   PIL import ImageDraw
import base64
import tempfile
import inspect
import zipfile
import zlib
import ctypes
import gettext
import urllib.request
import webbrowser
import threading
from textwrap import wrap
import glob
import math
import struct
from itertools import cycle

#
def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True

def heure():        #  time.struct_time(tm_year=2015, tm_mon=4, tm_mday=7, tm_hour=22, tm_min=56, tm_sec=23, tm_wday=1, tm_yday=97, tm_isdst=1)
        return ("le %(jour)s/%(mois)s/%(annee)s à %(heure)s:%(minutes)s:%(secondes)s") % {"jour" : str(time.localtime()[2]), "mois" : str(time.localtime()[1]), "annee" : str(time.localtime()[0]), "heure" : str(time.localtime()[3]), "minutes" : str(time.localtime()[4]), "secondes": str(time.localtime()[5])}

def fin(codeRetour=0):
    print("fin")
    os._exit(codeRetour)

################################## Décorateur try

def decorateTry(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            tkinter.messagebox.showerror("Erreur",_("erreur inattendue = "+str(e)+"\n\n"+
                                                    _("Fichier incorrect. La fonction est abandonnée")))
            interface.menageEcran()
            return
        # Post-traitement
        return response
    return wrapper

def decorateTrySilencieux(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except:
            return
        # Post-traitement
        return response
    return wrapper

################################# Classe : Choix de la langue en cas d'absence dans les paramètres ###########################"
################################ Multilangue

class InitialiserLangue(tkinter.Frame):
    def __init__(self, frame, **kwargs):
        self.frame = tkinter.Frame
        self.frame.__init__(self, frame, **kwargs)
        frame.geometry("400x300")
        dataIcone = tkinter.PhotoImage(data=iconeTexte)
        frame.tk.call('wm', 'iconphoto', frame._w, dataIcone)
        self.pack(fill=tkinter.BOTH)
        frame.title("")
        langue = "NA"
        
        self.message = tkinter.Label(self, text="Choisissez une langue\nSelect your language")
        self.message.pack()

        self.bouton_francais = tkinter.Button(self, text = "Français/French", command = self.langueFrancaise)
        self.bouton_anglais = tkinter.Button(self, text = "Anglais/English", command = self.langueAnglaise)
        self.bouton_allemand = tkinter.Button(self, text = "Allemand/Deutsche", command = self.langueAllemande)
        self.bouton_espagnol = tkinter.Button(self, text = "Espagnol/Español", command = self.langueEspagnole)
        self.bouton_italien = tkinter.Button(self, text = "Italien/Italiano", command = self.langueItalienne)
        self.bouton_chinois = tkinter.Button(self, text = "Chinois/中文", command = self.langueChinoise)
        self.bouton_arabe = tkinter.Button(self, text = "Arabe/عربى", command = self.langueArabe)         
        self.bouton_francais.pack()
        self.bouton_anglais.pack()
        self.bouton_allemand.pack()
        self.bouton_espagnol.pack()
        self.bouton_italien.pack()        
        self.bouton_chinois.pack()
        self.bouton_arabe.pack()        
        print("langue=",langue)
        frame.protocol("WM_DELETE_WINDOW", self.arret)
        
    def arret(self):
        frame.destroy()
        print("Fermeture inatendue de la fenêtre / Unexpected closure of the window")
        sys.exit()


    def langueFrancaise(self):
        global langue
        langue = "fr"
        frame.destroy()
        

    def langueAnglaise(self):
        global langue
        langue = "en"
        print("anglais, langue = ",langue)
        frame.destroy()
        
    def langueAllemande(self):
        global langue
        langue = "de"
        frame.destroy()

    def langueEspagnole(self):
        global langue
        langue = "es"
        frame.destroy()

    def langueItalienne(self):
        global langue
        langue = "it"
        frame.destroy()

    def langueChinoise(self):
        global langue
        langue = "zh"
        frame.destroy()

    def langueArabe(self):
        global langue
        langue = "ar"
        frame.destroy()
        
################################# Outils de traduction ######################################################
def chargerLangue():
    try:
        sauvegarde2 = open(os.path.join(repertoire_data, "ParamMicmac.sav"),mode='rb')
        r2=pickle.load(sauvegarde2)
        sauvegarde2.close()
        langue                      =   r2[9]
        return(langue)
            
    except Exception as e:
        return "null"

################################## outils de géolocalistaion


def DMS2DD(dms):       # conversion degré minute seconde en degrés décimaux. : "49 deg 34' 18.59" N" ==> 49.5719444
    liste = dms.split()             # liste = 49,deg,34',18.59", N
    signe = 1                       # le nord et l'est sont positifs (défaut)
    s=0                             # ajout valeurs initiales le 7/4/20, fonction vérifiée
    m=0
    for e in liste:
        if e[-1]=="'":
            m = float(e[:-1])            
        if e[-1]=='"':
            s = float(e[:-1])            
        if e=="S" or e=="W":        # le Sud et l'ouest sont négatifs
            signe = -1
    dd = signe*(float(liste[0])+m/60+s/3600)
    return dd         

def conversionWGS84enRGF93(latitude,longitude):  
    pi = math.pi
    # définition des constantes
    c= 11754255.426096  #constante de la projection
    e= 0.0818191910428158  #première exentricité de l'ellipsoïde
    n= 0.725607765053267  #exposant de la projection
    xs= 700000  # coordonnées en projection du pole
    ys= 12655612.049876  #coordonnées en projection du pole

    # pré-calculs
    lat_rad= (latitude/180)*pi  #latitude en rad
    lat_iso= math.atanh(math.sin(lat_rad))-e*math.atanh(e*math.sin(lat_rad))  #latitude isométrique

    #calcul
    x= ((c*math.exp(-n*(lat_iso)))*math.sin(n*(longitude-3)/180*pi)+xs)
    y= (ys-(c*math.exp(-n*(lat_iso)))*math.cos(n*(longitude-3)/180*pi))

    return x,y    

def lambert93OK(latitude,longitude): # vérifie si le point est compatible Lambert93 (lat long en degré décimaux)
    if 40<latitude<60 and -10<longitude<10:
        return True
    return False

################################## INITIALISATION DU PROGRAMME ###########################################################

# Variables globales

numeroVersion = "5.52"
version = " V "+numeroVersion       # conserver si possible ce format, utile pour controler
versionInternet = str()             # version internet disponible sur GitHub, "" au départ
continuer = True                    # si False on arrête la boucle de lancement de l'interface
messageDepart = str()               # Message au lancement de l'interface
compteur = 0                        # Compte le nombre de relance de l'interface
listeDesFichiersTrace = list()      # pour modifier la trae en cours (par exemple pour les traces des MNT ou des volumes, variable modifiable globalement)

# voir ci dessus la fonction gif2txt() pour obtenir les textes suivants à partir d'un GIF
# voir ci-dessous la boucle principale pour transformer ces strings en images tkinter :

iconeTexte = "R0lGODlhIAAgAIcAMfr8+EqrpcfLEe16CJnE1Lnb3Hm7whaXjuzdu+VLEp64HuiRL9TYVfPImeqoU4e1NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAIAAgAAcI/gABCBxIEACCgwgENliYsKDDhwMVKHjwQOCAiwMgaiwoUaLABRgbboSIYKLEhCAvNhipkUFHBQwAOMC4gOVDBAI6CoiJAOMAkTYFMhCQUwHRjzSDDhxK1CjRmA18OlDKlKjVozKlssR5VQCAqzEBpLy4YGXBgwyqWk2oNmFPnwMWOGjQsOvVhAUCdHU7NoFfvwnt7hSYN4CBvQCi/l0cGGxDAgEiB3jQte/iBGzTiixgQHLkAlxnwh3A2CFnz5EJCB1L0wFQAAViE+iM2nABpD7LPixwoHdvw5INGJhNgPUAs7AJKFfN27dv28tnP6DZsMDs4cphO39+GwBx5TNrcCbHHl1ggOeeVXtfbmABXvLf1Q887bk7+9uc2RPoDhFyfdjkWXefTYVFZoBA7AUwYFAFKgggZAcMZwB/QflnGIKdRbifUgT9x9lv8nHonWTMnXdAABRyWOCBCJiIoogdSiaQczASJJxw5slY444DBQQAOw=="
logoIGN = 'R0lGODlhlQCjAIIAMXV4eo69Qs/OxtzotZqcmLa4s7TQffv9+iwAAAAAlQCjAAID/ni63P4wykmrvTjrPUcpwieKw8BNYXGubOsMAkEAdG3fAFGY7iHQhF5rRBwJF4UZbsnM7Ya14JHhKY4EyGZN6NF6mQTs6VcTTw8DL+9Q+LoGyq8cB+KQy2e0OusdxueANlIZbYJmXF5mhU2DGyGBkDgEaxZ3NodvewqLTWORnzeYFJw2lC1pWmukSxyroJAaloKmK6hNim4arq+BsYyIqXxaurzFxL+ZwZu5F7uBMn9zjZVe0xy2TLh9FzGROgK0aALdzM1fKizYS6rlHZHgGEnIGLJM6CfqOOzbFdGJY/5y+JIjCkO+UMI6VajX5N4KclGOEcSniU07CAezcfnj/pAaoHAVMuJZxk+CM4RTFnWscFJSQQoiaewb5m5inkIvJTDUMklDTAAzFeqUs/JIG5BDIVmD+Y8kTQkBbyydEkbisww/gzJBIQdpHnqgpmJsarHkg6g2in61qvRC1oRboX7JuZYbL7pUyLYEIOGnwLosdgLCq+CtU6EPBI8EfGJvNcKGyz49+8VrgxICDGjerBmc5YHF8P7UNtkBWiAhBxgIsDqA69ewN3/2WAxo34p7JXwRW7g17N/AX2uebbI2EKSj4bKCoBg1Rt/Bowc3QDxxNUBiI+dmPve59O/SDdhJ1DztWC2kETconxM6+Pevqyu/YcKx88u4L86nH8ED/vz/wmXQHA/2AbCSdvopIINZLwDoIHXmTHbaDR0ld1hcD+yFl3sOfgfhQhUdMOEleSkjmXoMaEgBhx1G9yFXJir40QIWnoihAyqu2CJ8L0bQ0gsjAiHGgPvZEEF5al0mwI7vfUbkekHmgEVz6d142YS8NcAik7Dh1VI45UUBQ34M0ribQQVwKR2MTYAUJhBfFrlFBF0ZtCWXdD1pnTR6JSgjWW7d6WBPxZXmwJuVyUlDoTxdI+h78LDJhGUFoqcoX0fKkU4BqxEAnqd1WBDnBJVOeult3aWDBmessTacfAroKdddp87KE6wdUPEAcc1dEKWpFy7nI1GMxdqNqCFO/sCLVsJyVycXJmAmTxy0AWvBryjZ2CwEjmVJiJ8NjFoJtjUwiwMFb3rrK7gM9CrgJ1VuC0GUSX6brLNtxkKuuTewhJ0L241yr7+BxHtuP9jh2sCI1a7TSiD8GgliIPUKPDCOZdo1R8RzEoxdxcwxPHG+jc1hcL8XhPUZDAtqOrK1HATJ8aLckCuIDiCM80HLEHsMc8ypantwhMYZ87K8HCQa7NBEFw0KsjGu0GfGpDr9ymyy1oLWzJjqa3UkDesDjMNLo+zI15DM9uMRO50s8Qk216ZD2PwZRbbQZjcWNyhPQE0y2zi43TELe2NH2KEXB1Y33m8DjHYOCjNOw+Eb/nCiyjiYZ475GfIUo0PkC2gueqRndDF5saPwLMfnqDOmBOWtw6DzFSGA3voGVcB+++689+7778AHL/zwxBdv/PHIJ6/88sw37/zz0Ecv/fTUV2/99dhnr/323Hd/ma59FYYR+G9YQItlyI2fhwxTso9EVXAsCI0PM0Ajgwoy0J9D/WGk4VAM+OPf/qBUFQVN41ixEuAMTJA/A/KPUEloRAPf15E2FMcEZICgbQqBs7lVQQkyYCBf4MDBJJTgL4UxEBt0QIMkYAKEWVhYCwuzMyfUgWYlVAI6dLgAFPpgMSKyDbcwlYYZoOMoQczJDxxCs2WYwX95uUcMptIGIy5j/g0/qB8llsiABs7ADFwM4gIV4EMjqnABM5BLtPa3wTaigxZZ7GLXLHIIH0IxhVOxH6bSiEYAPOIQYZSRjNZQRBnVj4yDKCIq1jDGIcbKj1y0YFn4d4g7knGOjdRDIyx5AB+myI9twJ8Q4xhHMzmEj3zs4Q758sVODiKUP7xHKjNkmzRg4YtI9EESppUXCc4xl4hs1xk1Oa+qLDCVVuzGE4cpIikAs5BBpN8kUHi6LPIgk6Yhoh8twsJdzZKTTQwiIX0YSFcOcUpOqKUg7sNJVG4zhausjx//sog4iGGWGMOgEKsoRBqhopdyZMc4e8LAuRVmgjLsIx+rqLNu8KCd/nvcpj6lwEdbUNRAIXjERZM0xh+YoVwr1GMjpijHLhbwknrsZ/y4VUByIJISrfzhIRqYRT2u8n0CKWUfsVBF+zVCkh59X0/qCbkoljQLlazf/jDhSaRmIQg6xeMjT9m1zllRkAdVYRswAUvT5aCp3gurWMdK1rKa9axoTata18rWtrr1rXCNa+jkerwY6I6uEYzgN4Sa15ckYT3vdKEBwUioKe7SoCHVK191MMFd4gixCZSiT3G2wtBBI4Kh++v75BiFGdooptmEUh/1WdQf8mAJR5TKGQMiBSBmkAqveyQdOqlOSfxpELN8Jj2ZqZt+iiMLazydafWglq2Gbrfj/kRHRProQ35Ow7h9nKqZLhrT3M7RnHS81nXDpU55rPG0VHwnMaM5XUTGtKZzlAloLQLT7jJgt1W84mjf60wbOnZe2/3kGsGRU3XibGdigO54jwIOjV4SlkGMr3QV7MSjBrWHFA0DLK3bABzaFr9IQaItxZmG086WvfT9ExCKWsg0FrKJrbQmcAOqB0rQbIGKzCQwsStgZeV3xVBconGhibFlppahFQ5CKI37F3LE4R417qh4adxGBA7yuPUF2ZOHuN9lNJK3WZDiXxaozPeO8KuYerENH1FV3y50mKVM5YjZMYJDlmWXH3hJ/YjwyRSKwRZrLK59ryrYbtxjyzMs/iQczGzQJNuGDCJwcy7v8EmpmEF1S4Yt01I8THnAc1hpueYoW7lSTYqhvx0ppaGfKib5Wjl5JQBMqsVHI9/Zjq6wjrWsZ03rWtv61rjOdVzvqusWlLbXjMkosFkAZ5xx9b+ss6xe+5bZnYmgXSAQgV25xWwaFfu+m6URZE0IW/uFCo0OIWG44gwCX0YDkHcbtAJLJJUKf9WeGAPrEk5K2yAfVaE8c/E0mMnBxiH4nJkaBBmwaCDkCETTtAAzkDC55G+WcY6ouPN67cjvSOt3KDnhMXkvrZuRRnrIWG4uMx1OVX1fvIcQH7lvE5qicNv3A8m9dyzbRboiYm7QTP0y/qGyyoMuo5wIIrf3fCFs1D4W4eTBPO67f63xWZazxuv0ZBivmlWxKRTMDx8o0ut9XIcQddu+pXjGVS5MqvayfqRjbsv2baBdpp22MUfjzrFr6qRLd+hokCHBPa7Ehxd9yi/9N5TzKtzxRsDpfg/xilFe9k/mpKfQYCaiRzDQRJMTCJFXqQq7MHfBM1jjDwhnObGJecYuGU41pOp/PyDpyM9d3e9uL5jpzU35hXuC95P4yktLUqiMFKHue2ocDrj0gkt66S/Ie66Uj7v+JN8nMHk+iCD7vegPG13cvr72t8/97nv/++APv/jHj70ak38F1BeCYecnVJ/ChLG5JyA0/kyhV2iIYtkI1aVPFTHZRNJ+ivaTIpO1EgCIWVC2PyEkd/KTfviBgPfTLg/kBJ+UUl6HgBJoJg54Uq7HfjPHB+4nfK43gQv4SSoQLXBEYlwBPzDQXk/AeXKEBfLkSy24asuwAw+1cDBoSi8YLcyXXbLzcC3Yg9gEAeGkE/nHXXvneJblS8VBGPhEXCxGZeWFdxgDfwwIVrviBPdDb8A0eu/kggrVV412WQUxhOBkIN72glAmR4wlWB54WaF3Yy+AeftTgS5WgR9mSLa3MApEC2aocpPVaNkiRkpFVTDIgw5QhP2BgvQnXlGlVJCUTaFCgzgYWvhBVUFICfyEUaZgk0QgMWNEqC5QOCwEZ4dV5Icr14TZZAoQhRQLFEGomGF1yFhxaD5YaGWHpXLoFGlGdFgj5WyFgIpzqHqHVYG7+EJt14bC9G5PSHcocIQlolT0loA/RG8ZhIACuHRL8Yf/M2JuZmpZhG5s9IQ8SImhUx2H81CiAANUwI7rES1vV44gYY6xcj6ISAWVRI+pdo/n1wMJAAA7'
logoCerema = 'R0lGODlhyABHAIIAMfstBC/TifepcLXxE6nt127nqvxnCfz9+ywAAAAAyABHAAID/ni63P4wykmrvTjrzbv/YCiOZGmeaKqubOu+cCzPdG3feK7vfO//wKBwSCwaj8ikcslsOp/QqHRKrVqv2KyWRDh0FYJDeEvuDM6BQVdgaBvG5biFkB6kxe63fE9Bn795cHyDDWd2Zwp5BoSMC4Z1A4mBJQKVloKNPIaHanh5ImyKipmaj5uSbpgaoaKKqqQ0m7Jgox2srZ+wOLK8qKkbt22WYpV6ujW8ybSuGcGvxzfJXb2etRbM0DgEyade1AIAiuFvz77GwMMY6Q6Xq5UQ6xKX5SncfwoEBdTV4QD+/uWsZcClKhSAMMXasBN3jkGbcOYULmAIL5iBcPRK2FuQ/i+APllfwP0bCSDCrYwPLE5iwCqMQJW/GqSCuegArpoyb0pkwY2jxwJAeSUk+e/ZrVWunOV8I8phIKVOdQrTqeriVKgrZjEAyjXoJotEIwi8FnPZzmqi4Kw0izPiO4IIxxJzIPdEJAdAf3Ltsm2A1HhLz1YAJ4xu2QPjDqNdeFEQNrYNWR0kWxhGvq5cA3xB+5SyYAq5GrRcEOzBWtKhbaY2Z7gyaMUnClzGnBkogTWtVG02DVvearZRG050AyH1aV9Ve4MpdnIFnQDQoXfVa1slg9u2C4j97Vtq6OaivRuH7WZy4LbDcZlP8Tx69L2y4xd4jD3fZZPc8Ys/e5zz/t/0wqnmGmoD+peWc+4l+MVsl8WEXXbxmZQYSqQl5h2BBRp4U3DJZfhSUi7lN0J77u2Fz2X5sDFGffJxpR9xFhz1zowIBZZSZzQS4xh5sI0GIHr9mTAdZprh0+KKXaF4226tZQiPiIw5CWWTHQZozVHhwejCbEkaGR9fX9rG5ItORoneBEEGWRyPGfq4WGAUlkCbbF4w+KB9Y6L5mAR13dhbn7x5yOZOhAlWmgxcAmXkZZrJx0FuNTKHYZuYiLjncnBSGSUc4JkTpwlcFnlAdnrdxoFKFmqpYXmCSGZUYqmqKqCVg7aVFi410OaldPZ9QNNq4tlIJq4capplZLFOg1WmC5jx1dFPebojlZkHTpoRVUutB2CH2hroCUQ1zCZqAe9pR8I8gLEzDzxiXIDuKzWaJK9RgH2qAmb4uBdtNlc064W+/MZBh4nPkbtvwFQwSieJByM8hambQezwxBRXbPHFGGes8cYcd+zxxyCHLPLIJJds8skop6zyyiy37PLLDCQAADs='
flecheGauche = 'R0lGODlhJAAkAIcAMSRSlJyuxEx+tDxqpNTa5HSGrFRypGSOvER2rLzGzOzu7GSCrExupHSezDxytFSGvMzS3DRenLS+1DxqrOTm5Pz6/IyevDRmpFx+tFR6rGyWxEx2rKyyxOTi5HSStGyOvMzO3PT29NTS1FR+tERqnNzi7MTO3GSKvFyGtDxinERurJSmxFx6pEx6rISWtKSyxNza3GSSxMTK1PTy9ExypISatERyrDRinLzCzDxurOzq7IyivDxmnNTW5FSCvERupFyKvJyuzFR2pGSOxER2tOzu9GyGtMzW5LTC1OTm7Pz+/FyCtFR6tEx2tKy2vHySvGySxPT2/NTW1FR+vERqpGSKxFyGvFx6rEx6tISWvNze3MTK3ExyrISavERytDRipDxutIyixDxmpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAJAAkAAcI/gCVCFQyQ4GCgiEGCix48KBCgg0dPhQYcUZChRUVPAxRkOHEhREvDuxocMZDhg0/QmxY4WRJiSM76jD5kaPNEBVy5rQ4wyJOnRVC3JwBVKWSChE1KgwDwaDBlgpRGkXakKbAFRG2KChSEOrAqlMZdlUS5cmHETJIegUJcyLSGToczjCyoIEQGQriEnVZcGrJuEkWQLFiBcsWtS7b9mx4sSUBIYMdAOECQufKkmu/khRpQogGH02IWMGQggGJ06gZiNlxdKJYiRIyQJlCBIvtA7iHDDlRBQiQKkOyqJTZU0mQDVAE2MZSGwERIs6fE2kiwEqX1ifjGgyxQjaWJsxb/tgGT148FgRTfFz/2LN9lhFQmn8n0oK+febnqfuwgP1jEg9LxADecgQWSKAPPoSRF1cfWcAFFBfkIGEOA0hY4QQUZljhADYQEQZcBn0URRhUMHHDFzdcgOIXK57I4otfXODFDnm19VAAPwhwwY489ugjjw58GFcRUwVAAhYDxLijkj/uKCGNJSlkU084IUFCEzkwqaKWPGJoQQVR5BRVVTQdQcMGOaQYow0O2OCFAyo4MCEYNQwX0kAlsGBDDirmwAMJQghhgKAM0GAAAwH0N9JLaxXBggoqfJFmD2NK9VFVMx1VAVEdLCCGhDeYUMFMM1Cgg6khsudUV4spoIUWigVEgMANOCjQgakdaHGrDjoYNdCmFFCQKwwd3FpDBDdwAAMEUsBAwUEWjZrScDoUqwUMp3agwwsAcKCFCDBI8SyVIYCl0qi4PpsXBRW8kEAHMOh60E9KvOSXQbwGJRRRp/aL05g2KvSWUw9R1VFmMgkc1MI4/eQwwzhFy/Cm//pq8cUYZ6zxxhsHBAA7'
flecheDroite = 'R0lGODlhJAAkAIcAMSxWjKS2zFSCtDxurNze3FR2pHyStER6tCxipMTGzExunGSSxPTy9MzS3DxinGyGrFyKvER2rOTq9GR+pERupFR+tHyizMTO3Nza3CxelDRqpEx2pNTa5DxqpGSCrOTm5Fx6pPT6/NTS1ERytLTC1FR6tEx6rDRmpMTK3ExyrGSOvOzq7ERypIyivDRelERqnKy6zFSGvOTi5FR6rHyavMTK1ExypHSezMzOzPz6/NTW5Ex+tOzu7JSqxDRalKS61FSCvDxyrNze5FR2rCxmpMTG1ExupGySxPT29MzW3DxmnHSOtFyOvER2tERurFx+rCxenDRqrEx2rDxqrGSCtOTm7NTW1Ex6tDRmrGSOxERyrIymvDRenERqpISexMzO3Pz+/Ozu9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAJAAkAAcI/gDBCBTIgAePgkgGEjRYkIFCMA0ZPhx4kGFChRUrPkQSkcfEhQV5XBzY0aHCkBo/hiyY4+HKgy4brjA5sSKDmQ9t4jyZkeZGBhyR5BhKNChQoURzIAnKkejHgTkMSlXYIoxUgy15enwKJmpDnz6oCAnTMCvFgly79lQo5UaBCzd5mAWZNmpGhTZuqLBB4ubEkHUPzlyhsECWCkdswJCbE+3JiA5btkTZZUGTHVlS/PgK86PNBlxs2DAymoIRCi8oqGhyZYcKClviOv7LYwWPIhUsZDmygHeW3yqAXDkwPIsTAzys+uRZsEgJCEEONIkwXUoT1sOvDIdw5YHtrbRn/hYxAYF49vPmzTeBAASEEAZzSTasIQUCa+L4h0s5kH84ECAzcJCWQDpIkQV22iWooII7XBFDBTOgMNtEOmhxRRQDZIjhABtqyGEQA0yhwRVaFNDZRzp0MQICLCJABIsvwujiCS4iIOIQSRjElQ4DaIHACUAGKWSQRAA5gAYTSNAQVxxMEcGPRUZ5QpEz/njCACcsEQIYUynEEQMMfEFBED9CGeSMQWIxBRQ0gAnfUC4lx0ARAwCx3xXXNTFCE1pMUSYWHWTQgmxPRZREF0NIUYCiohlhRAZYIhBFFFwEwJCOKkkVxkgLGaREECdMMYAScH03IUaQFcWADDIQ8IEDlByeQCoYH6xQxQo70Sbbl7VhYAUGGDgA6gsNMFBFqzLU+sGAXTHwQasEYPAsATI4gIUCCWCAg7S2AZVDt2k5O620z34AwAQ4cCDCrx8cdFRKT337wbwyGIRrD61iQAC1By01mW2B3YSrUv4iMe8KtQqFKngf2QWYQg5jFedyQwllMcEVK6VxwRpvrDCzIIcs8shgBAQAOw=='


# recherche du répertoire d'installation de "aperodedenis" (différent suivant les systèmes et les versions de système)

repertoire_script = os.path.dirname(sys.argv[0])
if not os.path.isdir(os.path.join(repertoire_script,"locale")):    
    repertoire_script=os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if not os.path.isdir(os.path.join(repertoire_script,"locale")):
    if __file__ in globals():
        repertoire_script = os.path.dirname(os.path.abspath(__file__))
if not os.path.isdir(os.path.join(repertoire_script,"locale")):
    try:
        if __cached__ in globals():
            repertoire_script = os.path.dirname(os.path.abspath(__cached__))
    except:
            pass
if not os.path.isdir(os.path.join(repertoire_script,"locale")):
    repertoire_script = os.getcwd()

if os.name=="nt":               
    # Répertoire de travail    
    repertoire_data = os.path.join(os.getenv('APPDATA'),'AperoDeDenis')
    try: os.mkdir(repertoire_data)
    except: pass
    if not os.path.isdir(repertoire_data):
        repertoire_data = repertoire_script
    langue = chargerLangue()
    if (langue != "en" and langue != "fr" and langue != "de" and langue != "es" and langue != "it" and langue != "zh"):
        frame = tkinter.Tk()
        initialiserLangue = InitialiserLangue(frame)
        initialiserLangue.mainloop()
else:           # sous Linux   
    if not os.path.isdir(repertoire_script):
        repertoire_script = os.getenv('HOME')
    repertoire_data = repertoire_script
    try: os.mkdir(repertoire_data)
    except: pass
    if not os.path.isdir(repertoire_data):
        repertoire_data = repertoire_script
    langue = chargerLangue()
    if(langue != "en" and langue != "fr" and langue != "de" and langue != "es" and langue != "it" and langue != "zh"):
        frame = tkinter.Tk()
        initialiserLangue = InitialiserLangue(frame)
        initialiserLangue.mainloop()
repertoire_langue = os.path.join( repertoire_script, 'locale')
try:
    traduction = gettext.translation('AperoDeDenis', localedir = repertoire_langue, languages=[langue])
    traduction.install()
except:
    def _(a=str(),b=str()):
        return a+b

if os.name=="nt":      
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible 
    titles = []
    EnumWindows(EnumWindowsProc(foreach_window), 0)     # liste des fenetres ouvertes dans titles 

# pour indiquer à pyproj ou se trouve le répertoire des data si installation via msi, la recherche se fait d'abord sur pyproj.datadir.get_data_dir()
# le même code peut servir avec ou sans l'installateur
os.environ['PROJ_LIB'] = os.path.join( repertoire_script, 'proj')
#print("PROJ_LIB",pyproj.datadir.get_data_dir())
############################ FIN DE L'INITIALISATION #########################################################

########################### Classe pour tracer les masques

class TracePolygone():
    def __init__(self, fenetre, image, masque,labelBouton=_('Tracer le masque')):  # fenetre : root de l'appli ; image : fichier image sur lequel tracer le polygone ; masque = nom du fichier à créer
        self.root = tkinter.Toplevel()                      #fenêtre spécifique à la saisie du masque
        self.root.title(_("Saisie sur la photo : ")+image)  # titre
        fenetreIcone(self.root)
        self.root.geometry( "900x900" )                     # Taille
        self.dimMaxiCanvas = 600                            # dimension max du canvas accueillant l'image       
        self.facteurZoom = 2                                # valeur du changement de niveau de zoom lorsque l'utilisateur "zoom" (par la molette de la souris)
        self.maxScale = 100                                 # Nb de zooms maximum autorisé
        self.listeSauveImages = list()                      # mémorisation des images zoomées pour accélérer le retour en arrière (deZoom)
        self.listePointsJPG = list()                        # liste des points du polygone
        self.polygone = False                               # deviendra vrai lorsque le polygone sera effectif
        self.file = image                                   # nom du fichier partagé, devient attribut de la classe
        self.nomMasque = masque                             # nom du fichier masque partagé (en principe : os.path.splitext(self.file)[0]+"_Mask.tif")
        self.inverse = False                                #pour inverser le masque : intervertit l'intérieur et l'extérieur
        # initialisations de l'affichage de l'image, dimensions du cadre, positionnement :
        
        self.imageFichier = Image.open(self.file)                                                   # ouverture de la photo
        self.largeurImageFichier, self.hauteurImageFichier = self.imageFichier.size                 # dimensions
        if self.hauteurImageFichier>self.largeurImageFichier:                                       # plus haut que large : on calcule l'échelle sur la hauteur
            self.hauteurCanvas = self.dimMaxiCanvas
            self.scale = self.hauteurCanvas/self.hauteurImageFichier
            self.largeurCanvas = int(self.largeurImageFichier * self.scale)                         # largeur correspondante pour conserver les proportions
        else:                                                                                       # plus large que haut :
            self.largeurCanvas = self.dimMaxiCanvas
            self.scale = self.largeurCanvas/self.largeurImageFichier                                # on cale sur l'échelle sur la largeur
            self.hauteurCanvas = int(self.hauteurImageFichier * self.scale)                         # hauteur correspondante pour conserver les proportions
            
        self.frame = ttk.Frame(self.root, borderwidth = 2,relief = 'sunken')                        # cadre pour la photo et les boutons
        self.frame.config(cursor="arrow")                                                           # le curseur indique si le tracé est en cours, ou le drag-and-drop 
        self.canvas = tkinter.Canvas(self.frame,width = self.largeurCanvas, height = self.hauteurCanvas) # pour accueillir l'image de la photo
        self.xNW,self.yNW,self.xSE,self.ySE = 0,0,self.largeurImageFichier,self.hauteurImageFichier   # position image dans le cadre
        self.retailleEtAffiche()                                                                    # affiche l'image retaillée dans le canvas
        self.listeSauveImages.append((self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale))     # sauvegarde du début, pour retour de zoom, qui ne sera pas effacée
        self.canvas.pack(fill='both',expand = 1)                                                    # met le canvas dans le cadre
        self.frame.pack()                                                                           # affiche le cadre (enfin !)
        
        # Initialisation des boutons de la souris, du gestionnaire d'événements, du bouton pour tracer, label pour aide
        # http://python.developpez.com/faq/?page=Evenements-Clavier
        
        self.root.bind("<Button-1>",self.bouton1)
        self.root.bind("<ButtonRelease-1>",self.finDrag)
        self.root.bind("<MouseWheel>",self.molette)                                             
        self.root.bind("<4>",self.moletteLinux4)
        self.root.bind("<5>",self.moletteLinux5)    
        self.root.bind("<Motion>",self.move)
        self.root.bind("<B1-Motion>",self.b1Move)
        self.root.bind("<Double-Button-1>",self.b1Double)
        self.root.bind("<Delete>",self.delete)
        self.root.bind("a",self.delete)

        self.frame2 = ttk.Frame(self.root, borderwidth = 2,relief = 'sunken')                        # cadre pour la photo et les boutons
        self.boutonInverser = ttk.Button(self.frame2, text=_("Inverser"),command = self.inverser)
        self.boutonValider = ttk.Button(self.frame2, text=_("Valider"),command = self.quitter)
        self.boutonAbandon = ttk.Button(self.frame2, text=_("Abandon"),command = self.abandon)        
        self.boutonTracer = ttk.Button(self.frame2, text=labelBouton,command = self.tracerMasqueBis)
        self.boutonAide = ttk.Label (self.frame2,
                                     text=  "\n" + _("molette de la souris = zoom,") + "\n"+\
                                            _("utilisable avant ET pendant le tracé") + "\n"+\
                                            _("glisser-déposer actif avant le tracé=") + "\n\n"+\
                                            _("Tracer :") + "\n"+\
                                            _("Clic gauche : ajouter un point;\n double clic gauche : fermer le polygone,") +"\n"+\
                                            _("Touche Del pour supprimer un point ou le polygone,") + "\n")      
        self.boutonAide.pack(side='left',pady=2,padx=2)
        self.boutonTracer.pack(side='left',pady=2,padx=8)
        self.boutonInverser.pack(side='left',pady=2,padx=8)
        self.boutonValider.pack(side='left',pady=2,padx=8)
        self.boutonAbandon.pack(side='left',pady=2,padx=8)
        self.frame2.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.quitter)    # Fonction a éxécuter lors de la sortie du programme
        self.root.transient(fenetre)                            # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.root.grab_set()
        fenetre.wait_window(self.root)                          
        
    def quitter(self):
        # libère les ressources images pour ne pas les "bloquer"
        
        try: self.imageFichier.close()
        except: pass
        try: self.imageMasque.close()
        except: pass
        try: del self.imageFichier
        except: pass
        try: del self.imageMasque
        except: pass     
        self.root.destroy()
        
    def abandon(self):                                          # Abandon utilisateur: polygone éventuel invalide
        self.polygone=False
        self.quitter()
        
    def bouton1(self,event):                                    # l'utilisateur appuie sur le bouton 1 de la souris
        if event.widget!=self.canvas:                           # si le clic n'est pas sur l'image (canvas=frame=image) on ne fait rien
            return
        try : self.bulle.destroy()
        except: pass
        if self.frame.cget("cursor").string=="plus":            # le cursor "plus" indique l'ajout d'un point
            self.ajouterPointPolyligne(event)                   # on ajoute (ou modifie) le point sur l'image
        if self.frame.cget("cursor").string=="arrow":           # sinon : drag and drop : bouton 1 enfoncé; on initialise le déplacement de l'image
            self.xDrag,self.yDrag = event.x,event.y
            self.frame.config(cursor="hand2")                   # cursor "main" pour déplacer l'image

    def finDrag(self,event):                                    # l'utilisateur relache le bouton 1 de la souris : fin du "drag"
        if self.frame.cget("cursor").string=="hand2":
            self.b1Move(event)                                  
            self.frame.config(cursor="arrow")
            
    def b1Move(self,event):                                     # l'utilisateur déplace la souris avec le bouton 1 enfoncé : déplacement de l'image

        if event.widget!=self.canvas: return                    # si le clic n'est pas sur l'image (canvas=frame=image) on ne fait rien        
        if self.frame.cget("cursor").string=="hand2":
            self.xNW,self.yNW = self.xNW - int((event.x-self.xDrag) / self.scale),self.yNW - int((event.y-self.yDrag) / self.scale)
            self.xSE,self.ySE = self.xSE - int((event.x-self.xDrag) / self.scale),self.ySE - int((event.y-self.yDrag) / self.scale)
            self.xDrag,self.yDrag = event.x,event.y
            self.retailleEtAffiche()
        if self.frame.cget("cursor").string=="plus":
            self.ajouterPointPolyligne(event)
            self.afficherPolyligne()
            self.retirerPointPolyligne()
            
    def move(self,event):
        if event.widget!=self.canvas: return                    # si le clic n'est pas sur l'image (canvas=frame=image) on ne fait rien
        if self.frame.cget("cursor").string=="plus":
            self.ajouterPointPolyligne(event)                   # ajoute provisoirement le point courant
            self.afficherPolyligne()                            # affiche la polyligne avec le point courant
            self.retirerPointPolyligne()                        # retire le point courant qui n'était que provisoire
            
    def delete(self,event):                                     # retirer un point dans le polygone en construction
        if self.frame.cget("cursor").string=="plus":
            self.retirerPointPolyligne()
            self.afficherPolyligne()                            # affiche la polyligne 
        if self.frame.cget("cursor").string=="arrow":
            self.tracerMasqueBis()
        
    def b1Double(self,event):                                   # pour clore la polyligne
        if event.widget!=self.canvas: return                    # si le clic n'est pas sur l'image (canvas=frame=image) on ne fait rien
        if self.frame.cget("cursor").string=="plus":            # le cursor "plus" indique l'ajout d'un point : on clot
            if self.listePointsJPG.__len__()<=1:                #polygone avec trop peu de point
                self.infoBulle(event,_("Il faut au moins 2 points dans le polygone."))
                return            
            self.tracerMasqueBis()                              # on désactive le bouton de tracé
            self.afficherPolygone()
            self.frame.config(cursor="arrow")
            self.polygone=True
            self.sauverMasque()
            self.ouvrirMasque()
            self.boutonTracer.state(["!active","!focus","!pressed","!focus",'!selected'])

    def molette(self,event):                                    # l'utilisateur utilise la molette de la souris
        if event.widget!=self.canvas:
            return       
        if event.delta<0:                                       # zoom avant par molette
            self.redrawDeZoom()           
        elif event.delta>0:                                     # zoom arrière par molette delta >0
            self.redrawZoom(event)
               
    def moletteLinux4(self,event):                              # l'utilisateur Linux utilise la molette de la souris vers l'avant
        if event.widget!=self.canvas:
            return       
        self.redrawDeZoom()           

    def moletteLinux5(self,event):                              # l'utilisateur Linux utilise la molette de la souris vers l'arrière
        if event.widget!=self.canvas:
            return       
        self.redrawZoom(event)  

    def redrawZoom(self, event):                                # l'utilisateur zoom avant avec la molette de la souris : mémo du zoom précédent
        if self.scale>self.maxScale:                            # si l'échelle passe à plusieurs pixels écran pour un pixel image on arrête
             self.infoBulle(event,texte=_("Zoom maximum atteint")) # l'utilisateur est informé
             return
        self.listeSauveImages.append((self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale)) # sauvegarde pour retour arrière (redrawDeZoom)       
        self.positionNouveauZoom(event.x,event.y)               # calcule les positions du centre, du coin nw pour le nouveau zoom
        self.zoomRetailleAffiche()                              # on taille l'image pour le zoom et affiche    
        
    def redrawDeZoom(self):                                     # l'utilisateur zoom arrière avec la molette de la souris : retour au zoom mémorisé précédent   
        try : self.bulle.destroy()
        except: pass
        if len(self.listeSauveImages)>1:                        # précédent zoom arrière, suppression
            self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale = self.listeSauveImages.pop()
        else:
            self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale = self.listeSauveImages[0]  # zoom de départ, conservé
        self.afficheImage()
       
    def positionNouveauZoom(self,xFrame,yFrame):                # à partir des coordonées dans le cadre
        self.xyCanvasVersJPG(xFrame,yFrame)                     # renvoie self.xJPG et self.yJPG : position dans l'image initiale
        self.scale *= self.facteurZoom                          # nouvelle échelle, multiplié par le facteur de Zoom
        self.xyJPGVersCanvas(self.xJPG,self.yJPG)               # renvoie la position xZoom,yZoom dans le nouveau zoom et le nouveau cadre du point cliqué
              
    def xyCanvasVersJPG(self,xFrame,yFrame):     
        self.xJPG = int(self.xNW + xFrame / self.scale)         # xJPG,yJPG : position du pixel dans l'image initiale :
        self.yJPG = int(self.yNW + yFrame / self.scale)
        return(self.xJPG,self.yJPG)

    def xyJPGVersCanvas(self,xJPG,yJPG):                        # xJPG,yJPG : position dans l'image originale (Jpeg)                              
        self.xFrame= (xJPG - self.xNW) * self.scale             # xFrame,yFrame : position dans l'image dans le cadre
        self.yFrame= (yJPG - self.yNW) * self.scale 
        return(self.xFrame,self.yFrame)
    
    def zoomRetailleAffiche(self):       
        self.xNW,self.yNW=int(self.xJPG-self.largeurCanvas/(self.facteurZoom*self.scale)),int(self.yJPG-self.hauteurCanvas/(self.facteurZoom*self.scale))
        self.xSE,self.ySE=int(self.xJPG+self.largeurCanvas/(self.facteurZoom*self.scale)),int(self.yJPG+self.hauteurCanvas/(self.facteurZoom*self.scale))
        self.retailleEtAffiche()
        
    def retailleEtAffiche(self):
        self.imgi = self.imageFichier.crop((self.xNW,self.yNW,self.xSE,self.ySE))
        self.img = self.imgi.resize((self.largeurCanvas,self.hauteurCanvas))
        self.afficheImage()
        
    def afficheImage(self):                                     # Remplace l'image actuelle du canvas par l'image self.img,
                                                                # positionnée dans le canvas suivant le calcul de "positionNouveauZoom"
        try: self.canvas.delete(self.imgTk_id)                  # si jamais il n'y a pas encore d'image
        except: pass
        self.imgTk = ImageTk.PhotoImage(self.img)      
        self.imgTk_id = self.canvas.create_image(0,0,image = self.imgTk,anchor="nw")
        self.afficheMasque()
                
    def tracerMasqueBis(self):                                  # appui sur un bouton "tracermasque" : on active le tracé
        if self.frame.cget("cursor").string=="plus":            # Nouvel appui sur le bouton : on arrête la saisie
            self.frame.config(cursor="arrow")                   # on remet le cursor "normal"
            return
        self.listePointsJPG=list()                              # nouvelles données
        self.polygone = False                                   # pas de polygone fini
        self.menagePol()
        self.fermerMasque()                                     # efface le masque affiché en cours
        self.frame.config(cursor="plus")                        # curseur en mode ajout          
        self.boutonTracer.state(["pressed","!focus",'selected'])# etat séléctionné du bouton

    def retirerPointPolyligne(self):
        try: self.listePointsJPG.pop()
        except: pass
            
    def ajouterPointPolyligne(self,event):
        self.listePointsJPG.append(self.xyCanvasVersJPG(event.x,event.y))
        self.afficherPolyligne()

    def afficheMasque(self):
        if self.polygone: self.afficherPolygone()
        else: self.afficherPolyligne() 
            
    def afficherPolyligne(self):
        if self.frame.cget("cursor").string=="plus": 
            self.menagePol()
            listePointsCanvas=[self.xyJPGVersCanvas(e[0],e[1]) for e in self.listePointsJPG]
            if len(listePointsCanvas)>1:
                self.pol = self.canvas.create_line(listePointsCanvas,fill='#f00')

    def afficherPolygone(self):
        self.menagePol()
        self.pol = self.canvas.create_polygon([self.xyJPGVersCanvas(e[0],e[1]) for e in self.listePointsJPG],fill='#f00',outline='#0f0', stipple='gray25')
              
    def infoBulle(self,event,texte=" "):                                # affiche une infobulle sous le curseur.
        i = ImageDraw.Draw(self.imageFichier)
        l,h = i.textsize(texte,font=None)
        try: self.bulle.destroy()
        except Exception as e: print(_("Erreur suppression d'info bulle : "),str(e))
        self.bulle = tkinter.Toplevel()                                 # nouvelle fenêtre pour l'info bulle
        self.bulle.overrideredirect(1)                                  # sans le bordel tout autour
        self.bulle.geometry("%dx%d%+d%+d" % (l+10,h+6,event.x_root+15,event.y_root))  # position du coin nw de la fenêtre par rapport au curseur
        ttk.Label(self.bulle,text = texte,background="#ffffaa",relief = 'solid').pack()    # texte, la taille de la fenêtre s'adapte au texte, style infobulle
        #self.bulle.mainloop()                                          # boucle d'attente d'événement sur la fenêtre (pas de pack possible)

    def inverser(self):
        self.inverse = not self.inverse
        self.sauverMasque()
        self.ouvrirMasque()
        
    def sauverMasque(self):                                             # création d'une image 200x200 avec un fond de couleur noire        
        if self.inverse:
            img = Image.new("1",self.imageFichier.size,color=255)       # 1 bit par pixel (noir et blanc (la couleur par défaut est le noir (http://pillow.readthedocs.org/en/latest/reference/Image.html)
            dessin = ImageDraw.Draw(img)                                # création d'un objet Draw
            dessin.draw
            dessin.polygon(self.listePointsJPG,fill="black",outline="green")
            img.save(self.nomMasque,"TIFF")
        else:
            img = Image.new("1",self.imageFichier.size,color=0)         # 1 bit par pixel (noir et blanc (la couleur par défaut est le noir (http://pillow.readthedocs.org/en/latest/reference/Image.html)
            dessin = ImageDraw.Draw(img)                                # création d'un objet Draw
            dessin.draw
            dessin.polygon(self.listePointsJPG,fill="white",outline="green")
            img.save(self.nomMasque,"TIFF")

    def ouvrirMasque(self):
        try: self.cadre.destroy()
        except: pass
        self.cadre = ttk.Frame(self.root)
        self.cadre.pack(pady=15)
        self.imageMasque = Image.open(self.nomMasque)
        self.canvasMasque = tkinter.Canvas(self.cadre,width = self.largeurCanvas/4, height = self.hauteurCanvas/4)        
        self.imageMasqueRetaille = self.imageMasque.resize((int(self.largeurCanvas/4),int(self.hauteurCanvas/4)))        
        self.iMasqueTk = ImageTk.PhotoImage(self.imageMasqueRetaille)
        self.imasqueTk_id = self.canvasMasque.create_image(0,0,image = self.iMasqueTk, anchor="nw")
        self.canvasMasque.pack(fill='both',expand = 1)

    def fermerMasque(self):
        try: self.canvasMasque.delete("all")
        except: pass

    def menagePol(self):
        try: self.canvas.delete(self.pol)
        except: pass

################# Classe CalibrationGPS : placer des points repérés en XYZ sur des images.
# création d'un dictionnaire dicoPointsJPG : clé = tuple (nom du point, nom de la photo); valeur = tuple (X,Y)

class CalibrationGPS:                       # Paramètres : fenetre maitre,Nom du fichier image, liste des noms des boutons, dictionnaire des points déjà placés
    
    def __init__(self,fenetre,image,points,dejaPlaces,position="900x900+100+100"):        
        # controle présence photo :
        
        if image.__len__()==0:              # pas d'image
            return
        if image.__class__()==list():
            image = image[0]
            
        self.root = tkinter.Toplevel()
        self.root.title( _("Calibration GCP ")+image)
        self.root.title(_("Position des points sur la photo  : ")+os.path.basename(image))       # titre
        fenetreIcone(self.root)
        self.root.geometry( position )    
        self.dimMaxiCanvas = 600            # dimension max du canvas accueillant l'image
        self.facteurZoom = 2                # valeur du changement de niveau de zoom lorsque l'utilisateur "zoom" (par la molette de la souris)
        self.maxScale = 50                 # zoom max autorisé
        self.listeCouleurs = ["black","white","blue","red","green","yellow"]
        self.couleurTexte = self.listeCouleurs[0]
        self.xyInfo = True
        self.listeSauveImages = list()      # mémorisation des images zoomés pour accélérer le retour en arrière (deZoom)
        self.xDrag = -1
        self.yDrag = -1
        self.imgTk_id = 'none'
        self.dicoBoutons = dict()           # key = nom du point, value = référence du bouton correspondant dans la fenêtre, dico utile localement        
        self.dicoPointsJPG = dejaPlaces     # key = (nom du point,nom de la photo), value = tuple à 2 valeurs : (x,y dans le jpeg) dico utile globalement
        self.retourSiAbandon = dict(dejaPlaces)
        self.boutonActif = ttk.Button()
        self.tempo = 0
        self.points = points                # pour la suppression d'un point
        self.afficheXY = False              # on n'affiche pas (par défaut) les coordonnées xy des points placés sur une image
        
        # initialisations de l'affichage de l'image, dimensions du cadre, positionnement :

        self.affichePhoto(image)
        
        # Initialisation des boutons de la souris, du gestionnaire d'événements, des boutons pour placer les points
        self.placerBoutons(points)

        # boutons de controle :
        
        self.frame3 = ttk.Frame(self.root,borderwidth = 2,relief = "sunken")
        self.boutonValider = ttk.Button(self.frame3, text=_("Valider"),command = self.quitter)
        self.boutonValiderPrecedent = ttk.Button(self.frame3, image=dataFlecheGauche,command = self.precedent)        
        self.boutonValiderSuivant = ttk.Button(self.frame3, image=dataFlecheDroite,command = self.suivant)
        self.boutonSupprimerUnPoint = ttk.Button(self.frame3, text=_("Supprimer des points"),command = self.supprimerUnPoint)        
        self.boutonAbandon = ttk.Button(self.frame3, text=_("Abandon"),command = self.abandon)
        self.boutonValider.pack(side='left',pady=2,ipady=2)
        self.boutonValiderPrecedent.pack(side='left',pady=2,ipady=2,padx=5)        
        self.boutonValiderSuivant.pack(side='left',pady=2,ipady=2,padx=5)
        self.boutonSupprimerUnPoint.pack(side='left',pady=2,ipady=2,padx=5)       
        self.boutonAbandon.pack(side='left',pady=2,ipady=2,padx=5)
        self.frame3.pack(pady=10)
        self.frame4 = ttk.Frame(self.root,borderwidth = 2,relief = "sunken")        
        self.boutonchangerCouleurTexte = ttk.Button(self.frame4, text=_("Changer la couleur des libellés"),command = self.changerCouleurTexte)
        self.boutonchangerAffichageXY = ttk.Button(self.frame4, text=_("Afficher les coordonnées pixels xy des points"),command = self.supprimeXY)
        self.boutonchangerCouleurTexte.pack(side='left',pady=2,ipady=2,padx=5)
        self.boutonchangerAffichageXY.pack(side='left',pady=2,ipady=2,padx=5)
        self.frame4.pack(pady=10)

        # message d'information

        self.frame5 = ttk.Frame(self.root,borderwidth = 2)
        ttk.Label(self.frame5,text=_("Utiliser la molette pour zoomer/dezoomer pendant la saisie.")).pack()
        ttk.Label(self.frame5,text=_("la position du curseur devient le centre du zoom suivant.")).pack()        
        self.frame5.pack()
        
        # évènements

        self.root.bind("<Button-1>",self.bouton1)
        self.root.bind("<ButtonRelease-1>",self.finDrag)
        self.root.bind("<MouseWheel>",self.molette)
        self.root.bind("<B1-Motion>",self.b1Move)
        self.root.bind("<4>",self.moletteLinux4)
        self.root.bind("<5>",self.moletteLinux5)
        self.boutonValiderPrecedent.bind("<Enter>",self.infoPrecedent)   # http://tkinter.fdex.eu/doc/event.html
        self.boutonValiderSuivant.bind("<Enter>",self.infoSuivant)
        self.boutonValiderPrecedent.bind("<Leave>",self.infoClear)
        self.boutonValiderSuivant.bind("<Leave>",self.infoClear)
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)    # Fonction a éxécuter lors de la sortie du programme
        self.root.transient(fenetre)                            # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.root.grab_set()
        fenetre.wait_window(self.root)

    def affichePhoto(self,photo):        
        self.file = photo                   # nom de la photo avec chemin (au moins relatif)        
        self.imageFichier = Image.open(self.file)
        self.largeurImageFichier, self.hauteurImageFichier = self.imageFichier.size
        if self.hauteurImageFichier>self.largeurImageFichier:                           # plus haut que large : on calcule l'échelle sur la hauteur
            self.hauteurCanvas = self.dimMaxiCanvas
            self.scale = self.hauteurCanvas/self.hauteurImageFichier
            self.largeurCanvas = int(self.largeurImageFichier * self.scale)             # largeur correspondante pour conserver les proportions
        else:                                                                           # plus large que haut :
            self.largeurCanvas = self.dimMaxiCanvas
            self.scale = self.largeurCanvas/self.largeurImageFichier                    # on cale sur l'échelle sur la largeur
            self.hauteurCanvas = int(self.hauteurImageFichier * self.scale)             # hauteur correspondante pour conserver les proportions           
        self.frame = ttk.Frame(self.root, borderwidth = 2,relief = "sunken")
        self.frame.config(cursor="arrow")
        self.canvas = tkinter.Canvas(self.frame,width = self.largeurCanvas, height = self.hauteurCanvas)
        self.xNW,self.yNW,self.xSE,self.ySE=0,0,self.largeurImageFichier,self.hauteurImageFichier
        self.retailleEtAffiche()                                                             # affiche l'image retaillée, coin nw en 0,0
        self.listeSauveImages.append((self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale))   # sauvegarde propre du début, qui ne sera pas effacée
        self.canvas.pack(fill='both',expand = 1)
        self.frame2 = ttk.Frame(self.root,borderwidth = 2,relief = "sunken")
        self.frame.pack(side='top')             
        self.frame2.pack(side='top')        

    def infoPrecedent(self,event):
        interface.infoBulle(_("valide + photo précédente"))

    def infoSuivant(self,event):
        interface.infoBulle(_("valide + photo suivante"))

    def infoClear(self,event):
        try: interface.bulle.destroy()
        except: pass 
        
    def placerBoutons(self,listePoints):                        # Place les boutons correspondants aux points de listePoints
        textePoint = _("Placer le point ")                         # on raccourcit les textes si il y bcp de points  (30 max))
        padding = 5                                             # version 2.41
        if listePoints.__len__()>5:
            textePoint = _("Point ")
            padding = 3
        if listePoints.__len__()>10:
            textePoint = ""
            padding = 1
        for e in listePoints:                                   # un bouton pour chaque référence de la liste des boutons;
            b = ttk.Button(self.frame2, text=textePoint+e[0],cursor="plus",width=0,command = lambda i = (e[0],e[1]) :self.activerBouton(i))
            self.dicoBoutons.update({e[0]:b})                      # mémo dans un dico du nom du point / références du bouton
            b.pack(side="left",padx=padding)

    def bouton1(self,event):                                    # l'utilisateur appuie sur le bouton 1 de la souris
        try : self.bulle.destroy()
        except: pass                                            # ménage écran (infobulle supprimée)
        if event.widget!=self.canvas:                           # si le clic n'est pas sur l'image (canvas=frame=image) on ne fait rien
            return
        if self.frame.cget("cursor").string=="plus":                   # le cursor "plus" indique l'ajout d'un point
            self.ajouterPoint(event)                            # on ajoute (ou modifie) le point sur l'image
        if self.frame.cget("cursor").string=="arrow":                                      # sinon : drag and drop : bouton 1 enfoncé; on initialise le déplacement de l'image
            self.xDrag,self.yDrag = event.x,event.y
            self.frame.config(cursor="hand2")
          
    def finDrag(self,event):                                    # l'utilisateur relache le bouton 1 de la souris : fin du "drag"
        if self.frame.cget("cursor").string=="hand2":
            self.b1Move(event)
            self.frame.config(cursor="arrow")

    def b1Move(self,event):                                     # l'utilisateur déplace la souris avec le bouton 1 enfoncé : déplacement de l'image        
        if self.frame.cget("cursor").string=="hand2":
            self.xNW,self.yNW = self.xNW - int((event.x-self.xDrag) / self.scale),self.yNW - int((event.y-self.yDrag) / self.scale)
            self.xSE,self.ySE = self.xSE - int((event.x-self.xDrag) / self.scale),self.ySE - int((event.y-self.yDrag) / self.scale)
            self.xDrag,self.yDrag = event.x,event.y
            self.retailleEtAffiche()
            
    def molette(self,event):                                    # l'utilisateur utilise la molette de la souris
        if event.widget!=self.canvas:
            return       
        if event.delta<0:                                       # zoom avant par molette
            self.redrawDeZoom()           
        elif event.delta>0:                                     # zoom arrière par molette delta >0
            self.redrawZoom(event)

    def moletteLinux4(self,event):                              # l'utilisateur Linux utilise la molette de la souris vers l'avant
        if event.widget!=self.canvas:
            return       
        self.redrawDeZoom()           

    def moletteLinux5(self,event):                              # l'utilisateur Linux utilise la molette de la souris vers l'arrière
        if event.widget!=self.canvas:
            return       
        self.redrawZoom(event)    

                
    def redrawZoom(self, event):                                # l'utilisateur zoom avant avec la molette de la souris : mémo du zoom précédent   
        if self.scale>self.maxScale:                                        # si l'échelle passe à plusieurs pixels écran pour un pixel image on arrête
             self.infoBulle(event,texte=_("Zoom maximum atteint"))                         # l'utilisateur est informé
             return
        self.listeSauveImages.append((self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale)) # sauvegarde pour retour arrière (redrawDeZoom)       
        self.positionNouveauZoom(event.x,event.y)                                               # calcule les positions du centre, du coin nw pour le nouveau zoom
        self.zoomRetailleAffiche()                                                              # on taille l'image pour le zoom et affiche    
        
    def redrawDeZoom(self):                                                                     # l'utilisateur zoom arrière avec la molette de la souris : retour au zoom mémorisé précédent   
        try : self.bulle.destroy()
        except: pass
        if len(self.listeSauveImages)>1:                                                        # précédent zoom arrière, suppression
            self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale = self.listeSauveImages.pop()
        else:
            self.xNW,self.yNW,self.xSE,self.ySE,self.img,self.scale = self.listeSauveImages[0]  # zoom de départ, conservé
        self.afficheImage()
       
    def positionNouveauZoom(self,xFrame,yFrame):                # à partir des coordonées dans le cadre
        self.xyCanvasVersJPG(xFrame,yFrame)                     # renvoie self.xJPG et self.yJPG : position dans l'image initiale
        self.scale *= self.facteurZoom                          # nouvelle échelle, multiplié par le facteur de Zoom
        self.xyJPGVersCanvas(self.xJPG,self.yJPG)               # renvoie la position xZoom,yZoom dans le nouveau zoom et le nouveau cadre du point cliqué
      
    def xyCanvasVersJPG(self,xFrame,yFrame):     
        self.xJPG = int(self.xNW + xFrame / self.scale)         # xJPG,yJPG : position du pixel dans l'image initiale :
        self.yJPG = int(self.yNW + yFrame / self.scale)

    def xyJPGVersCanvas(self,xJPG,yJPG):                        # xJPG,yJPG : position dans l'image originale (Jpeg)                              
        self.xFrame = (xJPG - self.xNW) * self.scale             # xFrame,yFrame : position dans l'image dans le cadre
        self.yFrame = (yJPG - self.yNW) * self.scale 

    def zoomRetailleAffiche(self):       
        self.xNW,self.yNW = int(self.xJPG-self.largeurCanvas/(self.facteurZoom*self.scale)),int(self.yJPG-self.hauteurCanvas/(self.facteurZoom*self.scale))
        self.xSE,self.ySE = int(self.xJPG+self.largeurCanvas/(self.facteurZoom*self.scale)),int(self.yJPG+self.hauteurCanvas/(self.facteurZoom*self.scale))
        self.retailleEtAffiche()
        
    def retailleEtAffiche(self):
        self.imgi = self.imageFichier.crop((self.xNW,self.yNW,self.xSE,self.ySE))
        self.img = self.imgi.resize((self.largeurCanvas,self.hauteurCanvas))
        self.afficheImage()
        
    def afficheImage(self):                                     # Remplace l'image actuelle du canvas par l'image self.img, positionnée dans le canvas suivant le calcul de "positionNouveauZoom"
        self.canvas.delete(self.imgTk_id)
        self.imgTk = ImageTk.PhotoImage(self.img)
        self.imgTk_id = self.canvas.create_image(0,0,image = self.imgTk, anchor="nw")
        self.afficherTousLesPoints()

    def afficherTousLesPoints(self):                            # affiche les point s de l'imager en cours sur le canvas en cours (info dans le dico self.dicoPointsJPG)
        for cle in self.dicoPointsJPG:
            if cle[1]==self.file:
                self.canvas.delete(cle[0])                      # suppression du point en cours (sans erreur si absent)
                self.afficheUnPoint(self.dicoPointsJPG[cle][0],self.dicoPointsJPG[cle][1],bouton=cle[0])

    def afficheUnPoint(self,xJPG,yJPG,bouton):
        self.xyJPGVersCanvas(xJPG,yJPG)
        self.canvas.create_oval(self.xFrame-5, self.yFrame-5,self.xFrame+5, self.yFrame+5,fill='yellow',tag=bouton)
        if self.afficheXY:
            self.canvas.create_text(self.xFrame, self.yFrame+20,text = bouton+" x="+str(xJPG)+" y="+str(yJPG),tag=bouton,fill=self.couleurTexte)
        else:
            self.canvas.create_text(self.xFrame, self.yFrame+20,text = bouton,tag=bouton,fill=self.couleurTexte)
      
    def activerBouton(self,boutonChoisi):                                                               # appui sur un bouton "ajouter un point"
        self.boutonActif.state(["!active","!focus","!pressed",'!selected'])                             # RAZ état de l'ancien bouton
        if self.boutonActif==self.dicoBoutons[boutonChoisi[0]]:                                         # réappuie sur le bouton actif : on le désactive  et on quitte
            self.frame.config(cursor="arrow")            
            self.boutonActif = ttk.Button()
            return                                                                                      # dans ce cas, c'est fini      
        self.boutonActif  = self.dicoBoutons[boutonChoisi[0]]
        self.boutonChoisi = boutonChoisi[0]                                                             # mémo bouton en cours
        self.numBoutonChoisi = boutonChoisi[1]
        self.boutonActif.state(["active","focus","pressed","focus",'selected'])                         # activation du nouveau bouton
        self.frame.config(cursor="plus")          

    def ajouterPoint(self,event):                                       # clic sur le canvas avec le bouton self.boutonActif : ajoute la position du point sur le canvas et dans le dico local "widget" et global "points"
        self.canvas.delete(self.boutonChoisi)                           # suppression de l'item via le tag (qui ne doit pas comporter d'espace.       
        self.xyCanvasVersJPG(event.x,event.y)
        self.dicoPointsJPG[(self.boutonChoisi,self.file,self.numBoutonChoisi)] = (self.xJPG,self.yJPG)
        #self.afficheUnPoint(self.xJPG,self.yJPG,self.boutonChoisi)
        self.afficheImage()

    def changerCouleurTexte(self):
        self.listeCouleurs.insert(0,self.listeCouleurs.pop()) # pythonesque : passe de (1,2,3) à (3,1,2)
        self.couleurTexte = self.listeCouleurs[0]
        self.afficherTousLesPoints()

    def supprimeXY(self):
        self.afficheXY = not self.afficheXY
        if self.afficheXY:
            self.boutonchangerAffichageXY.config(text=_("Supprimer les coordonnées pixels xy des points placés"))
        else:
            self.boutonchangerAffichageXY.config(text=_("Afficher les coordonnées pixels xy des points placés"))
        self.afficheImage()
        
    def infoBulle(self,event,texte=" "):                                # affiche une infobulle sous le curseur.
        try: self.bulle.destroy()
        except: pass
        self.bulle = tkinter.Toplevel()                                 # nouvelle fenêtre
        self.bulle.overrideredirect(1)                                  # sans le bordel tout autour
        self.bulle.geometry("+%d+%d"%((event.x_root,event.y_root+20)))  # position du coin nw de la fenêtre par rapport au curseur
        ttk.Label(self.bulle,text = texte,background="#ffffaa",relief = 'solid').pack()    # texte, la taille de la fenêtre s'adapte au texte, style infobulle
        #self.bulle.mainloop()                                           # boucle d'attente d'événement sur la fenêtre (pas de pack possible)

    def quitter(self):
        self.root.destroy()

    def suivant(self): # photo suivante sur la saisie des points/polylignes/polylignes 
        index = interface.photosAvecChemin.index(self.file)
        if index+1==interface.photosAvecChemin.__len__():
            interface.infoBulle(_("dernière photo atteinte"))
            return
        try :
            suivante = interface.photosAvecChemin[index+1]
            position = self.root.winfo_geometry()            
            self.root.destroy()
            CalibrationGPS(fenetre,suivante,self.points,self.dicoPointsJPG,position)
        except:
            self.quitter()

    def precedent(self): # photo précédente sur la saisie des points/polylignes/polylignes 
        index = interface.photosAvecChemin.index(self.file)
        if index==0:
            interface.infoBulle(_("première photo atteinte"))
            return
        try :
            precedente = interface.photosAvecChemin[index-1]
            position = self.root.winfo_geometry()             
            self.root.destroy()
            CalibrationGPS(fenetre,precedente,self.points,self.dicoPointsJPG,position)
        except:
            self.quitter()        

    def abandon(self):
        self.dicoPointsJPG = self.retourSiAbandon
        self.quitter()

    def supprimerTousLesPoints(self):                                   # suppression de la localisation de tous les points GCP présents sur l'image self.file
        aSupprimer = dict(self.dicoPointsJPG)                           # self.dicoPointsJPG[(self.boutonChoisi,self.file,self.numBoutonChoisi)] = (self.xJPG,self.yJPG)
        for cle in aSupprimer:                                          # 
            if cle[1]==self.file:
               del self.dicoPointsJPG[cle]
        self.afficheImage()

    def supprimerUnPoint(self):
         tousLesPoints = dict(self.dicoPointsJPG)
         aSupprimer = choisirDansUneListe(fenetre,[e for e,f,g in tousLesPoints if self.file==f],"Supprimer un ou plusieurs points").selectionFinale
         for cle in tousLesPoints:         
             if cle[1]==self.file and cle[0] in aSupprimer:
               del self.dicoPointsJPG[cle]
         self.afficheImage()                 
         
################# Classe Principale : la fenêtre maître de l'application, le menu, l'IHM

class Interface(ttk.Frame):
        
    ################################## INITIALISATIONS - MENU - VALEURS PAR DEFAUT - EXIT ###########################################################
        
    def __init__(self, fenetre, **kwargs):
 
        # initialise les "constantes"

        self.initialiseConstantes()
        
        # initialise les variables "chantier"
                
        self.initialiseValeursParDefaut()               # valeurs par défaut pour un nouveau chantier (utile si pas encore de chantier)                                                                                                                       # pour les paramètres du chantier sous le répertoire chantier, après lancement Micmac
        
        # On restaure les paramètres et la session précédente
        
        self.restaureParamEnCours()                     # restaure les paramètres locaux par défaut et le dernier chantier

        # vérifie si déjà lancé : si oui : nouveau chantier

        self.lancementMultiple()
        
        #affiche le logo durant 5 secondes, sauf demande expresse
        if self.tacky:
            try:
                global compteur
                if compteur==1:
                    self.canvasLogo1 = tkinter.Canvas(self.logo1,width = 500, height = 200)       # Canvas pour revevoir l'image
                    self.canvasLogo1.pack(fill='both',expand = 1)
                    self.logo1.pack()
                    self.imgTk_id = self.canvasLogo1.create_image(150,70,image = dataLogoCerema,anchor="nw") # affichage effectif de la photo dans canvasPhoto
                    fenetreIcone(fenetre)

                    try:
                        for i in range(len(self.titreFenetre+" "+_(": une interface graphique pour MicMac..."))+8):
                            fenetre.title((self.titreFenetre+" "+_(": une interface graphique pour MicMac..."))[0:i])        
                            fenetre.update()
                            time.sleep(0.03)
                    except:
                        print(_("Fermeture inatendue de la fenêtre."))
                    
            except Exception as e:
                print(_("Erreur initialisation de la fenêtre principale : ")),str(e)

        # Fenêtre principale : fenetre
       
        ttk.Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        fenetreIcone(fenetre)
        fenetre.title(self.titreFenetre)                                                        # Nom de la fenêtre
        fenetre.geometry("800x700+100+200")                                                     # fenetre.geometry("%dx%d%+d%+d" % (L,H,X,Y))

        # construction des item du menu

        mainMenu = tkinter.Menu()                                                               # Barre de menu principale

        # Fichier
        
        menuFichier = tkinter.Menu(mainMenu,tearoff = 0)                                        ## menu fils : menuFichier, par défaut tearOff = 1, détachable 
        menuFichier.add_command(label=_("Nouveau chantier"), command=self.nouveauChantier)           
        menuFichier.add_command(label=_("Ouvrir un chantier"), command=self.ouvreChantier)
        menuFichier.add_separator()        
        menuFichier.add_command(label=_("Enregistrer"), command=self.enregistreChantierAvecMessage)
        menuFichier.add_separator()        
        menuFichier.add_command(label=_("Renommer le chantier"), command=self.renommeChantier)
        menuFichier.add_command(label=_("Enregistrer sous..."), command=self.enregistreChantierSous)         
        menuFichier.add_separator()
        menuFichier.add_command(label=_("Exporter le chantier en cours"), command=self.exporteChantier)
        menuFichier.add_command(label=_("Importer un chantier"), command=self.importeChantier)         
        menuFichier.add_separator()        
        menuFichier.add_command(label=_("Ajouter un chantier à partir d'un répertoire"), command=self.ajoutRepertoireCommechantier)
        menuFichier.add_separator()        
        menuFichier.add_command(label=_("Du ménage !"), command=self.supprimeRepertoires)               
        menuFichier.add_separator()        
        menuFichier.add_command(label=_("Quitter"), command=self.quitter)

        # Edition

        menuEdition = tkinter.Menu(mainMenu,tearoff = 0)                                        ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuEdition.add_command(label=_("Afficher l'état du chantier"), command=self.afficheEtat)
        menuEdition.add_separator()        
        menuEdition.add_command(label=_("Visualiser toutes les photos sélectionnées"), command=self.afficherToutesLesPhotos)
        menuEdition.add_command(label=_("Visualiser les photos pour la calibration intrinsèque"), command=self.afficherCalibIntrinseque)               
        menuEdition.add_command(label=_("Visualiser les maîtresses et les masques"), command=self.afficherLesMaitresses)
        menuEdition.add_command(label=_("Visualiser le masque sur mosaique Tarama"), command=self.afficherMasqueTarama)        
        menuEdition.add_command(label=_("Visualiser le masque 3D"), command=self.afficheMasqueC3DC)
        menuEdition.add_command(label=_("Visualiser les points GCP"), command=self.afficherLesPointsGPS)
        menuEdition.add_separator()        
        menuEdition.add_command(label=_("Visualiser la ligne horizontale/verticale"), command=self.afficherLigneHV)
        menuEdition.add_command(label=_("Visualiser la zone plane"), command=self.afficherZonePlane)
        menuEdition.add_command(label=_("Visualiser la distance"), command=self.afficherDistance)
        menuEdition.add_separator()
        menuEdition.add_command(label=_("Afficher la trace synthétique du chantier"), command=self.lectureTraceSynthetiqueMicMac)
        menuEdition.add_command(label=_("Afficher la trace complète du chantier"), command=self.lectureTraceMicMac)
        menuEdition.add_separator()
        menuEdition.add_command(label=_("Afficher la mosaïque Tarama"), command=self.afficheMosaiqueTarama)
        menuEdition.add_command(label=_("Afficher l'ortho mosaïque Tawny"), command=self.afficheMosaiqueTawny)        
        menuEdition.add_separator()
        menuEdition.add_command(label=_("Afficher l'image 3D non densifiée"), command=self.afficheApericloud)         
        menuEdition.add_command(label=_("Afficher l'image 3D densifiée"), command=self.affiche3DNuage)
        menuEdition.add_separator()        
        menuEdition.add_command(label=_("Lister-Visualiser les images 3D"), command=self.lister3DPly)
        menuEdition.add_command(label=_("Fusionner des images 3D"), command=self.choisirPuisFusionnerPly)
        menuEdition.add_separator()        
        menuEdition.add_command(label=_("Informations sur un nuage de points du chantier"), command=self.demandePlyChantierPourInfo)
        menuEdition.add_command(label=_("Informations sur un fichier ply"), command=self.demandePlyPourInfo)
        
        # MicMac
                
        menuMicMac = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuMicMac.add_command(label=_("Choisir des photos"), command=self.lesPhotos)
        menuMicMac.add_command(label=_("Options"), command=self.optionsOnglet)
        menuMicMac.add_separator()     
        menuMicMac.add_command(label=_("Lancer MicMac"), command=self.lanceMicMac)                 ## Ajout d'une option au menu fils menuFile

        # GoPro
                
        menuGoPro = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuGoPro.add_command(label=_("Options (GoPro par défaut)"), command=self.optionsGoPro)
        menuGoPro.add_separator()          
        menuGoPro.add_command(label=_("Nouveau chantier : choisir une vidéo GoPro, ou autre"), command=self.laVideo)   
        menuGoPro.add_command(label=_("Sélection des meilleures images"), command=self.selectionGoPro)        ## Sélection des "meilleures images" avec le taux passé en paramètre

        # Outils

        menuOutils = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable

        menuOutils.add_command(label=_("Nom et focale de l'appareil photo, dimension des photos"), command=self.outilAppareilPhoto)
        menuOutils.add_command(label=_("Toutes les focales et les noms des appareils photos"), command=self.toutesLesFocales)          
        menuOutils.add_command(label=_("Mettre à jour DicoCamera.xml"), command=self.miseAJourDicoCamera)        
        menuOutils.add_separator()
        menuOutils.add_command(label=_("Qualité des photos du dernier traitement"), command=self.nombrePointsHomologues)
        menuOutils.add_command(label=_("Qualité des points GCP"), command=self.consulterEcartsGCP)
        menuOutils.add_separator()        
        menuOutils.add_command(label=_("Sélectionner les N meilleures photos"), command=self.outilMeilleuresPhotos)
        menuOutils.add_command(label=_("Retirer des photos"), command=self.retirerPhotos)       
        menuOutils.add_separator()        
        menuOutils.add_command(label=_("Modifier l'exif des photos"), command=self.majExif)
        menuOutils.add_separator()
        menuOutils.add_command(label=_("Modifier les paramètres par défaut"), command=self.majOptionsParDefaut)
        menuOutils.add_separator()
        menuOutils.add_command(label=_("Vérifie la présence d'une nouvelle version sur GitHub"),command=self.verifVersion)    ## Meslab

        # mode Expert
        
        def updatePlusieursAppareilsPhotos(): # si nouvel item changer le premier paramètre = numéro d'ordre dans la liste
            menuPlusieursAppareilsPhotos.entryconfig(1, label=_("Définir la longueur du préfixe des photos ; %s") % (self.nbCaracteresDuPrefixe))
                
        menuExpert = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuExpert.add_command(label=_("Exécuter une ligne de commande système"), command=self.lignesExpert)
        menuExpert.add_command(label=_("Exécuter une commande python"), command=self.lignesPython)        
        menuExpert.add_separator()
        menuExpert.add_command(label=_("Personnaliser les paramètres optionnels des modules Micmac"), command=self.personnaliseOptions)
        menuExpert.add_separator()
        menuExpert.add_command(label=_("Consulter le fichier mm3d-LogFile.txt"), command=self.logMm3d)        
        menuExpert.add_separator()

        menuExpertImport = tkinter.Menu(menuExpert,tearoff = 0)
        menuExpertImport.add_command(label=_("Importer points homologues, calibration, orientation, Tarama"), command=self.copierHomolOriTarama)
        menuExpertImport.add_separator()         
        menuExpertImport.add_command(label=_("Importer les points homologues d'un autre chantier"), command=self.copierPointsHomologues)             
        menuExpertImport.add_command(label=_("Importer la calibration d'un autre chantier"), command=self.chargerCalibrationIntrinsequeDepuisMenu)
        menuExpertImport.add_command(label=_("Importer l'orientation d'un autre chantier"), command=self.copierOrientation)
        menuExpertImport.add_command(label=_("Importer la mosaique Tarama d'un autre chantier"), command=self.copierMosaiqueTarama)                
        menuExpertImport.add_command(label=_("Importer les points GCP d'un autre chantier"), command=self.ajoutPointsGPSAutreChantier)
        menuExpertImport.add_separator()        
        menuExpertImport.add_command(label=_("Importer les points GCP à partir d'un fichier"), command=self.ajoutPointsGPSDepuisFichier)
        
        menuExpert.add_cascade(label = _("Importer points homologues, les points GCP/GPS"),menu=menuExpertImport)
    
        menuExpert.add_separator()        
        menuPlusieursAppareilsPhotos = tkinter.Menu(menuExpert,tearoff = 0,postcommand=updatePlusieursAppareilsPhotos)        
        menuPlusieursAppareilsPhotos.add_command(label=_("Définir plusieurs appareils photos"), command=self.plusieursAppareils)
        menuPlusieursAppareilsPhotos.add_command(label=(_("Définir la longueur du préfixe des photos ; %s") % (self.nbCaracteresDuPrefixe)), command=self.longueurPrefixe)        
        menuPlusieursAppareilsPhotos.add_command(label=_("Lister les appareils photos"), command=self.listeAppareils)

        menuExpert.add_cascade(label = _("Plusieurs appareils photos"),menu=menuPlusieursAppareilsPhotos)

        menuExpert.add_separator()
        self.menuNavigationGPS = tkinter.Menu(menuExpert,tearoff = 0)
        self.menuNavigationGPS.add_command(label=_("navigation GPS : information sur le reférentiel choisi"), command=self.afficheMessageRepereLocal)
        self.menuNavigationGPS.add_separator()
        self.menuNavigationGPS.add_command(label=_("navigation GPS : ne pas utiliser les données GPS de navigation"), command=self.swapGPSEmbarque)        
        self.menuNavigationGPS.add_separator()
        self.menuNavigationGPS.add_command(label=_("Référentiel : utiliser le Lambert 93"), command=self.choixRepereLambert93)        
        self.menuNavigationGPS.add_command(label=_("Référentiel : utiliser un code EPSG"), command=self.choixRepereEpsg)       
        self.menuNavigationGPS.add_command(label=_("Référentiel : utiliser un repère local plan tangent"), command=self.choixRepereLocal)
        self.menuNavigationGPS.add_command(label=_("Référentiel : utiliser le WGS884"), command=self.choixRepereWGS84)
        self.menuNavigationGPS.add_command(label=_("Référentiel : utiliser un repère géocentrique cartésien"), command=self.choixRepereGeoC)
        
        menuExpert.add_cascade(label = _("Navigation GPS"),menu=self.menuNavigationGPS)

        # Mise à jour du libellé du menu expert/navigation GPS/ utiliser les données GPS
        
        self.miseAJourLibelleNavigationGPS()
                

        # menu métiers

        menuMetier = tkinter.Menu(mainMenu,tearoff = 0)         ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuMetier.add_command(label=_("Ecrire un MNT à partir d'un PLY"), command=self.ply2Mnt)
        menuMetier.add_command(label=_("Ecrire un MNT à partir d'un fichier XYZ"), command=self.xyz2Mnt)                       
        menuMetier.add_separator()
        menuMetier.add_command(label=_("Information sur le calcul des volumes"), command=infoVolume)
        menuMetier.add_command(label=_("Calculer le volume d'un MNT"), command=calculVolumeMnt)        
        menuMetier.add_command(label=_("Calculer le volume entre 2 MNT"), command=calculVolumeEntre2Mnt)           
        menuMetier.add_command(label=_("Visualiser l'écart entre les 2 MNT"), command=self.afficheEcart)
        menuMetier.add_separator()        
        menuMetier.add_command(label=_("Modifier la tolérance utilisée pour calculer le volume"), command=self.paramTolerance)
        menuMetier.add_command(label=_("Modifier l'arrondi des résultats du calcul des volumes"), command=self.paramArrondi)        
        menuMetier.add_separator()
        menuMetier.add_command(label=_("Ecrire un fichier XYZ à partir d'un PLY"), command=self.ecrireXYZ)
        menuMetier.add_command(label=_("Visualiser un fichier XYZ"), command=self.afficheXYZ)        
        menuMetier.add_separator()         
        menuMetier.add_command(label=_("Aide sur les outils métiers"), command=self.aideMetiers)         
     

        # Paramétrage       

        def updateParam():
            if self.tacky:
                menuParametres.entryconfig(10, label=_("Désactiver le 'tacky' message de lancement"))
            else:
                menuParametres.entryconfig(10, label=_("Activer le 'tacky' message de lancement"))
            if self.avertirNouvelleVersion:
                menuParametres.entryconfig(11, label=_("Désactiver la recherche de nouvelle version au lancement"))
            else:
                menuParametres.entryconfig(11, label=_("Activer la recherche de nouvelle version au lancement"))
                
                
        menuParametres = tkinter.Menu(mainMenu,tearoff = 0,postcommand=updateParam)
        menuParametres.add_command(label=_("Afficher les paramètres"), command=self.afficheParam)              ## Ajout d'une option au menu fils menuFile
        menuParametres.add_separator()        
        menuParametres.add_command(label=_("Associer le répertoire bin de MicMac"), command=self.repMicmac)    ## Ajout d'une option au menu fils menuFile
        menuParametres.add_command(label=_("Associer 'exiftool'"), command=self.repExiftool)                   ## Exiftool : sous MicMac\binaire-aux si Windows, mais sinon ???   
        menuParametres.add_command(label=_("Associer 'convert' d'ImageMagick"), command=self.repConvert)       ## convert : sous MicMac\binaire-aux si Windows, mais sinon ???   
        menuParametres.add_command(label=_("Associer 'ffmpeg (décompacte les vidéos)"), command=self.repFfmpeg)                        ## ffmpeg : sous MicMac\binaire-aux si Windows, mais sinon ???
        menuParametres.add_command(label=_("Associer 'Meshlab' ou 'CloudCompare'"), command=self.repMeslab)    ## Meslab
        menuParametres.add_separator()
        menuParametres.add_command(label=_("Changer la langue")+" change the language", command = self.modifierLangue)
        menuParametres.add_separator() 
        menuParametres.add_command(label=_("Désactive/Active le tacky message de lancement..."),command=self.modifierTacky)    # supprime le logo cerema au lancement
        # supprime le controle de la présence d'une nouvelle veersion au lancement
        menuParametres.add_command(label=_("Désactive/Active le  controle nouvelle version de lancement..."),command=self.modifierGitHub)
        menuParametres.add_separator() 
     
        # Aide
        
        menuAide = tkinter.Menu(mainMenu,tearoff = 0)                                           ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuAide.add_command(label=_("Pour commencer..."), command=self.commencer)
        menuAide.add_separator()
        menuAide.add_command(label=_("Aide sur les menus"), command=self.aide)           
        menuAide.add_command(label=_("Quelques conseils sur les prises de vue"), command=self.conseilsPhotos)
        menuAide.add_command(label=_("Quelques conseils sur le choix des options de MicMac"), command=self.conseilsOptions)
        menuAide.add_command(label=_("Et si MicMac ne trouve pas de points homologues ou d'orientation"), command=self.conseilsPlantageNonDense)        
        menuAide.add_command(label=_("Et si MicMac ne trouve pas de nuage dense"), command=self.conseilsPlantageDense)        
        menuAide.add_separator()
        menuAide.add_command(label=_("Historique"), command=self.historiqueDesVersions)
        menuAide.add_separator()        
        menuAide.add_command(label=_("A Propos"), command=self.aPropos) 
        
        # ajout des items dans le menu principal :
        
        mainMenu.add_cascade(label = _("Fichier"),menu=menuFichier)
        mainMenu.add_cascade(label = _("Edition"),menu=menuEdition)        
        mainMenu.add_cascade(label = "MicMac",menu=menuMicMac)
        mainMenu.add_cascade(label = _("Vidéo"),menu=menuGoPro)                              
        mainMenu.add_cascade(label = _("Outils"),menu=menuOutils)
        mainMenu.add_cascade(label = _("Expert"),menu=menuExpert)
        mainMenu.add_cascade(label = _("Outils métier"),menu=menuMetier)              
        mainMenu.add_cascade(label = _("Paramétrage"),menu=menuParametres)
        mainMenu.add_cascade(label = _("Aide"),menu=menuAide)
        
        # affichage du menu principal dans la fenêtre

        fenetre.config(menu = mainMenu)       

        # Fonction a éxécuter lors de la sortie du programme

        fenetre.protocol("WM_DELETE_WINDOW", self.quitter)

        # annonce du lancement :

        self.ajoutTraceComplete(heure()+" "+_("lancement d'aperodedenis")+version+".")

        # zone de test éventuel :
        
    #initialise les valeurs par défaut au lancement de l'outil
        
    def initialiseConstantes(self):         #les constantes, mais pas que (ménage à faire)

        # Pour suivre les nouvelles versions

        self.versionInternetAncienne    =   str()       # Dernière version lue sur GitHub (ne sert plus)
       
        # initialisation variables globales et propre au contexte local :

        self.repertoireScript           =   repertoire_script                                   # là où est le script et les logos cerema et IGN
        self.repertoireData             =   repertoire_data                                     # là ou l'on peut écrire des données
        self.systeme                    =   os.name                                             # nt ou posix
        self.nomApplication             =   os.path.splitext(os.path.basename(sys.argv[0]))[0]  # Nom du script
        self.nomApplication             =   self.nomApplication[0].upper()+self.nomApplication[1:]
        self.titreFenetre               =   self.nomApplication+version                         # nom du programme titre de la fenêtre (version = varaioble globale)
        self.tousLesChantiers           =   list()                                              # liste de tous les réchantiers créés, avec chemin
        self.exptxt                     =   "0"                                                 # 0 pour exptxt format binaire, 1 format texte (pts homologues)             
        self.indiceTravail              =   0                                                   # lors de l'installation, valeur initial de l'indice des répertoires de travail

        # Les 3 chemins utiles : mecmac\bin, meshlab et exiftool :  
        self.micMac                     =   _('Pas de répertoire désigné pour MicMac\\bin')        # oar défaut il n'y a pas de répertoire micMac, sauf si restauration ligne suivante
        self.meshlab                    =   _('Pas de fichier désigné pour ouvrir les .PLY')
        self.exiftool                   =   _("Pas de chemin pour ExifTool")
        self.mm3d                       =   _("Pas de fichier pour mm3d")                          # lanceur des commandes micmac
        self.ffmpeg                     =   _("Pas de fichier pour ffmpeg")                        # outil d'extraction des images à partir de video
        self.mercurialMicMac            =   _("Pas de version MicMac")
        self.mercurialMicMacChantier    =   ""      
        self.convertMagick              =   _("Pas de version Image Magick")                       # pour convertir les formats
        self.noRep = [self.micMac, self.meshlab, self.exiftool, self.mm3d, self.convertMagick,self.ffmpeg] # pour des question de traduction si message et pas si répertoire !!

        # le controle des photos

        self.dimensionsDesPhotos        =   list()                                              # [(x,Image.open(x).size) for x in self.photosSansChemin] 
        self.dimensionsOK               =   bool()                                              # set([y for (x,y) in self.dimensionsDesPhotos]).__len__()==1     # vrai si une seule taille
        self.nbFocales                  =   int()                                               # nb de focales parmi les photos
        self.tagsExifUtiles             = ["FocalLength",                                       # les tags récupérés dans l'exif
                                           "Model",
                                           "SerialNumber",
                                           "FocalLengthIn35mmFormat",
                                           "Make",
                                           "GPSLatitude",                                       # les tags pour les photos prises à partir de drones
                                           "GPSLongitude",                                      # voir l'utilité dansl'exemple MicMac : Grand Leez et OriConvert (forum)
                                           "AbsoluteAltitude",
                                           "GimbalYawDegree",
                                           "GimbalPitchDegree",
                                           "GimbalRollDegree",
                                           "FlightYawDegree",
                                           "FlightPitchDegree",
                                           "FlightRollDegree",
                                           "GPSLatitudeRef",
                                           "GPSLongitudeRef"
                                           ]
        
        self.nomOriGPS                  =   "OriGPS.TXT"                                        # fichier des positions GPS extraites des photos (drones)
        
        # les caractéristiques de l'appareil photo :
        
        self.fabricant                  =   str()
        self.nomCamera                  =   str()
        self.focale                     =   str()
        self.focale35MM                 =   str()
        
        # Les noms des fichiers xml

        self.masque3DSansChemin         =   "AperiCloud_selectionInfo.xml"                      # nom du fichier XML du masque 3D, fabriqué par 
        self.masque3DBisSansChemin      =   "AperiCloud_polyg3d.xml"                            # nom du second fichier XML pour le masque 3D
        self.dicoAppuis                 =   "Dico-Appuis.xml"                                   # nom du fichier XML des points d'appui (nom, X,Y,Z,incertitude) pour Bascule
        self.mesureAppuis               =   "Mesure-Appuis.xml"                                 # nom du XML positionnant les points d'appuis GCP dans les photos
        self.miseAEchelle               =   "MiseAEchelle.xml"                                  # pour l'axe des x, le plan 
        self.dicoCameraUserRelatif      =   "include/XML User/DicoCamera.xml"                   # relatif au répertoire MicMac
        self.dicoCameraGlobalRelatif    =   "include/XML_MicMac/DicoCamera.xml"                 # relatif au répertoire MicMac
        
        # Constante sous nt et posix :

        self.nomTapioca                 =   "Tapioca"   
        self.nomTapas                   =   "Tapas"
        self.nomMalt                    =   "Malt"
        self.nomApericloud              =   "AperiCloud"
        self.nomNuage2Ply               =   "Nuage2Ply"
        self.nomC3DC                    =   "C3DC"

        # pour affichage correct des chemins on mémorise le séparateur \ pour nt et le séparateur de l'autre OS \ ; (voir os.path.normcase)
        
        self.separateurChemin           =   "\\"
        self.separateurAutre            =   "/"

        # particularités sous linux :
        
        if self.systeme=="posix":
            self.separateurChemin       =   "/"
            self.separateurAutre        =   "\\"

        # Les widgets graphiques : le style, 
        style = ttk.Style()
        style.map   (   "C.TButton",
                        foreground=[('pressed', 'red'), ('active', 'blue')],
                        background=[('pressed', '!disabled', 'black'), ('active', 'white')]
                    )

        # le cadre et le label d'encadre :
        
        self.resul100=ttk.Frame(fenetre,height=50,relief='sunken')
        self.texte101=ttk.Label(self.resul100, text="",justify='center',style="C.TButton")        
        self.texte101.pack(ipadx=5,ipady=5)

        # la fenetre pour afficher les textes (traces et aides), rechercher dans la fenêtre

        self.resul200 = ttk.Frame(fenetre,height=100,relief='sunken')  # fenêtre texte pour afficher le bilan
        self.scrollbar = ttk.Scrollbar(self.resul200)
        self.scrollbar.pack(side='right',fill='y',expand=1)              
        self.scrollbar.config(command=self.yviewTexte)
        self.texte201 = tkinter.Text(self.resul200,width=200,height=100,yscrollcommand = self.scrollbar.set,wrap='word')
        self.texte201.bind("<Control-f>",self.find201)
        self.texte201.bind("<Control-F>",self.find201)
        self.texte201.bind("<Control-Shift-f>",self.findAll201)
        self.texte201.bind("<Control-Shift-F>",self.findAll201)
        self.texte201.bind("<F3>",self.suivant201)
        self.find201 = str()
        self.listePositions201 = list()
        self.suite201 = -1
        self.ending_index = "1.0"
        self.suite201 = -1
        self.texte201.pack()

        # Les variables, Widgets et options de la boite à onglet :

        # Pour tapioca

        self.echelle1           = tkinter.StringVar()               # nécessaire pour définir la variable obtenue le widget : pour All
        self.echelle2           = tkinter.StringVar()               #  
        self.echelle3           = tkinter.StringVar() 
        self.echelle4           = tkinter.StringVar()        
        self.delta              = tkinter.StringVar()
        self.fileTapioca        = tkinter.StringVar()               # Pour usage futur       
        self.modeTapioca        = tkinter.StringVar()
        self.modeCheckedMalt    = tkinter.StringVar()
        
        # Pour tapas calibration puis Tapas :

        self.modeCheckedTapas   = tkinter.StringVar()                   # nécessaire pour définir la variable obtenue par radiobutton
        self.arretApresTapas    = tkinter.IntVar()                      # booléen : le calcul s'arrête aprés l'orientation.
        self.lancerTarama       = tkinter.IntVar()                      # booléen : exécuter Tarama pour créer une mosaique des images, utilisable pour faire un masque sur Malt/ortho
        self.calibSeule         = tkinter.BooleanVar()                  # booléen 0 ou 1 (pas True or False) : les photos de calibration ne servent que pour la calibration
        self.repCalibSeule      = "PhotosCalibrationIntrinseque"        # nom du répertoire pour cantonner les photos servant uniquement à la calibration
        self.choixCalibration   = tkinter.StringVar()                   # calibration par autre chantier ou par photos 
        self.chantierOrigineCalibration =str()                          # si calibration copiée depuis un autre chantier

        # Faut-il calculer et afficher le nuage non dense

        self.calculNuageNonDense = tkinter.BooleanVar()                 # booléen 0 ou 1 (pas True or False) : faut-il calculer apericloud.ply
        
        # pour la calibration

        self.distance           = tkinter.StringVar()

        # pour Campari : pour l'onglet des points GCP :

        self.incertitudeCibleGPS    =   tkinter.StringVar()
        self.incertitudePixelImage  =   tkinter.StringVar()

        # Pour Malt

        self.zoomF                  =  tkinter.StringVar()              # niveau de zoom final pour malt : 8,4,2,1 1 le plus dense
        self.photosUtilesAutourDuMaitre = tkinter.IntVar()              # pour le mode geomimage seul : nombre de photos avant/après autour de la maitresse

        # Nuage2Ply

        self.nuage2Mesh             =  tkinter.StringVar()              # string :  0 ou 1 (pas True or False) : nuage (0) ou maillage (1)

        # pour Tawny
        
        self.tawny                  =  tkinter.BooleanVar()             # booléen 0 ou 1 (pas True or False) :pour le mode Orthophoto seul : lancer ou non tawny

        # pour C3DC

        self.choixDensification = tkinter.StringVar()                      # 
        self.modeC3DC           = tkinter.StringVar()       

        # Pour la localisation GPS par exif des photos :

        self.repereLocalXml         =   "SysCoRTL.xml"          # fichier systéme de coordonnées : référentiel terrestre local
        self.repereGeoc             =   "GeoC"
        self.repereWGS84            =   "WGS84"                 # fichier systéme de coordonnées, mot clé : WGS84
        self.repereLambert93        =   "Lambert93"             # fichier systéme de coordonnées, mot clé : lambert 93 epsg 2154
        self.repereEpsgXml          =   "EPSG.xml"              # repére défini par un code epsg
        self.repereSupprime         =   _("Données GPS de navigation supprimées") # si le repère n'est pas utilisé
        self.repereAbsent           =   _("Absence de données GPS 'drones' dans les photos.")   # s'il n'y a pas de données GPS dans les photos
        self.messageGPSDroneAbsent  =   self.repereAbsent
        self.repereADeterminer      =   str()

        # paramètres nommés personnalisés : initialisation
    
        self.tapiocaMulScalePerso   = tkinter.StringVar()
        self.tapiocaLinePerso       = tkinter.StringVar()
        self.tapiocaAllPerso        = tkinter.StringVar()
        self.tapasPerso             = tkinter.StringVar()      
        self.maltOrthoPerso         = tkinter.StringVar()
        self.maltGeomImagePerso     = tkinter.StringVar()
        self.maltUrbanMnePerso      = tkinter.StringVar()                
        self.C3DCPerso              = tkinter.StringVar()       
        self.campariPerso           = tkinter.StringVar()     
        self.tawnyPerso             = tkinter.StringVar()                        
        self.gcpBasculPerso         = tkinter.StringVar()
        self.taramaPerso            = tkinter.StringVar()
        self.aperiCloudPerso        = tkinter.StringVar()
        self.nuage2PlyPerso         = tkinter.StringVar()
        self.divPerso               = tkinter.StringVar()
        self.mergePlyPerso          = tkinter.StringVar()
        self.initDicoPerso()

        self.memoPerso()            # crée le dico des paramètres perso

        # paramètres langues
        self.langues = list()
        self.langues = ("Français/French","Anglais/English","Allemand/Deutsch","Espagnol/Español",
                        "Italien/Italiano","Chinois/中文","Arabe/عربى")
       
        # L'onglet :
        
        self.onglets = ttk.Notebook(fenetre)                           # create Notebook in "master" : boite à onglet, supprimé par menageEcran() comme les frames
        
        #   tapioca : 400
        
        self.item400=ttk.Frame(self.onglets,borderwidth=5,height=50,relief='sunken',padding="0.3cm")        
        self.item410=ttk.Label(self.item400, text=_("Tapioca recherche les points homologues entre photos : indiquer l'échelle ou les échelles utilisées"))
        self.item401 = ttk.Radiobutton(self.item400, text="All",      variable=self.modeTapioca, value='All',     command=self.optionsTapioca)
        self.item402 = ttk.Radiobutton(self.item400, text="MulScale", variable=self.modeTapioca, value='MulScale',command=self.optionsTapioca)
        self.item403 = ttk.Radiobutton(self.item400, text="Line",     variable=self.modeTapioca, value='Line',    command=self.optionsTapioca)
        self.item404 = ttk.Radiobutton(self.item400, text="File",     variable=self.modeTapioca, value='File')
        self.item410.pack(anchor='w')
        self.item401.pack(anchor='w')
        self.item402.pack(anchor='w')
        self.item403.pack(anchor='w')
        self.item404.pack(anchor='w')
        self.item404.state(['disabled'])                # dans cette version de l'outil

        # tapioca Echelle 1 All
        
        self.item480  = ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")        
        self.item481  = ttk.Label(self.item480, text=_("Echelle image (-1 pour l'image entière) :"))
        self.item482  = ttk.Entry(self.item480,textvariable=self.echelle1)
        self.item481.pack()
        self.item482.pack()

        # tapioca Echelle2 et 3 (MultiScale) 

        self.item460=ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")        
        self.item461=ttk.Label(self.item460, text=_("Echelle image réduite : "))
        self.item462=ttk.Entry(self.item460,textvariable=self.echelle2)
        self.item461.pack()
        self.item462.pack()
        self.item463=ttk.Label(self.item460, text=_("Seconde Echelle (-1 pour l'image entière) :"))
        self.item464=ttk.Entry(self.item460,textvariable=self.echelle3)
        self.item463.pack()
        self.item464.pack()
        
        # tapioca Delta Echelle4

        self.item470=ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")
        self.item471=ttk.Label(self.item470, text=_("Echelle image (-1 pour l'image entière) :"))
        self.item472=ttk.Entry(self.item470,textvariable=self.echelle4)
        self.item473=ttk.Label(self.item470, text=_("Delta (nombre d'images se recouvrant, avant et après) : "))
        self.item474=ttk.Entry(self.item470,textvariable=self.delta)
        self.item471.pack()
        self.item472.pack()
        self.item473.pack()
        self.item474.pack()


        #   Tapas : 500
        
        self.item500=ttk.Frame(self.onglets,height=150,relief='sunken',padding="0.3cm")                               
        self.item505=ttk.Label(self.item500, text=_("Tapas positionne les appareils photos sur le nuage de points homologues. Préciser le type d'appareil."))
        self.item506=ttk.Label(self.item500, text=_("Quelques photos avec une grande profondeur d'image aident à calibrer l'optique des appareils photos."))        
        self.item505.pack()
        self.item506.pack()
        modesTapas=[('RadialExtended (REFLEX)','RadialExtended','active'),
                    ('RadialStd (Compact)','RadialStd','active'),
                    ('RadialBasic (SmartPhone)','RadialBasic','active'),
                    ('FishEyeBasic (GOPRO)','FishEyeBasic','active'),                      
                    ('FishEyeEqui','FishEyeEqui','active'),       # déconnexion texte affichée, valeur retournée
                    ('Fraser','Fraser','active'),
                    ('FraserBasic','FraserBasic','active'),]                    
##                    ('HemiEqui','HemiEqui','disabled'),
##                    ('AutoCal','AutoCal','disabled'),
##                    ('Figee','Figee','disabled')        
        for t,m,s in modesTapas:
            b=ttk.Radiobutton(self.item500, text=t, variable=self.modeCheckedTapas, value=m)
            b.pack(anchor='w')
            b.state([s])

        # choix pour calibration autre chantier ou photos

        self.item560 = ttk.Frame(self.item500,height=50,relief='sunken',padding="0.2cm")      # pour le check button, fera un encadrement
        self.item561 = ttk.Frame(self.item560,height=50,relief='sunken',padding="0.2cm")
        self.item562 = ttk.Frame(self.item560)
        self.item564 = ttk.Radiobutton(self.item561, text=_("Pas de calibration"),
                                       variable=self.choixCalibration, value='sans', command=self.visuOptionsCalibration)
        self.item565 = ttk.Radiobutton(self.item561, text=_("Choisir la calibration d'un autre chantier"),
                                       variable=self.choixCalibration, value='chantier', command=self.visuOptionsCalibration)
        self.item566 = ttk.Radiobutton(self.item561, text=_("Choisir des photos de calibration"),
                                       variable=self.choixCalibration, value='photos', command=self.visuOptionsCalibration)
        self.item560.pack()
        self.item561.pack()
        self.item564.pack(side='left')
        self.item565.pack(side='left')
        self.item566.pack(side='left')
        
        # frame Autre chantier : 570
        self.item570 = ttk.Frame(self.item562)
        self.item571 = ttk.Button(self.item570,text=_("Charger la calibration intrinsèque d'un autre chantier"),command=self.chargerCalibrationIntrinseque)  
        self.item572 = ttk.Label(self.item570, text="")
        self.item571.pack()
        self.item572.pack()
        
        # ou frame 520 photosPourCalibrationIntrinseque
        self.item520 = ttk.Frame(self.item562)      # pour la calibration, fera un encadrement        
        self.item525 = ttk.Button(self.item520,text=_("Photos pour la calibration intrinsèque"),command=self.imagesCalibrationIntrinseques)  
        self.item526 = ttk.Label(self.item520, text="")
        self.item527 = ttk.Checkbutton(self.item520, variable=self.calibSeule,
                                       text=" "+_("N'utiliser ces photos que pour la calibration")) 
        self.item528 = ttk.Label(self.item520, text=_("Toutes ces photos doivent avoir la même focale."))
        
        # lancer tarama ? item510
        self.item510 = ttk.Frame(self.item500,height=50,relief='sunken',padding="0.3cm")      # pour le check button, fera un encadrement
        self.item530 = ttk.Checkbutton(self.item510, variable=self.lancerTarama, text=_("lancer Tarama après TAPAS : mosaique pouvant définir un masque pour Malt/ortho)"))
        self.item530.pack(ipady=5)
        
        # Calculer le nuage non dense
        self.item535 =  ttk.Frame(self.item500,height=50,relief='sunken',padding="0.3cm")
        self.item536 = ttk.Checkbutton(self.item535, variable=self.calculNuageNonDense,
                                       text=_("Générer et afficher le nuage non dense, pour construire un masque 3D"))
        self.item536.pack(ipady=5)
        
        # lancer la densification ? item 540
        self.item540 = ttk.Frame(self.item500,height=50,relief='sunken',padding="0.3cm")      # pour le check button, fera un encadrement
        self.item550 = ttk.Checkbutton(self.item540, variable=self.arretApresTapas,
                                       text=_("Ne pas lancer la densification - permet de définir un masque"))
        self.item550.pack(ipady=5)

        self.item505.pack()
        self.item506.pack()            
        self.item525.pack()
        self.item526.pack()
        self.item527.pack() # je ne comprends plus l'intérêt de cet item : la suite s'accomode très bien de 2 focales différentes... mais si : camille utilise des photos d'un autre site
        self.item528.pack() 
        
        # Mise à l'échelle : 950
        
        self.item950 = ttk.Frame(  self.onglets,
                                   height=5,
                                   relief='sunken')
        self.item955=ttk.Label(self.item950, text=_("Définition d'un référentiel et d'une métrique sur le nuage de points homologues."))
        self.item956=ttk.Label(self.item950, text=_("Une ligne, un plan et la distance entre 2 points sont nécessaires."))        
        self.item955.pack()
        self.item956.pack()

        # Cadre définition des axes :
        
        self.item960 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")
        
        self.item961 = ttk.Label(self.item960,
                                  text=_('Choisir entre :'))
        
        self.item962 = ttk.Button(self.item960,
                                  text=_('Ligne horizontale'),
                                  command= self.ligneHorizontale)            

        self.item963 = ttk.Label(self.item960,
                                  text=_('ou'))        

        self.item964 = ttk.Button(self.item960,
                                  text=_('Ligne verticale'),
                                  command= self.ligneVerticale)

        self.item961.pack(ipadx=5,padx=5,ipady=2)
        self.item962.pack(side='left',ipadx=15,padx=5)        
        self.item963.pack(side='left',padx=5)
        self.item964.pack(side='left',ipadx=5)
        
        self.item960.pack(padx=5,pady=10,ipady=2,ipadx=15)
        
        # conjonction de coordination :
        
        self.item965 = ttk.Frame(  self.item950)
        self.item966 = ttk.Label(self.item965,text=_('ET :'))
        self.item966.pack()
        self.item965.pack()
        
        # cadre définition des plans :

        self.item970 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")
        
        self.item971 = ttk.Label(self.item970,
                                  text=_('Choisir entre :'))
        
        self.item972 = ttk.Button(self.item970,
                                  text=_('Zone plane horizontale'),
                                  command= self.planHorizontal)   

        self.item973 = ttk.Label(self.item970,
                                  text=_('ou')) 

        self.item974 = ttk.Button(self.item970,
                                  text=_('Zone plane verticale'),
                                  command= self.planVertical)
        
        self.item971.pack(ipadx=5,padx=5,ipady=2)               
        self.item972.pack(side='left',ipadx=15,padx=5)        
        self.item973.pack(side='left',padx=5)
        self.item974.pack(side='left',ipadx=5)
        self.item970.pack(padx=5,pady=10,ipady=2,ipadx=15)
        
        # conjonction de coordination :
        
        self.item975 = ttk.Frame(self.item950)
        self.item976 = ttk.Label(self.item975,text=_('ET :'))
        self.item976.pack()            
        self.item975.pack()
        
        # Cadre pour la distance entre 2 points :

        self.item980 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")        
        self.item981 = ttk.Label(self.item980,
                                  text=_('Distance entre les 2 points :'))        

        self.item982 = ttk.Entry(self.item980,textvariable=self.distance)          # distance

        self.item983 = ttk.Button(self.item980,
                                  text=_('Placer 2 points identiques sur 2 photos'),
                                  command= self.placer2Points)

        self.item981.pack()
        self.item982.pack()
        self.item983.pack(pady=10)
        self.item980.pack()

        self.item990 = ttk.Frame(  self.item950,
                                   relief='sunken') 
        self.item991 = ttk.Label(self.item990,text='\n' + _("Pour annuler la mise à l'échelle mettre la distance = 0"))       
        self.item991.pack()

        # des données GPS issues des exifs prennent le dessus sur la calibration : 
        self.item992 = ttk.Label(self.item990,text='\n' + _("Des données GPS provenant des exifs des photos sont prioritaires sur la mise à l'échelle")+"\n"+
                                 _("Vous pouvez les ignorez : menu expert/Supprimer l'orientation de navigation GPS"))
        self.item992.configure(foreground='red')

        # Item de la densification : 600, recevra item700 (Malt) ou Item800 (C3DC)

        self.item600 = ttk.Frame(self.onglets,height=5,relief='sunken',padding="0.15cm")
        self.item605 = ttk.Frame(self.item600,height=50,relief='sunken',padding="0.15cm")      # pour le check button, fera un encadrement
        self.item606 = ttk.Radiobutton(self.item605, text=_("Utiliser C3DC"),   variable=self.choixDensification, value='C3DC', command=self.optionsDensification)
        self.item607 = ttk.Radiobutton(self.item605, text=_("Utiliser MALT"),   variable=self.choixDensification, value='Malt', command=self.optionsDensification)           
        self.item605.pack(pady=3)  
        self.item606.pack(side='left')
        self.item607.pack(side='left')
    
        
        # Onglet Malt  : item700

        self.item700 = ttk.Frame(self.item600,height=5,relief='sunken',padding="0.15cm")
        self.item709 = ttk.Label(self.item700, text= _("Option de Malt :" ))
        self.item709.pack(anchor='w') 

        self.modesMalt = [(_('UrbanMNE pour photos urbaines'),'UrbanMNE'),
                          (_("GeomImage pour photos du sol ou d'objets"),'GeomImage'),
                          (_('Ortho pour orthophotos de terrain naturel [f(x,y)=z)]'),'Ortho'),
                          #(_('AperoDeDenis choisit pour vous les options de GeomImage'),'AperoDeDenis')
                          ]

        for t,m in self.modesMalt:
            b = ttk.Radiobutton(self.item700, text=t, variable=self.modeCheckedMalt, value=m, command=self.optionsMalt)
            b.pack(anchor='w')
                
        # Boites item710 et 730 dans item700 pour l'option GeomImage
        
        self.item710 = ttk.Frame(self.item700,height=50,relief='sunken',padding="0.15cm")    # pour le check button, fera un encadrement
        self.item701 = ttk.Label(self.item710)                                              # nom ou nombre d'images maitresses
        self.item702 = ttk.Button(self.item710,text=_("Choisir les maîtresses"),command=self.imageMaitresse)
        self.item703 = ttk.Label(self.item710)                                              # nom ou nombre de masques
        self.item704 = ttk.Button(self.item710,text=_('Tracer les masques'),command=self.tracerLesMasques) 
        self.item705 = ttk.Label(self.item710,text= _("Pour supprimer un masque : supprimer la maitresse"))
        self.item730 = ttk.Frame(self.item700,relief='sunken',padding="0.15cm")      # fera un encadrement pour nb photos à retenir
        self.item732 = ttk.Label(self.item730,text=_("Nombre de photos à retenir autour de l'image maitresse (-1 = toutes) :"))
        self.item733 = ttk.Entry(self.item730,width=5,textvariable=self.photosUtilesAutourDuMaitre)        


        # Boite item720 pour le niveau de zoom final
        
        self.item720 = ttk.Frame(self.item700,relief='sunken',padding="0.15cm")      # fera un encadrement pour le zoom 
        self.item722 = ttk.Label(self.item720,text=_("Zoom final : 8, 4, 2 ou 1 (8=le plus rapide, 1=le plus précis)"))
        self.item723 = ttk.Entry(self.item720,width=5,textvariable=self.zoomF)

        # Boite item725 pour obtenir un maillage ou un nuage
        
        self.item725 = ttk.Frame(self.item700,relief='sunken',padding="0.15cm")      # fera un encadrement pour le type de rendu
        self.item726 = ttk.Label(self.item725,text=_("Générer un maillage (1) ou un nuage (0) :"))
        self.item727 = ttk.Entry(self.item725,width=5,textvariable=self.nuage2Mesh)

        # Boite item740 pour Tawny dans item700 pour l'option Ortho 
        
        self.item740 = ttk.Frame(self.item700,relief='sunken',padding="0.2cm")      # fera un encadrement 
        self.item741 = ttk.Checkbutton(self.item740, variable=self.tawny, text=_("Lancer tawny après MALT"))
        self.item742 = ttk.Label(self.item740,text=_("Tawny génère une ortho mosaïque qui sera drapée sur le nuage densifié."))

        # Bouton pour tracer un masque sur la mosaique créée par tarama
        
        self.item745 = ttk.Button(self.item700,text=_('Tracer un masque sur la mosaïque Tarama'),command=self.tracerUnMasqueSurMosaiqueTarama)  
                                         
        self.item701.pack()
        self.item702.pack()         
        self.item703.pack()                
        self.item704.pack(ipady=2,pady=3)
        self.item705.pack()        
        self.item722.pack(side='left')
        self.item723.pack(side='left')
        self.item726.pack(side='left')
        self.item727.pack(side='left')        
        self.item720.pack(pady=3)
        self.item725.pack(pady=3)           
        self.item732.pack(side='left')
        self.item733.pack(side='left')        
        self.item741.pack()
        self.item742.pack()
        
        # Boite item800 pour l'onglet C3DC
        
        self.item800 = ttk.Frame(self.item600,height=5,relief='sunken',padding="0.3cm")     
        self.item808 = ttk.Label(self.item800, text= _("Option de C3DC :" ))
        self.item811 = ttk.Radiobutton(self.item800, text=_("Forest - rapide"),     variable=self.modeC3DC, value='Forest')
        self.item812 = ttk.Radiobutton(self.item800, text=_("Statue - "),     variable=self.modeC3DC, value='Statue')        
        self.item813 = ttk.Radiobutton(self.item800, text=_("QuickMac - rapide"),   variable=self.modeC3DC, value='QuickMac')
        self.item814 = ttk.Radiobutton(self.item800, text=_("MicMac - "),   variable=self.modeC3DC, value='MicMac')
        self.item815 = ttk.Radiobutton(self.item800, text=_("BigMac - plus précis"),   variable=self.modeC3DC, value='BigMac')        
        self.item808.pack(anchor='w')          
        self.item811.pack(anchor='w')
        self.item812.pack(anchor='w')
        self.item813.pack(anchor='w')          
        self.item814.pack(anchor='w')
        self.item815.pack(anchor='w')        
        self.item801 = ttk.Button(self.item800,text=_('Tracer un masque 3D'),command=self.affiche3DApericloud)              
        self.item801.pack(ipady=2,pady=3)
        self.item802 = ttk.Button(self.item800,text=_('Supprimer le masque 3D'),command=self.supprimeMasque3D)              
      
        self.item803 = ttk.Label(self.item800, text= \
                                                   _("Dans la boîte de dialogue pour tracer le masque : " ) +"\n"+\
                                                   _("Agrandir/Diminuer la taille des points : +/-") + "\n"+\
                                                   _("Définir le masque : F9 ") + "\n"+\
                                                   _("Ajouter un point : clic gauche") + "\n"+\
                                                   _("Fermer le polygone : clic droit") + "\n"+\
                                                   _("Sélectionner : touche espace") +"\n"+\
                                                   _("Sauver le masque : Ctrl S.") + "\n"+
                                                   _("Quitter : Ctrl Q.") + "\n\n"+
                                                   _("Saisie simultanée de plusieurs masques disjoints possible"))
        self.item803.pack(ipady=2,pady=3)
        self.item802.pack(ipady=2,pady=3)  
        self.item804 = ttk.Label(self.item800, text= "")    # état du masque (créé, supprimé, absent, absence de nuage non dense)
        self.item804.pack(ipady=2,pady=3)

        
        # Ajout des onglets dans la boite à onglet :
        
        self.onglets.add(self.item400,text=_("Points homologues"))   # add onglet to Notebook        
        self.onglets.add(self.item500,text=_("Orientation"))          # add onglet to Notebook
        self.onglets.add(self.item950,text=_("Mise à l'échelle"))      # add onglet to Notebook
        self.onglets.add(self.item600,text=_("Densification"))


        # boutons  généraux à la boite à onglet :

        self.item450 = ttk.Frame(fenetre)                           # frame pour bouton de validation, permet un ménage facile
        self.item451 = ttk.Button(self.item450,
                                text=_(' Valider les options'),
                                command=self.finOptionsOK)          # bouton permettant de tout valider
        self.item452 = ttk.Button(self.item450,
                                text=_(' Annuler'),
                                command=self.finOptionsKO)          # bouton permettant de tout annuler
        
        # les 2 boutons globaux :
   
        self.item451.pack(side='left')
        self.item452.pack(side='left')

        # La boite de dialogue pour demander les dimensions du capteur de l'appareil photo
        
        self.item1000 = ttk.Frame(fenetre)
        self.item1001 = ttk.Label(self.item1000)
        self.item1002 = ttk.Label(self.item1000,
                                  text= _("Indiquer les dimensions du capteur, en mm.") + "\n"+\
                                        _("par exemple :") + "\n\n                                  5.7  7.6  \n\n"+\
                                        _("Le site :") + "\n \http://www.dpreview.com/products\n"+\
                                        _("fournit les dimensions de presque tous les appareils photos."))
        self.item1003 = ttk.Entry(self.item1000)
        self.item1004 = ttk.Button(self.item1000,
                                text=_(' Valider'),
                                command=self.dimensionCapteurOK)          # bouton permettant de tout valider
        self.item1005 = ttk.Button(self.item1000,
                                text=_(' Annuler'),
                                command=self.dimensionCapteurKO)          # bouton permettant de tout annuler
        self.item1001.pack(pady=15)
        self.item1002.pack(pady=15)
        self.item1003.pack(pady=15)
        self.item1004.pack(pady=15)
        self.item1005.pack(pady=15)


        # La boite de dialogue pour demander les options pour la video (GoPro par défaut)

        self.goProMaker     =   tkinter.StringVar()
        self.goProFocale35  =   tkinter.StringVar()
        self.goProFocale    =   tkinter.StringVar()
        self.goProNomCamera =   tkinter.StringVar()
        self.goProNbParSec  =   tkinter.StringVar()             # taux de conservation des photos pour DIV
        self.goProEchelle   =   tkinter.StringVar()             # pour tapioca 
        self.goProDelta     =   tkinter.StringVar()   

        # l'extension des photos traitées, si les photos choisies sont autres alors conversion automatique   
        self.extensionChoisie = ".JPG"

        
        self.item2000 = ttk.Frame(fenetre)
        self.item2010 = ttk.Label(self.item2000,
                                  text=_("Marque de l'appareil : "))
        self.item2011 = ttk.Entry(self.item2000,
                                  textvariable=self.goProMaker)         
        self.item2001 = ttk.Label(self.item2000,
                                  text=_("Nom de la camera : "))
        self.item2002 = ttk.Entry(self.item2000,
                                  textvariable=self.goProNomCamera)        
        self.item2003 = ttk.Label(self.item2000,
                                  text= _("Focale en mm:"))
        self.item2004 = ttk.Entry(self.item2000,
                                  textvariable=self.goProFocale)
        self.item2005 = ttk.Label(self.item2000,
                                  text= _("Focale équivalente 35mm :"))
        self.item2006 = ttk.Entry(self.item2000,
                                  textvariable=self.goProFocale35)
        self.item2007 = ttk.Label(self.item2000,
                                  text= "--------------\n" + _("Nombre d'images à conserver par seconde :"),
                                  justify='center')
        self.item2008 = ttk.Entry(self.item2000,
                                  textvariable=self.goProNbParSec)        
        
        self.item2020 = ttk.Button(self.item2000,
                                text=_(' Valider'),
                                command=self.optionsGoProOK)          # bouton permettant de tout valider
        self.item2021 = ttk.Button(self.item2000,
                                text=_(' Annuler'),
                                command=self.optionsGoProKO)          # bouton permettant de tout annuler
        self.item2010.pack(pady=5)
        self.item2011.pack(pady=1)        
        self.item2001.pack(pady=5)
        self.item2002.pack(pady=1)
        self.item2003.pack(pady=5)
        self.item2004.pack(pady=1)
        self.item2005.pack(pady=5)
        self.item2006.pack(pady=1)
        self.item2007.pack(pady=5)
        self.item2008.pack(pady=1)  
        self.item2020.pack(pady=5)        
        self.item2021.pack(pady=5)        

        self.goProMaker.set("GoPro") 
        self.goProFocale35.set("16.53") # Hero3
        self.goProFocale.set("2.98") #2.98 4.52
        self.goProNomCamera.set("GoPro Hero3 HD3")
        self.goProNbParSec.set("3")                 # taux de conservation des photos pour DIV
        self.goProEchelle.set("1000")               # pour tapioca 
        self.goProDelta.set("10")
        
    # La fenetre des options pour l'exif :

        self.exifMaker     =   tkinter.StringVar()
        self.exifFocale35  =   tkinter.StringVar()
        self.exifFocale    =   tkinter.StringVar()
        self.exifNomCamera =   tkinter.StringVar()

        self.exifMaker.set("") 
        self.exifFocale35.set("") 
        self.exifFocale.set("")
        self.exifNomCamera.set("")
        
        self.item3000 = ttk.Frame(fenetre)
        self.item3010 = ttk.Label(self.item3000,
                                  text=_("Modification des Exif") + "\n\n" + _("Marque de l'appareil : "))
        self.item3011 = ttk.Entry(self.item3000,
                                  textvariable=self.exifMaker)         
        self.item3001 = ttk.Label(self.item3000,
                                  text=_("Modèle de l'appareil: "))
        self.item3002 = ttk.Entry(self.item3000,
                                  textvariable=self.exifNomCamera)        
        self.item3003 = ttk.Label(self.item3000,
                                  text= _("Focale en mm:"))
        self.item3004 = ttk.Entry(self.item3000,
                                  textvariable=self.exifFocale)
        self.item3005 = ttk.Label(self.item3000,
                                  text= _("Focale équivalente 35mm :"))
        self.item3006 = ttk.Entry(self.item3000,
                                  textvariable=self.exifFocale35)

        self.item3020 = ttk.Button(self.item3000,
                                text=_('Valider et mettre à jour'),
                                command=self.exifOK)          # bouton permettant de tout valider
        self.item3021 = ttk.Button(self.item3000,
                                text=_(' Annuler'),
                                command=self.exifKO)          # bouton permettant de tout annuler
        
        self.item3010.pack(pady=5)
        self.item3011.pack(pady=1)        
        self.item3001.pack(pady=5)
        self.item3002.pack(pady=1)
        self.item3003.pack(pady=5)
        self.item3004.pack(pady=1)
        self.item3005.pack(pady=5)
        self.item3006.pack(pady=1)
        self.item3020.pack(pady=5)        
        self.item3021.pack(pady=5)

        # La boite de dialogue pour demander le nombre de photos a retenir parmi les meilleures
        
        self.item9000 = ttk.Frame(fenetre)
        self.item9002 = ttk.Label(self.item9000,
                                  text= _("Indiquer le nombre de photos à retenir.") + "\n"+
                                        _("Un nouveau chantier sera créé avec les photos ayant, par paire, le plus de points homologues")+ "\n"+
                                        _("Ce choix est différent du nombre moyen de points homologues par photo."))
        self.item9003 = ttk.Entry(self.item9000)
        self.item9004 = ttk.Button(self.item9000,
                                text=_(' Valider'),
                                command=self.nbMeilleuresOK)          # bouton permettant de tout valider
        self.item9005 = ttk.Button(self.item9000,
                                text=_(' Annuler'),
                                command=self.nbMeilleuresKO)          # bouton permettant de tout annuler
        self.item9002.pack(pady=15)
        self.item9003.pack(pady=15)
        self.item9004.pack(pady=15)
        self.item9005.pack(pady=15)

        # La boite de dialogue pour personnaliser les options des modules micmac
        py = 5
        self.item9100 = ttk.Frame(fenetre)
        self.item9101 = ttk.Label(self.item9100,
                                  text= _("Personnaliser les options des modules MicMac.") + "\n\n"+
                                        _("Chaque module MicMac accepte des paramètres nommés, voir la documentation MicMac.")+ "\n"+
                                        _("Vous pouvez définir ici les valeurs de ces paramètres, séparés par des virgules.")+ "\n"+
                                        _("Exemple pour le module Tapioca MulScale : NbMinPt = 20")+ "\n"+
                                        _("Pour le module Malt Ortho : NbProc=3")+ "\n"+
                                        _("Ces paramètres sont enregistrés pour le chantier en cours,")+ "\n"+
                                        _("Utiliser le menu 'Outils/modifier les paramètres par défaut' pour les sauvegarder."))

        self.item9110 = ttk.Frame(self.item9100)
        self.item9112 = ttk.Label(self.item9110, text=_("Paramètres nommés pour Tapioca All : "))
        self.item9113 = ttk.Entry(self.item9110, textvariable=self.tapiocaAllPerso)
        self.item9112.pack(pady=py,side="left")
        self.item9113.pack(pady=py)
        self.item9101.pack()
        self.item9110.pack()
        
        self.item9120 = ttk.Frame(self.item9100)
        self.item9122 = ttk.Label(self.item9120, text=_("Paramètres nommés pour Tapioca MulScale : "))
        self.item9123 = ttk.Entry(self.item9120, textvariable=self.tapiocaMulScalePerso)
        self.item9122.pack(pady=py,side="left")
        self.item9123.pack(pady=py)
        self.item9120.pack()

        self.item9130 = ttk.Frame(self.item9100)
        self.item9132 = ttk.Label(self.item9130, text=_("Paramètres nommés pour Tapioca Line : "))
        self.item9133 = ttk.Entry(self.item9130, textvariable=self.tapiocaLinePerso)
        self.item9132.pack(pady=py,side="left")
        self.item9133.pack(pady=py)
        self.item9130.pack()

        self.item9140 = ttk.Frame(self.item9100)
        self.item9142 = ttk.Label(self.item9140, text=_("Paramètres nommés pour Tapas : "))
        self.item9143 = ttk.Entry(self.item9140, textvariable=self.tapasPerso)
        self.item9142.pack(pady=py,side="left")
        self.item9143.pack(pady=py)
        self.item9140.pack()

        self.item9150 = ttk.Frame(self.item9100)
        self.item9152 = ttk.Label(self.item9150, text=_("Paramètres nommés pour Malt UrbanMNE : "))
        self.item9153 = ttk.Entry(self.item9150, textvariable=self.maltUrbanMnePerso)
        self.item9152.pack(pady=py,side="left")
        self.item9153.pack(pady=py)
        self.item9150.pack()

        self.item9160 = ttk.Frame(self.item9100)
        self.item9162 = ttk.Label(self.item9160, text=_("Paramètres nommés pour Malt GeomImage: "))
        self.item9163 = ttk.Entry(self.item9160, textvariable=self.maltGeomImagePerso)
        self.item9162.pack(pady=py,side="left")
        self.item9163.pack(pady=py)
        self.item9160.pack()

        self.item9170 = ttk.Frame(self.item9100)
        self.item9172 = ttk.Label(self.item9170, text=_("Paramètres nommés pour Malt Ortho : "))
        self.item9173 = ttk.Entry(self.item9170, textvariable=self.maltOrthoPerso)
        self.item9172.pack(pady=py,side="left")
        self.item9173.pack(pady=py)
        self.item9170.pack()        

        self.item9180 = ttk.Frame(self.item9100)
        self.item9182 = ttk.Label(self.item9180, text=_("Paramètres nommés pour C3DC : "))
        self.item9183 = ttk.Entry(self.item9180, textvariable=self.C3DCPerso)
        self.item9182.pack(pady=py,side="left")
        self.item9183.pack(pady=py)
        self.item9180.pack()

        self.item9190 = ttk.Frame(self.item9100)
        self.item9192 = ttk.Label(self.item9190, text=_("Paramètres nommés pour Tawny : "))
        self.item9193 = ttk.Entry(self.item9190, textvariable=self.tawnyPerso)
        self.item9192.pack(pady=py,side="left")
        self.item9193.pack(pady=py)
        self.item9190.pack()

        self.item9200 = ttk.Frame(self.item9100)
        self.item9202 = ttk.Label(self.item9200, text=_("Paramètres nommés pour GcpBascul : "))
        self.item9203 = ttk.Entry(self.item9200, textvariable=self.gcpBasculPerso)
        self.item9202.pack(pady=py,side="left")
        self.item9203.pack(pady=py)
        self.item9200.pack()

        self.item9210 = ttk.Frame(self.item9100)
        self.item9212 = ttk.Label(self.item9210, text=_("Paramètres nommés pour Campari : "))
        self.item9213 = ttk.Entry(self.item9210, textvariable=self.campariPerso)
        self.item9212.pack(pady=py,side="left")
        self.item9213.pack(pady=py)
        self.item9210.pack()

        self.item9220 = ttk.Frame(self.item9100)
        self.item9222 = ttk.Label(self.item9220, text=_("Paramètres nommés pour Apericloud : "))
        self.item9223 = ttk.Entry(self.item9220, textvariable=self.aperiCloudPerso)
        self.item9222.pack(pady=py,side="left")
        self.item9223.pack(pady=py)
        self.item9220.pack()

        self.item9230 = ttk.Frame(self.item9100)
        self.item9232 = ttk.Label(self.item9230, text=_("Paramètres nommés pour Nuage2Ply : "))
        self.item9233 = ttk.Entry(self.item9230, textvariable=self.nuage2PlyPerso)
        self.item9232.pack(pady=py,side="left")
        self.item9233.pack(pady=py)
        self.item9230.pack()

        self.item9230 = ttk.Frame(self.item9100)
        self.item9232 = ttk.Label(self.item9230, text=_("Paramètres nommés pour div : "))
        self.item9233 = ttk.Entry(self.item9230, textvariable=self.divPerso)
        self.item9232.pack(pady=py,side="left")
        self.item9233.pack(pady=py)
        self.item9230.pack()

        self.item9240 = ttk.Frame(self.item9100)
        self.item9242 = ttk.Label(self.item9240, text=_("Paramètres nommés pour mergePly : "))
        self.item9243 = ttk.Entry(self.item9240, textvariable=self.mergePlyPerso)
        self.item9242.pack(pady=py,side="left")
        self.item9243.pack(pady=py)
        self.item9240.pack()
        
        self.item9500 = ttk.Frame(self.item9100)
        self.item9501 = ttk.Button(self.item9500,
                                text=_('Valider'),
                                command=self.optionsPersoOK)          # bouton permettant de tout valider
        self.item9502 = ttk.Button(self.item9500,
                                text=_('Effacer tout'),
                                command=self.initPerso)        # bouton permettant de tout annuler        
        self.item9503 = ttk.Button(self.item9500,
                                text=_('Abandon'),
                                command=self.optionsPersoKO)        # bouton permettant de tout annuler   
        self.item9501.pack(pady=py,side="left")
        self.item9502.pack(pady=py,side="left")
        self.item9503.pack(pady=py,side="left")         
        self.item9500.pack()
        
        # les logo, l'apropos

        self.logo1          = ttk.Frame(fenetre)                                    # cadre dans la fenetre de départ : CEREMA !
        self.logo           = ttk.Frame(self.resul100)                              # logo cerema dans l'apropos             
        self.canvasLogo     = tkinter.Canvas(self.logo,width = 225, height = 80)    # Canvas pour revevoir l'image
        self.logoIgn        = ttk.Frame(self.resul100)                              # logo IGN dans l'apropos 
        self.canvasLogoIGN  = tkinter.Canvas(self.logoIgn,width = 149, height = 162)# Canvas pour revevoir l'image
        self.labelIgn       = ttk.Label(self.logo,text=_("MicMac est une réalisation de\n Marc Pierrot-Deseilligny, IGN"))

        
        # Les fichiers XML :

        # fichier XML de description du masque

        self.masqueXMLOriginal          =   (   '<?xml version="1.0" ?>\n'+
                                                "<FileOriMnt>\n"+
                                                "<NameFileMnt>MonImage_Masq.tif</NameFileMnt>\n"+
                                                "<NombrePixels>largeur hauteur</NombrePixels>\n"+
                                                "<OriginePlani>0 0</OriginePlani>\n"+
                                                "<ResolutionPlani>1 1</ResolutionPlani>\n"+
                                                "<OrigineAlti>0</OrigineAlti>\n"+
                                                "<ResolutionAlti>1</ResolutionAlti>\n"+
                                                "<Geometrie>eGeomMNTFaisceauIm1PrCh_Px1D</Geometrie>\n"+
                                                "</FileOriMnt>"
                                            )

    # Fichier XML self.dicoAppuis de description des points d'appuis X,Y,Z :

        self.dicoAppuisDebut             =  (   '<?xml version="1.0" ?>\n'+
                                                "<Global>\n"+
                                                "<DicoAppuisFlottant>\n"
                                            )
        self.dicoAppuis1Point            =  (  "<OneAppuisDAF>\n"+
                                                "<Pt> X Y Z </Pt>\n"+
                                                "<NamePt> Nom </NamePt>\n"+
                                                "<Incertitude> 10 10 10 </Incertitude>\n"+
                                                "</OneAppuisDAF>\n"
                                            )

        self.dicoAppuisFin               =  (   "</DicoAppuisFlottant>\n"+
                                                "</Global>\n"
                                            )

    # Fichier XML self.mesureAppuis (Mesure-Appuis.xml) positionnant les points d'appuis dans les photos
    # Pour SBGlobBascule les points "Line1" et "Line2" sont interprétés comme définissant une ligne parallèle à l'axe de x.

        self.mesureAppuisDebut          =   ('<?xml version="1.0" ?>\n'+
                                             " <SetOfMesureAppuisFlottants>\n" 
                                            )
        
        self.mesureAppuisDebutPhoto     =   ("   <MesureAppuiFlottant1Im>\n"+
                                            "        <NameIm> NomPhoto </NameIm>\n"
                                            )
        
        self.mesureAppuis1Point         =   ("          <OneMesureAF1I>\n"+
                                             "             <NamePt> NomPoint </NamePt>\n"+
                                             "             <PtIm> X Y </PtIm>\n"+
                                             "          </OneMesureAF1I>\n"
                                             )

        self.mesureAppuisFinPhoto       =   "    </MesureAppuiFlottant1Im>\n"

        self.mesureAppuisFin            =   " </SetOfMesureAppuisFlottants>\n" 

    # Fichier xml de mise à l'échelle : plan horizontal, axe Ox, calibre par distance entre 2 points

        '''"<!--  remplacer :  Or-Init ???

        "Pattern
        
        "Plan :
        "
        "monImage_MaitrePlan,
        "monImage_Plan,
        "
        "Axe :
        "
        "X1H,
        "X2H,
        "Y1H,
        "Y2H,
        "vecteurHV
        "
        "photoHorizon,
        "
        "Echelle :
        "
        "photo1Debut et 
        "X1P1,Y1P1,
        photo1Fin
        "X2P1,Y2P1
        "
        "photo2Debut
        "X1P2,Y1P2,
        "photo2Fin
        "X2P2,Y2P2
        "
        "distance
        "-->'''
       
        self.miseAEchelleXml = ("<Global>\n"+
        "   <ParamApero>\n"+
        "      <DicoLoc>\n"+
        "         <Symb>  AeroIn=-Arbitrary  </Symb>\n"+
        "         <Symb>  AeroOut=-echelle3  </Symb>\n"+
        "      </DicoLoc>\n"+
        "      <SectionBDD_Observation>\n"+
        "         <BDD_PtsLiaisons>\n"+
        "            <Id>    Id_Pastis_Hom  </Id>\n"+
        "            <KeySet> NKS-Set-Homol@@dat  </KeySet>\n"+
        "            <KeyAssoc>  NKS-Assoc-CplIm2Hom@@dat   </KeyAssoc>\n"+
        "          </BDD_PtsLiaisons>\n"+
        "             <BDD_Orient>\n"+
        "                  <Id>  Or-Init   </Id>\n"+
        "                  <KeySet>  NKS-Set-Orient@${AeroIn} </KeySet>\n"+
        "                  <KeyAssoc>  NKS-Assoc-Im2Orient@${AeroIn} </KeyAssoc>\n"+
        "             </BDD_Orient>\n"+ 
        "       </SectionBDD_Observation>\n"+
        "       <SectionInconnues>\n"+
        "          <CalibrationCameraInc>\n"+
        "             <Name> GenerateKC-Others   </Name>\n"+
        "             <CalValueInit>\n"+
        "                <CalFromFileExtern>\n"+
        "                   <NameFile>   ####  </NameFile>\n"+
        "                   <NameTag>    CalibrationInternConique </NameTag>\n"+
        "                </CalFromFileExtern>\n"+
        "             </CalValueInit>\n"+
        "             <CalibPerPose>\n"+
        "                <KeyPose2Cal> NKS-Assoc-FromFocMm@TheKeyCalib_@ </KeyPose2Cal>\n"+
        "                <KeyInitFromPose>  NKS-Assoc-FromFocMm@Ori${AeroIn}/AutoCal@.xml  </KeyInitFromPose>\n"+
        "             </CalibPerPose>\n"+ 
        "          </CalibrationCameraInc>\n"+
        "          <PoseCameraInc>\n"+
        "             <PatternName>  Fichiers </PatternName>\n"+
        "             <CalcNameCalib>  GenerateKC-Others  </CalcNameCalib>\n"+
        "             <PosValueInit>\n"+
        "                <PosFromBDOrient> Or-Init </PosFromBDOrient>\n"+
        "             </PosValueInit>\n"+
        "          </PoseCameraInc>\n"+
        "       </SectionInconnues>\n"+
        "       <SectionChantier>\n"+
        "	       <DirectoryChantier> ThisDir </DirectoryChantier>\n"+
        "       </SectionChantier>\n"+
        "       <SectionSolveur>\n"+
        "    	   <ModeResolution> eSysL2BlocSym </ModeResolution>\n"+ 
        "       </SectionSolveur>\n"+                                
        "       <SectionCompensation>\n"+
        "	   <EtapeCompensation>\n"+
        "             <IterationsCompensation>\n"+
        "	         <SectionContraintes>\n"+
        "		    <ContraintesCamerasInc>\n"+
        "		       <Val> eAllParamFiges  </Val>\n"+
        "		       </ContraintesCamerasInc>\n"+
        "		          <ContraintesPoses>\n"+
        "			     <NamePose>   .* </NamePose>\n"+
        "                            <ByPattern> true </ByPattern>\n"+
        "			     <Val>      ePoseFigee   </Val>\n"+
        "		          </ContraintesPoses>\n"+
        "		       </SectionContraintes>\n"+
        "                      <BasculeOrientation >\n"+
        "                         <PatternNameEstim> monImage_MaitrePlan </PatternNameEstim>\n"+
        "                          <ModeBascule>\n"+
        "                             <BasculeLiaisonOnPlan >\n"+
        "                                <EstimPl>\n"+
        "                                   <KeyCalculMasq>  monImage_Plan </KeyCalculMasq>\n"+
        "                                       <IdBdl >Id_Pastis_Hom </IdBdl>\n"+
        "                                           <Pond>\n"+
        "                                              <EcartMesureIndiv>  1.0 </EcartMesureIndiv>\n"+
        "                                              <Show> eNSM_Paquet     </Show>\n"+
        "                                              <NbMax>   100   </NbMax>\n"+
        "                                              <ModePonderation>  eL1Secured </ModePonderation>\n"+
        "                                              <SigmaPond> 2.0 </SigmaPond>\n"+
        "                                              <EcartMax> 5.0 </EcartMax>\n"+
        "                                       </Pond>\n"+
        "                                       </EstimPl>\n"+
        "                                   </BasculeLiaisonOnPlan>\n"+
        "                               </ModeBascule>\n"+
        "                        </BasculeOrientation>\n"+
        "                        <FixeOrientPlane>\n"+
        "                              <ModeFOP>\n"+
        "                                  <HorFOP>\n"+
        "                                     <VecFOH>\n"+
        "                                        <Pt>  X1H Y1H </Pt>\n"+
        "                                        <Im>  photoHorizon </Im>\n"+
        "                                     </VecFOH>\n"+
        "                                     <VecFOH>\n"+
        "                                        <Pt>  X2H Y2H </Pt>\n"+
        "                                        <Im>   photoHorizon </Im>\n"+
        "                                     </VecFOH>\n"+
        "                                  </HorFOP>\n"+
        "                              </ModeFOP>\n"+
        "                              <Vecteur> vecteurHV </Vecteur>\n"+            # 1 0 si horizontal 01 si vertical
        "                          </FixeOrientPlane>\n"+
        "			   <FixeEchelle>\n"+
        "                               <ModeFE>\n"+
        "                                    <StereoFE>\n"+
        "                                       <!-- <Point1>-->\n"+
        "                                     <HomFE>\n"+ 
        "                                             <P1> X1P1 Y1P1 </P1>\n"+
        "                                             <Im1> photo1Debut  </Im1>\n"+
        "                                             <P2> X1P2 Y1P2 </P2>\n"+
        "                                             <Im2> photo2Debut  </Im2>\n"+
        "                                     </HomFE>\n"+
        "                                     <!--  <Point2>-->\n"+
        "                                      <HomFE>\n"+ 
        "                                            <P1> X2P1 Y2P1 </P1>\n"+
        "                                            <Im1>  photo1Fin </Im1>\n"+
        "                                            <P2> X2P2 Y2P2 </P2>\n"+
        "                                            <Im2>  photo2Fin </Im2>\n"+
        "                                        </HomFE>\n"+
        "                                    </StereoFE>\n"+
        "                               </ModeFE>\n"+
        "                               <DistVraie> distance </DistVraie>\n"+
        "                           </FixeEchelle>\n"+
        "                   </IterationsCompensation>\n"+
        "             <SectionObservations> </SectionObservations>\n"+
        "	      </EtapeCompensation>\n"+
        "	      <EtapeCompensation>\n"+
        "                    <IterationsCompensation> </IterationsCompensation>\n"+
	"				<SectionObservations>\n"+
        "                   <ObsLiaisons>\n"+
        "                      <NameRef> Id_Pastis_Hom </NameRef>\n"+
        "                      <Pond>\n"+
        "                         <EcartMesureIndiv>  1.0 </EcartMesureIndiv>\n"+
        "                         <Show> eNSM_Paquet     </Show>\n"+
        "                         <NbMax>   100    </NbMax>\n"+
        "                         <ModePonderation>  eL1Secured </ModePonderation>\n"+
        "                         <SigmaPond> 2.0 </SigmaPond>\n"+
        "                         <EcartMax> 5.0 </EcartMax>\n"+
        "                      </Pond>\n"+
        "                   </ObsLiaisons>\n"+
        "            </SectionObservations>\n"+                     
        "                    <SectionExport>\n"+
        "                            <ExportPose>\n"+
        "                                <PatternSel> (.*) </PatternSel>\n"+
        "                                <KeyAssoc> NKS-Assoc-Im2Orient@${AeroOut} </KeyAssoc>\n"+
        "                                <AddCalib>  true </AddCalib>\n"+
        "                                <NbVerif>  10 </NbVerif>\n"+
        "                                <TolWhenVerif> 1e-3 </TolWhenVerif>\n"+
        "                                <FileExtern> NKS-Assoc-FromFocMm@Ori${AeroOut}/AutoCal@.xml </FileExtern>\n"+
        "                                <FileExternIsKey> true </FileExternIsKey>\n"+
        "                            </ExportPose>\n"+
        "                             <ExportCalib>\n"+
        "                                 <KeyAssoc>  NKS-Assoc-FromKeyCal@Ori${AeroOut}/AutoCal@.xml </KeyAssoc>\n"+
        "                                 <KeyIsName> false </KeyIsName>\n"+
        "                            </ExportCalib>\n"+
        "                            <ExportNuage>\n"+
        "                                   <NameOut> echelle3.ply </NameOut>\n"+
        "                                   <PlyModeBin> true </PlyModeBin>\n"+
        "                                   <NameRefLiaison> Id_Pastis_Hom </NameRefLiaison>\n"+
        "                                   <Pond>\n"+
        "                                          <EcartMesureIndiv>  1.0 </EcartMesureIndiv>\n"+
        "                                          <EcartMax> 0.4 </EcartMax>\n"+
        "                                   </Pond>\n"+
        "                                   <KeyFileColImage>NKS-Assoc-Id   </KeyFileColImage>\n"+
        "                                   <NuagePutCam >\n"+
        "                                       <ColCadre > 255 0 0 </ColCadre>\n"+
        "                                       <ColRay >  0 255 0 </ColRay>\n"+
        "                                       <Long > 0.3 </Long>\n"+
        "                                       <StepSeg > 0.01 </StepSeg>\n"+
        "                                   </NuagePutCam>\n"+
        "                             </ExportNuage>\n"+
        "                    </SectionExport>\n"+
        "	      </EtapeCompensation>\n"+
        "	</SectionCompensation>\n"+
        "   </ParamApero>\n"+
        "</Global>")

    # Contenu Fichier xml DicoCamera
    
        self.dicoCameraXMLDebut = "<MMCameraDataBase>\n"
        
        self.dicoCameraXMLTaille = ("   <CameraEntry>\n"+
                                    "          <Name> Nom </Name>\n"+
                                    "          <SzCaptMm> tailleEnMM </SzCaptMm>\n"+
                                    "          <ShortName> NomCourt </ShortName>\n"+
                                    "   </CameraEntry>\n")
        
        self.dicoCameraXMLFin = "</MMCameraDataBase>"

    # fichier définissant un repère local(système de coordonnées) euclidien (RTL = Référentiel Terrestre Local)
    # utile pour exploité les coordonnées GPS des appareils photos embarqués sur des drones

        self.sysCoRTL = (   "<SystemeCoord>\n"+
                            "    <BSC>\n"+
                            "        <TypeCoord>  eTC_RTL </TypeCoord>\n"+
                            "        <AuxR> longitude	  </AuxR>\n"+
                            "        <AuxR> latitude	  </AuxR>\n"+
                            "        <AuxR> altitude	  </AuxR>\n"+
                            "    </BSC>\n"+		
                            "    <BSC>\n"+                            
                            "        <TypeCoord>  eTC_WGS84 </TypeCoord>\n"+
                            "        <AuxRUnite> eUniteAngleDegre </AuxRUnite>\n"+
                            "    </BSC>\n"+
                            "</SystemeCoord>")

    # fichier définissant le système de projection Lambert 93 (système de coordonnées) euclidien

        self.lambert93XML = (  "<SystemeCoord>\n"+
                            "   <BSC>\n"+
                            "       <TypeCoord>  eTC_Proj4 </TypeCoord>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "   <AuxStr>\n"+
                           "       +proj=lcc +lat_0=46.5 +lon_0=3 +lat_1=49 +lat_2=44 +x_0=700000 +y_0=6600000 +ellps=GRS80 +units=m +no_defs \n"+
			    "   </AuxStr>\n"+
			    "   <!--	Lambert 93 EPSG 2154 -->\n"+
                            "   </BSC>\n"+
                            "</SystemeCoord>")
    # Template définissant un système de projection EPSG en format proj4 (système de coordonnées) : remplacer epsgproj4 par la bonne valeur

        self.SysCoEpsg = (  "<SystemeCoord>\n"+
                            "   <BSC>\n"+
                            "       <TypeCoord>  eTC_Proj4 </TypeCoord>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "       <AuxR>       1        </AuxR>\n"+
                            "       <AuxStr>\n"+
                            "            epsg2proj4     \n"+
			    "       </AuxStr>\n"+
			    "   <!--	nomEpsg -->\n"+                            
                            "   </BSC>\n"+
                            "</SystemeCoord>")
    
    # Fichier de persistance des paramètres
        
        self.paramChantierSav           =   'ParamChantier.sav'
        self.fichierParamMicmac         =   os.path.join(self.repertoireData,'ParamMicmac.sav')       # sauvegarde des paramètres globaux d'AperodeDenis
        self.fichierParamChantierEnCours=   os.path.join(self.repertoireData,self.paramChantierSav)   # sauvegarde du chantier encours 
        self.fichierSauvOptions         =   os.path.join(self.repertoireData,'OptionsMicmac.sav')     # pour la sauvegarde d'options personnalisées

    # concernant le nettoyage des chantiers : on ne supprime que les répertoires de la liste listeRepertoiresASupprimer
    
        self.chantierNettoye            = False   # par défaut : le chantier n'est pas nettoyé !
        self.listeRepertoiresASupprimer = ["Homol*","Ori-*","PIMs-*","MTD-*","MM-*","MEC*","Tmp*","Ortho*","test_*","Pastis*","Pyram*","TA*"]
        self.listeRepertoiresAConserver = ["PhotosCalibrationIntrinseque"]      # pour mémoire et usage futur
    
    # Divers

        self.logoCerema                 =       os.path.join(self.repertoireScript,'logoCerema.jpg')
        self.logoIGN                    =       os.path.join(self.repertoireScript,'logoIGN.jpg')
        self.messageNouveauDepart       =       str()   # utilisé lorsque l'on relance la fenêtre
        self.nbEncadre                  =       0       # utilisé pour relancer la fenetre
        self.suffixeExport              =       "_export"  # ne pas modifier : rendra incompatible la nouvelle version
        self.messageSauvegardeOptions   =       (_("Quelles options par défaut utiliser pour les nouveaux chantiers ?") + "\n"+
                                                _("Les options par défaut concernent :") + "\n"+
                                                _("Points homologues : All, MulScale, line ,les échelles et delta") + "\n"+
                                                _("Orientation : toutes les options de la boite de dialogue") + "\n"+                                                 
                                                _("Densification Malt : mode, zoom final, nombre de photos autour de la maîtresse") + "\n"+
                                                _("Densification Malt Ortho : Tawny et ses options en saisie libre") + "\n"+
                                                _("Densification C3DC : mode") + "\n"+
                                                _("Les paramètres presonnalisés des modules Micmac (menu Expert)") + "\n\n"+
                                                _("Calcul du volume entre 2 MNT : tolerance") + "\n\n"
                                                 )
        
        self.tacky                      = True    # Suite au message de Luc Girod sur le forum le 21 juin 17h        
        self.avertirNouvelleVersion     = True    # vérifie au lancement la présence d'une version sur GitHub
        
    # il faudrait mettre ici les textes de l'Aide, des conseils, de l'historique, de l'apropos
    # les menus
        self.aide1 = _("Interface graphique du CEREMA pour lancer les modules de MICMAC.") + "\n\n"+\
            _("Utilisable sous Linux, Windows, Mac OS.") + "\n"+\
            _("Logiciel libre et open source diffusé sous licence CeCILL-B.") + "\n"+\
            "-----------------------------------------------------------------------------------------------------------------\n\n"+\
            _("La barre de titre présente le nom du chantier et la version de l'outil. Une * indique que le chantier est à sauvegarder.") + "\n\n"+\
            _("Menu Fichier :") + "\n\n"+\
            _("       - Nouveau chantier : constitution d'un 'chantier' comportant les photos, les options d'exécution de Micmac et") + "\n"+\
            _("         les résultats des traitements.") +"\n"+\
            _("         Les paramètres du chantier sont conservés dans le fichier ")+self.paramChantierSav+".\n"+\
            _("         Enregistrer le chantier crée une arborescence dont la racine est le répertoire des photos et le nom du chantier.") + "\n\n"+\
            _("       - Ouvrir un chantier : revenir sur un ancien chantier pour le poursuivre ou consulter les résultats.") + "\n\n"+\
            _("       - Enregistrer le chantier : enregistre le chantier en cours.") + "\n"+\
            _("         Une * dans la barre de titre indique que le chantier a été modifié.") + "\n"+\
            _("         Le chantier en cours est conservé lors de la fermeture de l'application.") + "\n\n"+\
            _("       - Renommer le chantier : personnalise le nom du chantier.") + "\n\n"+\
            _("         Le chantier est déplacé dans l'arborescence en indiquant un chemin absolu ou relatif.") + "\n"+\
            _("         Par exemple : 'D:\\MonPremierChantier' nomme 'MonPremierChantier' sous la racine du disque D.") + "\n"+\
            _("         Attention : le changement de disque n'est pas possible dans cette version de l'outil.") + "\n\n"+\
            _("       - Enregistrer sous... : copie du chantier sous un nouveau répertoire. Le répertoire initial est conservé, inutilisé.") + "\n"+\
            _("         Le changement d'unité disque est valide. Attention à la taille du chantier.:") + "\n"+\
            _("       - Exporter le chantier en cours : création d'une archive du chantier, qui permet :") + "\n"+\
            _("            - de conserver le chantier en l'état, pour y revenir.") + "\n"+\
            _("            - de l'importer sous un autre répertoire, un autre disque, un autre ordinateur, un autre système d'exploitation") + "\n\n"+\
            _("       - Importer un chantier :") + "\n"+\
            _("            - copie le chantier sauvegardé dans un nouvel environnement (ordinateur, système d'exploitation)") + "\n"+\
            _("            - un exemple d'intérêt : copier un chantier après tapas, lancer malt avec des options variées sans perdre l'original.") + "\n\n"+\
            _("       - Ajouter le répertoire d'un chantier :") + "\n"+\
            _("            - ajoute le chantier présent sous le répertoire indiqué. Alternative moins robuste à l'export/import)") + "\n"+\
            _("       - Du ménage ! : nettoyer ou supprimer les chantiers : chaque chantier crée une arborescence de travail assez lourde.") + "\n"+\
            _("         Le nettoyage ne garde que les photos, les modèles 3D résultats, les traces, les paramètres : gain de place assuré !.") + "\n"+\
            _("         La suppression supprime tout le chantier sans mise à la corbeille.") + "\n"+\
            _("         Un message demande confirmation avant la suppression définitive, sans récupération possible :") + "\n"+\
            _("         Toute l'arborescence est supprimée, même les archives exportées.") + "\n\n"+\
            _("       - Quitter : quitte l'application, le chantier en cours est conservé et sera ouvert lors du prochain lancement.") + "\n\n"+\
            _("Menu Edition :") + "\n\n"+\
            _("       - Afficher l'état du chantier : affiche les paramètres du chantier et son état d'exécution.") + "\n"+\
            _("         Par défaut l'état du chantier est affiché lors du lancement de l'application.") + "\n"+\
            _("         Cet item est utile après un message ou l'affichage d'une trace.") + "\n\n"+\
            _("       - Plusieurs items permettent de consulter les photos, les traces et les vues 3D du chantier en cours.") + "\n\n"+\
            _("            Visualiser toutes les photos sélectionnées : visualise les photos") + "\n"+\
            _("            Visualiser les photos pour la calibration intrinsèque") + "\n"+\
            _("            Visualiser les maitresses et les masques   : visualise les masques 2D pour la densification Malt/géoimage.") + "\n"+\
            _("            Visualiser le masque sur mosaïque TARAMA   : visualise le masque défini sur la mosaïque TARAMA.") + "\n"+\
            _("            Visualiser le masque 3D                    : visualise le masque 3D pour la densification C3DC") + "\n"+\
            _("            Visualiser les points GCP                  : visu des seules photos avec points GCP.") + "\n"+\
            "\n"+\
            _("            Visualiser la ligne horizontale/verticale  : visualise le repère Ox ou Oy pour la mise à l'échelle.") + "\n"+\
            _("            Visualiser la zone plane                   : visualise la zone plane") + "\n"+\
            _("            Visualiser la distance                     : visualise de la distance et les points associés.") + "\n"+\
            "\n"+\
            _("            Afficher la trace complete du chantier     : visualise la trace complète, standard micmac") + "\n"+\
            _("            Afficher la trace synthétique du chantier  : visualise la trace filtrée par aperoDeDenis, moins bavarde") + "\n\n"+\
            "\n"+\
            _("            Afficher la mosaïque Tarama                : si la mosaïque tarama est demandée dans l'onglet 'orientation'") + "\n"+\
            _("            Afficher l'ortho mosaïque Tawny            : l'ortho mosaïque tawny est demandée dans l'onglet Densifisation/Malt/Ortho") + "\n"+\
            "\n"+\
            _("            Afficher l'image 3D non densifiée          : lance l'outil pour ouvrir les .PLY sur l'image 3D produite par Tapas") + "\n"+\
            _("            Afficher l'image 3D densifiée              : lance l'outil pour ouvrir les .PLY sur l'image 3D produite par Malt ou C3DC") + "\n"+\
            "\n"+\
            _("            Lister Visualiser les images 3D            : liste la pyramide des images 3D, créées à chaque étape de Malt") + "\n"+\
            _("            Fusionner des images 3D                    : permet de fusionner plusieurs PLY en un seul") + "\n"+\
            _("            Infos sur une image 3D                     : affiche le nombre de points, les dimensions de la 'box',") + "\n"+\
            _("                                                         la surface et le volume, la densité de points sur la surface et le volume. ") + "\n\n"+\
            _("Menu MicMac :") + "\n\n"+\
            _("       - Choisir les photos : permet choisir les photos JPG, GIF, TIF ou BMP pour le traitement.") + "\n\n"+\
            _("         Les photos GIF et BMP seront converties en JPG (nécessite la présence de l'outil convert).") + "\n"+\
            _("         Un EXIF avec la focale utilisée pour la prise de vue est nécessaire : si besoin l'ajouter (menu Outil/ajout exif).") + "\n"+\
            _("         Remarques : 1) Si l'exif ne comporte pas la focale équivalente en 35 mm alors ")+ "\n"+\
            _("                     le fichier DicoCamera.xml doit comporter la taille du capteur de l'appareil (voir menu Outils)") + "\n\n"+\
            _("                     la page web http://www.dpreview.com/products fournit beaucoup de tailles de capteurs.") + "\n\n"+\
            _("                     2) Si les photos proviennent de plusieurs appareils alors les tags 'model' des exif doivent") + "\n"+\
            _("                     être différenciés (voir menu Expert)") + "\n\n"+\
            _("       - Options : choisir les options des modules Tapioca, Tapas, GCP (nuage non densifié)  puis de densification : ") + "\n\n"+\
            _("                   Consulter le wiki MicMac pour obtenir de l'info sur les options, par exemple : https://micmac.ensg.eu/index.php/Tapas") + "\n\n"+\
            _("         Les options suivantes concernent le calcul du nuage de points NON densifié :") + "\n\n"+\
            _("                    - Points homologues : Tapioca : options et sous options associées (échelles, fichier xml)")+ "\n"+\
            _("                                Voir la documentation MicMac sur Tapioca.") + "\n"+\
            _("                    - Orientation : Tapas : choix d'un type d'appareil  photo , possibilité d'arrêter le traitement après tapas.") + "\n"+\
            _("                                Le type d'appareil photo détermine le nombre de paramètres décrivant l'optique et le capteur.") + "\n"+\
            _("                                Si plusieurs appareils photos alors il faut les distinguer, voir menu expert.") + "\n"+\
            _("                                La calibration intrinsèque permet de déterminer les caractéristiques de l'appareil sur des photos spécifiques :") + "\n"+\
            _("                                  Par exemple photos d'un angle de batiment avec une grande longueur de mur.")+ "\n"+\
            _("                                  Ces photos ne servent pas nécessairement pour la suite du chantier.")+ "\n"+\
            _("                                L'arrêt après Tapas est nécessaire pour décrire le masque 2D ou 3D.") + "\n"+\
            _("                                La production du nuage de point non dense est optionnelle.") + "\n\n"+\
            _("                                Si elle est demandée l'image 3D non dense positionne les appareils photos.") + "\n\n"+\
            _("                    - Mise à l'échelle : définir un axe, une zone plane, une distance pour définir la métrique du chantier.") + "\n\n"+\
            _("                                cette mise à l'échelle définit un repère pour les nuages de points") + "\n\n"+\
            _("                    - GCP : Ground Control Point : point de repère marqués sur le terrain, coordonnées repérées localement ou par GPS.") + "\n"+\
            _("                    - GCP : définir les points de calage qui permettent de (géo)localiser la scène.") + "\n"+\
            _("                            Une première ligne permet de définir les options du module CAMPARI qui améliore la précision des calculs.") + "\n"+\
            _("                            Il faut indiquer la précision des cibles GCP (en unité du GCP) et la précision des points images (en pixels).") + "\n"+\
            _("                            CAMPARI ne sera lancé que si les points GCP sont corrects ainsi que les 2 paramètres ci-dessus.") + "\n\n"+\
            _("                            Pour être utilisé chaque point GCP, au minimum 3, doit être placé sur au moins 2 photos.") + "\n"+\
            _("                            Le bouton 'appliquer' permet de calibrer le modèle non densifié immédiatement sur le nuage de points homologues.") + "\n\n"+\
            _("                            La qualité de positionnement des points GCP est consultable (menu Outils).") + "\n\n"+\
            _("                    - Densification    : choix du module de densification : C3DC (récent) ou Malt (ancien).") + "\n"+\
            _("                      - Malt : Si le mode est GeomImage : ") + "\n"+\
            _("                                  désigner une ou plusieurs images maîtresses") + "\n"+\
            _("                                  dessiner si besoin le ou les masques associés.") + "\n"+\
            _("                                  Seuls les points visibles sur les images maitres seront sur l'image 3D finale.") + "\n"+\
            _("                                  Le masque limite la zone utile de l'image 3D finale.") + "\n"+\
            _("                                  La molette permet de zoomer et le clic droit maintenu de déplacer l'image.") + "\n"+\
            _("                                  Supprimer une image maîtresse de la liste réinitialise le masque.") + "\n\n"+\
            _("                                  Nombre de photos utiles autour de l'image maîtresse :") + "\n"+\
            _("                                    Permet de limiter les recherches aux images entourant chaque image maîtresse.") + "\n\n"+\
            _("                                  Choix du niveau de densification final : 8,4,2 ou 1.") + "\n"+\
            _("                                  Le niveau 1 est le plus dense. ") + "\n"+\
            _("                                  La géométrie est revue à chaque niveau et de plus en plus précise : ") + "\n"+\
            _("                                    la densification s'accroît, et la géométrie s'affine aussi.") + "\n\n"+\
            _("                      - C3DC : choix par défaut. Plusieurs options, de précision croissante.") + "\n"+\
            _("                               Possibilité de dessiner un masque 3D sur le nuage de points non dense.") + "\n"+\
            _("                               Les touches fonctions à utiliser sont décrites dans l'onglet.") + "\n"+\
            _("                               Le masque limite la zone en 3 dimensions de l'image finale.") + "\n"+\
            _("                               L'outil de saisie est issu de micmac.") + "\n\n"+\
            _("       - Lancer MicMac : enregistre le chantier et lance le traitement avec les options par défaut ou choisies par l'item 'options'.") + "\n"+\
            _("                         Relance micmac si l'arrêt a été demandé après tapas.") + "\n"+\
            _("                         Une fois la densification terminée le chantier est 'bloqué'.") + "\n"+\
            _("                         Pour le débloquer il faut lancer micmac à nouveau et choisir le débloquage.") + "\n"+\
            _("                         Le débloquage permet de relancer Tapas ou Malt sans relancer tapioca tout en conservant le modèle densifié, renommé.") + "\n\n"+\
            _("menu Vidéo :") + "\n\n"+\
            _("       - Options : indiquer le nom de la camera (GoPro, smartphone...), sa focale, sa focale equivalente 35mm") + "\n"+\
            _("         et le nombre d'images à conserver par seconde de film") + "\n"+\
            _("         Le nom permet de faire le lien avec DicoCamera.xml qui contient la taille du capteur.") + "\n"+\
            _("         Les focales seront recopiées dans l'exif des images.") + "\n"+\
            _("         Le nombre d'images par seconde sera utilisé pour la sélection des meilleures images.") + "\n\n"+\
            _("         Remarque :") + "\n"+\
            _("           Il faut indiquer dans DicoCamera la taille du capteur effectivement utilisée par la fonction camera,") + "\n"+\
            _("           taille qui peut être inférieure à la taille du capteur utilisée pour les photos.") + "\n"+\
            _("           Voir par exemple pour une camera Gopro :") + "\n"+\
            "           http://www.kolor.com/wiki-en/action/view/Autopano_Video_-_Focal_length_and_field_of_view#About_GoPro_focal_length_and_FOV" + "\n\n"+\
            _("       - Nouveau chantier : choisir une video : choisir un fichier video issu d'une camera ou d'une GoPro.") + "\n"+\
            _("         La vidéo sera décompactée en images, l'exif sera créé avec les informations en options.") + "\n"+\
            _("         Cette étape nécessite la présence de l'outil ffmpeg sous le répertoire bin de MicMac (dépend de la version de MicMac).") + "\n"+\
            _("         Un nouveau chantier est créé avec les options suivante : Line pour Tapioca et FishEyeBasic pour Tapas.") + "\n\n"+\
            _("       - Sélection des images : il est raisonnable de ne garder que quelques images par seconde de film.") + "\n"+\
            _("         Le nombre d'images conservées par seconde est indiqué dans les options.") + "\n"+\
            _("         Chaque seconde de film les 'meilleures' images seront retenues, les autres effacées.") + "\n"+\
            _("         Attention : cette étape n'est pas effective pour toutes les versions de MicMac. La version mercurial 5508 fonctionne.") + "\n\n"+\
            _("         Une fois les images sélectionnées le chantier est créé : utiliser le menu MicMac comme pour un chantier normal.") + "\n\n"+\
            _("menu Outils :") + "\n\n"+\
            _("       - Info extraites de l'exif : fabricant, modèle, focale  et dimensions en pixels de la première photo.") + "\n"+\
            _("         Il y a 2 types de focales : focale effective et focale équivalente 35 mm.") + "\n"+\
            _("         Indique si l'appareil photo est connu dans '/XML MicMac/DicoCamera.xml'.") + "\n\n"+\
            _("       - Afficher toutes les focales des photos : focales et focales equivalentes en 35mm.") + "\n"+\
            _("         Si les focales ne sont pas identiques pour toutes les photos : utiliser la calibration intrinséque de tapas.") + "\n"+\
            _("         Affiche aussi le nom de l'appareil photo pour chaque photo.") + "\n\n"+\
            _("       - Mettre à jour DicoCamera.xml : ajouter la taille du capteur dans '/XML MicMac/DicoCamera.xml'.") + "\n"+\
            _("         La taille du capteur dans DicoCamera.xml est requise si la focale équivalente 35mm est absente de l'exif.") + "\n"+\
            _("         La taille du capteur facilite les calculs et améliore les résultats.") + "\n"+\
            _("         La taille du capteur se trouve sur le site du fabricant ou sur http://www.dpreview.com.") + "\n\n"+\
            _("       - Qualité des photos du dernier traitement : calcule le nombre moyen de points homologues par photo.") + "\n"+\
            _("         La présence de photos avec peu de points homologues peut faire échouer le traitement.") + "\n"+\
            _("         Il est parfois préférable de traiter peu de photos mais de bonne qualité.") + "\n\n"+\
            _("       - Qualité des points GCP : le module GCPBascule vérifie la position annoncée des points GCP.") + "\n\n"+\
            _("         Cet item affiche le résultat synthétique du controle. La trace détaillée comporte plus de détails.") + "\n\n"+\
            _("       - Modifier l'exif des photos : permet la création et la modification des exifs des photos du chantier.") + "\n\n"+\
            _("       - Modifier les options par défauts : les valeurs par défaut de certains paramètres sont modifiables.") + "\n"+\
            _("         Les paramètres concernés sont ceux des onglets du menu MicMac/options : 'Points homologues',... : .") + "\n\n"+\
            _("menu Expert :") + "\n\n"+\
            _("       Le menu expert comporte des sous menus dédiés :).") + "\n\n"+\
            _("         - aux chantiers comportant plusieurs appareils photos différents.") + "\n"+\
            _("         - aux importaions de données d'un autre chantier (points homologues, orientation).") + "\n"+\
            _("         - aux photos de drones comportant des données GPS.") + "\n"+\
            _("       - Ouvrir une console permettant de passer des commandes système et MicMac (par exemple : mm3d).") + "\n\n"+\
            _("       - Ouvrir une console permettant de passer des commandes Python (ex. : afficher une variable.)") + "\n\n"+\
            _("       - Insérer de points GCP à partir d'un fichier texte, séparateur espace, format : NomDuPoint X Y Z 'dx dy dz' ") + "\n"+\
            _("         Les valeurs dx dy dz sont des écarts en nombre entier de pixels image, en une seule chaine : exemple : '2 2 2' ") + "\n"+\
            _("         Le caractère # en début de ligne signale un commentaire.") + "\n\n"+\
            _("       - Recopier des points GCP à partir d'un autre chantier.") + "\n\n"+\
            _("       - Recopier les points homologues à partir d'un autre chantier, seuls les chantiers compatibles sont proposés.") + "\n\n"+\
            _("         Utile pour éviter le recalcul pour les nouveaux chantiers composés d'un sous ensemble de photos du chantier initial.") + "\n\n"+\
            _("       - Définir plusieurs appareils photos.") + "\n"+\
            _("         Si le lot de photos provient de plusieurs appareils de même type il faut informer MicMac de cette situation.") + "\n"+\
            _("         AperoDeDenis propose de modifier le tag 'model' de l'exif des photos :") + "\n"+\
            _("           - à défaut en utilisant le préfixe des noms de fichiers, que l'utilisateur a préparé de telle sorte") + "\n"+\
            _("             que chaque préfixe corresponde à un appareil. Certains appareil proposent de modifier ce préfixe.") + "\n\n"+\
            _("       - Définir la longueur du préfixe utilisé dans l'item précédent.") + "\n\n"+\
            _("       - Lister les appareils photos présents dans le lot de photos.") + "\n\n"+\
            _("       - Personnaliser les paramètres optionnels des modules MicMac.") + "\n\n"+\
            _("         Permet l'ajout et la surcharge des paramètres nommés des modules MicMac.") + "\n\n"+\
            _("         Exemple : Malt est très consommateur de ressources CPU et utilise tous les coeurs du processeur.") + "\n"+\
            _("         Il admet un paramètre NbProc qui permet de limiter ce nombre, facilitant les autres activités de l'ordinateur.") + "\n\n"+\
            _("         Autre exemple : Tapioca MulScale admet NbMinPt=XX indiquant le nombre minimum de points pour conserver les paires.") + "\n\n"+\
            _("       - Consulter le fichier de logging MicMac : mm3d-logFile.txt.") + "\n\n"+\
            _("       - Navigation GPS : utilisation des données GPS mémorisées par les caméras embarquées sur les drones.") + "\n"+\
            _("         Les données sont exploitées automatiquement et un repère local WGS84 est créé.") + "\n"+\
            _("         Si des points GCP sont saisis alors ils sont prioritaires et les données GPS sont ignorées.") + "\n"+\
            _("         4 items de menus permettent de : .") + "\n"+\
            _("           - choisir le repère : local (WGS84, équivalent Lambert 93 en France métropolitaine) , ou géocentrique") + "\n"+\
            _("           - choisir un référentiel EPSG. Le référentiel doit avoir ses coordonnées en mètres. Le module pyproj est nécessaire.") + "\n"+\
            _("           - ignorer les données GPS des photos.") + "\n"+\
            _("           - afficher les ccoordonnées (WGS84 et Lambert 93) du point origine du repère local.") + "\n\n"+\
            _("       - exporter un nuage de points au format MNT IGN et GRASS. Le ply doit être un nuage de points.")+ "\n\n"+\
            _("menu Outils métiers :") + "\n\n"+\
            _("       - Voir l'aide dans l'item Aide du menu Outils métiers") + "\n\n"+\
            _("menu Paramétrage :") + "\n\n"+\
            _("       - Afficher les paramètres : visualise les chemins de micmac\\bin, d'exiftool, du fichier pour visualiser les .ply (Meshlab ou Cloud Compare),") + "\n"+\
            _("         ainsi que le répertoire où se trouve les fichiers paramètres de l'interface.") + "\n"+\
            _("         Ces paramètres sont sauvegardés de façon permanente dans le fichier :")+\
            "         "+self.fichierParamMicmac+"." + "\n\n"+\
            _("       - Désigner le répertoire MicMac\\bin : répertoire où se trouvent les modules de MicMac ") + "\n"+\
            _("         Si plusieurs versions sont installées cet item permet de changer facilement la version de MicMac utilisée.") + "\n\n"+\
            _("       - Désigner l'application exiftool, utile pour modifier les exif (elle se trouve sous micMac\\binaire-aux).") + "\n\n"+\
            _("       - Désigner l'application convert d'ImageMagick, utile pour convertir les gif, tif et bmp en jpg (elle se trouve sous micMac\\binaire-aux).") + "\n\n"+\
            _("       - Désigner l'application ouvrant les fichiers .PLY. Ce peut être  Meshlab, CloudCompare ou autre.") + "\n"+\
            _("         Sous Windows Meshlab se trouve sous un répertoire nommé VCG.") + "\n\n"+\
            _("       - Activer/désactiver le 'tacky' message de lancement")+ "\n\n"+\
            _("menu Aide :") + "\n\n"+\
            _("       - Pour commencer : à lire lors de la prise en main de l'interface.") + "\n\n"+\
            _("       - Aide : le détail des items de menu.") + "\n\n"+\
            _("       - Quelques conseils sur la prise de vue.") + "\n\n"+\
            _("       - Quelques conseils sur le choix des options.") + "\n\n"+\
            _("       - Quelques conseils si MicMac ne trouve pas de points homologues ou d'orientation.") + "\n\n"+\
            _("       - Quelques conseils si MicMac si MicMac ne trouve pas de nuage dense.") + "\n\n"+\
            _("       - Historique : les nouveautés de chaque version.") + "\n\n"+\
            _("       - A propos") + "\n\n\n"+\
            _(" Consulter la documentation de MicMac, outil réalisé par l'IGN.") + "\n\n"+\
            _(" Consulter le guide d'installation et de prise en main d'AperoDeDenis.") + "\n\n"+\
            "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

    # les prises de vue
        self.aide2 = _("Interface graphique AperoDeDenis : quelques conseils concernant les prises de vues.") + "\n\n"+\
                _("Prises de vue  :") + "\n"+\
                _("                - Le sujet doit être immobile durant toutes la séance de prise de vue.") + "\n"+\
                _("                - Le sujet doit être unique et d'un seul tenant") + "\n"+\
                _("                - Le sujet doit être bien éclairé, la prise de vue en plein jour doit être recherchée.") + "\n"+\
                _("                - Les photos doivent être nettes, attention à la profondeur de champ :") + "\n"+\
                _("                  utiliser la plus petite ouverture possible (nombre F le plus grand, par exemple 22).") + "\n"+\
                _("                - Utiliser la calibration intrinsèque des appareils photos (item MicMac/Options/Orientation ).") + "\n"+\
                _("                - Les photos de personnes ou d'objet en mouvement sont déconseillées") + "\n"+\
                _("                - Les surfaces lisses ou réfléchissantes sont défavorables.") + "\n"+\
                _("                - Si le sujet est central prendre une photo tous les 20°, soit 9 photos pour un 'demi-tour', 18 pour un tour complet.") + "\n"+\
                _("                - Si le sujet est en 'ligne' le recouvrement entre photos doit être des 2/3.") + "\n"+\
                _("                - Tester la 'qualité' des photos au sein du chantier (voir les items du menu Outils).") + "\n"+\
                _("                  les photos ayant un mauvais score (voir le menu Outils/Qualité des photos 'All') doivent être supprimées du chantier : ")+ "\n"+\
                _("                  une seule mauvaise photo peut faire échouer le traitement.") + "\n"+\
                _("                - La présence des dimensions du capteur de l'appareil dans DicoCamera.xml améliore le traitement.") + "\n"+\
                _("                  Cette présence est obligatoire si l'exif ne présente pas la focale équivalente 35mm.") + "\n"+\
                _("                  Pour ajouter la taille du capteur utiliser le menu 'Outils//mettre à jour DicoCamera'.") + "\n\n"+\
                _("                 Précautions :    ") + "\n"+\
                _("                 Ne pas utiliser la fonction autofocus. Deux focales différentes maximum pour un même chantier.") + "\n"+\
                _("                 Eviter aussi la fonction 'anti tremblement' qui agit en modfiant la position du capteur.") + "\n\n"         +\
                "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

   
    # pour commencer
        self.aide3 =  \
                _("   Pour commencer avec l'interface graphique MicMac :") + "\n\n"+\
                _("   Tout d'abord : installer MicMac. Consulter le wiki MicMac : https://micmac.ensg.eu/index.php") + "\n"+\
                _("   Puis : installer CloudCompare (ou Meshlab) (pour afficher les nuages de points)") + "\n\n"+\
                _("   Installer l'interface CEREMA : ") + "\n"+\
                _("   - sous Windows 64 bits utiliser l'installateur AperoDeDenis.msi") + "\n"+\
                _("   - sous Linux, Ubuntu, Mac-Os, Windows 32 bits : installer Python et le module suivant :") + "\n"+\
                _("     - PIL, indispensable (commande : pip install pillow)"+ "\n"+\
                _("     et éventuellement :"+ "\n")+\
                _("     - pyproj, facultatif, est utile pour les données GPS embarquée pour choisir un epsg autre que Lambert 93 ") + "\n"+\
                _("     - scipy, est utile pour écrire un MNT au format IGN ou GRASS à partir d'un ply)") + "\n\n"+\
                _("   Ensuite, dans cette interface graphique :") + "\n\n"+\
                _("1) Paramètrer l'interface : indiquer ou se trouvent le répertoire bin de MicMac et l'éxécutable CloudCompare (ou Meshlab).") + "\n"+\
                _("   Indiquer éventuellement ou se trouvent exiftool et convert d'ImageMagick (en principe sous MicMac\\binaire-aux).") + "\n"+\
                _("   Vérifier en affichant les paramètres (menu paramètrage).") + "\n\n"+\
                _("2) Choisir quelques photos (4 à 6) pour commencer (menu MicMac/choisir des photos).") + "\n\n"+\
                _("   Par exemple : prendre les 4 photos Gravillons du tutoriel disponible sur GitHub).") + "\n\n"+\
                _("3) Lancer MicMac en laissant les paramètres par défaut (menu MicMac/lancer MicMac).") + "\n"+\
                _("   Si tout va bien une vue en 3D non densifiée doit s'afficher, puis une vue 3D densifiée. Patience : cela peut être long.") + "\n\n"+\
                _("4) Si tout ne va pas bien prendre un pastis puis :") + "\n"+\
                _("   Lire 'quelques conseils' (menu Aide).") + "\n"+\
                _("   Tester la qualité des photos (menu Outils).") + "\n"+\
                _("   Examiner les traces (menu Edition),") + "\n"+\
                _("   Consulter l'aide (menu Aide),") + "\n"+\
                _("   Consulter le guide d'installation et de prise en main de l'interface.") + "\n"+\
                _("   Consulter le forum MicMac sur le net, consulter la doc MicMac.") + "\n\n"+\
                _("5) Si une solution apparaît : modifier les options (menu MicMac/options).") + "\n"+\
                _("   puis relancer le traitement.") + "\n\n"+\
                _("6) Si le problème persiste faire appel à l'assistance de l'interface (adresse mail dans Aide/A-propos)") + "\n")

    # Historique
        self.aide4 = \
              _("Historique des versions de l'interface CEREMA pour MicMac") + "\n"+\
              "----------------------------------------------------------"+\
              "\n" + _("Version 5.52 :")+chr(9)+_("juillet 2020") + "\n"+\
              chr(9)+chr(9)+_("Nouveautés :") + "\n"+\
              chr(9)+chr(9)+_("- Multilingue : choix de la langues : Anglais, Allemand, Espagnol, Italien et même CHINOIS !") + "\n"+\
              chr(9)+chr(9)+_("- affichage de la taille du chantier dans la liste des chantiers à ouvrir") + "\n"+\
              chr(9)+chr(9)+_("- ajout d'un item de menu expert : copier la calibration d'un autre chantier") + "\n"+\
              chr(9)+chr(9)+_("- ajout d'un item de menu paramètres : vérification automatique de la présence d'une nouvelle version sur GitHub") + "\n"+\
              chr(9)+chr(9)+_("- les fichiers ply dense sont désormais nommés dans l'ordre de leur création : modele3D_V1, V2, V3...") + "\n"+\
              chr(9)+chr(9)+_("- modifications mineures, voir le script") + "\n"+\
              "\n" + _("Version confinée bis 5.51 :")+chr(9)+_("juin 2020") + "\n"+\
              chr(9)+chr(9)+_("Nouveautés :") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item de menu principal : Outils métier") + "\n"+\
              chr(9)+chr(9)+_("- écriture d'un MNT à partir d'un Ply (déjà en 5.50)") + "\n"+\
              chr(9)+chr(9)+_("- écriture d'un MNT à partir d'un fichier texte XYZ") + "\n"+\
              chr(9)+chr(9)+_("- Calcul du volume d'un MNT") + "\n"+\
              chr(9)+chr(9)+_("- Calcul du volume entre 2 MNT et génération d'un nuage 3D des écarts") + "\n"+\
              chr(9)+chr(9)+_("- Visualisation des écarts entre 2 MNT") + "\n\n"+\
              "\n" + _("Version confinée 5.50 :")+chr(9)+_("4 mai 2020") + "\n"+\
              chr(9)+chr(9)+_("Nouveautés :") + "\n"+\
              chr(9)+chr(9)+_("- Choix du référentiel EPSG pour les données GPS des drones : expert/navigation GPS/référentiel : utiliser EPSG.") + "\n"+\
              chr(9)+chr(9)+_("- Ecriture d'un MNT (format IGN et GRASS) à partir d'un nuage de point ply : expert/Importer... exporter/écrire fichier MNT.") + "\n"+\
              chr(9)+chr(9)+_("- Choix entre nuage et maillage pour les modèles 3D obtenus par Malt.") + "\n\n"+\
              chr(9)+chr(9)+_("Des plus  :") + "\n"+\
              chr(9)+chr(9)+_("- Le calcul du nuage non dense devient facultatif") + "\n"+\
              chr(9)+chr(9)+_("- Copie possible de l'orientation depuis un autre chantier, menu expert/importer ...exporter") + "\n\n"+\
              chr(9)+chr(9)+_("Modifications diverses, corrections d'anomalies : voir en tête du script") + "\n\n"+\
              "\n" + _("Version 5.49 :")+chr(9)+_("20 janvier 2020") + "\n"+\
              chr(9)+chr(9)+_("Nouveautés :") + "\n"+\
              chr(9)+chr(9)+_("- Prise en compte automatique des données GPS des photos prises par drones.") + "\n"+\
              chr(9)+chr(9)+_("  L'utilisateur peut choisir un repère local, géocentrique ou ignorer ces données (voir le menu Expert) .") + "\n"+\
              chr(9)+chr(9)+_("  En repère local les coordonnées WGS84 et Lambert93 du point origine sont affichées et écrites dans la trace.") + "\n"+\
              chr(9)+chr(9)+_("- Copie des points homologues d'un autre chantier. Seuls les chantiers compatibles sont proposés. (menu Expert)") + "\n"+\
              chr(9)+chr(9)+_("- Lorsque les photos forment plusieurs scènes disjointes il est proposé à l'utilisateur de lancer le traitement") + "\n"+\
              chr(9)+chr(9)+_("  sur le groupe de photos le plus nombreux") + "\n"+\
              chr(9)+chr(9)+_("Modifications diverses :") + "\n"+\
              chr(9)+chr(9)+_("- controle des photos très amélioré (durée divisée par 10 en moyenne, ajout de certains controles, voir le source).") + "\n"+\
              chr(9)+chr(9)+_("- retirer des photos du chantier : fix de certains bugs.") + "\n"+\
              chr(9)+chr(9)+_("- ménage dans les chantiers : ne supprime que les sous-répertoires liés au chantier, pas les autres.") + "\n"+\
              chr(9)+chr(9)+_("- modification des exifs : suppression des fichiers créés par exiftool") + "\n"+\
              chr(9)+chr(9)+_("- interrogation systématique de GitHub pour rechercher une nouvelle version.") + "\n"+\
              chr(9)+chr(9)+_("- suppression du chois 'AperoDeDenis' comme mode pour Malt.") + "\n"+\
              "\n" + _("Historique chronologique depuis la version 1.5 de novembre 2015 ") + "\n"+\
              "\n" + _("Version 1.5  : première version diffusée sur le site de l'IGN le 23/11/2015.") + "\n"+\
              "\n" + _("Version 1.55 : sous Windows le fichier paramètre est placé sous le répertoire APPDATA de l'utilisateur,") + "\n"+\
              chr(9)+chr(9)+_("ce qui règle les questions relatives aux droits d'accès en écriture. Mise en ligne le 04/12/2015.") + "\n"+\
              "\n" + _("Version 1.60 : ajout des fonctions :") + "\n"+\
              chr(9)+chr(9)+_("- Qualité des photos lors du dernier traitement") + "\n"+\
              chr(9)+chr(9)+_("- Exporter le chantier en cours") + "\n"+\
              chr(9)+chr(9)+_("- Importer un chantier (permet de recopier le chantier sur un autre répertoire, disque, ordinateur, système d'exploitation)") + "\n"+\
              chr(9)+chr(9)+_("- Les fichiers 'trace' sont enregistrés au format utf-8.") + "\n\n"+\
              _("Version 2.00 : ajout des fonctions :") + "\n"+\
              chr(9)+chr(9)+_("- Choix de photos pour la calibration intrinsèque par Tapas.") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de relancer Malt sans relancer Tapioca/Tapas tout en conservant les images 3D générées.") + "\n"+\
              chr(9)+chr(9)+_("- Conservation de plusieurs fichiers modele3D.ply après Malt pour un même chantier.") + "\n"+\
              chr(9)+chr(9)+_("- Choix du niveau de zoom d'arrêt de la procédure Malt : de 1 (par défaut) à 8.") + "\n"+\
              chr(9)+chr(9)+_("- Création de tous les fichiers .ply correspondants à tous les niveaux de zoom calculés.") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item du menu édition listant et visualisant toutes les images 3D générées.") + "\n"+\
              chr(9)+chr(9)+_("- Choix du nombre de photos à retenir autour de l'image maître pour Malt.") + "\n"+\
              chr(9)+chr(9)+_("- Traitement des vidéos (par exemple GoPro) : décompactage, sélection, mise à jour de l'exif") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de deux contrôles sur le lot des photos : mêmes dimensions, même focale.") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item 'historique' dans le menu Aide.") + "\n"+\
              "\n" + _("Version 2.10")+chr(9)+_("- Ajout d'un item du menu édition fusionnant les images 3D.") + "\n"+\
              chr(9)+chr(9)+_("- Plusieurs images maîtresses, plusieurs masques.") + "\n"+\
              chr(9)+chr(9)+_("- Conversion automatique des fichiers PNG, BMP, GIF, TIF en JPG") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item du menu Outils permettant de modifier les exifs. Diffusion restreinte à la DTer NC le 16/02/2016") + "\n"+\
              "\n" + _("Version 2.20 :")+chr(9)+_("- Maintien des options compatibles lors du choix de nouvelles photos. Février 2016") + "\n"+\
              "\n" + _("Version 2.30 : ")+\
              chr(9)+_("- Modification des options par défaut dans le menu outils.") + "\n"+\
              "\n" + _("Version 2.40 :")+chr(9)+_("- Choix de l'option (Statue ou QuickMac) pour C3DC. Avril 2016") + "\n"+\
              "\n" + _("Version 2.45 :")+chr(9)+_("- Référentiel GCP calculé après Tapas (et toujours avant Malt). La virgule est un séparateur décimal accepté.") + "\n"+\
              chr(9)+chr(9)+_("- Possiblité d'appliquer la calibration GCP sans relancer malt. Mai 2016") + "\n"+\
              "\n" + _("Version 2.50 :")+chr(9)+_("- Ajout de Tawny après Malt en mode Ortho, désactivation du message de lancement. Juin 2016") + "\n"+\
              "\n" + _("Version 3.00 :")+chr(9)+_("- Version bilingue Français/Anglais. Octobre 2016") + "\n"+\
              "\n" + _("Version 3.10 :")+chr(9)+_("- Choix des N meilleures photos pour un nouveau dossier. Novembre 2016") + "\n"+\
              "\n" + _("Version 3.20 :")+chr(9)+_("janvier 2017") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un choix pour Malt : AperoDeDenis, l'interface recherche pour vous les maîtresses et les photos correspondantes") + "\n"+\
              chr(9)+chr(9)+_("- Item de sélection des meilleures images pour créer un nouveau chantier. janvier 2017") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de saisir une unité avec la distance.") + "\n"+\
              chr(9)+chr(9)+_("- Lancement de Tapas accéléré : suppression du controle des photos") + "\n"+\
              chr(9)+chr(9)+_("- Les photos autour de la maîtresse pour Malt sont choisies parmi les meilleures en correspondances") + "\n"+\
              chr(9)+chr(9)+_("- Controle affiné des points GCP, message informatif détaillé") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de supprimer UN seul point GCP sur une photo") + "\n"+\
              "\n" + _("Version 3.30 :")+chr(9)+_("janvier 2017") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de tarama : création d'une mosaïque après Tapas.") + "\n"+\
              chr(9)+chr(9)+_("- le mode Ortho de Malt utilise la mosaïque tarama, avec masque") + "\n"+\
              chr(9)+chr(9)+_("- drapage du nuage densifié par l'ortho mosaïque obtenue par Tawny") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité d'inverser les masques 2D") + "\n"+\
              chr(9)+chr(9)+_("- Ouverture des mosaïques Tarama et Tawny par menu") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un menu 'expert' permettant de saisir une ligne de commande.") + "\n"+\
              "\n" + _("Version 3.31 :")+chr(9)+_("février 2017") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item du menu 'expert' : recopie les points GCP d'un chantier à un autre.") + "\n"+\
              "\n" + _("Version 3.34 :")+chr(9)+_("Janvier 2018") + "\n"+\
              chr(9)+chr(9)+_("- Du ménage! permet de conserver les résultats OU de supprimer tout le chantier.") + "\n"+\
              chr(9)+chr(9)+_("- Affichage de la taille du dossier.") + "\n"+\
              chr(9)+chr(9)+_("- Correction de régressions de la V 3.20.") + "\n"+\
              chr(9)+chr(9)+_("Remarque : la version 4.11 de décembre 2017 ajoute un item métier de calcul d'indice surfacique,") + "\n"+\
              "\n" + _("Version 5.0 :")+chr(9)+_("Janvier 2018") + "\n"+\
              chr(9)+chr(9)+_("la version suivante 5.0 supprime l'item 'indices surfaciques'.") + "\n"+\
              "\n" + _("Version 5.1 :")+chr(9)+_("décembre 2018") + "\n"+\
              chr(9)+chr(9)+_("- permet d'oublier les photos ayant servies à la calibration de l'appareil pour l'exécution de Tapas.") + "\n"+\
              chr(9)+chr(9)+_("- insertion d'un fichier texte de points GCP par le menu expert (séparateur espace : nom,x,y,z,dx,dy,dz.") + "\n"+\
              chr(9)+chr(9)+_("- affichage des dimensions des photos dans le menu outils/nom de l'appareil photo") + "\n"+\
              chr(9)+chr(9)+_("- Amélioration de libellés de boites de dialogue, suppression du polysème 'calibration'") + "\n"+\
              "\n" + _("Version 5.2 :")+chr(9)+_("janvier 2019") + "\n"+\
              chr(9)+chr(9)+_("- ajout du modulé CAMPARI après chaque géolocalisation par points GCP (améliore les valeurs des Z).") + "\n"+\
              chr(9)+chr(9)+_("- répartition des photos provenant de plusieurs appareils par modification du 'model' dans l'exif (menu expert)") + "\n"+\
              chr(9)+chr(9)+_("- affichage des noms des appareils photos présents dans le chantier (menu expert)") + "\n"+\
              chr(9)+chr(9)+_("- affichage du log des traitement MicMac : mm3d-logFile.txt (menu expert)") + "\n"+\
              chr(9)+chr(9)+_("- amélioration de la fonction console système (Expert/Exécuter une commande)") + "\n"+\
              "\n" + _("Version 5.21 :")+chr(9)+_("février 2019") + "\n"+\
              chr(9)+chr(9)+_("- Argument de Tapas aprés calibration : Figee (au lieu de Autocal)") + "\n"+\
              chr(9)+chr(9)+_("- Ajout dans le menu expert d'un console python") + "\n"+\
              "\n" + _("Version 5.22 :")+chr(9)+_("11 février 2019") + "\n"+\
              chr(9)+chr(9)+_("- fix 2 issues remontées sur github, numéro de version inchangée : 5.21") + "\n"+\
              "\n" + _("Version 5.30 :")+chr(9)+_("21 février 2019") + "\n"+\
              chr(9)+chr(9)+_("- dans les items 'Outils/Qualité des photos' ajout des photos 'isolées', en disjontion de toutes les autres.") + "\n"+\
              chr(9)+chr(9)+_("  Ces photos font 'planter' la recherche de l'orientation.") + "\n"+\
              chr(9)+chr(9)+_("- Suite à la recherche des points homologues vérification de l'unicité de la scène photographiée.") + "\n"+\
              chr(9)+chr(9)+_("  Plusieurs scènes sans points homologues communs font planter la recherche d'une orientation.") + "\n"+\
              chr(9)+chr(9)+_("  Cette fonction est ajoutée à l'item 'Outils/Qualité des photos'.") + "\n"+\
              chr(9)+chr(9)+_("- Lorsque le message MAXLINELENGTH est émis par Tapioca il est affiché et expliqué dans la trace synthétique.") + "\n"+\
              chr(9)+chr(9)+_("- prise en compte de l'issue concernant la fonction filedialog sous Mac-Os lors des recherche de programmes (exiftool...).") + "\n"+\
              chr(9)+chr(9)+_("- Ajout d'un item dans paramètrage : recherche d'une nouvelle version GitHub.") + "\n"+\
              "\n" + _("Version 5.31 :")+chr(9)+_("8 mars 2019") + "\n"+\
              chr(9)+chr(9)+_("- Les échelles par défaut de Tapioca sont calculées suivant les photos : 60% de la dimension maxi des photos.") + "\n"+\
              chr(9)+chr(9)+_("- suppresssion des items de menu outils\qualité des photos line et qualité des photos ALL.") + "\n"+\
              chr(9)+chr(9)+_("- Arrêt de Tapioca MulScele aprés le premier passage si la scène n'est pas unique, rendant l'échec certain.") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de 1 item outils/retirer des photos.") + "\n"+\
              "\n" + _("Version 5.32 - 5.33 :")+chr(9)+_("25 mars 2019") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de relancer un chantier non terminé en conservant les points homologues.") + "\n"+\
              chr(9)+chr(9)+_("- ajout d'un item au menu expert : modifier la longueur du préfixe utilisé pour définir plusieurs appareils.") + "\n"+\
              "\n" + _("Version 5.34 :")+chr(9)+_("26 mars 2019, suivant les conseils de Xavier Rolland") + "\n"+\
              chr(9)+chr(9)+_("- l'affichage des coordonnées en pixels des point GCP devient optionnel.") + "\n"+\
              chr(9)+chr(9)+_("- Au retour de saisie des points GCP : fenêtre liste des photos.") + "\n"+\
              chr(9)+chr(9)+_("- remplacement global de GCP par GCP (sauf définition dans l'aide)") + "\n"+\
              chr(9)+chr(9)+_("- zoom plus important possible sur la fenêtre de saisie des points GCP") + "\n"+\
              "\n" + _("Version 5.40 :")+chr(9)+_("30 mars 2019, suivant les conseils de Xavier Rolland") + "\n"+\
              chr(9)+chr(9)+_("- amélioration ergonomie saisie des points gcp (flèches : photo suivante/précédente).") + "\n"+\
              chr(9)+chr(9)+_("- corrections de quelques bugs sur la prise en compte des points gcp (voir entête du code source).") + "\n"+\
              chr(9)+chr(9)+_("- correction du changement de langue si appel depuis un raccourci.") + "\n"+\
              "\n" + _("Version 5.41 :")+chr(9)+_("avril 2019") + "\n"+\
              chr(9)+chr(9)+_("- amélioration ergonomie de la fonction 'du ménage', correction du bug : ménage uniquement fait sur le chantier en cours).") + "\n"+\
              chr(9)+chr(9)+_("- Fichier/renommer le chantier devient fichier/enregistrer sous....") + "\n"+\
              "\n" + _("Version 5.43 :")+chr(9)+_("18 avril 2019") + "\n"+\
              chr(9)+chr(9)+_("- Propose à l'utilisateur (sous Windows) de lancer plusieurs instance d'AperoDeDenis).") + "\n"+\
              chr(9)+chr(9)+_("- l'aide 'quelques conseils' est répartie sur 3 items") + "\n"+\
              chr(9)+chr(9)+_("- quelques corrections de bugs, voir en tête du script") + "\n"+\
              "\n" + _("Version 5.44 et 5.45 :")+chr(9)+_("mai 2019") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de la fonction recherche (F3) dans les traces et l'aide.") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de relancer Tapas sans relancer Tapioca") + "\n"+\
              chr(9)+chr(9)+_("- Sécurisation de l'import d'un chantier à partir d'un répertoire") + "\n"+\
              chr(9)+chr(9)+_("- Sécurisation de l'import des points GCP (Ground Control Point=GPS) à partir d'un chantier ou d'un fichier") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de la fonction 'renommer un chantier' (fonction supprimée dans la V5.41)") + "\n"+\
              "\n" + _("Version 5.46 :")+chr(9)+_("20 mai 2019") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de l'item Outils/Qualité des points GCP.") + "\n"+\
              chr(9)+chr(9)+_("- Ajout de l'item Expert/Personnaliser les paramètres optionnels de MicMac") + "\n"+\
              "\n" + _("Version 5.47 :")+chr(9)+_("21 mai 2019") + "\n"+\
              chr(9)+chr(9)+_("- amélioration robustesse") + "\n"+\
              chr(9)+chr(9)+_("- voir détails en tête du source") + "\n"+\
              "\n" + _("Version 5.48 :")+chr(9)+_("21 mai 2019") + "\n"+\
              chr(9)+chr(9)+_("- Possibilité de charger la calibration d'un autre chantier (onglet Orientation du menu micMac/options") + "\n"+\
              "----------------------------------------------------------"
                
    # choix des options
        self.aide5 = _("Interface graphique AperoDeDenis : quelques conseils concernant le choix des options.") + "\n\n"+\
                _("Options :") + "\n"+\
                _("               - Points homologues : ") + "\n"                             +\
                _("                           L'échelle est la taille en pixels de l'image (ou -1 pour l'image entière) pour la recherche des points homologues.") + "\n" +\
                _("                           Par défaut la taille retenue est les 2/3 de la largeur des photos (2000 pixels si les photos font 300 de large.") + "\n" +\
                _("                           L'option ALl recherche les points homologues sur toutes les paires de photos (ce qui peut faire beaucoup !)") + "\n" +\
                _("                           L'option MulScale recherche les points homologues en 2 temps :") + "\n" +\
                _("                             1) sur toutes les paires avec une taille de photo réduite (typiquement 300)") + "\n" +\
                _("                             2) Seules les paires de photos ayant eu au moins 2 points homologues à cette échelle seront") + "\n" +\
                _("                                retenues pour rechercher les points homologues à la seconde échelle. Gain de temps important possible.") + "\n" +\
                _("                           Si les photos sont prises 'en ligne' choisir 'line' dans les options de Tapioca, ") + "\n"                    +\
                _("                             MicMac ne recherchera que les paires de photos se succédant.") + "\n"             +\
                _("                             Choisir delta en fonction du taux de recouvrement des photos (delta = 2 voire +, si le recouvrement est important.") + "\n\n" +\
                _("               - Orientation : si l'appareil photo est un compact ou un smartphone choisir RadialBasic, ") + "\n"+\
                _("                         si l'appareil photo est un reflex choisir RadialExtended ") + "\n"                    +\
                _("                         si l'appareil photo est de moyenne gamme choisir RadialStd") + "\n"                               +\
                _("                         Ces conseils ne sont pas toujours vérifiés : modifier votre choix s'il échoue. ") + "\n"+\
                _("                         L'arrêt après l'orientation permet de définir un masque 3D sur le nuage, pour la densification par C3DC.") + "\n\n"       +\
                _("               - Mise à l'échelle : permet de définir un repère et une métrique (axe, plan et distance, tous obligatoires).") + "\n"+\
                _("                 Si les photos proviennent d'une camera embarquée sur un drone les photos comportent des informations GPS sur la prise de vue :") + "\n"+\
                _("                 Ces informations sont exploitées par apéroDeDenis pour définir un repere local en coordonnées métriques et orienté comme le WGS84.") + "\n"+\
                _("                 Ces informations remplacent et supplantent la mise à l'échelle manuelle. Un item du menu expert permet de les ignorer") + "\n\n"+\
                _("               - Points GCP (ou GPS) : définir au moins 3 points cotés et les placer sur 2 photos. L'état du chantier indique s'ils sont pris en compte") + "\n\n"+\
                _("               - Densification :") + "\n"          +\
                _("                       Malt fournit des nuages beaucoup plus denses que C3DC mais parfois exotiques si peu de points homologues") + "\n"+\
                _("                            Pour éviter cela utiliser l'option geoimage avec masque sur les zones denses en points homologues") + "\n" +\
                _("                       C3DC fournit des nuages peu denses mais plus précis") + "\n" +\
                _("                            Masque 3D possible sur le nuage non dense'") + "\n" +\
                _("                            L'option la plus fructueuse est 'BigMac'") + "\n" +\
                _("               - Densification par Malt : pour le mode GeomImage indiquer une ou plusieurs images maîtresses.") + "\n"          +\
                _("                        Seuls les points visibles sur ces images seront conservés dans le nuage de points.") + "\n"                +\
                _("                        Sur ces images maîtresses tracer les masque délimitant la partie 'utile' de la photo.") + "\n"+\
                _("                        Le résultat sera mis en couleur suivant les images maitresses.") + "\n"+\
                _("                        (éviter trop de recouvrement entre les maîtresses !).") + "\n"+\
                _("                        Le traitement avec masque sera accéléré et le résultat plus 'propre'.") + "\n\n"                                 +\
                _("               - Densification par C3DC : propose de définir un masque en 3D qui conservera tout le volume concerné.") + "\n"                  +\
                _("                        Alternative à Malt, le traitement est parfois plus rapide, plus précis, moins dense. Nécessite une version récente de MicMac.") + "\n\n"+\
                "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

    # pas d'orientation
        self.aide6 = _("Interface graphique AperoDeDenis : quelques conseils si MicMac ne trouve pas de points homologues.") + "\n\n"+\
            _("               - Une cause possible est le trop grand nombre de photos : au dela de 200 sous windows et de 400 sous linux le risque est important.") + "\n"+\
            _("                 Relancer le traitement aprés avoir découper le chantier en paquets plus petits.") + "\n"+\
            _("                 Vous pourrez regrouper les nuages obtenus s'ils sont référencés par des points GCP ou GPS.") + "\n"+\
            _("               - Une cause possible est la non conformité des photos aux standards minimum de la phtogrammétrie :") + "\n"+\
            _("                 la scéne photographiée doit être 'immobile', une nature morte. Les êtres vivants et la nature ventée sont à proscrire.") + "\n"+ "\n"+\
            _("Si MicMac trouve des points homologues mais ne trouve pas l'orientation des appareils photos:") + "\n\n"+\
            _("               - Consulter la trace :") + "\n"+\
            _("                        1) si erreur dans la trace : 'Radiale distorsion abnormaly high' :") + "\n"+\
            _("                           modifier le type d'appareil pour l'orientation (radialstd ou radialbasic ou RadialExtended ou...)") + "\n"+\
            _("                        2) Eliminer les photos ayant les plus mauvais scores : menu Outils/qualité des photos puis Outils/retirer des photos") + "\n"+\
            _("                        3) si ce n'est pas suffisant ne garder que les meilleures photos (typiquement : moins de 10)") + "\n"+\
            _("                           Penser que des photos floues ou avec un sujet brillant, lisse, mobile, transparent, vivant sont défavorables.")+ "\n"+\
            _("                        4) Augmenter l'échelle des photos pour tapioca, mettre -1 au lieu de la valeur par défaut.") + "\n"+\
            _("                        5) Utiliser la calibration intrinsèque sur des photos adaptées") + "\n"+\
            _("                        6) Si plusieurs appareils photos sont utilisés il faut les distinguer dans l'exif (voir menu expert)") + "\n"+\
            _("                           et prendre des photos spécifiques pour la calibration intrinsèque de chaque appareil.") + "\n"+\
            _("                        7) vérifier la taille du capteur dans dicocamera, nécessaire si la focale equivalente 35 mm est absente de l'exif") + "\n"+\
            _("                        8) examiner la trace synthétique et la trace complète : MicMac donne quelques informations") + "\n"+\
            _("                           si la trace compléte contient : 'Error: -- Input line too long, increase MAXLINELENGTH'") + "\n"+\
            _("                           alors tenter, sous windows, de modifier le fichier /binaire-aux/windows/startup/local.mk") + "\n"+\
            _("                           ou, sous windows, limiter la longueur du chemin menant aux fichiers en recopiant les photos sous la racine du disque.") + "\n"+\
            _("                           Le nombre maximum de photos d'un chantier sous windows semble être de 250 à 300, si plus utiliser Linux ou Mac") + "\n"+\
            _("                        9) Si la trace synthétique contient'Not Enouh Equation in ElSeg3D::L2InterFaisceaux' alors choisir 'radialbasic'.") + "\n"+\
            _("                        10) consulter le wiki micmac (https://micmac.ensg.eu/index.php)") + "\n"+\
            _("                        11) consulter le forum micmac (http://forum-micmac.forumprod.com)") + "\n"+\
            _("                        12) faites appel à l'assistance de l'interface (voir adresse dans l'a-propos)") + "\n\n"+\
            "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

    # A propos
    
        self.aide7=self.titreFenetre+("\n\n" + _("Réalisation Denis Jouin 2015-2020") + "\n\n" + _("Laboratoire Régional de Rouen") + "\n\n"+
                                _("CEREMA Normandie Centre") + "\n\n" + "mail : interface-micmac@cerema.fr")


    # pas de nuage dense
        self.aide8 = _("Interface graphique AperoDeDenis : quelques conseils si MicMac ne trouve pas de nuage de points dense.") + "\n\n"+\
            _("               - Examiner la trace (Menu Edition/afficher la trace) et la qualité des photos (menu outils/Qualité des photos): .") + "\n"+\
            _("                        0) Prenez un pastis, contemplez le nuage de points non dense") + "\n"+\
            _("                        1) Avec C3DC nous avons constaté des échecs avec le message 'cAppliMICMAC::SauvMemPart File for _compl.xml'.") + "\n"       +\
            _("                           Le passage au paramètre 'BigMac' ou a 'Malt' a permis l'obtention d'un nuage dense.") + "\n"+\
            _("                        2) assurez vous que le sujet est immobile (pas de végétation mouvante, de pluie") + "\n"+\
            _("                        3) assurez vous que le recouvrement des photos est suffisant : chaque point du sujet doit être sur 3 photos au moins") + "\n"+\
            _("                        4) assurez vous qu'il n'y a pas une photos très maivaise : une seule photo suffit à faire échouer un chantier,") + "\n"+\
            _("                        5) consulter le forum micmac (http://forum-micmac.forumprod.com)") + "\n"+\
            _("                        6) faites appel à l'assistance de l'interface (voir adresse dans l'a-propos)") + "\n\n"\
            "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

    # aide métiers : MNT, XYZ, calcul volume
        avertissement  = _("Avertissement sur les calculs de volume entre 2 MNT :")+"\n\n"
        avertissement += _("Les MNT sont obtenus à partir des nuages de points PLY ou XYZ par 2 items du menu Outils_métier.")+"\n\n"
        avertissement += _("Les fichiers PLY ou XYZ sont des semis de points 3D irréguliers.")+"\n"
        avertissement += _("Le MNT enregistre les valeurs d'altitude suivant une grille carrée régulière, par exemple un point tous les 50 cm.")+"\n"
        avertissement += _("La taille de la maille est un paramètre crucial pour un MNT : elle conditionne sa précision spatiale.")+"\n"
        avertissement += _("La taille de la maille doit être évaluée suivant la densité de points du fichier origine (PLY ou XYZ).")+"\n"
        avertissement += _("Une trop petite maille ne pourra améliorer la précision initiale du PLY ou du XYZ.")+"\n\n"
        avertissement += _("Le calcul du volume entre 2 MNT ne s'effectuera (dans cette version) que si les tailles des mailles sont identiques.")+"\n"               
        avertissement += _("Si les mailles sont identiques l'outil recherche la zone de recouvrement des 2 MNT.")+"\n"
        avertissement += _("Les 2 grilles sont alors ajustées et le calcul se fait pour les mailles ayant une valeur dans chaque MNT.")+"\n"
        avertissement += _("Un paramètre de 'tolerance' permet d'ignorer les écarts trop faibles, inférieurs à cette tolérance, dans l'épaisseur du trait.")+"\n\n"
        avertissement += _("Un nuage de points 3D des écarts est produit, au format XYZ : un item du menu permet de le visualiser dans Cloud Compare.")+"\n\n"
        avertissement += _("Remarques :")+"\n"    
        avertissement += _(" - Ces fonctions 'métiers' sont indépendantes de l'utilisation de l'outil MicMac")+"\n"    
        avertissement += _(" - le mètre est supposé être l'unité de mesure des PLY, des XYZ et des MNT : les résultats sont données en m, m2, m3.")+"\n"    
        avertissement += _(" - lorsque AperoDeDenis est installé sous windows  par l'installateur AperoDeDenis.msi la création des MNT n'est pas opérationelle.")+"\n"    
    
        self.aide9 = _("Les outils 'métiers'") + "\n\n"+\
            _("               Les outils métiers exploitent les nuages de points PLY ou XYZ et les MNT.") + "\n\n"+\
            _("               Les outils métiers sont utilisables sans créer de chantier MicMac.") + "\n\n"+\
            _("               Les résultats sont mémorisés dans des fichiers textes.") + "\n\n"+\
            _("               1 - Création de MNT à partir d'un nuage de points, ou d'un maillage (mesh) fichier PLY") + "\n"+\
            _("                   Lorsque les nuages PLY ou XYZ représentent le sol ou une surface il est possible de créer des MNT (Modèle Numérique de Terrain, DEM en anglais).") + "\n"+\
            _("                   Les MNT sont ouverts par les SIG, comme QGIS ou ArcGIS.") + "\n"+\
            _("                   Les MNT embarquent la localisation et la métrique mais pas le référentiel EPSG qui doit être précisé dans le SIG.") + "\n"+\
            _("                   Les MNT créés sont au format 'IGN'.") + "\n"+\
            _("                   Remarques : Les formats Ply acceptés sont : Binary pour les nuages et ASCII pour les Mesh.") + "\n"+\
            _("                               Le format du nuage/mesh peut être modifié par CloudCompare en l'enregistrant sous le nouveau format. ") + "\n"+\
            _("                               l'écriture d'un MNT ne fonctionne pas si AperoDeDenis est installé par aperodedenis.msi") + "\n\n"+\
            _("               2 - Création de MNT à partir d'un nuage de points XYZ") + "\n"+\
            _("                   Le format XYZ est très fréquent, lisible par tout éditeur de texte et visualisé par Cloud Compare,.") + "\n\n"+\
            _("               3 - Calcul du volume d'un MNT, au dessus d'une cote de base fixée par l'utilisateur.") + "\n"+\
            _("                   Les résultats sont présentés en supposant que l'unité de longueur est le mètre.") + "\n\n"+\
            _("               4 - Calcul du volume entre 2 MNT") + "\n"+\
            _("                   Un besoin fréquent consiste à comparer 2 MNT du même terrain à 2 dates différentes.") + "\n"+\
            _("                   Il s'agit d'évaluer les transformations du terrain : apport de matériaux, éboulement de falaises.") + "\n"+\
            _("                   Le calcul du volume entre 2 MNT est disponible : il nécessite quelques précautions d'usage.") + "\n\n"+\
            _("                 * les photos doivent avoir été correctement géoréférencées par GPS en posant des cibles localisées en x,y,z.") + "\n"+\
            _("                    La précision des résultats dépend largement de la précisions du géoréférencement des prises de vue.") + "\n"+\
            _("                    Par exemple une erreur d'altitude très faible de 1 cm correspond à un volume de 100 m3 par hectare.") + "\n"+\
            _("                 *  Le calcul de volume est paramétré : il est possible de ne tenir compte que des écarts signifiants") + "\n"+\
            _("                    Ainsi les écarts 'dans l'épaisseur du trait', par exemple inférieur à 5 ou 10 cm, seront ignorés.") + "\n"+\
            _("                    Cette tolérance est modifiable par menu") + "\n"+\
            _("                 *  L'outil recherche la zone de recouvrement entre les 2 MNT et le calcul s'effectue sur les surfaces communes.") + "\n"+\
            _("                    Un fichier XYZ des écarts est constitué, un item de menu permet de le visualiser en 3D.") + "\n"+\
            _("                 *  Un compte rendu détaillé est affiché en fin de traitement et mémorisé dans un fichier trace.") + "\n\n"+\
            _("                 *  Ce calcul peut servir à comparer la précision de 2 nuages MicMac ou d'autres provenances :") + "\n"+\
            _("                     - obtenus par Malt avec différents niveaux de zoom : dans ce cas comparer les nuages intermédiaires Zoom_8, Zoom_4..") + "\n"+\
            _("                     - Obtenus par Malt et C3DC") + "\n"+\
            _("                     - Obtenus sans points GCP, ou GPS puis avec des points GCP ou GPS") + "\n"+\
            _("                     - Obtenus par MicMac et Metashape ou Pix4D ou ...") + "\n\n"+\
            _("               5 - Un item permet de visualiser le maillage des écarts entre 2 MNT.") + "\n"+\
            _("                   Nota : Les écarts inférieurs à la tolérance sont considérés comme nuls. ") + "\n\n"+\
            _("               6 - 2 items permettent de modifier : la tolérance et le nombre de décimales dans les résultats des calculs.") + "\n"+\
            _("                   Nota : Les écarts inférieurs à la tolérance sont considérés comme nuls. ") + "\n\n"+\
            _("               7 - Un item écrit les fichiers PLY sous forme de liste de points X,Y,Z.") + "\n"+\
            _("                   Ce format texte, très répandu, permet de lire les valeurs x,y z dans tout éditeur de texte.") + "\n\n"+\
            avertissement + "\n\n"+\
            "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

    # fichier pour modifier la clé de registre de saisiemasqQT : par défaut l'origine est le centre, ce qui rend invisible les nuages en EPSG.
    # ce fichier remet le centre au barycentre, il permettrait de modifier l'épaisseur des traits, la taille des points par défaut

        self.cleMasqQT    =  "HKEY_USERS\S-1-5-21-1400669940-2874269118-2294255063-1600\Software\Culture3D\SaisieMasqQT\Drawing settings"
        self.sousCleMasqQT=  "SceneCenterType"
        self.majCleMasqQT =  (
                                self.cleMasqQT+"\n"+                                      
                                '"SceneCenterType"=REG_DWORD 0\n'
                             )

        
    ####################### initialiseValeursParDefaut du défaut : nouveau chantier, On choisira de nouvelles photos : on oublie ce qui précéde,
                          # sauf les paramètres généraux de aperodedenis (param micmac)
       
    def initialiseValeursParDefaut(self):
        
    # Etat du chantier : variable self.etatDuChantier
    
    # 0 : en cours de construction, pas encore de photos
    # 1 : photos saisies, répertoire origine fixé, non modifiable
    # 2 : chantier enregistré
    # 3 : micmac lancé, pendant l'exécution de Tapioca et tapas, reste si plantage
    # 35 : arrêté après tapas, points homologues conservés
    # 4 : arrêt après tapas et durant malt en cours d'exécution
    # 5 : densification terminée OK
    # 7 : densification effectuée mais pas de nuage dense généré
    # - 1 : en cours de suppression
        
        self.etatDuChantier             =   0
        self.tailleDuChantierEnMO       =   -1
        
    # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
    # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
    # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
    # [2] = 'original' ou "importé"

        self.typeDuChantier             =   ['photos','initial','original']
    
    # La sauvegarde : self.etatSauvegarde
    # ""  : lorsque le chantier est sauvegardé sous son répertoire de travail, l'exécution de micMac sauve le chantier
    # "*" : lors de sa création avant sauvegarde et lorsque le chantier a été modifié par l'utilisateur.

        self.etatSauvegarde             =   ""                                                 # Indicateur du caractère sauvegardé ("") ou à sauvegarder ("*") du chantier. utile pour affichage title fenetre

            
    # les photos :
   
        self.repertoireDesPhotos        =   _('Pas de répertoire pour les photos')
        self.photosAvecChemin           =   list()                                              # liste des noms des fichiers photos avec chemin complet
        self.photosSansChemin           =   list()                                              # nom des photos sans le chemin
        self.lesExtensions              =   str()                                               # l'utilisateur pourrait sélectionner des photos avec des extensions différentes
        self.repTravail                 =   self.repertoireData                                 # répertoire ou seront copiés les photos et ou se fera le traitement,Pour avoir un répertoire valide au début
        self.chantier                   =   str()                                               # nom du chantier (répertoire sosu le répertoire des photos)
        self.extensionChoisie           =   str()                                               # extensions des photos (actuellement JPG obligatoire)
        self.lesTagsExif                =   dict()                                              # pour mémoriser les valeurs des tags de l'exif, long à récolter
                                                     
    # Tapioca

        self.modeTapioca.set('MulScale')# Mode (All, MulScale, Line)
        self.echelle1.set('1200')       # echelle pour "All"
        self.echelle2.set('300')        # echelle base pour MulScale (si 2 photos n'ont qu'un seul point homologues a cette échelle la paire est ignorées dans l'étape suivante
        self.echelle3.set('1200')       # echelle haute pour MulScale 
        self.echelle4.set('1200')       # echelle pour Line
        self.delta.set('3')             # delta en + et en = pour Line

    # TAPAS

        self.modeCheckedTapas.set('RadialExtended')             # mode par défaut depuis la v 5.43 avril 2019 (RadialExtended, RadialStd,RadialBasic...
        self.arretApresTapas.set(0)                             # 1 : on arrête le traitement après Tapas, 0 on poursuit
        self.lancerTarama.set(0)                                # 0 : on ne lance pas Tarama (mosaique des photos après Tapas)       
        self.photosPourCalibrationIntrinseque = list()          # quelques images pour calibrer Tapas
        self.photosCalibrationSansChemin      = list()
        self.calibSeule.set(True)                               # par défaut : uniquement pour la calibration
        self.mosaiqueTaramaTIF = str() 
        self.mosaiqueTaramaJPG = str()
        self.masqueTarama = str()
        self.choixCalibration.set("sans")
        self.chantierOrigineCalibration =str()                  # si calibration copiée depuis un autre chantier

    # GoPRO : les options à saisir pour le traitement GoPro : valeurs par défaut (non modifiées lors de la création d'un nouveau chantier)
    
        self.goProMaker.set("GoPro") 
        self.goProFocale35.set("16.53") # Hero3
        self.goProFocale.set("2.98") #2.98 4.52
        self.goProNomCamera.set("GoPro Hero3 HD3")
        self.goProNbParSec.set("3")                 # taux de conservation des photos pour DIV
        self.goProEchelle.set("1000")               # pour tapioca 
        self.goProDelta.set("10")

    # Calculer le nuage non dense :
    
        self.calculNuageNonDense.set(1)                         # par défaut : le nuage non dense est calculé
        
    # Malt
    # mieux que Mic Mac qui prend par défaut le masque de l'image maitre avec le nom prédéfini masq

        self.modeCheckedMalt.set('Ortho')                       # par défaut (GeoImage,AperoDedenis,UrbanMNE,Ortho
        self.photosUtilesAutourDuMaitre.set(5)                  # 5 autour de l'image maîtresse (les meilleures seront choisies en terme de points homologues)
        self.tawny.set(1)                                       # lancement par défaut de Tawny après Malt Ortho (1, sinon 0)
        self.zoomF.set('4')                                     # doit être "1","2","4" ou "8" (1 le plus détaillé, 8 le plus rapide)
        self.etapeNuage                 = "5"                   # par défaut (très mystérieux!)
        self.modele3DEnCours            = "modele3D.ply"        # Nom du nuage en cours de traitement avec son niveau de zoom
        self.modele3DFinal              = "modele3D_V1.ply"     # nom du premier nuage final (puis _V2, _V3...)
        self.dicoInfoBullesAAfficher    = None                  # pour passer l'info à afficherLesInfosBullesDuDico (dans choisirUnePhoto)
        self.listeDesMaitresses         = list()
        self.listeDesMasques            = list()
        self.zoomI                      = ""                    # le niveau de zoom initial en reprise de Malt
        self.reinitialiseMaitreEtMasque()                       # initialise toutes les variables lièes à l'image maitresse et au masque 

    # nuage2Ply
    
        self.nuage2Mesh.set("0")                                  # par défaut nuage et pas maillage
        
    # C3DC

        self.modeC3DC.set("BigMac")                             # valeur possible : Statue, Ground,  QuickMac, Forest...

    # choix de la densification par défaut : C3DC ou MALT
    
        self.choixDensification.set("C3DC")                     # valeur possible : C3DC ou Malt
        
    # Tawny : drapage pour nuage dense généré par MALT option Ortho  : nom du fichier généré

        self.orthoMosaiqueTawny         = "OrthoMosaique.tif"
        self.resultatAConserver         = [os.path.join("Ortho-MEC-MALT",self.orthoMosaiqueTawny),] # à conserver si ménage

    # Calibration par points GCP 

        self.listePointsGPS             =   list()                      # 6-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
        self.idPointGPS                 =   0				# identifiant des points, incrémenté de 1 a chaque insertion
        self.dicoPointsGPSEnPlace       =   dict()                      # dictionnaire des points GCP placés dans les photos (créé par la classe CalibrationGPS)
        self.listeWidgetGPS             =   str()                       # liste des widgets pour la saisie
        self.incertitudePixelImage.set("1")
        self.incertitudeCibleGPS.set("0.05")
        
    # données GPS de navigation  drone
    
        self.repereChoisi               =   self.repereADeterminer
        self.messageRepereLocal         =   str()
        self.nomEpsg                    =   str()

    # et mise à l'échelle
    
        self.dicoLigneHorizontale       =   dict()                      # les deux points de la ligne horizontale              
        self.dicoLigneVerticale         =   dict()                      # les 2 points décrivant une ligne 
        self.planProvisoireHorizontal   =   "planHorizontal.tif"        # nom du fichier masque plan
        self.planProvisoireVertical     =   "planVertical.tif"
        self.savePlanH                  =   "savePlanH"                 # sauvegarde utile si abandon
        self.savePlanV                  =   "savePlanV"
        self.distance.set("")
        self.dicoCalibre                =   dict()                      # les 2 points décrivant un segment de longueur donnée sur 2 photos

    # affichage des points GCP ou distance dans la boite de dialogue de visu:saisie des photos

        self.dicoPointsAAfficher        =   None                        # pour passer l'info à afficherTousLesPointsDuDico (dans choisirUnePhoto)

    # orientation courante, référentiel à jour :

        self.orientationCourante        =   str()                       # réinitialise l'orientatio courante
        self.referentielOK              =   False                       # indique si le référentiel GCP, GPS ou "mise à l'échelle " est modifié

    # Pour le calcul du volume entre 2 MNT (menu métier)

        self.tolerance                  =   0.05                        # tout écart inféieur à 5 cm sera considéré comme nul
        self.arrondi                    =   2                           # les résultat des calculs seront présentés arrondis (fixe)
        self.limitesHistogrammeDesEcarts=   range(-5,5)                 # (fixe pour l'instant)
        self.ecartXyz                   =   str()                       # le nom du fichier XYZ des écarts entre les 2 mnt
        
    # pour la trace :
    
        self.lignePourTrace             =   str()
        self.ligneFiltre                =   str()
        self.TraceMicMacComplete        =   str()
        self.TraceMicMacSynthese        =   str()
        self.fichierParamChantier       =   str()                       # fichier paramètre sous le répertoire du chantier

        
    # divers 

        self.messageSiPasDeFichier      =   1                           #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        if self.systeme=="posix":                                       #  dépend de l'os, mais valeur par défaut nécessaire
            self.shell                  =   False
        if self.systeme=="nt": 
            self.shell                  =   True                                
        self.homolActuel                =   str()                       # nom du répertoire qui a été renommé en "Homol"
        self.fermetureOngletsEnCours    =   False                       # pour éviter de boucler sur la fermeture de la boite à onglet
        self.fermetureOptionsGoProEnCours=  False
        self.fermetureModifExif         =   False
        self.nbCaracteresDuPrefixe      =   "3"                         # préfixe du nom des photso mis par un appareil (cas d'appareils multiples)
        self.ecartPointsGCPByBascule    =   str()
        self.optionsMicMacActivees      =   False                       # mémorise l'ouverture des onglets options, pour les écrire dans la trace 
        
    # si les options par défaut sont personnalisées on les restaure :

        self.restaureOptions() 
        
    ################# Le Menu FICHIER : Ouvre un nouveau chantier avec les valeurs par défaut, ouvre un chantier existant, enregistrer, renommer, supprimer 

    # Enregistre le chantier précédent, prépare un chantier vide avec le répertoire de travail par défaut   

    def nouveauChantier(self):                                          # conserve : micMac,meshlab,tousLesRepertoiresDeTravail
        self.menageEcran()
        texte=""                                                        # réinitialise les paramètres du chantier (initialiseValeursParDefaut)
        if self.etatDuChantier == 1 :
            if self.troisBoutons(_("Enregistrer le chantier ?"),
                                _("Chantier non encore enregistré. Voulez-vous l'enregistrer ?"),
                                _("Enregistrer"),
                                _("Ne pas enregistrer.")) == 0:
                self.enregistreChantier()
                texte=_("Chantier précédent enregistré : %s") % (self.chantier)+ "\n" 
            
        if self.etatDuChantier >= 2 and self.etatSauvegarde =="*":
            if self.troisBoutons(_("Enregistrer le chantier %s ?") % (self.chantier),
                                _("Chantier modifié depuis la dernière sauvegarde. Voulez-vous l'enregistrer ?"),
                                _("Enregistrer"),
                                _("Ne pas enregistrer.")) == 0:
                self.copierParamVersChantier()
                texte = _("Chantier précédent enregistré : %s") % (self.chantier)+ "\n"                 
        self.initialiseValeursParDefaut()
        oschdir(self.repTravail)                # lors de la création d'un chantier il s'agir du répertoire des paramètres d'AperoDeDenis
        self.copierParamVersChantier()
        self.afficheEtat(texte)
                   
    def ouvreChantier(self):
        self.menageEcran()
        self.enregistreChantier()   # enregistrement systématique du chantier précédent (la variable self.etatSauvegarde est peu fiable)
        bilan = self.choisirUnChantier(_("Choisir un chantier."))        # boite de dialogue de sélection du chantier à ouvrir, renvoi : self.selectionRepertoireAvecChemin
        if bilan!=None:
            self.encadre(bilan)
            return   
        self.fichierParamChantier = os.path.join(self.selectionRepertoireAvecChemin,self.paramChantierSav)
        if os.path.exists(self.fichierParamChantier):        
            self.restaureParamChantier(self.fichierParamChantier)           
            self.sauveParam()           # pour assurer la cohérence entre le chantier en cours et le chantier ouvert (écrase le chantier en cours)
            self.afficheEtat()
        else:
            self.encadre (_('Chantier choisi %s corrompu. Abandon.') % (self.selectionRepertoireAvecChemin))

    def enregistreChantierAvecMessage(self):
        if(self.enregistreChantier()):
            self.afficheEtat(_("Chantier enregistré")+"\n")

    def enregistreChantier(self):               # Correspond simplement à la copie du fichier paramètre sous le répertoire de travail et à l''apparition du nom
        self.menageEcran()
        if self.etatDuChantier == 0:		# pas de photo : pas d'enregistrement
            self.encadre(_("Indiquer les photos à traiter avant d'enregistrer le chantier."))
            return False
        if self.etatDuChantier == 1:		# des photos, pas encore enregistré : on mote l'enregistrement : etat = 2
            self.etatDuChantier = 2
        self.copierParamVersChantier()          # on enregistre, ou on réenregistre 
        return True

    def renommeChantier(self):
        self.menageEcran()
        if self.etatDuChantier==0:
            self.encadre(_("Le chantier est en cours de définition.") + "\n" +
                         _("Il n'a pas encore de nom, il ne peut être renommé.") + "\n\n" +
                         _("Commencer par choisir les photos"))
            return                      
        texte = _("Nouveau nom ou nouveau chemin pour le chantier %s :") % (self.chantier) + "\n"
        bas = (_("Donner le nouveau nom du chantier") + "\n"+
               _("Un chemin absolu sur la même unité disque ou relatif au répertoire pére est valide") + "\n"+
               _("Aucun fichier de l'arborescence du chantier ne doit être ouvert.")+ "\n\n"+
               _("Chemin actuel : ") + "\n"+
                self.repTravail)
        repertoirePere = os.path.dirname(self.repTravail)
        new = MyDialog(fenetre,texte,basDePage=bas).saisie
        if new in (False,""):
            self.encadre(_("Renommer le chantier : Abandon utilisateur"))
            return
        nouveauRepertoire = os.path.normcase(os.path.normpath(os.path.join(repertoirePere,new)))                                                  # sinon on renomme sous ou sur le répertoire des photos
        if nouveauRepertoire==self.repTravail :
            self.encadre(_("Nouveau nom = ancien nom ; Abandon"))
            return # destination == origine : retour
        
        if self.nomDuChantierExisteDeja(nouveauRepertoire):
            self.encadre(_("Le nom du nouveau chantier :\n %s \n est déjà un chantier:\n %s\n Abandon.") % (os.path.basename(nouveauRepertoire),
                                                                                                            self.nomDuChantierExisteDeja(nouveauRepertoire)[0]))
            return  
        
        if os.path.splitdrive(nouveauRepertoire)[0].upper()!=os.path.splitdrive(self.repTravail)[0].upper():
            self.encadre(_("Le nouveau répertoire ") + "\n\n" +
                         nouveauRepertoire + "\n\n" +
                         _("implique un changement de disque.") + "\n" +
                         _("Utiliser l'item 'Enregistrer sous...' ou l'Export-Import."))
            return
        
        if os.path.exists(nouveauRepertoire):
            self.encadre(_("Le répertoire") + "\n" + nouveauRepertoire + "\n" +
                         _("est déjà utilisé.") + "\n" +
                         _("Choisissez un autre nom."))
            return
        
        try: 
            if os.path.commonpath([self.repTravail,nouveauRepertoire]) == self.repTravail: # Attention : commande nouvelle en version python 3.5
                self.encadre(_("Le répertoire choisi :") + "\n" + nouveauRepertoire + "\n" +
                             _("désigne un sous-répertoire du chantier en cours.") + "\n" +
                             _("Choisissez un autre nom."))
                return
        except: pass

        # tout est bon :
        self.deplaceChantier(nouveauRepertoire)

    def nomDuChantierExisteDeja(self,nouveauRepertoire):
        nouveauChantier = os.path.basename(nouveauRepertoire).upper()
        chantierExistant = [e for e in self.tousLesChantiers if os.path.basename(e).upper()==nouveauChantier]
        if chantierExistant:
            return chantierExistant      

    def enregistreChantierSous(self):
        message = _("Cette fonction permet de changer l'unité disque du chantier.")
        message += "\n"+"\n"+_("Le nom du répertoire choisi deviendra le nom du chantier.")                    
        message += "\n"+_("S'il existe le répertoire choisi doit être vide.")
        message += "\n"+_("Les fichiers seront copiés, le répertoire initial ne sera pas modifié.")                                      
        if MyDialog_OK_KO(fenetre,titre=_("Enregistre sous..."),texte=message,b1="OK",b2="KO").retour!=1:
            return        

        nouveauRepChantier  = tkinter.filedialog.askdirectory(
                                                                    initialdir = "/",
                                                                    title = _("Choisir ou créer le répertoire ou sera enregistré le chantier"),
                                                                    parent=fenetre,
                                                                    )
        if not nouveauRepChantier:
            self.encadre(_("Abandon utilisateur"))
            return

        if not os.path.isdir(nouveauRepChantier):      # c'est pas un répertoire : abandon
            self.encadre(_("Le chenim choisi doit être un répertoire : abandon !"))
            return

        if os.listdir(nouveauRepChantier):
            self.encadre(_("Le répertoire choisi n'est pas VIDE : abandon !"))
            return            

        if self.nomDuChantierExisteDeja(nouveauRepChantier):
            self.encadre(_("Le nom du nouveau chantier :\n %s \n est déjà un chantier:\n %s\n Abandon.") % (os.path.basename(nouveauRepertoire),
                                                                                                            self.nomDuChantierExisteDeja(nouveauRepertoire)[0]))
            return  
        

        # le répertoire cible existe, le chantier est nouveau : il faut copier ou renommer
        self.deplaceChantier(nouveauRepChantier)
           
    def deplaceChantier(self,nouveauRepertoire):    # le paramètre est le chemin complet du chantier = nouveau self.repTravail 
        # on essaie de fermer les fichiers ouverts
        self.fermerVisuPhoto()                                                    # fermer tous les fichiers potentiellement ouvert.
        oschdir(self.repertoireData)                                              # quitter le répertoire courant
        # Avant la copie ou le renommage, il faut d'abord supprimer le répertoire destination :
        if os.path.isdir(nouveauRepertoire):      # c'est pas un répertoire : abandon
            try: os.rmdir(nouveauRepertoire)
            except Exception as e:
                self.encadre(_("Le répertoire\n %s \ndestination est probablement non vide :\nErreur :  %s.\n Abandon.") %   (nouveauRepertoire,str(e)))
                return   
        # si l'unité disque ne change pas : on renomme (rapide et fiable, sauf si un fichier est ouvert, par exemple un ply par cloudcompare)
        if os.path.splitdrive(nouveauRepertoire)[0].upper()==os.path.splitdrive(self.repTravail)[0].upper():
            try:
                time.sleep(0.1)
                os.renames (self.repTravail,nouveauRepertoire)                               # RENOMMER
            except Exception as e:
                self.encadre(_("Le renommage du chantier ne peut se faire actuellement,") + "\n" +
                             _("soit le nom fourni est incorrect,") + "\n"+
                             _("soit un fichier du chantier est ouvert par une autre application.") + "\n"+
                             _("soit l'explorateur explore l'arborescence.") + "\n" + _("erreur : ") + "\n\n"+str(e))
                return
        #il faut changer de support disque : recopie des fichiers, peut-être long !
        else:                
            # répertoire destination supprimé pour autoriser la commande shutil.copytree : copie :       
            try :
                self.encadre(_("La copie de l'arborescence du chantier est en cours.\n %s \nPatience....")
                             % ( "\n"+" "+_("Taille du chantier : ")+str(sizeDirectoryMO(self.repTravail))+" MO" ))
                shutil.copytree(self.repTravail,nouveauRepertoire)
            except Exception as e:
                self.encadre(_("La copie du chantier ne peut se faire actuellement,") + "\n" +
                              _("erreur : ") + "\n\n"+str(e))
                return
        # Chantier renommé correctement       
        try: self.tousLesChantiers.remove(self.repTravail)                          # retirer l'ancien nom de la liste des répertoires de travail
        except: pass
        ancienChantier = self.chantier
        self.chantier = os.path.basename(nouveauRepertoire)        
        self.repTravail = nouveauRepertoire                                         # positionner le nouveau nom        
        self.redefinirLesChemins()                                                  # mettre à jour le nom de tous les chemins realtifs
        self.ajoutChantier()                        # ajouter le nouveau nom parmi les noms de chantiers
    # Type de chantier : self.typeDuChantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
    # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' ou du calcul d'un 'volume'
    # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
    # [2] = 'original' ou "importé"
        self.typeDuChantier[1] = 'renommé'
        self.encadreEtTrace("\n---------\n"+ heure() + "\n" +
                            _("Chantier :") + "\n" +
                            ancienChantier + "\n" +
                            _("renommé en :") + "\n" +
                            self.chantier + "\n" + 
                            _("enregistré sous le répertoire : ") +"\n" + 
                            self.repTravail + "\n") 

    def redefinirLesChemins(self):       # Mettre self.repTravail dans les chemins des images, des  maitres et masques et dans les dictionnaires, sauver
                                         # si le chantier n'est plus sous le répertoire des photos alors le répertoire des photos devient le chantier lui même       
        self.photosAvecChemin   = [os.path.join(self.repTravail,os.path.basename(afficheChemin(e))) for e in self.photosAvecChemin]
        self.listeDesMaitresses = [os.path.join(self.repTravail,os.path.basename(afficheChemin(e))) for e in self.listeDesMaitresses]
        self.listeDesMasques    = [os.path.join(self.repTravail,os.path.basename(afficheChemin(e))) for e in self.listeDesMasques]                              
        self.lesTagsExif        = dict()

        # le répertoire où se trouvent les photos pour la calibration change après Tapas :
 
        if self.photosPourCalibrationIntrinseque:
            if self.repCalibSeule in os.path.dirname(self.photosPourCalibrationIntrinseque[0]):
                self.photosPourCalibrationIntrinseque = [os.path.join(self.repTravail,self.repCalibSeule,os.path.basename(afficheChemin(e)))
                                                         for e in self.photosPourCalibrationIntrinseque]
            else:
                self.photosPourCalibrationIntrinseque = [os.path.join(self.repTravail,os.path.basename(afficheChemin(e)))
                                                         for e in self.photosPourCalibrationIntrinseque]

 
        if self.fichierMasqueXML!=str():
            self.fichierMasqueXML       = os.path.join(self.repTravail,os.path.basename(afficheChemin(self.fichierMasqueXML)))
        if self.monImage_MaitrePlan!=str():
            self.monImage_MaitrePlan    = os.path.join(self.repTravail,os.path.basename(afficheChemin(self.monImage_MaitrePlan)))
            self.monImage_PlanTif       = os.path.join(self.repTravail,os.path.basename(afficheChemin(self.monImage_PlanTif)))

        
        # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y          
        dico=dict()
        for  e in self.dicoPointsGPSEnPlace.keys():
            f = (e[0],os.path.join(self.repTravail,os.path.basename(afficheChemin(e[1]))),e[2])
            dico[f]=self.dicoPointsGPSEnPlace[e]
        self.dicoPointsGPSEnPlace = dict(dico)

        # axe horizontal, dans le dico : self.dicoLigneHorizontale. key = nom point, chemin complet photo, identifiant ;Retrouver nom de la photo, coordonnées des points
        # items = liste de tuple (key,values) soit tuple = (point,photo, id),(x1,y1)
       
        dico=dict()
        for  e in self.dicoLigneHorizontale.keys():
            f = (e[0],os.path.join(self.repTravail,os.path.basename(afficheChemin(e[1]))),e[2])
            dico[f]=self.dicoLigneHorizontale[e]
        self.dicoLigneHorizontale = dict(dico)           
        dico=dict()
        for  e in self.dicoLigneVerticale.keys():
            f = (e[0],os.path.join(self.repTravail,os.path.basename(afficheChemin(e[1]))),e[2])
            dico[f]=self.dicoLigneVerticale[e]
        self.dicoLigneVerticale = dict(dico)           
        dico=dict()
            
        for  e in self.dicoCalibre.keys():
            f = (e[0],os.path.join(self.repTravail,os.path.basename(afficheChemin(e[1]))),e[2])
            dico[f]=self.dicoCalibre[e]
        self.dicoCalibre = dict(dico)

        # nouveau répertoire des photos :

        self.repertoireDesPhotos = afficheChemin(self.repertoireDesPhotos)
        
        if  not os.path.isdir(self.repertoireDesPhotos):
            self.repertoireDesPhotos = self.repTravail
        
        self.definirFichiersTrace()                                                 # positionne sous le répertoire de travail
        self.copierParamVersChantier()                                              # sauve param puis copie vers chantier en cours 

    def exporteChantier(self):
        self.menageEcran()
        if self.etatDuChantier == 0:
            self.encadre(_("Pas de chantier en cours"))
            return
        self.encadre(_("Patience : chantier en cours d'archivage...") + "\n")
        self.copierParamVersChantier()      # enregistre et sauve le chantier
        self.encadre(_("Archive ") + "\n" + self.chantier + ".exp" + "\n" +
                     _("créée sous ") + "\n" + self.repTravail + "\n\n" +
                     _("Taille =") + str(int(zipdir(self.repTravail)/1024)) + "Ko")

    def importeChantier(self):
        self.menageEcran()
        try:
            self.encadre(_("Choisir le nom de l'archive à importer."))
            archive = tkinter.filedialog.askopenfilename( initialdir=self.repTravail,                                                 
                                                        filetypes=[(_("Export"),"*.exp"),(_("Tous"),"*")],
                                                        multiple=False,
                                                        title = _("Chantier à importer"))
            if archive==str():
                self.encadre(_("Importation abandonnée."))
                return
            if not zipfile.is_zipfile(archive):
                self.encadre(archive+" "+_("n'est pas un fichier d'export valide") + "\n"+
                             _("ou alors, sous ubuntu,il lui manque le droit d'exécution."))
                return                                                               
            
            self.encadre(_("Choisir le répertoire dans lequel recopier le chantier."))          
            destination = tkinter.filedialog.askdirectory(title=_('Désigner le répertoire où importer le chantier '),
                                                        initialdir=self.repTravail)
            if not os.path.isdir(destination):
                self.encadre(destination+" "+_("n'est pas un répertoire valide."))
                return
            oschdir(destination)                   # relativise les chemins
            self.encadre(_("Recopie en cours dans") + "\n" + destination + "\n" + _("Patience !"))
     
            zipf = zipfile.ZipFile(archive, 'r')    # ouverture du zip
            # récupération du nom du futur chantier : c'est la racine commune de tous les fichiers dans la sauvegarde
            nouveauChantier = os.path.normpath(os.path.commonprefix(zipf.namelist())[:-1])
            ancienChantier = nouveauChantier.split(self.suffixeExport)[0]  # ancien chantier = nouveau - suffixe
            if os.path.isdir(nouveauChantier):
                zipf.close()
                self.encadre(_("Le répertoire destination") + "\n" +
                             os.path.join(destination, nouveauChantier) + "\n" +
                             _("existe déjà. Abandon"))
                return
            zipf.extractall(path=destination)
            zipf.close()
            oldChantier = nouveauChantier
            i = 0
            while (os.path.basename(nouveauChantier) in [os.path.basename(e) for e in self.tousLesChantiers]) or os.path.isdir(os.path.join(destination,nouveauChantier)) and i<20:
                nouveauChantier = nouveauChantier+"x"
                i += 1
            try: os.renames (oldChantier,nouveauChantier)   # on a trouvé un nom nouveau de chantier ET de répertoire (plante si old=nouveau) 
            except Exception as e:
                print(_("Erreur copie lors d'un import : "),str(e))
                self.encadre(_("L'importation a échouée. Erreur : ")+str(e))
                return
            
            nouveauChemin = os.path.normcase(os.path.normpath(os.path.join(destination,nouveauChantier)))

            # on copie si possible l'archive sous le nouveau répertoire de travail
            try: shutil.copy(archive,nouveauChemin)
            except Exception as e:
                print(_("Erreur copie lors d'un import : "),str(e))
                self.encadre(_("L'importation a échouée. Erreur : ")+str(e))
                return            
            
            # on met à jour les paramètres locaux : remplacer les répertoires ancien par le nouveau, sauvegarder
            fichierParam = os.path.join(nouveauChemin,self.paramChantierSav)

            if os.path.isfile(fichierParam):
                self.restaureParamChantier(fichierParam)        # la restauration positionne self.reptravail et self.chantier sur l'ancien répertoire de travail
            else:
                self.encadre(fichierParam+" "+_("absent"))
                return
            self.repTravail = nouveauChemin                     # le répertoire des photos devient le répertoire de travail
            self.chantier = nouveauChantier
            self.definirFichiersTrace()                         # la restauration a défini des chemins suivant l'ancien reptravail : il faut corriger                      
            self.ajoutChantier()# on ajoute le chantier dans les paramètres généraux             

    # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
    # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
    # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
    # [2] = 'original' ou "importé"
            self.typeDuChantier[2] = 'importé'
            self.redefinirLesChemins()                      # mise à jour des chemins et sauvegarde des paramètres.
            
            # on affiche l'état du chantier :
            
            self.encadreEtTrace("\n\n -------------- \n"+
                                heure()+
                                "\n" + _("Chantier importé :") + "\n" + self.chantier + "\n\n" + _("Répertoire :") + "\n" +self.repTravail+ "\n\n" + _("Vous pouvez le renommer si  besoin.")+
                                "\n -------------- ")
            try:
                self.ajoutLigne("\n" + _("Version de MicMac avant l'import : %s") % (self.mercurialMicMacChantier) +"\n")
                self.ajoutLigne("\n" + _("Version de MicMac : %s") % (self.mercurialMicMac) +"\n")            
                self.ecritureTraceMicMac()
            except Exception as e:
                print(_("erreur affichage version lors de l'import d'un chantier : ")+str(e))
        except Exception as e:
            self.encadre(_("Anomalie lors de l'importation : ")+str(e))
            return
        
    def ajoutRepertoireCommechantier(self): # ajoute un répertoire dans le liste des chantiers : le répertoire doit contenir  le fichier paramChantier.sav
        self.menageEcran()
        nouveauRepChantier  = tkinter.filedialog.askdirectory(title=_('Désigner le répertoire contenant un chantier '),
                                                        initialdir=self.repTravail)
        if nouveauRepChantier in self.tousLesChantiers:
            self.encadre(_("Ce répertoire est déjà un chantier. Abandon"))
            return
        if os.path.isdir(nouveauRepChantier):       # c'est bien un répertoire
            param = os.path.join(nouveauRepChantier,self.paramChantierSav)
            if os.path.isfile(param): # il existe un fichier paramètre
                if nouveauRepChantier in self.tousLesChantiers:
                    self.encadre(_("Le répertoire du nouveau chantier \n %s \n est déjà un chantier.\n Abandon.") % (nouveauRepChantier))
                    return
                self.encadre(_("Répertoire correct. Patience..."))
            # on ajoute le chantier dans les paramètres généraux
                self.restaureParamChantier(param)
                self.repTravail = nouveauRepChantier
                self.chantier = os.path.basename(self.repTravail)                 
                self.typeDuChantier[2] = 'ajouté'
                self.sauveParam()                                       # pour assurer la cohérence entre le chantier en cours et le chantier ouvert (écrase le chantier en cours)
                self.redefinirLesChemins()                              # pour convertir les chemins dans les paramètres
                self.ajoutChantier()    # on ajoute le chantier dans les paramètres généraux
                self.afficheEtat()
            else:
                self.encadre(_("Le répertoire ne contient pas le fichier :\n")+
                             self.paramChantierSav+_("Ce n'est pas un chantier.\nAbandon."),
                             nouveauDepart="non")
            

    def copierParamVersChantier(self):          # copie du fichier paramètre sous le répertoire du chantier, pour rejouer et trace
        try:
            self.etatSauvegarde = ""             
            self.sauveParam()                   # sauve les paramètres généraux et ceux du chantier
            try: shutil.copy(self.fichierParamChantierEnCours,self.repTravail)          # pour éviter de copier un fichier sur lui même
            except Exception as e:
                print(heure()," "+_("anomalie copie fichier param chantier : %(param)s vers %(rep)s ")
                                  % {"param" : self.fichierParamChantierEnCours, "rep" : self.repTravail} ,str(e))
            fenetre.title(self.etatSauvegarde+self.titreFenetre)            
        except Exception as e:
            self.ajoutLigne(_("Erreur lors de la copie du fichier paramètre chantier") + "\n" + self.fichierParamChantierEnCours + "\n" + _("vers") + "\n" + self.repTravail + "\n" + _("erreur :") + "\n" +str(e))


    ################################## LE MENU EDITION : afficher l'état, les photos, lire une trace, afficher les nuages de points ############################
                                                
    def afficheEtat(self,entete="",finale=""):

        if not os.path.isdir(self.repTravail):
            self.encadre(_("Le répertoire ")+"\n"+self.repTravail+"\n "+_("du chantier précédent n'est pas trouvé sur disque.")+
                         "\n"+_("Choisir un autre chantier."))
            return
        if self.pasDeMm3d():
            return
        nbPly = 0
        texte = str()        
        photosSansChemin = self.toutesLesPhotosSansChemin()
        photosSansCheminDebutFin = photosSansChemin
        if len(photosSansChemin)>5:
            photosSansCheminDebutFin =photosSansChemin[:2]+list('..',)+photosSansChemin[-2:]
        try:
            # affiche les options du chantier (try car erreur si le format de la sauvegarde a changé cela plante) :
            # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
            # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
            # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
            # [2] = 'original' ou "importé"          
            if self.typeDuChantier[0]=='photos':
                texte = entete + _('Répertoire des photos :') +  "\n" + afficheChemin(self.repertoireDesPhotos)
            if self.typeDuChantier[0]=='vidéo':
                 texte = entete + "\n" + _("Répertoire de la vidéo :") + "\n" + afficheChemin(self.repertoireDesPhotos)                 
            if len(photosSansChemin)==0:
                texte = texte+'\n\n'+_('Aucune photo sélectionnée.') + '\n'
                # SI les options par défaut sont personnalisée on informe :

                if os.path.exists(self.fichierSauvOptions):
                    texte += "\n "+_("Nouveau chantier : Les options par défaut sont personnalisées ")           
               
            if len(photosSansChemin)>=1:                                   # Il ne peut en principe pas y avoir une seule photo sélectionnée
                # nombre de photos sélectionnées : 
                if self.calibSeule.get():
                    m = _(' photos sélectionnées') + '\n'
                else:
                    m = _(' photos sélectionnées : ') + '\n'
                texte = texte+'\n\n'+str(len(photosSansChemin))+m+'\n'.join(photosSansCheminDebutFin)+finale
            if self.nombreDExtensionDifferentes(photosSansChemin)>1:       # il y a plus d'un format de photo !
                texte = texte+'\n\n' + _('ATTENTION : plusieurs extensions différentes dans les photos choisies !') + '\n' + _('Le traitement ne se fera que sur un type de fichier.')

            # Indication de la présence de paramètres nommés personnalisés :

            if self.nettoiePerso()[1]:
                texte += "\n"+_("Il y a des paramètres nommés personnalisés qui surchargent les valeurs ci-dessous")
  
            # Options pour Tapioca :

            if self.modeTapioca.get()!='':
                texte = texte+'\n\n' + _('Recherche des points homologues :') + '\n' + _('Mode : ')+self.modeTapioca.get()+'\n'
            if self.modeTapioca.get()=="All":
                texte = texte+_('Echelle 1 : ')+self.echelle1.get()+'\n'
            if self.modeTapioca.get()=="MulScale":
                texte = texte+_('Echelle 1 : ')+self.echelle2.get()+'\n'
                texte = texte+_('Echelle 2 : ')+self.echelle3.get()+'\n'
            if self.modeTapioca.get()=="Line":
                texte = texte+_('Echelle : ')+self.echelle4.get()+'\n'
                texte = texte+_('Delta : ')+self.delta.get()+'\n'


            # Options pour Tapas :
            
            if self.modeCheckedTapas.get()!='':
                texte = texte+'\n' + _('Orientation des appareils photos : ')+'\n' + _('Mode : ')+self.modeCheckedTapas.get()+'\n'              
            if self.photosPourCalibrationIntrinseque.__len__()>0 and self.choixCalibration.get()=="photos":
                texte = texte+_("Nombre de photos pour calibration intrinsèque : ")+str(self.photosPourCalibrationIntrinseque.__len__())+"\n"
                if self.calibSeule.get():
                     texte = texte+_('Ces photos servent uniquement à la calibration.') + '\n'
            if self.chantierOrigineCalibration and self.choixCalibration.get()=="chantier":
                texte = texte+_('Calibration du chantier "%s".') % (self.chantierOrigineCalibration) + '\n'
            if self.lancerTarama.get()==1:
                texte = texte+_('Tarama demandé après orientation') + '\n'                     
            if self.arretApresTapas.get()==1:
                texte = texte+_('Arrêt demandé après orientation') + '\n'

            # Calcul du nuage non dense

            if self.calculNuageNonDense.get():
                 texte = texte+_('Calcul du nuage non dense demandé') + '\n'
            else:
                texte = texte+_('Pas de calcul du nuage non dense') + '\n'

            # Quel référentiel pour le nuage ? par ordre de priorité : - GCP terrain - GPS Drone - Mise à l'échelle

            # Points GCP
            pointsGCPOk = self.controlePointsGPS()
            if self.listePointsGPS:
                if pointsGCPOk:
                    texte += "\n"+_("Points GCP : Saisie complète, les points seront pris en compte") + "\n"
                else:
                    texte += self.etatPointsGPS
                    
            # données navigation drone gps dans les exif : self.repereChoisi = str() : pas de GPS, "
            
            self.miseAJourLibelleNavigationGPS()
                
            if os.path.isdir("Ori-nav-Brut") and len(photosSansChemin)>2:
                if pointsGCPOk:
                    texte = texte+'\n' + _("Les données GPS dans les exif sont ignorées, supplantées par les points GCP") + '\n'
                else:
                    texte = texte+'\n' + _("Les données GPS dans les exif sont prises en compte") + '\n'
                    if self.repereChoisi==self.repereLocalXml:
                        texte += _("Référentiel : projection plane locale (métrique)") + '\n'
                    if self.repereChoisi==self.repereLambert93:
                        texte += _("Référentiel WGS84 projeté en Lambert 93")+"\n"
                    if self.repereChoisi==self.repereWGS84:
                        texte += _("Référentiel WGS84")+"\n"                   
                    if self.repereChoisi==self.repereGeoc:
                        texte += _("Référentiel WGS84 projeté dans un repère géocentrique cartésien X,Y,Z") + '\n'
                    if self.repereChoisi==self.repereEpsgXml:
                        texte += _("Référentiel : "+self.nomEpsg) + '\n'                    
                    if self.controleMiseALEchelle():
                        texte +=  _("Remarque : la mise à l'échelle ci-dessous sera ignorée") + '\n'
                    if self.repereChoisi==self.repereSupprime:
                        texte = texte+'\n' + _("Les données GPS sont ignorées sur demande utilisateur.") + '\n'
            
            # Mise à l'échelle

            if self.controleMiseALEchelle():
                texte = texte+'\n' + _("Mise à l'échelle présente") + '\n'+self.etatMiseALEchelle
            else:
                if self.distance.get()=='0':
                    texte = texte+'\n' + _("Mise à l'échelle invalide : distance=0") + '\n'
                elif self.etatMiseALEchelle!=str():             # calibration incomplète
                    texte = texte+"\n" + _("Mise à l'échelle incomplète :") + "\n"+self.etatMiseALEchelle+"\n"   
                    
            # C3DC est-il installé ?

            if not self.mm3dOK:         # La version de MicMac n'autorise pas les masques 3D : info
                texte = texte + "\n" + _("La version installée de Micmac n'autorise pas les masques en 3D") + "\n"

            # C3DC est choisi :
            
            if self.choixDensification.get()=="C3DC":            
                if self.existeMasque3D():
                    texte = texte+'\n' + _('Densification : C3DC %s avec masque 3D ') % (self.modeC3DC.get())+ '\n'
                else:
                    texte = texte+'\n' + _('Densification : C3DC %s') % (self.modeC3DC.get()) + '\n'
                    
            # Malt est choisi : 

            if self.choixDensification.get()=="Malt":
                texte = texte+'\n' + _('Densification : ')+' Malt\n' + _('Mode : ')+self.modeCheckedMalt.get()
                if self.modeCheckedMalt.get()=="GeomImage":
                    if self.listeDesMaitresses.__len__()==0:
                        texte = texte+"\n" + _("Pas d'image maîtresse\n")
                    if self.listeDesMaitresses.__len__()==1:
                        texte = texte+'\n' + _('Image maîtresse : ')+os.path.basename(self.listeDesMaitresses[0])
                    if self.listeDesMaitresses.__len__()>1:
                        texte = texte+'\n'+str(self.listeDesMaitresses.__len__())+_(' images maîtresses')                        
                    if self.listeDesMasques.__len__()==1:
                        texte = texte+'\n' + _('1 masque') + '\n'
                    if self.listeDesMasques.__len__()==0 and self.listeDesMaitresses.__len__()>0:
                        texte = texte+"\n" + _("Pas de masque.") + "\n"
                    if self.listeDesMasques.__len__()>1:
                        texte = texte+"\n"+str(self.listeDesMasques.__len__())+" "+_("masques") + "\n"
                    if self.listeDesMaitresses.__len__()>0 and self.photosUtilesAutourDuMaitre.get()>0:                        
                        texte = texte+_("%s photos utiles autour de la maîtresse") %(str(self.photosUtilesAutourDuMaitre.get()))+"\n"

                if self.modeCheckedMalt.get()=="Ortho":
                    if self.tawny.get():
                        texte = texte+"\n" + _("Drapage demandé")+"\n"
                    else:
                        texte = texte+"\n" + _("Pas de drapage")+"\n"
                                                
                texte = texte +_("arrêt au zoom : ")+self.zoomF.get()+", rendu : "

                if self.nuage2Mesh.get()=="0":
                      texte = texte +_("Nuage")+"\n" 
                if self.nuage2Mesh.get()=="1":
                      texte = texte +_("Maillage")+"\n"
                     
            # état du chantier :
            # EtatDuChantier :
            # 0 : pas encore de photos
            # 1 : il y a des photos choisies
            # 2 : des photos, enregistré                              
            # 3 en cours d'exécution de Tapioca/Tapas, a sans doute planté pendant
            # 35 Chantier arrêté aprés tapioca, points homoloques conservés
            # 4 arrêt après tapas,
            # 5 terminé après malt ou c3dc,
            # 6 terminé, redevenu modifiable (??)
            # 7 : la densification a échoué
            
            if self.etatDuChantier == 0:                                        # pas encore de chantier
                texte = texte+"\n" + _("Chantier en cours de définition.") + "\n"


            # un chantier avec des traitements effectués et pas de sous-répertoire : il a été nettoyé !
            lesRepertoires = [f for f in os.listdir(self.repTravail) if os.path.isdir(os.path.join(self.repTravail, f))]
            if self.etatDuChantier >= 3 and lesRepertoires.__len__()==0:
                self.chantierNettoye = True                
                self.etatDuChantier = 2
                self.ajoutLigne("\n"+heure()+_("****** ouverture du chantier."))
                self.ajoutLigne("\n"+_("Le chantier a été nettoyé, les résultats et les traces sont conservées."))
                
            # chantier nettoyé mais relancé depuis donc etatDuChantier >= 3 :                
            if self.chantierNettoye and self.etatDuChantier>=3:
                self.chantierNettoye = False                 # le chantier a été relancé, n'est plus nettoyé

            # Message si chantier nettoyé non relancé :
                
            if self.chantierNettoye:
                texte = texte+"\n" + _("Chantier nettoyé. Résultats et traces conservées.") + "\n"
                
            # Affichage de l'état du chantier :

            if self.etatDuChantier >= 1:        # 0 : pas encore de photos
                                                # 1 : il y a des photos choisies
                                                # 2 : des photos, enregistré                              
                                                # 3 en cours d'exécution de Tapioca/Tapas
                                                # 35 Chantier arrêté aprés tapioca, points homoloques conservés
                                                # 4 arrêt après tapas,
                                                # 5 terminé après malt ou c3dc,
                                                # 6 terminé, redevenu modifiable
                                                # 7 : densification à échoué
                                                
                texte = texte+"\n" + _("Chantier : ")+self.chantier+".\n"
                # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
                # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
                # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
                # [2] = 'original' ou "importé"

                if self.typeDuChantier[1]=="renommé" or self.typeDuChantier[2]=="importé" or self.typeDuChantier[2]=="ajouté":
                    texte = texte + _("Chemin du chantier :") + "\n"+self.repTravail+"\n\n"
            else:
                texte = texte+"\n" + _("Chantier en attente d'enregistrement.") + "\n"
            if self.etatDuChantier in (2,3,4,5,35) and self.etatSauvegarde=="":		
                texte = texte+"\n" + _("Chantier enregistré.") + "\n"
            if self.etatDuChantier == "2":		
                texte = texte+_("Options du chantier modifiables.") + "\n"               
            if self.etatDuChantier == 3:		
                texte = texte+"\n" + _("Chantier interrompu lors de la recherche des points homologues.") + "\n" + _("Modifier les options, relancer micmac.") + "\n"
            if self.etatDuChantier == 4:		
                texte = texte+_("Options de Malt/C3DC modifiables.") + "\n"
            if self.etatDuChantier == 5:		
                texte = texte+_("Chantier terminé.")+ "\n"
                             
            # Résultat des traitements :
                          
            if os.path.exists('AperiCloud.ply'):
               texte = texte+_("Nuage de point non densifié généré après Tapas.") + "\n"
               nbPly=1
            elif self.etatDuChantier == 35:		
                texte = texte+"\n" + _("Chantier interrompu lors de la recherche de l'orientation.") + "\n" + _("Modifier les options, relancer micmac.") + "\n"                

            if os.path.exists(self.modele3DEnCours):
               texte = texte+_("Nuage de points densifié généré.")+"\n"
               nbPly+=1
            else:   
                if self.etatDuChantier == 7:		
                    texte = texte+"\n" + _("La densification a echoué : pas de nuage dense généré.") + "\n"
                if self.etatDuChantier in (4,5,7) and nbPly==0:
                   texte = texte+_("Aucun nuage de point généré.") + "\n"
            self.tailleDuChantierEnMO = sizeDirectoryMO(self.repTravail)
            texte += "\n"+_("Taille du chantier : ")+str(self.tailleDuChantierEnMO)+" MO"            
            oschdir(self.repTravail)
                
            
        except Exception as e:
            texte = _("Les caractéristiques du chantier précédent") + "\n" + self.chantier + "\n" + _("n'ont pas pu être lues correctement." ) + "\n"+\
                    _("Le fichier des paramètres est probablement incorrect ou vous avez changé la version de l'interface.") + "\n"+\
                    _("Certaines fonctions seront peut_être défaillantes.") + "\n"+\
                    _("Désolé pour l'incident.") + "\n\n"+\
                    _("Erreur : ")+str(e) +"\n"+texte
            self.ajoutTraceSynthese(texte)

        # si les options ont été activées, même abandonnées, alors ont mémorise texte dans la trace complète pour garder une trace des modifs
        # pour débug 
        if self.optionsMicMacActivees:
            self.ajoutTraceComplete("\n"+heure()+" "+_(" Options modifiées, état du chantier :\n")+texte)
            self.optionsMicMacActivees = False
        self.ecritureTraceMicMac()
        self.sauveParam()
        self.encadre(texte)            

    def toutesLesPhotosSansChemin(self):
        photosPourNuage = set(self.photosSansChemin)
        photosPourCalibration = set([ os.path.basename(e) for e in self.photosPourCalibrationIntrinseque])
        toutesLesPhotos = list(photosPourNuage.union(photosPourCalibration))
        toutesLesPhotos.sort()
        return toutesLesPhotos
        

############### Existence des maitres 2D 3D : vrai, faux 
       
    def existeMasque3D(self):
        if self.repTravail==self.repertoireData:
            return False
        self.masque3D = os.path.join(self.repTravail,self.masque3DSansChemin)
        if os.path.exists(self.masque3D):
            return True
        else:
            return False
        
    def existeMaitre2D(self):
        if self.repTravail==self.repertoireData:    # pas enregistré
            return False     
        if str(self.modeCheckedMalt.get())!="GeomImage":   # pas besoin d'image maîtresse !
            return True
        if self.listeDesMaitresses.__len__()>0:     # GeoImage et maitresses : OK
            return True
        else:                                       # le mode est geomimage et il n'y a pas d'image maitre
            return False      

############### Affichages des photos choisies, points, masques, distance...
        
    def afficherToutesLesPhotos(self):
        if self.photosPourCalibrationIntrinseque.__len__()==0:
            titre = _('Toutes les photos')
            message = _('Toutes les photos')
        else:
            titre = _('Toutes les photos utiles')
            message = _('Toutes les photos') + '\n' + _('sans les %s photos pour calibration intrinseque') % (str( self.photosPourCalibrationIntrinseque.__len__()))
            
        self.choisirUnePhoto(self.photosSansChemin,
                             titre=titre,
                             mode='single',
                             message=message,
                             messageBouton=_("Fermer"))

    def afficherLesPointsGPS(self):
        photosAvecPointsGPS = [ e[1] for e in self.dicoPointsGPSEnPlace.keys() ]    # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
        if photosAvecPointsGPS.__len__()==0:
            self.encadre(_("Aucun point GCP saisi."))
            return
        self.choisirUnePhoto(photosAvecPointsGPS,
                             titre=_('Affichage des photos avec points GCP'),
                             mode='single',
                             message=_("seules les photos avec points sont montrées."),
                             messageBouton=_("Fermer"),
                             dicoPoints=self.dicoPointsGPSEnPlace)
        
    def afficherLesMaitresses(self):
        
        if self.listeDesMaitresses:            
            self.choisirUnePhoto(self.listeDesMaitresses+self.listeDesMasques,
                                 titre=_('Liste des images maîtresses et des masques '),
                                 mode='single',
                                 message=_("Images maîtresses et masques"),
                                 messageBouton=_("Fermer")
                                 )            
        else:
            self.encadre(_("Pas de maîtresses définies pour ce chantier"))

    def afficherMasqueTarama(self):

        if os.path.exists(self.masqueTarama):            
            self.choisirUnePhoto([self.mosaiqueTaramaJPG,self.masqueTarama],
                                 titre=_('Mosaique Tarama et masque ')+"\n"+_("Option Ortho de Malt"),
                                 mode='single',
                                 message=_("Image maîtresse et masque"),
                                 messageBouton=_("Fermer")
                                 )             
        

    def afficheMasqueC3DC(self):
        if self.existeMasque3D()==False:
            self.encadre(_("Pas de masque 3D pour ce chantier."))
            return
        oschdir(self.repTravail)
        self.menageEcran()
        self.topMasque3D = tkinter.Toplevel(relief='sunken')
        fenetreIcone(self.topMasque3D)           
        self.item900 = ttk.Frame(self.topMasque3D,height=5,relief='sunken',padding="0.3cm")        
        self.item901 = ttk.Button(self.item900,text=_('Visaliser le masque 3D'),command=self.affiche3DApericloud)              
        self.item901.pack(ipady=2,pady=10)
        self.item903 = ttk.Button(self.item900,text=_('Fermer'),command=lambda : self.topMasque3D.destroy())              
        self.item903.pack(ipady=2,pady=10)        
        self.item902 = ttk.Label(self.item900, text=_("Affichage du masque 3D :") + "\n\n"+
                                                    _("Les points blancs du nuage sont dans le masque") + "\n"+
                                                    _("ATTENTION : pour continuer FERMER la fenêtre 3D")+ "\n"+
                                                    _("puis cliquer sur le bouton FERMER ci-dessus."))
        self.item902.pack(ipady=2,pady=10)               
        self.item900.pack()                                   
        fenetre.wait_window(self.topMasque3D)

    def afficherZonePlane(self):
        if len(self.monImage_MaitrePlan)>0:
            if os.path.exists(self.monImage_PlanTif) and os.path.exists(self.monImage_MaitrePlan):
                masqueEtMaitre = [self.monImage_PlanTif,self.monImage_MaitrePlan]
                if self.monImage_PlanTif==self.planProvisoireHorizontal:
                    plan = _("horizontale")
                else:
                    plan = _("verticale")
                self.choisirUnePhoto(masqueEtMaitre,
                                 titre=_("Visualiser l'image maîtresse et le plan horizontal ou vertical"),
                                 mode='single',
                                 message=_("Zone plane ")+plan,
                                 messageBouton=_("Fermer"))     
            else:
                self.monImage_PlanTif = self.monImage_MaitrePlan = str()
                self.encadre("Pas de plan horizontal ou vertical défini pour ce chantier")          
        else:
            self.encadre(_("Pas de plan horizontal ou vertical défini pour ce chantier"))

    def afficherLigneHV(self):        
        photosAvecLigneH = [ e[1] for e in self.dicoLigneHorizontale.keys() ]
        photosAvecLigneV = [ e[1] for e in self.dicoLigneVerticale.keys() ]
        photosAvecLigne = list(set(photosAvecLigneH+photosAvecLigneV))
        dicoAvecLigne = dict()
        sens = str()
        for e in self.dicoLigneHorizontale:
            dicoAvecLigne[e] = self.dicoLigneHorizontale[e]
            sens = _("HORIZONTALE")
        for e in self.dicoLigneVerticale:
            dicoAvecLigne[e] = self.dicoLigneVerticale[e]
            sens = _("VERTICALE")
        if photosAvecLigne.__len__():    
            self.choisirUnePhoto(photosAvecLigne,
                                 titre=_('Affichage des photos avec ligne horizontale ou verticale'),
                                 mode='single',
                                 message=_("ligne ")+sens,
                                 messageBouton=_("Fermer"),
                                 dicoPoints=dicoAvecLigne)
        else:
            self.encadre(_("Pas de ligne horizontale ou verticale définie pour ce chantier"))            

    def afficherDistance(self):
        try:
            float(self.distance.get().split(" ")[0])       #pour permettre la saisie d'une unité
        except:
            self.encadre(_("Pas de distance correcte définie pour ce chantier."))
            return
        
        photosAvecDistance = list(set([ e[1] for e in self.dicoCalibre.keys() ]))
        self.choisirUnePhoto(photosAvecDistance,
                             titre=_("Visualiser les photos avec distance"),
                             mode='single',
                             message=_("Valeur de la distance : ")+self.distance.get(),
                             messageBouton=_("Fermer"),
                             dicoPoints=self.dicoCalibre)           

    def afficherCalibIntrinseque(self):
        if self.choixCalibration.get()=='sans':
            self.encadre(_("Pas de calibration intrinsèque demandée."))    
            return            
        if self.photosPourCalibrationIntrinseque.__len__()==0:
            self.encadre(_("Pas de photos pour la calibration intrinsèque par Tapas."))    
            return
        self.choisirUnePhoto(self.photosPourCalibrationIntrinseque,
                             titre=_('Les photos pour calibration intrinsèque'),
                             mode='single',
                             message=_("Calibration intrinsèque"),
                             messageBouton=_("Fermer"))
        
    def afficheMosaiqueTarama(self):
              
        if not os.path.exists(self.mosaiqueTaramaTIF):
            self.encadre(_("Pas de mosaique. Choisir l'option Tarama de tapas."))    
            return

        if not os.path.exists(self.mosaiqueTaramaJPG):
            self.conversionJPG(liste=[self.mosaiqueTaramaTIF])
            if not os.path.exists(self.mosaiqueTaramaJPG):
                self.encadre(_("Echec de la conversion mosaique en JPG."))    
                return        

        self.choisirUnePhoto([self.mosaiqueTaramaJPG],
                             titre=_('Mosaique créée par Tarama'),
                             mode='single',
                             message="",
                             messageBouton=_("Fermer"))

    def afficheMosaiqueTawny(self):
        orthoMosaiqueTIF = os.path.join(self.repTravail,"Ortho-MEC-Malt",self.orthoMosaiqueTawny) # chemin complet  
        if not os.path.exists(orthoMosaiqueTIF):
            orthoMosaiqueTIF = os.path.join(self.repTravail,self.orthoMosaiqueTawny) # chemin après ménage
            if not os.path.exists(orthoMosaiqueTIF):
                self.encadre(_("Pas d'ortho mosaique par Tawny. Choisir Malt Ortho ou Malt UrbanMNE."))    # l'option tawny de malt n'est pas utilisée
                return
        orthoMosaiqueJPG = os.path.splitext(orthoMosaiqueTIF)[0]+".JPG"
        if not os.path.exists(orthoMosaiqueJPG):
            self.conversionJPG(liste=[orthoMosaiqueTIF])
            if not os.path.exists(orthoMosaiqueJPG):
                self.encadre(_("Echec de la conversion de la mosaïque TIF en JPG."))    
                return        

        self.choisirUnePhoto([orthoMosaiqueJPG],
                             titre=_('Ortho mosaique créée par Tawny'),
                             mode='single',
                             message="",
                             messageBouton=_("Fermer"))
        
############### Affichages des traces
        
    def lectureTraceMicMac(self,complete=True):
        if self.etatDuChantier == 0:
            self.encadre(_("Pas de chantier, pas de trace !"))
            return
        self.ecritureTraceMicMac()
        
        if complete:
            fichier = self.TraceMicMacComplete
        else:
            fichier = self.TraceMicMacSynthese
        oschdir(self.repTravail)
        if os.path.exists(fichier):
            self.cadreVide()            
            trace=open(fichier,"r",encoding="utf-8")
            try:
                contenu=trace.read()
            except:                     # pour compatibilité ascendante
                trace.close
                trace=open(fichier,"r",encoding="latin-1")
                contenu=trace.read()
            trace.close
            self.listePositions201 = list()
            self.suite201 = -1
            self.ending_index = "1.0"
            self.texte201.insert('end',str(contenu))                  
            self.texte201.update()
            self.texte201.see("1.1")
            self.texte201.focus_set()
        else:
            texte = _("Pas de trace de la trace !")
            self.encadre(texte)
            
    def lectureTraceSynthetiqueMicMac(self):
        self.lectureTraceMicMac(complete=False)

############### Affichages des nuages de points
        
    def afficheApericloud(self):
        retour = self.lanceApericloudMeshlab()
        if retour == -1:
            self.encadre(_("Pas de nuage de points non densifié."))
        if retour == -2:
            self.encadre(_("Programme pour ouvrir les .PLY non trouvéé."))

    def affiche3DNuage(self):
        retour = self.ouvreModele3D()
        if  retour == -1 :
             self.encadre(_("Pas de nuage de points densifié."))                
        if retour == -2 :
            self.encadre(_("Programme pour ouvrir les .PLY non trouvé."))

    def afficheEcart(self):
        if self.ecartXyz==str():
            self.encadre(_("Pas de fichier ecart entre 2 MNT. Abandon"))
            return
        
        if os.path.exists(self.ecartXyz):
                xyz = self.ecartXyz
                self.afficheXYZ(xyz)
        else:
            self.encadre(_("Fichier ecart entre 2 MNT non trouvé. Abandon"))
            return                
                
    def afficheXYZ(self,xyz=str()):
        if xyz==str():
            extensions = ("ecart*.asc","*.xyz")
            message = _("Choisir le fichier x,y,z, à visualiser :")                              
            xyz=tkinter.filedialog.askopenfilename(title=message,
                                                              filetypes=[(_("fichier XYZ"),extensions),(_("Tous"),"*")],
                                                              multiple=False,
                                                            )
            if xyz==str():
                self.encadre(_("Visualisation d'un fichier XYZ abandonnée."))
                return
            
        meshlab = [self.meshlab, xyz]        
        self.lanceCommande(meshlab,
                           info=_("Fichier XYZ %s a visualiser.") % (xyz),
                           attendre=False)

    def paramTolerance(self):
        tolerance = MyDialog(fenetre,_("Tolérance pour le calcul des volumes entre 2 MNT"),
                        basDePage=_("La tolérance est l'écart d'altitude minimum pris en compte dans le calcul du volume")+"\n"+
                        _("Valeur actuelle : %s correspond à %s cm.") % (self.tolerance,str(round(self.tolerance*100,1)))+"\n"+
                        _("Tout écart d'altitude inférieur à %s cm sera considéré comme nul, dans l'épaisseur du trait.")
                             % (str(round(self.tolerance*100,1)))+"\n\n"+
                        _("Cette valeur est enregistrée par le menu Outils/sauvegarder les paramètres par défaut")).saisie
        if tolerance in (False,""):
            self.encadre(_("Abandon utilisateur, tolérance inchangée : %s m")% (self.tolerance))
            return
        if isNumber(tolerance):
            if float(tolerance)<0:
                self.encadre(_("La tolérance doit être positive, Abandon : %s.\nTolérance inchangée : %s m") % (tolerance,self.tolerance))
            else:
                self.tolerance = float(tolerance)
                self.encadre(_("Nouvelle valeur de la tolérance : %s m") % (tolerance))
            return
        self.encadre(_("Valeur de la tolérance non numérique : %s\n Tolérance inchangée : %s m") % (tolerance,self.tolerance))

    def paramArrondi(self):
        arrondi = MyDialog(fenetre,_("Nombre de décimales dans les résultats de calcul des volumes"),
                        basDePage=_("Par défaut les résultat des calculs de volumes sont arrondis avec 2 décimales.")+"\n"+
                        _("L'unité est supposée être le mètre. La précision est donc de 0.01 m soit 1 cm.")+"\n"+                           
                        _("Cette précision est insuffisante pour les petits objets.")+"\n"+
                        _("Un arrondi a 3 décimales, soit 0.001 m, ou 4, soit 0.0001 m, permet d'améliorer cette précision.")+"\n"+ 
                        _("La valeur actuelle du nombre de décmales est : %s.") % (self.arrondi)                          
                        ).saisie
        if arrondi in (False,""):
            self.encadre(_("Abandon utilisateur, valeur inchangée : %s décimales")% (self.arrondi))
            return
        if isNumber(arrondi):
            if float(arrondi)<0:
                self.encadre(_("Le nombre de décimale doit être positif ou nul, Abandon : %s.\nValeur inchangée : %s décimales") % (arrondi,self.arrondi))
            else:
                self.arrondi = int(float(arrondi))
                self.encadre(_("Nouvelle valeur du nombre de décimales : %s ") % (self.arrondi))
            return
        self.encadre(_("Valeur non numérique : %s\n nombre de décimales inchangé : %s") % (arrondi,self.arrondi))
        
    ################################## Le menu PARAMETRAGE : répertoires MicMAc et Meshlab ###########################################################

    def afficheParam(self):
        texte =('\n' + _("Répertoire bin de MicMac : ")+'\n\n'+afficheChemin(self.micMac)+
                '\n------------------------------\n'+
                '\n' + _("Version MicMac :")+'\n\n' + str(self.mercurialMicMac)+
                '\n------------------------------\n'+
                '\n' + _("Outil exiftool :") + '\n\n' + afficheChemin(self.exiftool)+
                '\n------------------------------\n'+
                '\n' + _("Outil convert d\'ImageMagick :") + ' \n\n' + afficheChemin(self.convertMagick)+                
                '\n------------------------------\n'+                
                '\n' + _("Outil pour afficher les .ply :") + '\n\n' + afficheChemin(self.meshlab)+
                '\n------------------------------\n'+
                '\n' + _("Outil pour décompacter les vidéos (ffmpeg):") + "\n\n" + afficheChemin(self.ffmpeg)+                
                '\n------------------------------\n'+
                '\n' + _("Répertoire d'AperoDeDenis :") + "\n\n" + afficheChemin(self.repertoireScript)+
                '\n------------------------------\n'+
                '\n' + _("Répertoire des paramètres :") + "\n\n" + afficheChemin(self.repertoireData)+
                '\n------------------------------\n')       
        self.encadre(texte)

    def repMicmac(self):
        
        self.menageEcran()
        
        #affichage de la valeur actuelle du répertoire de micmpac :
        
        texte=_("Répertoire bin sous MICMAC : ")+afficheChemin(self.micMac)
        self.encadre(texte)               # pour éviter le redémarrage de la fenêtre      
        existe = False
        exiftoolOK = False
        convertOK = False
        ffmpegOK = False
        
        # Choisir le répertoire de MicMac
        
        source=tkinter.filedialog.askdirectory(title=_('Désigner le répertoire bin sous Micmac '),initialdir=self.micMac)
        if len(source)==0:
            texte=_("Abandon, pas de changement.") + "\n" + _("Répertoire bin de Micmac :") + "\n\n"+afficheChemin(self.micMac)
            self.encadre(texte)
            return

        if " " in source:
            texte = _("Le chemin du répertoire bin de micmac ne doit pas comporter le caractère 'espace'.") + "\n"
            texte = _("Renommer le répertoire de MicMac.") + "\n"            
            texte += _("Abandon, pas de changement.") + "\n" + _("Répertoire bin de Micmac :") + "\n\n"+afficheChemin(self.micMac)
            self.encadre(texte)
            return
        
        # mm3d  sous Windows :
        
        if self.systeme=="nt":
            mm3d = os.path.join(source,"mm3d.exe")
            
            if os.path.exists(mm3d):
                self.micMac = source
                self.mm3d = mm3d
                existe = True
            else:
                self.encadre(_("Le répertoire %s ne contient pas le fichier mm3d.exe. Abandon") % (source))
                return

         # chemin pour lire les exifs               
            if self.pasDeExiftool():    
                exiftool = os.path.join(source+"aire-aux","exiftool.exe")   # recherche de l'existence de exiftool sous binaire-aux
                if os.path.exists(exiftool):
                    self.exiftool = exiftool
                    exiftoolOK = True
                else:
                    exiftool = os.path.join(source+"aire-aux\\windows","exiftool.exe") # le répertoire change dans les dernières versions de micmac
                    if os.path.exists(exiftool):
                        self.exiftool = exiftool
                        exiftoolOK = True
            else: exiftoolOK = True

        # chemin pour convertir les formats de photos            
            if self.pasDeConvertMagick():
                convertMagick = os.path.join(source+"aire-aux","convert.exe")
                if os.path.exists(convertMagick):
                    self.convertMagick = convertMagick
                    convertOK = True
                else:
                    convertMagick = os.path.join(source+"aire-aux\\windows","convert.exe")
                    if os.path.exists(convertMagick):
                        self.convertMagick = convertMagick
                        convertOK = True                    
            else: convertOK = True
                
        # Chemin de ffmpeg pour décompacter les vidéo : si existe
            if self.pasDeFfmpeg():
                ffmpeg = os.path.join(source,"ffmpeg.exe")  # vrai dans certaines anciennes versions de micmac
                if os.path.exists(ffmpeg):
                    self.ffmpeg = ffmpeg
                    ffmpgegOK = True
 

        # mm3D sous linux, mas os :
            
        if self.systeme=="posix":
            mm3d = os.path.join(source,"mm3d")
            if os.path.exists(mm3d):
                self.micMac = source
                self.mm3d = mm3d
                existe = True
            else:
                self.encadre(_("Le répertoire %s ne contient pas le fichier mm3d. Abandon") % (source))
                return                

        # DicoCamera : 

        self.CameraXML = os.path.join(os.path.dirname(self.micMac),self.dicoCameraGlobalRelatif)

        # Vérification que mm3D fonctionne :
        
        executable = verifierSiExecutable(self.mm3d)
            
        if executable:                                                          # nouveau répertoire correct
            self.micMac = source
            texte=_("Nouveau répertoire de Micmac :") + "\n\n"+afficheChemin(self.micMac)
            self.sauveParam()
            
        else:
            if existe:
                texte = _("Le programme mm3d est présent mais ne peut s'exécuter.") + "\n" + _("Vérifier si la version est compatible avec le système. :") + "\n"
            else:
                texte = _("Le programme mm3d est absent du répertoire choisi :") + "\n"+source+"\n" + _("Répertoire bin sous MicMac incorrect.") +"\n" + _("Abandon.")

        # C3DC est-il accessible dans cette version de MicMac (la saisie d'un masque 3d est prévue) :

        self.mm3dOK = verifMm3d(self.mm3d)                # Booléen indiquant si la version de MicMac permet la saisie de masque 3D

        # recherche du mercurial de la version MicMac :
        
        self.mercurialMicMac = mercurialMm3d(self.mm3d)
        if self.mercurialMicMac==False:
            self.mercurialMicMac = _("Pas de version identifiée de MicMac")
            
        texte += "\n\n" + _("Version MicMac : ")+"\n\n"+self.mercurialMicMac 
        
        # chemin pour exiftool si sous micmac\bin :

        if exiftoolOK:
            texte = texte + "\n\n" + _("Chemin de exiftool :") + "\n\n"+self.exiftool
        if convertOK:
            texte = texte + "\n\n" + _("Chemin de convert d'image Magick :") + "\n\n" +self.convertMagick
        if ffmpegOK:
            texte = texte + "\n\n" + _("Chemin de ffmpeg :") + "\n\n" +self.ffmpeg           
         
        # Mémorisation du choix :
        
        self.sauveParamMicMac()

        #COmpte rendu :
        
        self.ajoutLigne("\n" + _("Nouvelle version de MicMac : ")+str(self.mercurialMicMac)+"\n")
        self.ecritureTraceMicMac()
        self.encadre(texte)
        
    def repExiftool(self):
        self.menageEcran()
        if self.exiftool=="":
            texte=_("Pas de chemin pour le programme exiftool")
        else:
            texte=_("Programme exiftool :") + "\n"+afficheChemin(self.exiftool)
        self.encadre(texte)         
        
        # Choisir le répertoire de Meshlab ou CLoudCompare :
        _filetypes = [] if sys.platform == 'darwin' else [("exiftool","exiftool*"),(_("Tous"),"*")]
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.exiftool),                                                 
                                                  filetypes=_filetypes,
                                                  multiple=False,
                                                  title = _("Recherche exiftool"))
        if len(source)==0:
            texte=_("Abandon, pas de changement.") + "\n" + _("Fichier exiftool inchangé :") + "\n\n"+afficheChemin(self.exiftool)
            self.encadre(texte)
            return
        self.exiftool=''.join(source)
        self.sauveParam()
        texte="\n" + _("Programme exiftool :") + "\n\n" +afficheChemin(self.exiftool)
        self.encadre(texte)

    def repConvert(self):
        self.menageEcran()
        if self.convertMagick=="":
            texte=_("Pas de chemin pour le programme convert d'ImageMagick")
        else:
            texte=_("Programme convert :") + "\n"+afficheChemin(self.convertMagick)
        self.encadre(texte)         
        
        # Choisir le répertoire de convert :
        _filetypes = [] if sys.platform == 'darwin' else [("convert",("convert*","avconv*")),(_("Tous"),"*")]        
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.exiftool),                                                 
                                                  filetypes=_filetypes,
                                                  multiple=False,
                                                  title = _("Recherche convert"))
        if len(source)==0:
            texte=_("Abandon, pas de changement.") + "\n" + _("Fichier convert inchangé :") + "\n\n"+afficheChemin(self.convertMagick)
            self.encadre(texte)
            return
        self.convertMagick=''.join(source)
        self.sauveParam()
        texte="\n" + _("Programme convert :") + "\n\n"+afficheChemin(self.convertMagick)
        self.encadre(texte)
        
    def repMeslab(self):
        self.menageEcran()
        if self.meshlab=="":
            texte=_("Pas de chemin pour le programme ouvrant les .PLY")
        else:
            texte=_("Programme ouvrant les .PLY :") + "\n"+afficheChemin(self.meshlab)
        self.encadre(texte)                       
        # Choisir le répertoire de Meshlab ou CLoudCompare
        _filetypes = [] if sys.platform == 'darwin' else [(_("meshlab ou CloudCompare"),("meshlab*","Cloud*")),(_("Tous"),"*")]                
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.meshlab),                                                 
                                                  filetypes=_filetypes,
                                                  multiple=False,
                                                  title = _("Recherche fichier Meshlab sous VCG, ou CloudCompare"))
        if len(source)==0:
            texte=_("Abandon, pas de changement.") + "\n" + _("Fichier Meshlab ou Cloud Compare :") + "\n\n"+afficheChemin(self.meshlab)
            self.encadre(texte)
            return
        self.meshlab = source
        self.sauveParam()
        texte="\n" + _("Programme ouvrant les .PLY :") + "\n\n"+afficheChemin(self.meshlab)
        self.encadre(texte)

    def repFfmpeg(self):
        self.menageEcran()
        if self.ffmpeg=="":
            texte=_("Pas de chemin pour le programme Ffmpeg")
        else:
            texte=_("Programme ffmpeg :") + "\n"+afficheChemin(self.ffmpeg)
        self.encadre(texte)         
        
        # Choisir le répertoire de ffmpeg:
        _filetypes = [] if sys.platform == 'darwin' else [("ffmpeg","ffmpeg*"),(_("Tous"),"*")]            
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.ffmpeg),                                                 
                                                  filetypes=_filetypes,
                                                  multiple=False,
                                                  title = _("Recherche ffmpeg"))
        if len(source)==0:
            texte=_("Abandon, pas de changement.") + "\n" + _("Fichier ffmpeg inchangé :") + "\n\n"+afficheChemin(self.ffmpeg)
            self.encadre(texte)
            return
        self.ffmpeg=''.join(source)
        self.sauveParam()
        texte="\n" + _("Programme ffmpeg :") + "\n\n"+afficheChemin(self.ffmpeg)
        self.encadre(texte)

    def modifierTacky(self):
        self.tacky = not self.tacky
        if self.tacky:
            self.encadre(_("Tacky message au lancement activé"))
        else:
            self.encadre(_("Tacky message au lancement désactivé"))

    def modifierGitHub(self):
        self.avertirNouvelleVersion = not self.avertirNouvelleVersion
        if self.avertirNouvelleVersion:
            self.encadre(_("Controle de la présence d'une nouvelle version sur GitHub activé"))
        else:
            self.encadre(_("Controle de la présence d'une nouvelle version sur GitHub désactivé"))
            
    def modifierLangue(self):
        self.menageEcran()
        if not os.path.isdir(repertoire_langue):
            self.encadre(_("Version bilingue non installée."))
            return
        self.encadre(_("Sélectionnez la langue à utiliser. L'application sera redémarrée."))
        self.frame = tkinter.Frame(fenetre)
        frameListe = tkinter.Frame(self.frame)
        frameBoutton = tkinter.Frame(self.frame)
        self.choixLangue = tkinter.Listbox(frameListe)
        self.frame.pack()
        frameListe.pack(side = tkinter.TOP)
        frameBoutton.pack(side = tkinter.BOTTOM)
        valider = tkinter.Button(frameBoutton, text = _("Appliquer"), command = self.selectionLangue)
        self.choixLangue.pack(side = tkinter.LEFT, fill = tkinter.Y)
        valider.pack()
        self.choixLangue.insert(1, ("Français/French"))
        self.choixLangue.insert(2, ("Anglais/English"))
        self.choixLangue.insert(3, ("Allemand/Deutsch"))
        self.choixLangue.insert(4, ("Espagnol/Español"))
        self.choixLangue.insert(5, ("Italien/Italiano"))
        self.choixLangue.insert(6, ("Chinois/中文"))
        self.choixLangue.insert(7, ("Arabe/عربى"))
        
    def selectionLangue(self):
        try:
            nouvelleLangue = self.choixLangue.get(self.choixLangue.curselection())            
            global langue
            if(nouvelleLangue == ("Français/French")):
                langue = 'fr'
            elif nouvelleLangue == ("Anglais/English"):
                langue = 'en'
            elif nouvelleLangue == ("Allemand/Deutsch"):
                langue = 'de'
            elif nouvelleLangue == ("Espagnol/Español"):
                langue = 'es'
            elif nouvelleLangue == ("Italien/Italiano"):
                langue = 'it'
            elif nouvelleLangue == ("Chinois/中文"):
                langue = 'zh'
            elif nouvelleLangue == ("Arabe/عربى"):
                langue = 'ar'                
        except: pass
        try:
            print("selection repertoire_langue=",repertoire_langue," langue=",langue)
            traduction = gettext.translation('AperoDeDenis', localedir = repertoire_langue, languages=[langue])
            traduction.install()
        except Exception as e:
            message = "Version bilingue non installée. Revoir la procédure d'installation.\nChoisir KO pour quitter l'application"
            message += "\nErreur : "+str(e)
            message == "\nlocaledir = "+repertoire_langue
            if self.troisBoutons(titre="traduction absente",question=message,b1='OK',b2='KO',b3=None,b4=None)==1:
                self.quitter()
        try: fenetre.destroy()
        except: pass

    ################################## LE MENU MICMAC : Choisir les photos, les options, le traitement ##########################################################


    def lesPhotos(self):                                # Choisir des images dans un répertoire

        if not os.path.isdir(self.micMac):
                self.encadre(_("Avant de choisir les photos associer le répertoire bin de micmac (Menu Paramétrage\\associer le répertoire bin de MicMac)."))
                return
            
        if not os.path.isfile(self.exiftool):
                self.encadre(_("Avant de choisir les photos associer le chemin du programme exiftool (Menu trage\\Associer exiftool)."))
                return

        self.fermerVisuPhoto()                          #  s'il y a une visualisation en cours des photos ou du masque on la ferme             
        self.menageEcran()
        repIni = self.repertoireDesPhotos if os.path.isdir(self.repertoireDesPhotos) else ""
           
        # Nouvelles photos sur le chantier en cours ???
        messageReinit = ""
        if self.etatDuChantier>2:                       # 1 = avec photo ; 2 = enregistré, plus = traitement effectué
            if self.troisBoutons(_("Nouvelles photos pour le meme chantier"),
                                 _("Choisir de nouvelles photos réinitialisera le chantier." ) + "\n"+
                                _("Les traces et l'arborescence des calculs seront effacées.") + "\n"+
                                _("Le nuages de points obtenus sont conservés.") + "\n"+                                 
                                _("Les options compatibles avec les nouvelles photos seront conservées.") + "\n",
                                _("Abandon"),
                                _("Réinitialiser le chantier")) == 0:
                self.encadre(_("Abandon, le chantier n'est pas modifié options et fichiers ply conservés, traces et calculs antérieurs supprimés"))
                return
            else:
                # self.initialiseValeursParDefaut()       # valeurs par défaut pour un nouveau chantier (utile si pas encore de chantier)
                messageReinit ="\n"+_("Nouvelles photos choisies.")+"\n"
                
        photos=tkinter.filedialog.askopenfilename(title=_('Choisir des photos'),
                                                  initialdir=repIni,
                                                  filetypes=[(_("Photos"),("*.JPG","*.jpg","*.BMP","*.bmp","*.TIF","*.tif")),(_("Tous"),"*")],
                                                  multiple=True)
        
        if len(photos)==0:
            self.restaureParamChantier(self.fichierParamChantierEnCours) # on remet le chantier 
            self.sauveParam()
            self.encadre(_("Abandon, aucune sélection de fichier image,") + "\n" + _("le répertoire et les photos restent inchangés.") + "\n")
            return 

        if self.nombreDExtensionDifferentes(photos)==0:
            self.encadre(_("Aucune extension acceptable pour des images. Abandon."))
            return
        
        if self.nombreDExtensionDifferentes(photos)>1:
            self.encadre(_("Plusieurs extensions différentes :") + "\n"+
                         ",".join(self.lesExtensions)+".\n" +
                         _("Impossible dans cette version. Abandon."))
            return

        if self.lesExtensions[0].upper() not in ".JPG.JPEG":
            
            if self.troisBoutons(_("Info : format des photos"),
                                 _("La version actuelle ne traite que les photos au format JPG,") +
                                 "\n\n" + _("or le format des photos est : ")+
                                 self.lesExtensions[0]+".\n\n" +
                                 _("les photos vont être converties au format JPG."),
                                 b1=_('Convertir en JPG'),
                                 b2=_('Abandonner'))==1:
                return
            if verifierSiExecutable(self.convertMagick)==False:
                self.encadre(_("Désigner l'outil de conversation 'convert' d'ImageMagick") + "\n" + _("(Menu Paramétrage)"))
                return
            if  self.pasDeConvertMagick():return

            self.conversionJPG(photos)
            photos = [os.path.splitext(e)[0]+".JPG" for e in photos]
           
        if self.nombreDExtensionDifferentes(photos)==0:
            self.encadre(_("Aucune extension acceptable pour des images. Abandon."))
            return
                
        # Nouvelle sélection valide : du ménage :
        
        self.lesTagsExif = dict()                           # réinitialise la mémo des exifs          
        self.supOriNavBrut()                                # suppression des anciennes données de navigation drone
        self.repereChoisi = self.repereADeterminer          # raz le repère choisi : (mis à "repere supprimé par supOriNavBrut)
        self.extensionChoisie = self.lesExtensions[0]       # l'extension est OK

        self.encadre(_("Copie des photos en cours...\n Patience\n")) #  pour éviter le redémarage

        # crée le repertoire de travail, copie les photos avec l'extension choisie et renvoit le nombre de fichiers photos "aceptables",
        # met à 1 l'état du chantier crée self.photosAvecChemin et self.photosSansChemin
        # ATTENTION : Supprime l'arborescence et certains résultats.
        
        retourExtraire = self.extrairePhotoEtCopier(photos) # réinitialise la trace (errare humanum est)
        self.ajoutLigne(messageReinit)

        if retourExtraire.__class__()=='':              # si le retour est un texte alors erreur, probablement création du répertoire impossible
            self.encadre (_("Impossible de créer le répertoire de travail.") + "\n" +
                          _("Vérifier les droits en écriture sous le répertoire des photos") +
                          "\n"+str(retourExtraire))
            return 
        if retourExtraire==0:                           # extraction et positionne  self.repertoireDesPhotos, et les listes de photos avec et sanschemin (photosAvecChemin et photosSansChemin)
            self.encadre (_("Aucun JPG, PNG, BMP, TIF, ou GIF  sélectionné,") + "\n" +
                          _("le répertoire et les photos restent inchangés.") + "\n")
            return

        self.etatSauvegarde="*"                         # chantier modifié

        # Controle des photos :
        self.encadrePlus("\n"+_("Controle des photos (dimensions et focales)... Patience"))
        message = str()
        
        ######### définir le dictionnnaire de tous les tags utiles :
        
        self.tousLesTagsUtiles()
        
        # controles :        
        self.controlePhotos()                           # Compte le nombre de focales et les dimensions des photos
        
        if self.nbFocales==0:
            message+=_('Les focales sont absentes des exif.') + "\n" + _('Mettez à jour les exifs avant de lancer MicMac.') + '\n'+\
                            _("Utiliser le menu Outils/Modifier l'exif des photos.") + "\n\n"
        if self.nbFocales>1:
                message += _("Attention : Les focales des photos ou ne sont pas toutes identiques.") + "\n\n"                
        if self.dimensionsOK==False:
            message += _("Attention : les dimensions des photos ne sont pas toutes identiques.") + "\n"+\
                      "\n" + _("Le traitement par MicMac ne sera peut-être pas possible.") + "\n\n"
            
        # conséquences du choix de nouvelles photos sur un ancien chantier : on supprime tous le répertoire de travail ancien
        # on conserve les options
        #  - s'il y a une visualisation en cours des photos ou du masque on la ferme

        self.reinitialiseMaitreEtMasqueDisparus()           # fait un grand ménage
        self.photosPourCalibrationIntrinseque = [e for e in self.photosPourCalibrationIntrinseque if e in photos]
        
        # Adaption des options au lot de photos choisi :
        # l'échelle de Tapioca est dimensionnée par défaut à 60% de la dimension maxi des photos :
        
        echelle = int(round(max(self.dimensionsDesPhotos[0][1])*6/10,-2))
        self.echelle1.set(echelle)
        self.echelle3.set(echelle)       
        self.echelle4.set(echelle)

        # S'il y a des données GPS dans les exifs on crée une orientation provisoire "Ori-nav-Brut" (qui est prioritaire sur la mise à l'échelle)

        self.GpsExif()

        # sauvegarde = recréation du fichier param.sav qui a été supprimé

        self.enregistreChantier()

        # affiche etat avec message :

        self.afficheEtat(message)        

    # extraire les photos dans le résultat de l'opendialogfilename (celui-ci dépend de l'OS et du nombre 0,1 ou plus de fichier choisis) :
    # puis création du chantier (si impossible : erreur !


    ################################## COPIER LES FICHIERS DANS LE REPERTOIRE DE TRAVAIL ###########################################################       
    ################################## ATTENTION : FAIT UN GRAND MENAGE : supprime toute l'arborescence de travail et des fichiers dans le chantier dont param.sav ###############
    # quelques fichiers/répertoires sont cependant sauvegardés : ce sont des intrants, pas des résultats
    
    def extrairePhotoEtCopier(self,photos): # création repertoire du chantier,  copie les photos OK, chdir. retour : nombre de photos ou message d'erreur
                                            #  photosAvecChemin photosSansChemin
                                            #attention : self.extensionChoisie doit être positionné

        liste=[x for x in photos if x[-3:].upper() in 'JPGJPEGPNGRAWBMPTIFTIFFGIF']        # on restreint aux seul format d'images accepté : JPG, PNG, BMP, TIF, RAW, GIF 
        if len(liste)==0: return 0
        
        # Quel répertoire pour le chantier ?
        retour = self.quelChantier(liste[0])
        
        if retour!=None:
                return retour               # y a un pb
            
        # copie des photos sous le répertoire de travail : (attention, il peut y en avoir d'autres,
        # qui seront supprimées au lancement de Micmac, mais pas de la qualité)

        liste.sort()
        self.photosAvecChemin = list(liste)                                 # les photos avec les chemins initiaux, triées alphabétique 
        listeCopie=list()                                                   # liste des fichiers copiés, vide
        try:
            self.extensionChoisie = self.extensionChoisie.upper()
            for f in self.photosAvecChemin:                                 # self.photosAvecChemin est la  liste des photos nettoyées à copier
                self.encadrePlus("...")
                if self.extensionChoisie in f.upper():                      # ON NE COPIE QUE L'EXTENSION CHOISIE, en majuscule
                    dest=os.path.join(self.repTravail,os.path.basename(f).upper().replace(" ","_")) # en majuscule et sans blanc : mm3d plante !
                    if os.path.exists(dest):                                # si déjà présent
                        supprimeFichier(dest)
                    shutil.copy(f,dest)                                     # copie du fichier sous le répertoire de travail                            
                    ajout(listeCopie,dest)                                  # liste des fichiers à traiter
        except Exception as e:
            texte=  _("erreur lors de la copie du fichier") + "\n" + f + "\n" + _("dans le répertoire ") + "\n" + self.repTravail + "\n" + _("libellé de l\'erreur :") + "\n" + str(e) + "\n" + _("Causes possibles : manque d\'espace disque ou droits insuffisants.")
            return texte
        self.photosAvecChemin =  list(listeCopie)                                   # on oublie les photos initiales
        self.photosSansChemin = list([os.path.basename(x) for x in listeCopie]) # liste des noms de photos copiès, sans le chemin.
        # on conserve les options déjà saisies, mais pas les résultats de traitement qui n'ont plus de sens
        # suppression de tous sous le répertoire actuel : sauf photos sélectionnées et paramètres saisis
        aConserver = list(self.photosSansChemin)
        aConserver += [e for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".xml"] # garde les xml (paramètres)
        aConserver += [e for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".exp"] # garde les exports
        aConserver += [e for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".ply"] # garde les ply
        aConserver += [e for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".txt"] # garde les traces          
        aConserver.append(self.monImage_PlanTif)
        aConserver += self.listeDesMasques
        supprimeArborescenceSauf(self.repTravail,aConserver)     
        oschdir(self.repTravail)
        self.etatDuChantier = 1                                 # les photos sont choisies, le répertoire de travail est créé        
    # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
    # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
    # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
    # [2] = 'original' ou "importé" ou "ajouté" 
        # définit les fichiers trace vides, débuter la trace à vide (tout nouveau choix de photos efface la trace précédente
        self.typeDuChantier =   ['photos','initial','original']
        self.definirFichiersTrace()                             # affecte leur noms auc fichiers trace, existant ou pas, sous le répertoire de travail
        self.initialisationFichiersTrace()                      # Efface les anciens et initialisation de nouveaux fichiers trace
        return len(listeCopie)                                  # on retourne le nombre de photos

    ################# controler les photos dans leur ensemble : même focale, mêmes dimensions, présence d'un exif avec focale :
    @decorateTry       
    def controlePhotos(self):   #[liste = self.photosSansChemin] Vérification globale des focales et des dimensions. en retour nbFocales et dimensionsOk
        # les dimensions :        
        self.dimensionsDesPhotos = [(x,Image.open(x).size) for x in self.photosSansChemin]  # si OK : x = self.dimensionsDesPhotos[0][0] et y=self.densionsDesPhotos[0][1]
        self.dimensionsOK = set([y for (x,y) in self.dimensionsDesPhotos]).__len__()==1     # vrai si une seule taille        
        # le nombre de focales :
        touteLesFocales = [(x,self.tagExif(tag="FocalLength",photo=x)) for x in self.photosSansChemin]
        lesFocales = set([y for (x,y) in touteLesFocales if y!='']) # les focales parmi les couples (photo, focale)        
        self.nbFocales = lesFocales.__len__()
        
    def controleCoherenceFichiers(self):    # retourne false si incohérent et self.jpgAjout et jpgRetrait
        # Controle que toutes les photos présentes sous le répertoires sont bien enregistrées dans le chantier et réciproquement
        tousLesJpg = glob.glob(os.path.join(self.repTravail,"*.JPG"))
        self.jpgAjout = [e for e in tousLesJpg if e not in self.photosAvecChemin and not os.path.isdir(e)]
        self.jpgAjoutVrai = [os.path.basename(e) for e in self.jpgAjout if os.path.basename(e) not in self.photosCalibrationSansChemin]
        self.jpgRetrait = [os.path.basename(e) for e in self.photosAvecChemin if e not in tousLesJpg]  # et les photos de calibration ??
        if self.jpgAjout.__len__()+self.jpgRetrait.__len__():
            return False
        return True
     
    ################# définir le répertoire de travail, le créer :
    
    def quelChantier(self,unePhoto):                            # on a une photo ou une vidéo : quel répertoire de travail et quel chantier ?

        self.chantier = os.path.basename(self.repTravail)       #   par défaut on suppose que le répertoire existe déjà : on ne change rien

        # Le répertoire de unePhoto est-il le répertoire des photos : si oui on ne change pas le répertoire de travail, sinon nouveau $repTravail et nouveau chantier
        
        oldRepertoireDesphotos =  self.repertoireDesPhotos
        
        self.repertoireDesPhotos = os.path.normcase(os.path.dirname(unePhoto))              # si positif alors on affecte le repertoire (string)

        # création du répertoire du chantier si nouveau chantier
        # état du chantier : 1 = créé, fixé ; si 0 : alors il faut créer un nouveau chantier
        if self.etatDuChantier==0 or oldRepertoireDesphotos!=self.repertoireDesPhotos:      # nouveau répertoire si pas de photos ou changement de répertoire                                                              # si pas encore de nom pour le chantier on lui en donne un !
            return self.creationNouveauRepertoireTravail()                                  # si pas de changement de répertoire des photos alors pas de création

    def creationNouveauRepertoireTravail(self):       
        # Numéro du chantier : pour indicer le numéro du répertoire de travail : un nouveau est créé à chaque éxécution
        self.restaureParamMicMac()
        try: self.indiceTravail         +=   1                          # on incrémente s'il existe
        except: self.indiceTravail      =   1                           # sinon met à 1 sinon

        self.repTravail = os.path.normcase(os.path.normpath(os.path.join(self.repertoireDesPhotos,'MicMac_'+str(self.indiceTravail))))
        while os.path.exists(self.repTravail):                                                      # détermine le nom du répertoire de travail (chantier)
            self.indiceTravail+=1                                                                   # numéro particulier au répertoire de travail créé
            self.repTravail = os.path.normcase(os.path.normpath(os.path.join(self.repertoireDesPhotos,'MicMac_'+str(self.indiceTravail)))) # répertoire différent à chaque éxécution (N° séquentiel)
        try: os.mkdir(self.repTravail)                                                              # création répertoire du chantier
        except Exception as e : return _("Impossible de créer le répertoire de travail : erreur = ") + "\n"+str(e)
        self.chantier = os.path.basename(self.repTravail)                                           # nom du chantier, puis état du chantier : 1 = créé, fixé
        self.ajoutChantier()                                        # on ajoute le répertoire créé dans la liste des répertoires

    ################################## LE SOUS MENU OPTIONS : TAPIOCA, TAPAS,APERICLOUD, MALT, C3DC : accès par onglets ###########################################################
    # les onglets permettent de modifier les options localement.
    # si l'utilisateur valide alors les options modifiées sont controlées et si OK elles sont sauvegardées
    # si l'utilisateur abandonne alors il y a restauration des options à partir du fichier de sauvegarde
    # anormal : chantier planté lors de la dernière éxécution de tapioca/Tapas : on propose le déblocage mais on sort dans tous les cas

    def optionsOnglet(self):
    # EtatDuChantier :
    # 0 : pas encore de photos
    # 1 : il y a des photos choisies
    # 2 : des photos, enregistré                              
    # 3 en cours d'exécution de Tapioca/Tapas, a sans doute planté pendant, ou erreur photo calibration
    # 35 Chantier arrêté aprés tapioca, points homoloques conservés
    # 4 arrêt après tapas,
    # 5 terminé après malt ou c3dc,
    # 6 terminé, redevenu modifiable (??)
    # 7 : la densification a échoué

        if self.etatDuChantier==0:
            self.encadre(_("Choisir les photos avant de définir les options"))
            return
    
        if self.etatDuChantier==3:	# En principe ne doit pas arriver : plantage en cours de tapas ou Tapioca, ou erreur photo calibration
            retour = self.troisBoutons(  titre=_("Le chantier %s a été interrompu lors de Tapioca/Tapas.") % (self.chantier),
                                         question=_("Le chantier est interrompu.") + "\n" + _("Vous pouvez le débloquer,")+
                                         _( "ce qui permettra de modifier les options et de le relancer.") + "\n",
                                         b1=_('Débloquer le chantier- effacer les points homologues'),
                                         b2=_('Débloquer le chantier- conserver les points homologues'),
                                         b3=_('Abandon'))
            if retour==-1 or retour==2:                         # 2 ou -1 : abandon ou fermeture de la fenêtre par la croix
                return
            if retour==0:
                self.nettoyerChantier()                          # etat = 2 :  chantier est noté comme de nouveau modifiable, les points homologues sont supprimés
                self.afficheEtat(_("Chantier %s de nouveau modifiable, paramètrable et exécutable pour la recherche des points homologues.") % (self.chantier))                

            if retour==1:
                self.nettoyerChantierApresTapioca()             # etat = 35 le chantier est noté comme de nouveau modifiable, les points homologues sont conservés
                self.afficheEtat(_("Chantier %s de nouveau modifiable, paramètrable et exécutable à partir de l'orientation.") % (self.chantier))                


    # Chantier arrété après tapas : l'utilisateur a pu modifier les options et veut continuer ou reprendre au début suivant les résultats
    # poursuite du traitement ou arrêt suivant demande utilisateur

            
    # Chantier terminé, l'utilisateur peur décider de le débloquer en conservant les résultats de tapas ou supprimer tous les résultats
        toutesOptions = True    
        if self.etatDuChantier==5:		                # Chantier terminé

            retour = self.troisBoutons(  titre=_('Le chantier %s est terminé.') % {self.chantier},
                                         question=_("Le chantier est terminé après ")+self.choixDensification.get()+".\n"+
                                         _("Vous pouvez :") + "\n "+
                                         _("- Modifier les options 'points homologues' et 'orientation' : supprime les traitements effectués") + "\n "+
                                         _("- Conserver les points homologues et l'orientation pour relancer la densification") + "\n "+
                                         _("- Ne rien faire.") + "\n",                                    
                                         b1=_("Modifier les options des points homologues et d'orientation"),
                                         b2=_('Modifier les options de la densification'),
                                         b3=_('Ne rien faire'),)
            if retour in (-1,2):                                # -1 : fermeture fenêtre ou 2 : b3 ne rien fire
                self.afficheEtat()
                return
            if retour==0:                                       # 1 : on nettoie, on passe à l'état 2  (avec photos, enregistr(b1))
                self.nettoyerChantierApresTapioca()             # l'etatDuChantier passe à 35 ! points homologues conservés
            if retour==1:                                       # modifier les options de malt C3DC et points GCP      (b2))
                self.etatDuChantier = 4
                toutesOptions = False

        # L'état du chantier permet de choisir des options :

        # sauvegarde des valeurs modifiables :

        self.sauveParamChantier()
        self.menageEcran()
  
        #if self.etatDuChantier in (0,1,2,7,35):                     # sinon self.etatDuChantier vaut 4 et on va direct à Malt ou C3DC
        if toutesOptions:                                                    # modif du 5 juin 2020 : on affiche touj 
            self.onglets.add(self.item400)                          # tapioca
            self.onglets.add(self.item500)                          # tapas
            self.onglets.add(self.item950)                          # Calibration            
            self.optionsTapioca()                                   # les frames à afficher ne sont pas "fixes"
            self.item570.pack(pady=10)                              # la frame fixe de tapas pour choix de calibration
            self.item526.config(text=_("Nombre de photos choisies : ")+str(self.photosPourCalibrationIntrinseque.__len__()))
            self.item720.pack(pady=10)                              # Malt zoom final
            self.item725.pack(pady=10)                              # Malt nuage ou maillage 
            self.optionsMalt()                                      # La frame Image Maitre à afficher n'est pas "fixe"           
            if os.path.isdir("Ori-nav-Brut"):
                self.item992.pack()
            else:
                self.item992.forget()                                            
            selection = self.item400                                # onglet sélectionné par défaut
            self.visuOptionsCalibration()                           # les frame de calibration chantier ou photo

        else:                                                       # masque les options de Tapioca et Tapas
            
            self.onglets.hide(self.item400)                         # tapioca
            self.onglets.hide(self.item500)                         # tapas
            self.item720.pack(pady=10)                              # Malt zoom
            self.item725.pack(pady=10)                              # Malt rendu nuage ou maillage
            self.optionsMalt()                                      # La frame Image Maitre à afficher n'est pas "fixe"
            selection = self.item600
            
        # on affiche les frames de la calibration :
        
        self.item960.pack(padx=5,pady=10,ipady=2,ipadx=15)      # Calibration de 960 à 980
        self.item965.pack()                                     # calibration suite
        self.item970.pack(padx=5,pady=10,ipady=2,ipadx=15)      # calibration suite
        self.item975.pack()                                     # calibration suite
        self.item980.pack(padx=5,pady=10,ipady=2,ipadx=15)      # calibration suite
        self.item990.pack()                                     # calibration suite

        # Onglet Densification :
        
        self.optionsDensification()                                 # onglet Densification variable suivant Malt ou C3DC          
    
        if not self.mm3dOK:                                         # ne pas proposer C3DC si MicMac ne l'accepte pas
            self.item804.configure(text= _("La version de Micmac installée ne propose pas le module C3DC. Choisir MALT."),foreground='red',style="C.TButton")            
        else:                                                       # Si l'onglet existe on met à jour les messages :
            oschdir(self.repTravail)        
            if os.path.exists("AperiCloud.ply")==False:
                self.item804.configure(text= _("Pas de nuage pour construire un masque") + "\n" +
                                       _("Calculer un nuage de points, non dense, pour définir un masque 3D."),foreground='red',style="C.TButton")
                self.item801.configure(state = "disable")
            else:
                self.item801.configure(state = "normal")
                if self.existeMasque3D():
                    self.item804.configure(text = _("Masque 3D créé"),foreground='red')
                else:
                    self.item804.configure(text = _("Pas de masque 3D"),foreground='black')            
            

        # met à jour les infos sur les maîtresses et les masques
        
        self.miseAJourItem701_703()
        self.masqueProvisoire = str()   # utile pour tracemasque
        
        # dernier onglet (qui se régénére, forcément le dernier)

        self.optionsReperes()                                       # points GCP, en nombre variable # points de repères calés dans la scène

        self.onglets.pack(fill='none', padx=2, pady=0)              # on active la boite à onglet
        self.item450.pack()                                         # et les 2 boutons en bas : 451 valider et 452 annuler
        self.onglets.select(selection)                              # onglet sélectionné par défaut
        self.optionsMicMacActivees = True                           # flag : les onglets sont disponibles, on écrira dans la trace complete l'état du chantier      
        fenetre.wait_window(self.onglets)                           # boucle d'attente : la fenêtre pricncipale attend la fin de l'onglet
        
    def finOptionsOK(self,affiche=True):                                         # l'utilisateur a valider l'ensemble des options
        self.ajoutTraceComplete("\n"+heure()+" "+_("Les options sont validées par l'utilisateur"))
        self.onglets.pack_forget()      # on ferme la boite à onglets             
        texte = str()

        # on enregistre les options de calibration et de GCP 
        
        self.finCalibrationGPSOK()                                      # mise à jour des coordonnées des Points GPS
        self.finRepereOK()                                              # mise à jour des options de repérage (axe Ox, plan horizontal, distance

        # Controle puis Sauvegarde des nouvelles info :

        retour = self.controleOptions()
        
        self.etatSauvegarde="*"         # chantier modifié  ="*"#Pour indiquer que le chantier a été modifié, sans être sauvegardé sous le répertoire du chantier
        self.sauveParam()               # si la sauvegarde marche le chantier est mis  a "non modifié"

        if retour!=True:
            texte = "\n" + _("Option incorrecte :") + "\n"+str(retour)
            self.encadreEtTrace(texte)
            return
        if affiche:
            self.afficheEtat(texte)
        
    def finCalibrationGPSOK(self):                                  # crée le fichier xml qui va bien avec les données saisies
        supprimeFichier(self.dicoAppuis)
        supprimeFichier(self.mesureAppuis)
        nbPointsIncorrect = int()
        listePointsOK = list()                                      # les points actifs avec toutes les infos
        self.actualiseListePointsGPS()                              # met a jour proprement la liste des 6-tuples (nom,x,y,z,actif,identifiantgps)
        if self.dicoPointsGPSEnPlace.__len__()==0:                  # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
            return False
        if self.controlePointsGPS()==False:                         # retour False si problème !
            self.encadre(_("Points GCP non conformes. Nom est absent ou en double. Vérifiez."))
            return False
        
        oschdir(self.repTravail)
        with open(self.dicoAppuis, 'w', encoding='utf-8') as infile: # écriture de la description de chaque point GCP
            infile.write(self.dicoAppuisDebut)
            for Nom,X,Y,Z,actif,ident,incertitude in self.listePointsGPS:   # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
                if actif and isNumber(X) and isNumber(Y) and isNumber(Z) and Nom and re.match("\d+\s+\d+\s+\d+\s*$",incertitude):        # si actif et tous les éléments présent    
                    point=self.dicoAppuis1Point.replace(_("Nom"),Nom)
                    point=point.replace("X",X)
                    point=point.replace("Y",Y)
                    point=point.replace("Z",Z)
                    point=point.replace("10 10 10",incertitude)
                    infile.write(point)
                    listePointsOK.append(Nom)
                else:
                    nbPointsIncorrect += 1
            infile.write(self.dicoAppuisFin)

        with open(self.mesureAppuis, 'w', encoding='utf-8') as infile:             
                                                                        # modification des xml 
                infile.write(self.mesureAppuisDebut)
                key = ""
                listeDico=list(self.dicoPointsGPSEnPlace.items())       # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
                listeDico.sort(key= lambda e:  e[0][1])
                listeDico = [e for e in listeDico if e[0][0] in listePointsOK] # seuls les points actifs et complets
                for cle,p in listeDico:
                    if key!=cle[1]:
                        if key!="":
                            infile.write(self.mesureAppuisFinPhoto)                    
                        key = cle[1]   
                        photo = self.mesureAppuisDebutPhoto.replace(_("NomPhoto"),os.path.basename(cle[1]))
                        infile.write(photo)
                        point = self.mesureAppuis1Point.replace(_("NomPoint"),cle[0])
                        point = point.replace("X",self.dicoPointsGPSEnPlace[cle][0].__str__())
                        point = point.replace("Y",self.dicoPointsGPSEnPlace[cle][1].__str__())
                        if  cle[0] not in self.pointsPlacesUneFois:   # on n'écrit pas le point s'il  n'est présent que sur une seule photo
                            infile.write(point)                   
                    else:
                        point = self.mesureAppuis1Point.replace(_("NomPoint"),cle[0])
                        point = point.replace("X",self.dicoPointsGPSEnPlace[cle][0].__str__())
                        point = point.replace("Y",self.dicoPointsGPSEnPlace[cle][1].__str__())
                        if  cle[0] not in self.pointsPlacesUneFois:   # on n'écrit pas le point s'il  n'est présent que sur une seule photo
                            infile.write(point)
                infile.write(self.mesureAppuisFinPhoto)
                infile.write(self.mesureAppuisFin)
        return True
    
    def controlePointsGPS(self):            # controle pour affiche etat et afficher tous les points : informer de la situation :
                                            # le message self.etatPointsGPS sera affiché dans l'état du chantier
                                            # finCalibrationGPSOK doit avoir été éxécuté avant
        self.etatPointsGPS = str()
        retour = True
       
        if self.repTravail==self.repertoireData:    # si pas de chantier, pas de problème mais retour False :  pas de calibration
            return False

        if self.nbPointsGCPActifs()==0:
            return False
        
        # listePointsGPS : liste de (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant, incertitude)
        listePointsOK = list()
        listePointsKO = list()
        
        # ICI : controle que les x,y,z et incertitudes sont bien des valeurs numériques correctes, que le point n'est pas supprimé, qu'il a un nom

        for Nom,X,Y,Z,actif,ident,incertitude in self.listePointsGPS:   # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
            if actif and isNumber(X) and isNumber(Y) and isNumber(Z) and Nom and re.match("\d+\s+\d+\s+\d+\s*$",incertitude): # si actif et tous les éléments présent        
                listePointsOK.append(Nom)
            else:
                listePointsKO.append(Nom)

        
        if not listePointsOK:
            self.etatPointsGPS += ("\n" + _("%s points GCP. Aucun n'est correctement défini.")) % (self.nbPointsGCPActifs())
            return False
        else:
            listeDico =list(self.dicoPointsGPSEnPlace.items())       # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
            listeDico = [e for e in listeDico if e[0][0] in listePointsOK] # seuls les points actifs et complets

            
            # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y            
            self.etatPointsGPS += ("\n" + _("%s points GCP placés OK") % (str(len(listeDico))) + "\n"  +       
                                  _("pour %s points GCP définis") % (str(len(listePointsOK)))) + "\n" 
            if len(listePointsOK)<3:
                 self.etatPointsGPS += _("Attention : il faut au moins 3 points pour qu'ils soient pris en compte.") + "\n"
                 retour = False
            # sur le modèle pythonique l'élément le plus représenté dans une liste l : x=sorted(set(l),key=l.count)[-1]
            # ou pour avoir toute l'info [(valeur,nombre),...] : [(e,a.count(e)) for e in a]
            # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
            # ce bout de code est dupliqué dans controlePointsGPS et actualiseListePointsGPS
            
            listePointsPlaces=[e[0] for e in self.dicoPointsGPSEnPlace if e[0] in listePointsOK] 
            pointsPlaces = [(e,listePointsPlaces.count(e)) for e in listePointsPlaces]
            self.pointsPlacesUneFois = [f[0] for f,g in set([(e,pointsPlaces.count(e)) for e in pointsPlaces]) if g==1]
            self.pointsPlacesUneFois.sort()
            # Nombre de points placés 2 fois ou plus :
            self.pointsPlacesDeuxFoisOuPlus = [f[0] for f,g in set([(e,pointsPlaces.count(e)) for e in pointsPlaces]) if g>1]
           ############################################
            
            if self.pointsPlacesDeuxFoisOuPlus.__len__()<3:
                 self.etatPointsGPS += _("Il n'y a pas 3 points placés sur 2 photos : les points GCP seront ignorés.")+"\n"
                 retour = False
            if self.pointsPlacesUneFois.__len__()>1:
                 self.etatPointsGPS += _("Anomalie : les points suivants ne sont placés que sur une seule photo : ")+"\n"+\
                                         " ".join(self.pointsPlacesUneFois)+"\n"
            if self.pointsPlacesUneFois.__len__()==1:
                 self.etatPointsGPS += _("Anomalie : le point suivant n'est placé que sur une seule photo : ")+"\n"+\
                                         " ".join(self.pointsPlacesUneFois)+"\n"
                 
        # vérification : y-a-t-il 2 points avec les mêmes coordonnées géographiques ?

        xyz = [(f[1],f[2],f[3]) for f in self.listePointsGPS if f[0] in listePointsOK]
        if xyz.__len__()!=set(xyz).__len__():
            self.etatPointsGPS+=_("Attention : plusieurs points GCP ont les mêmes coordonnées.") + "\n"

        if retour==False:
            self.etatPointsGPS += _("Saisie incomplète : les points GCP ne seront pas pris en compte") + "\n" +_("Consulter la trace") + "\n"
            self.ajoutLigne(self.etatPointsGPS)
            self.ajoutLigne(_("Les points GCP doivent avoir un nom, des valeurs X Y et Z numériques, une incertitude de la forme '10 10 10'")+ "\n")
            self.ajoutLigne(_("liste des points incorrects : %s \n") % "\n".join(listePointsKO))
            self.ecritureTraceMicMac()
        return retour
                         
    def controleMiseALEchelle(self):  # controle de saisie globale du repère axe, plan métrique, arrêt à la première erreur, True si pas d'erreur, sinon message
        #si pas de chantier, pas de problème mais retour False :  pas de calibration
        self.etatMiseALEchelle = str()
        if self.repTravail==self.repertoireData:
            return False
        # fichier xml présent :
       
        if os.path.exists(os.path.join(self.repTravail,self.miseAEchelle))==False:
            return False
        #ligne :
        if len(self.dicoLigneHorizontale)+len(self.dicoLigneVerticale)!=2:
            self.etatMiseALEchelle = self.etatMiseALEchelle+_("La ligne horizontale ou verticale ne comporte pas 2 points") + "\n"
        # Plan :
        if os.path.exists(self.monImage_MaitrePlan)==False or self.monImage_MaitrePlan==str():
            self.etatMiseALEchelle = self.etatMiseALEchelle+_("Pas de maitre plan horizontal ou vertical") + "\n"
            self.monImage_PlanTif = str()       # réinit le plan sans maitre
        else:
            if os.path.exists(self.monImage_PlanTif)==False:
                self.etatMiseALEchelle = self.etatMiseALEchelle+_("Pas de plan horizontal ou vertical") + "\n"
        # Distance
        try :
            d=float(self.distance.get().split(" ")[0])       # pour permettre la saisie d'une unité
            if d<0:
                self.etatMiseALEchelle = _("{x} Distance {y} invalide.".format(x=self.etatMiseALEchelle, y=self.distance.get())) + "\n" 
            if d==0:
                self.etatMiseALEchelle = _("Distance numlle. Calibration annulée.") + "\n"                
        except: 
            self.etatMiseALEchelle = _("%s Pas de distance pour la mise à l'échelle.") % (self.etatMiseALEchelle) + "\n" 
            return False
        # métrique :
        if self.dicoCalibre.__len__()>0:
            liste = list(self.dicoCalibre.items())
            if liste.__len__()!=4:
                self.etatMiseALEchelle += _("La distance n'est pas mesurée par 2 points repérés sur 2 photos.") + "\n"
            photosAvecDistance = list(set([os.path.basename(e[1]) for e in self.dicoCalibre.keys() ]))
            if not os.path.exists(photosAvecDistance[0]):
                self.etatMiseALEchelle += _("La photo avec distance %s est absente.") % (photosAvecDistance[0]) + "\n"
            if photosAvecDistance.__len__()>1:
                if not os.path.exists(photosAvecDistance[1]):
                    self.etatMiseALEchelle += _("La photo avec distance %s est absente.") % (photosAvecDistance[1]) + "\n"            
        if self.dicoCalibre.__len__()==0:
            self.etatMiseALEchelle += _("Pas de distance pour la calibration.") + "\n"
            
        if self.etatMiseALEchelle==str():
            return True                             # calibration OK, tout va bien
        else: return False

    def finRepereOK(self):                      # ne mettre à jour que pour les variables saisies :

        existe = False                          # par défaut : pas de xml, true si il existe une des variables "reperes"
        xml = self.miseAEchelleXml

        # remplace la virgule possible dans self.distance par un point :

        self.distance.set(self.distance.get().replace(",","."))     # on remplace la virgule éventuelle par un point

        # Pattern des fichiers à traiter : 
        
        xml = xml.replace(_("Fichiers"),str(' .*'+self.extensionChoisie))

        # axe horizontal, dans le dico : self.dicoLigneHorizontale. key = nom point, photo, identifiant ;Retrouver nom de la photo, coordonnées des points
        # items = liste de tuple (key,values) soit tuple = (point,photo, id),(x1,y1)
        # axe vertical possible, mais exclusif l'un de l'autre
        
        liste = list(self.dicoLigneHorizontale.items())                     # dico : (key=(nom point,nom photo, identifiant), value = (x,y)
        if liste.__len__()==2:                                              # s'il y a pas deux points 
            existe = True                                                   # liste horizontale OK
            xml = xml.replace("vecteurHV"," 1 0 ")                          # vecteur  horizontal            
        else:
            liste = list(self.dicoLigneVerticale.items())                   # pas de liste horizontale, on essaie la verticale
            if liste.__len__()==2:                                          # ligne verticale OK : 2 points
                existe = True
                xml = xml.replace("vecteurHV"," 0 1 ")                      # vecteur vertical                
            else:                                                           # s'il y n'y a pas deux points H ou V on met du blanc partout
                liste = [(("","",""),("","")),(("","",""),("",""))]         # rien ne va : on met du blanc partout !

        xml = xml.replace("photoHorizon",os.path.basename(liste[0][0][1]))
        xml = xml.replace("X1H",liste[0][1][0].__str__())
        xml = xml.replace("Y1H",liste[0][1][1].__str__())
        xml = xml.replace("X2H",liste[1][1][0].__str__())
        xml = xml.replace("Y2H",liste[1][1][1].__str__())

        # calibre pour les mesures

        liste = list(self.dicoCalibre.items())

        if liste.__len__()==4:
            existe=True                 # OK il y a 2*2 points sur 2 images
        else:                           # s'il y n'y a pas quatre points on met du blanc       
            liste = [(("","",""),("","")),(("","",""),("","")),(("","",""),("","")),(("","",""),("",""))]
        
        liste.sort(key = lambda e: e[0][0]+e[0][1])         # les points sont triés par point-photo     
        xml = xml.replace("photo1Debut",os.path.basename(liste[0][0][1]))
        xml = xml.replace("X1P1",liste[0][1][0].__str__())
        xml = xml.replace("Y1P1",liste[0][1][1].__str__())
        xml = xml.replace("photo2Debut",os.path.basename(liste[1][0][1]))
        xml = xml.replace("X1P2",liste[1][1][0].__str__())
        xml = xml.replace("Y1P2",liste[1][1][1].__str__())
        
        xml = xml.replace("photo1Fin",os.path.basename(liste[2][0][1]))                         
        xml = xml.replace("X2P1",liste[2][1][0].__str__())
        xml = xml.replace("Y2P1",liste[2][1][1].__str__())        
        xml = xml.replace("photo2Fin",os.path.basename(liste[3][0][1]))                          
        xml = xml.replace("X2P2",liste[3][1][0].__str__())
        xml = xml.replace("Y2P2",liste[3][1][1].__str__())

        xml = xml.replace("distance",self.distance.get().split(" ")[0]) # pour permettre la saisie d'une unité

        # le plan horizontal ou vertical (OK même si absent)

        self.monImage_PlanTif = str()
        if os.path.exists(self.planProvisoireHorizontal):
            self.monImage_PlanTif = self.planProvisoireHorizontal
            existe=True
        
        if os.path.exists(self.planProvisoireVertical):         
            self.monImage_PlanTif = self.planProvisoireVertical            
            existe=True
           
        xml = xml.replace("monImage_MaitrePlan",os.path.basename(self.monImage_MaitrePlan))                 # Nom de l'image maîtresse du plan repere (sans extension)
        xml = xml.replace("monImage_Plan",os.path.basename(self.monImage_PlanTif))                          # nom du masque correspondant 
        
        if existe:
            with open(self.miseAEchelle, 'w', encoding='utf-8') as infile:
                infile.write(xml)
            with open("MiseAEchelleInitial", 'w', encoding='utf-8') as infile:
                infile.write(self.miseAEchelleXml)                
        else:
            supprimeFichier(self.miseAEchelle)
            
    def controleOptions(self):                  # controle que les valeurs numériques echelle1, echelle2 et delta sont bien :
                                                # des nombres entiers positif sauf échelle2qui peut = -1
                                                # et que echelle1 < echelle2
                                                # et enfin que echelle 1 et 2 sont au max = taille la plus grande de l'image
                                                # ce controle peut-être appelé avant de lancer micMac
                                                # Retour : true si Ok, message d'erreur sinon (string) pas d'avertissement sans conséquence.
        texte  = str()  # message informatif (pas toujours !)
        erreur = str()  # message erreur 

        # remarque la fonction int(str) nécessite que la chaîne représente un nombre entier et non décimal
        
        # Controle echelle 1 pour le mode All de tapioca
        
        try:
            if self.modeTapioca.get()=="All":
                echelle1 = int(self.echelle1.get()) # si erreur saisie (texte!) alors valeur par défaut         
        except:
            echelle1 = 1000
            self.echelle1.set(str(echelle1))
            erreur += "\n" + _("L'échelle pour le mode All de Tapioca est invalide, une valeur par défaut, %s, est affectée.") % (self.echelle1.get()) + "\n"

        try:
            if echelle1<50 and echelle1!=-1 and self.modeTapioca.get()=="All":
                texte += "\n" + _("Echelle pour le mode All de Tapioca trop petite :") +  "\n" + self.echelle1.get() + "\n" + _("Minimum = 50") + "\n"
        except:
            pass

        # Controle echelle 2 pour le mode MulScale de tapioca (première échelle du MulScale)
        
        try:
            if self.modeTapioca.get()=="MulScale":
                echelle2 = int(self.echelle2.get())
        except:
            echelle2 = 300
            self.echelle2.set(str(echelle2))
            erreur += "\n" + _("L'échelle 1 pour MulScale de Tapioca est invalide, une valeur par défaut, %s, est affectée.") % (self.echelle2.get()) + "\n"

        try:
            if echelle2==-1 and self.modeTapioca.get()=="MulScale":
                texte += "\n" + _("L'échelle 1 de MulScale ne doit pas être -1.") + "\n" + _("Elle est mise à 300.") + "\n"
                echelle2 = 300
                self.echelle2.set(str(echelle2))
        except: pass
        
        try:
            if echelle2<50 and echelle2!=-1 and self.modeTapioca.get()=="MulScale":
                texte += "\n" + _("L'échelle 1 pour le mode MulScale de Tapioca est trop petite : ") + "\n" + self.echelle2.get() + "\n" + _("Minimum = 50, maximum conseillé : 300") + "\n"
        except:
            pass

        # Controle echelle 3 pour le mode MulScale de tapioca (seconde échelle du MulScale)
        
        try:
            if self.modeTapioca.get()=="MulScale":
                echelle3 = int(self.echelle3.get())
        except:
            echelle3 = 1200
            self.echelle3.set(str(echelle3))
            erreur += "\n" + _("L'échelle 2 pour le mode  MulScale de Tapioca est invalide, une valeur par défaut, %s, est affectée.") % (self.echelle3.get()) + "\n"      

        try:
            if echelle3<50 and echelle3!=-1 and self.modeTapioca.get()=="MulScale":
                texte += "\n" + _("L'échelle 2 pour le mode MulScale de Tapioca est trop petite :") + "\n" + self.echelle3.get() + "\n" + _("Minimum = 50") + "\n"
        except:
            pass

        # controle cohérence echelle2 et echelle3

        try:
            if echelle3<=echelle2 and echelle3!=-1 and self.modeTapioca.get()=="MulScale":
                texte += "\n" + _("L'échelle 2 de MulScale pour tapioca") + "\n" + self.echelle3.get() + "\n" + _("plus petite que l'échelle 1 :") + "\n" + self.echelle2.get() + "\n"              
        except:
            pass

        # Controle échelle pour le mode line

        try:
            if self.modeTapioca.get()=="Line":
                echelle4 = int(self.echelle4.get())
        except:
            echelle4 = 1200
            self.echelle4.set(str(echelle4))
            erreur += "\n" + _("L'échelle pour le mode Line de tapioca est invalide, une valeur par défaut, %s, est affectée.") % (self.echelle4.get()) + "\n"

        try:
            if echelle4<50 and echelle4!=-1 and self.modeTapioca.get()=="Line":
                texte += "\n" + _("Echelle pour le mode Line de tapioca trop petite : ") + "\n" + self.echelle4.get() + "\n" % (self.echelle4.get())
        except:
            pass

        # Controle delta pour le mode line
        
        try:
            if self.modeTapioca.get()=="Line":
                delta = int(self.delta.get())
        except:
            delta = 4
            self.delta.set(str(delta))
            erreur += "\n" + _("La valeur de delta pour le mode Line de Tapioca est invalide,") + "\n" + _("une valeur par défaut, %s, est affectée.") % self.delta.get() + "\n"        
            
        try:
            if delta<1 and self.modeTapioca.get()=="Line":
                texte += "\n" + _("Delta trop petit :") + "\n" + self.delta.get() + "\n" + _("Minimum = 1") + "\n"
        except:
            pass           

        # vérification du zoom final :
                    
        if self.zoomF.get() not in ("1","2","4","8"):
            erreur += "\n" + _("Le zoom final pour MALT n'est pas 1,2,4 ou 8 : %s") % (self.zoomF.get()) + "\n"

        # vérification du Mesh : nuage ou maillage :
                    
        if self.nuage2Mesh.get() not in ("0","1"):
            erreur += "\n" + _("Le choix entre nuage et maillage pour Malt est incorrect (ni 0 ni 1) : %s") % (self.nuage2Mesh.get()) + "\n"
        
        # zoom OK, les valeurs 8,4,2,1 correspondent au nuage étape 5, 6, 7, 8 
        
        if self.zoomF.get()=="8":self.etapeNuage = "5"
        if self.zoomF.get()=="4":self.etapeNuage = "6"
        if self.zoomF.get()=="2":self.etapeNuage = "7"        
        if self.zoomF.get()=="1":self.etapeNuage = "8"

        # vérification nombre d'images utiles autour du maître pour Malt en mode GeomImage

        try:
            self.photosUtilesAutourDuMaitre.set(int(self.photosUtilesAutourDuMaitre.get())) # met un entier (sinon galère !)
            if self.photosUtilesAutourDuMaitre.get()<1 and self.photosUtilesAutourDuMaitre.get()!=-1:
                texte += "\n" + _("Malt mode Geomimage :") + "\n" + _("Le nombre de photos utiles autour de l'image maîtresse est trop petit : %s")  % (str(self.photosUtilesAutourDuMaitre.get())) + "\n"
        except Exception as e:
            texte += "\n" + _("Malt mode Geomimage :") + "\n" + _("Le nombre de photos utiles autour de l'image centrale n'est pas numérique : ") + "\n" + _("Il est mis à 5.") + "\n"
            self.photosUtilesAutourDuMaitre.set(5)

            
        # vérif taille image (s'il y a des images !):
        
        if len(self.photosAvecChemin)>0:
            if os.path.exists(self.photosAvecChemin[0])==False:
                texte += _("La photo %s n'existe plus.") % (self.photosAvecChemin[0])
                return texte+erreur        
            photo1 = Image.open(self.photosAvecChemin[0])
            largeur,hauteur = photo1.size
            del photo1
            inutile = _("Inutile et ralenti le traitement. Modifier.")
            maxi = max(largeur,hauteur)
            if self.modeTapioca.get()=='All':
                if int(self.echelle1.get())>maxi:
                    texte += "\n" + _("L'échelle pour le mode All de tapioca = ") + self.echelle1.get() + "\n" + _(", est plus grande que la dimension maxi de la photo : ") + "\n" + str(maxi) + "." + "\n\n" + inutile

            if self.modeTapioca.get()=='MulScale':
                if int(self.echelle2.get())>maxi:
                    texte += "\n" + _("L'échelle 2 pour le mode MulScale de tapioca= ") + self.echelle2.get() + "\n" + _("est plus grande que la dimension maxi de la photo :") + "\n" + str(maxi) + "." + "\n\n" + inutile

            if self.modeTapioca.get()=='Line':
                if int(self.echelle4.get())>maxi:
                    texte += "\n" + _("L'échelle pour le mode Line de tapioca = ") + self.echelle2.get() + "\n" + _("est plus grande que la dimension maxi de la photo :") + "\n" + str(maxi) + "." + "\n\n" + inutile

        # controle calibration intrinsèque : si non demandé alors suppression des photos de calibration
        
        if self.choixCalibration.get()=="sans": 
              self.supprimeCalibrationParPhotos()

        # si les photos de calibration ne servent pas uniquement à la calibration on les remet :

        if not self.calibSeule.get():
            self.remettrePhotosCalibration()

        # controle que les incertitudes sur les pointss GPS répondent bien à une suite de 3 nombre entiers

        for Nom,X,Y,Z,actif,ident,incertitude in self.listePointsGPS:   # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
            if actif and not re.match("\d+\s+\d+\s+\d+\s*$",incertitude): # si actif et incertitude incorrecte :
                texte += "\n"+_("Incertitude\n %s \ndu point GCP \n%s\nincorrecte. Forme valable : 3 entiers séparés par des espaces, exemple : '2 2 2' ") % (Nom,incertitude) 
        
        # retour True ou String

        if texte+erreur==str():
            return True
        else:
            return texte+erreur

    def finOptionsKO(self):
        self.ajoutTraceComplete("\n"+heure()+" "+_("Les options sont abandonnées par l'utilisateur"))
        self.onglets.pack_forget()      # on ferme la boite à onglets          
        self.restaureParamChantier(self.fichierParamChantierEnCours)
        self.afficheEtat()
        
    #"""""""""""""""""""""""   Options de TAPIOCA, Tapas, densification
        
    def optionsTapioca(self):                     # utilisé dans la syntaxe : Tapioca Line Files Size delta ArgOpt=  (ce qui exclut implicitement la syntaxe multiscale)
        self.item460.pack_forget()
        self.item470.pack_forget()
        self.item480.pack_forget()
       
        if self.modeTapioca.get()=='All':
            self.item480.pack(pady=15)

        if self.modeTapioca.get()=='MulScale':
            self.item460.pack(pady=15)
            
        if self.modeTapioca.get()=='Line':
            self.item470.pack(pady=15)

    def visuOptionsCalibration(self):
        self.item520.pack_forget() # photos
        self.item570.pack_forget() # chantier
        self.item510.pack_forget() # tarama
        self.item535.pack_forget() # calculer nuage non dense
        self.item540.pack_forget() # densification        
        self.item562.pack_forget() # choix
        if self.choixCalibration.get()=='photos':
            self.item562.pack()
            self.item520.pack()
        if self.choixCalibration.get()=='chantier':
            self.item562.pack()
            self.item570.pack()
        self.item510.pack()
        self.item535.pack()        
        self.item540.pack()
        
    def optionsDensification(self):
        self.item700.pack_forget()
        self.item800.pack_forget()
       
        if self.choixDensification.get()=='C3DC':
            self.item801.pack(ipady=2,pady=3)       # bouton pour créer un masque
            self.item802.pack(ipady=2,pady=3)       # bouton pour supprimer le masque
            self.item803.pack(ipady=2,pady=3)       # Aide pour le widget IGN création de masque 3D
            self.item804.pack(ipady=2,pady=3)       # info sur la présence du masque    
            self.item800.pack(pady=15)              # regroupe les widgets 801 à 804
            if os.path.exists("AperiCloud.ply")==False:
                   self.item801.pack_forget()
                   self.item802.pack_forget()
                   self.item803.pack_forget()                   
            if not(self.existeMasque3D()):
                   self.item802.pack_forget()                                   

        if self.choixDensification.get()=='Malt':
            self.item700.pack(pady=15)
        

    #""""""""""""""""""""""""   Options de Malt

    def chargerCalibrationIntrinsequeDepuisMenu(self,repertoireInconnu=True):
        bilan = self.chargerCalibrationIntrinseque(repertoireInconnu=repertoireInconnu)
        if bilan:
            self.encadre(bilan)
            return bilan
        self.choixCalibration.set("chantier")
        bilanOK = _("Calibration du chantier\n '%s' \nrecopiée.") % (self.selectionRepertoireAvecChemin)
        self.encadre(bilanOK)
        return bilanOK
    
    def chargerCalibrationIntrinseque(self,repertoireInconnu=True):
        if self.pasDePhoto(False):
            self.item572.configure(text=_("Commencer par choisir des photos."),foreground='red')
            return
        if repertoireInconnu:
            bilan = self.choisirUnChantier(_("Choisir le chantier pour copier la calibration."),filtre="CALIB")
            if bilan!=None:
                message = _("Aucun chantier choisi.") + "\n" + bilan + "\n"
                self.item572.configure(text=_("Pas de chantier choisi."))
                self.afficheEtat(message)
                return message
        repertoireCalib  =   os.path.join(self.selectionRepertoireAvecChemin,"Ori-Calib")
        if not os.path.exists(repertoireCalib):
            bilan = _("le chantier choisi %s n'a pas de données de calibration.") % (repertoireCalib)
            self.item572.configure(text=bilan)
            return bilan
        # copie du répertoire : tentative
        calibChantier = os.path.join(self.repTravail,"Ori-Calib")
        supprimeRepertoire(calibChantier)        
        try: shutil.copytree(repertoireCalib,calibChantier)
        except Exception as e:
            self.item572.configure(text=_("la copie a échouée : %s.") % (str(e)))
            bilan = _("La copie de la calibration du chantier\n %s \na échoué : \n%s") % (repertoireCalib,str(e))
            self.ajoutLigne(bilan)
            return bilan
        # copie du répertoire: réussite
        if os.path.exists(calibChantier):
            self.chantierOrigineCalibration = os.path.basename(self.selectionRepertoireAvecChemin)
            self.item572.configure(text=_("Calibration du chantier '%s' recopiée.") % (self.chantierOrigineCalibration))
            self.supprimeCalibrationParPhotos()
            self.ajoutLigne(_("Copie de la calibration du chantier\n %s.") % (repertoireCalib))
        else:
            self.item572.configure(text=_("la recopie a échouée : %s.") % (str(e)))
            bilan = _("La copie de la calibration du chantier\n %s \na échoué.") % (repertoireCalib)
            self.ajoutLigne(bilan)           
            return bilan
            
    def imagesCalibrationIntrinseques(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return        
        bulles = dict([(e,"") for e in self.photosPourCalibrationIntrinseque])
        self.choisirUnePhoto(self.photosAvecChemin,
                             _("Pour calibrer l'appareil photo"),
                             _("Quelques photos, convergentes, d'angles écartés") + "\n" + _("en jaune la calibration actuelle"),
                             boutonDeux=_("Supprimer"),
                             bulles=bulles)
        if self.fermerVisu:                                             # sortie par second bouton
            self.item526.config(text=_("Pas de photos de calibration intrinseque."))
            self.photosPourCalibrationIntrinseque = list()                                 
            return
        if self.selectionPhotosAvecChemin.__len__()==0:             # sortie par fermeture fenêtre
            self.item526.config(text="")
            return
        self.photosPourCalibrationIntrinseque = self.selectionPhotosAvecChemin
        self.item526.config(text=_("Nombre de photos choisies : ")+str(self.photosPourCalibrationIntrinseque.__len__()))
        self.photosCalibrationSansChemin = [os.path.basename(f) for f in self.photosPourCalibrationIntrinseque]
        self.supprimeCalibrationParCopie()
        
    def supprimeCalibrationParCopie(self):
        # suppression de la calibration par copie de chantier
        if self.chantierOrigineCalibration:
            self.chantierOrigineCalibration = str()
            self.item572.configure(text="")
            calibChantier = os.path.join(self.repTravail,"Ori-Calib")
            supprimeRepertoire(calibChantier)
            self.ajoutLigne("\n"+_("Suppression de la calibration par copie depuis un autre chantier"))
        
    def supprimeCalibrationParPhotos(self):
        #suppression de la calibration par photos
        if self.photosCalibrationSansChemin:
            self.photosCalibrationSansChemin = list()
            self.photosPourCalibrationIntrinseque = list()
            self.ajoutLigne("\n"+_("Suppression de la calibration par photos"))

        
    #""""""""""""""""""""""""   Options de Malt        

    def optionsMalt(self):
        self.item710.pack_forget()
        self.item730.pack_forget()
        self.item740.pack_forget()
        self.item745.pack_forget()                       
        if self.modeCheckedMalt.get()=='GeomImage':
            self.item710.pack(pady=10)
            self.item730.pack(pady=10)            
        if self.modeCheckedMalt.get()=='Ortho':
            self.item745.pack(pady=5)
            self.item740.pack(pady=5)
        self.miseAJourItem701_703()
                                 
    def imageMaitresse(self):       # bouton "choisir les maitresses" de l'option GeomImage
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle("Choisir d'abord les photos du chantier.")
            return  

        # préparation des infos bulles
        
        bulles = dict()

        for f in self.listeDesMaitresses:
            for e in self.listeDesMasques:
                if os.path.splitext(f)[0]+"_masque.tif"==e:
                    bulles[f]=_("Image maitresse avec masque")
            if f not in bulles:
                bulles[f]=""    # image maitresse sans masque

        # suppression des fichiers masques pour malt ;; ces fichiers sont créés au lancement de Malt
        # par contre on garde les dessins des masques (_masque.tif) qui ne seront utiles qui si le nom est dans la liste des masques

        for e in self.photosAvecChemin:
            supprimeFichier(os.path.splitext(e)[0]+"_Masq.xml")
            supprimeFichier(os.path.splitext(e)[0]+"_Masq.tif")

        # choix des nouvelles maîtresses :
                
        self.choisirUnePhoto(self.photosAvecChemin,
                             _("Choisir les maîtresses"),
                             _("Choisir une ou plusieurs image(s) maîtresse(s)") + "\n" + _("en jaune : les maitresses actuelles") + "\n" + _("Une info bulle informe de la présence d'un masque"),
                             boutonDeux=_("Supprimer les images maîtresses"), # self.fermerVisu=True
                             mode="extended",
                             bulles=bulles)

        # suppression de toutes les maitresses
        if self.fermerVisu:                                             # sortie par bouton deux = fermeture de fenêtre + self.fermerVisu=True 
            self.reinitialiseMaitreEtMasque()                  
            return
        
        #abandon de la saisie
        if self.selectionPhotosAvecChemin.__len__()==0:                 #sortie par fermeture fenêtre ou sans choix
            self.item701.config(text=_("Abandon. Choix inchangé.") + "\n")
            return
        
        # nouvelle liste des maitresses : mettre à jour la nouvelle liste des masques
        self.listeDesMaitresses = self.selectionPhotosAvecChemin
        # mise à jour de la liste des masques : suppression des masques qui ne sont plus dans la liste des maitresses
        new = list()
        for e in self.listeDesMaitresses:
            if ' '.join(self.listeDesMasques).count(os.path.splitext(e)[0]): # la maitresse est dans la liste des masques
                nouveauMasque = os.path.splitext(e)[0]+"_masque.tif"
                if nouveauMasque in self.listeDesMasques:
                    new.append(nouveauMasque)            

        self.listeDesMasques = list(new)        # nouvelle liste des masques 
        self.miseAJourItem701_703()

    def miseAJourItem701_703(self):             # et 745 Onglet Malt, Cadres geomImage et Ortho
        try:
            if self.listeDesMaitresses.__len__()==0:
                self.item701.config(text=_("Image maitresse obligatoire pour GeomImage."))
  
            if self.listeDesMaitresses.__len__()==1:
                self.item701.config(text=_("image maîtresse = ")+os.path.basename(self.listeDesMaitresses[0]))
            
            if self.listeDesMaitresses.__len__()>1:
                self.item701.config(text=str(self.listeDesMaitresses.__len__())+_(" images maîtresses"))
        
            if self.listeDesMasques.__len__()==0:
                self.item703.config(text="\n" + _("Pas de masque."))                
                
            if self.listeDesMasques.__len__()==1:
                self.item703.config(text="\n" + _("un seul masque : ")+os.path.basename(self.listeDesMasques[0]))  

            if self.listeDesMasques.__len__()>1:
                self.item703.config(text="\n"+str(self.listeDesMasques.__len__())+" "+_("masques"))
                
            if not os.path.exists(self.mosaiqueTaramaTIF):
                self.item745.config(text="\n" + _("Pas de mosaique Tarama : pas de masque."))
                self.item745.config(state=DISABLED)
            elif os.path.exists(self.masqueTarama):
                self.item745.config(text=_("Tracer un nouveau masque sur la mosaique Tarama"))
                self.item745.config(state=NORMAL)
            else:
                self.item745.config(text=_("Tracer un masque sur la mosaique Tarama"))
                self.item745.config(state=NORMAL)                 
        except Exception as e:
            print(_("erreur dans miseAJour701_703 : "),str(e))                            

    def tracerLesMasques(self):     # Bouton de l'option GeomImage
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return      
        self.fermerVisuPhoto()

        if self.listeDesMaitresses.__len__()==0:
            self.item703.config(text=_("Il faut au moins une image maîtresse pour définir un masque."),
                                background="#ffffaa")
            return
        bulles=dict()     
        for e in self.listeDesMasques:
            for f in self.listeDesMaitresses:
                if os.path.splitext(f)[0]+"_masque.tif"==e:
                    bulles[f]=_("Un masque existe déjà")
        self.choisirUnePhoto(self.listeDesMaitresses,
                             _("Choisir l'image pour le masque"),
                             _("Choisir une image maîtresse pour le masque\nen jaune = un masque existe"),
                             mode="single",
                             bulles=bulles)
       
        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        maitre = self.selectionPhotosAvecChemin[0]
        masqueEnAttente = os.path.splitext(maitre)[0]+"_masque.tif"

        # l'utilisateur trace le masque
        
        self.masqueRetour = TracePolygone(fenetre,maitre,masqueEnAttente)        # L'utilisateur peut tracer le masque sur l'image maitre       
        if self.masqueRetour.polygone == True:
            ajout(self.listeDesMasques,masqueEnAttente)
        self.miseAJourItem701_703()    
            
    def traceMasque(self):      # Choisir le masque Bouton de l'option GeomImage ou AperoDeDenis
        self.fermerVisuPhoto()

        if self.listeDesMaitresses.__len__()==0:
            self.item703.config(text=_("Il faut au moins une image maîtresse pour définir un masque."),
                                background="#ffffaa")
            return

        if self.listeDesMaitresses.__len__()==1:
            self.maitre = self.listeDesMaitresses[0]
       
        # comme il y a  plusieurs maîtres possibles il faut choisir !
        else:
            self.choisirUnePhoto(self.listeDesMaitresses,
                                 _("Choisir l'image pour le masque"),
                                 _("Choisir une image maîtresse pour le masque"),
                                 mode="single")
            if self.selectionPhotosAvecChemin.__len__()==0:
                return
            else:
                self.maitre = self.selectionPhotosAvecChemin[0]
        

        # un peu brutal si la visu n'est pas celle de la photo maitre, évite les incohérences

        if os.path.exists(self.maitre):                                                         # l'image maître doit exister
            self.masqueProvisoire = os.path.splitext(self.maitre)[0]+"_Masq_provisoire.tif"     # Nom du fichier masque, à partir du fichier maître, imposé par micmac
            supprimeMasque(self.repTravail,"_Masq.tif")                                         # suppression des anciens masques
            supprimeFichier(self.fichierMasqueXML)
            self.masquesansChemin = str()
            self.masqueRetour = TracePolygone(fenetre,self.maitre,self.masqueProvisoire)        # L'utilisateur peut tracer le masque sur l'image maitre 
            if self.masqueRetour.polygone == False:                                             # si retour OK (masqueRetour est un élément de la classe tracePolygone)
                 self.masqueProvisoire = str()                                                  # pas de masque : détricotage
                 self.item703.config(text=_("pas de masque"))
        else:
            self.item703.config(text=_("Il faut une image maîtresse pour définir un masque."),
                                background="#ffffaa")

    def MasqueXML(self):      # préparation du masque pour malt GeomImage. self.maitreSansChemin est nécessaire
        
        # le masque est constitué d'un fichier .tif ET d'un fichier .xml (masqueSansChemin est le tif
        # la racine des noms est le nom de l'image maître, suivi de _Masq. puis de tif ou xml

        masque = os.path.splitext(self.maitreSansChemin)[0]+"_masque.tif"

        # On vérifie l'existencce du "masque" :
        if os.path.exists(masque)==False:
            supprimeFichier(self.fichierMasqueXML)              # suppression ancien xml
            return            
        # copie du fichier masque tif sous le nom requis par Malt = nom du maitre+"_Masq.tif"
        masqueTIF = os.path.splitext(self.maitreSansChemin)[0]+"_Masq.tif"
        supprimeFichier(masqueTIF)
        shutil.copy(masque,masqueTIF)

        #écriture xml
        self.masqueXML = self.masqueXMLOriginal     # version initiale du fichier XML
        self.masqueXML=self.masqueXML.replace("MonImage_Masq.tif",masqueTIF)                       # écriture dans le fichier xml        
        self.masqueXML=self.masqueXML.replace("largeur",str(self.dimensionsDesPhotos[0][1][0]))    # x = self.dimensionsDesPhotos[0][0] 
        self.masqueXML=self.masqueXML.replace("hauteur",str(self.dimensionsDesPhotos[0][1][1]))    # y=self.densionsDesPhotos[0][1]
        self.fichierMasqueXML=masqueTIF.replace(".tif",".xml")      # nom du fichier xml

        with open(self.fichierMasqueXML, 'w', encoding='utf-8') as infile:
            infile.write(self.masqueXML)

    def tracerUnMasqueSurMosaiqueTarama(self):

        if not os.path.exists(self.mosaiqueTaramaTIF):              # en principe existe si on arrive ici
            return
      
        if not os.path.exists(self.mosaiqueTaramaJPG):
            self.conversionJPG(liste=[self.mosaiqueTaramaTIF])          
        if not os.path.exists(self.mosaiqueTaramaJPG):
            return
        # l'utilisateur trace le masque
 
        self.masqueRetour = TracePolygone(fenetre,self.mosaiqueTaramaJPG,self.masqueTarama)        # L'utilisateur peut tracer le masque sur l'image maitre       
        if self.masqueRetour.polygone == True:
            self.miseAJourItem701_703()
            self.ajoutLigne("\n"+_("Masque 2D sur Tarama"))            
        pass

    #""""""""""""""""""""""" Options masque 3D pour C3DC

    def affiche3DApericloud(self):          # lance SaisieMasqQT, sur apericloud ou modele3d, attente de saisie/fermeture (subprocess.call)
        
        if not os.path.exists("AperiCloud.ply"):
            return
        
        nuage = "AperiCloud.ply"
        self.masque3DSansChemin         =   "AperiCloud_selectionInfo.xml"          # nom du fichier XML du masque 3D, fabriqué par 
        self.masque3DBisSansChemin      =   "AperiCloud_polyg3d.xml"                # nom du second fichier XML pour le masque 3D
        verifParametresSaisieMasqQT()                           # modifie si besoin le paramètre de centrage du nuage : au barycentre
        masque3D = [self.mm3d,"SaisieMasqQT",nuage]             # " SaisieAppuisInitQT AperiCloud.ply"
        self.lanceCommande (masque3D,
                            info=(_("Saisie masque 3D pour C3DC sur le nuage dense ou non dense."))
                           )

        try:                                                                # marche pas si on est en visu
            if self.existeMasque3D():
                self.item804.configure(text= _("Masque 3D créé"),foreground='red')
                self.item802.pack()     # bouton "supprimer"
            else:
                self.item804.configure(text= _("Abandon : pas de masque créé."),foreground='red')
                self.item802.forget()   # bouton "supprimer"
        except: pass


    def supprimeMasque3D(self):
        supprimeFichier(self.masque3DSansChemin)                # suppression définitive des fichiers pour le masque 3D 
        supprimeFichier(self.masque3DBisSansChemin)        
        self.item804.configure(text= _("Masque 3D supprimé."),foreground='red')
        self.item802.forget()
        self.ajoutLigne("\n"+_("Suppression du masque 3D"))
        
            
    #""""""""""""""""""""""" Options de CalibrationGPS : faire correspondre des points (x,y,z) numérotés de 1 à N, avec des pixels des images.

    def optionsReperes(self):				        # en entrée : self.listePointsGPS qui comporte la liste des points GCP a affiche, sauvegardée        

        try: self.item650.destroy()				# suppression de l'onglet s'il existait
        except: pass
        try: self.bulle.destroy()
        except: pass
        
        self.item650 = ttk.Frame(	self.onglets,		# création du cadre d'accueil de l'onglet
					height=5,
					relief='sunken')	    

        # message en haut de fenêtre
        
        self.item670 = ttk.Frame(self.item650,relief='sunken')
        texte = _("3 points doivent être placés sur au moins 2 photos") + "\n"
        texte+= _("Les points GCP sont prioritaires sur la mise à l'échelle.\n")
        texte+= _("Importation possible des points GCP depuis un fichier ou un chantier: voir menu Expert/Importation .\n")        
        self.item671=ttk.Label(self.item670,text=texte,justify='left')
        self.item671.pack(pady=1,padx=5,ipady=1,ipadx=1,fill="y")        
        self.item670.pack(side='top',pady=5,padx=5)

        # demande info globale pour Campari : erreur orientation cible GCP et pixel image
        
        self.item672 = ttk.Frame(self.item650,height=10,relief='sunken')        
        self.item673 = ttk.Label(self.item672,text=_('CAMPARI : incertitude cible GCP :'))        
        self.item674 = ttk.Entry(self.item672,textvariable=self.incertitudeCibleGPS)          # incertitude globale cible GCP
        self.item675 = ttk.Label(self.item672,text=_('incertitude pixel image :'))        
        self.item676 = ttk.Entry(self.item672,textvariable=self.incertitudePixelImage)          # incertitude globale cible GCP
        self.item673.pack(side="left",pady=5,padx=5,ipady=1,ipadx=1)
        self.item674.pack(side="left")
        self.item675.pack(side="left")
        self.item676.pack(side="left")
        self.item672.pack(side='top',pady=5,padx=5,ipady=1,ipadx=1)
        
        # affichage des entêtes de colonne
        self.item660 = ttk.Frame(self.item650,height=5,relief='sunken')
        self.item661 = ttk.Label(self.item660,text='point').pack(side='left',pady=10,padx=40,fill="both")
        self.item662 = ttk.Label(self.item660,text='X').pack(side='left',pady=10,padx=60)                  
        self.item663 = ttk.Label(self.item660,text='Y').pack(side='left',pady=10,padx=60)
        self.item664 = ttk.Label(self.item660,text='Z').pack(side='left',pady=10,padx=60)
        self.item665 = ttk.Label(self.item660,text=_('Incertitude sur X,Y,Z')).pack(side='left',pady=10,padx=30)        
        self.item660.pack(side="top")
        
        # préparation des boutons en bas de liste
		
        self.item653=ttk.Button(self.item650,text=_('Ajouter un point'),command=self.ajoutPointCalibrationGPS)
        self.item654=ttk.Button(self.item650,text=_('Supprimer des points'),command=self.supprPointsGPS)                  
        self.item655=ttk.Button(self.item650,text=_('Placer les points'),command=self.placerPointsGPS)
        self.item656=ttk.Button(self.item650,text=_('Appliquer au ') + '\n' + _('nuage non densifié'),command=self.appliquerPointsGPS)
        
        self.item653.pack_forget()											#on oublie les boutons du bas s'ils étaient affichés
        self.item654.pack_forget()
        self.item655.pack_forget()
        self.item656.pack_forget()
            
        # Affichage de la liste des points actuellement saisis:
        self.item680 = ttk.Frame(self.item650,height=10,relief='sunken') 
        self.listeWidgetGPS = list()							# liste des widgets affichés, qui sera abondée au fur et à mesure par copie de self.listePointsGPS		
        self.listePointsGPS.sort(key=lambda e: e[0])                                    # tri par ordre alpha du nom

        for n,x,y,z,actif,ident,incertitude in self.listePointsGPS:			# affichage de tous les widgets nom,x,y,z,actif ou supprimé (booléen), identifiant
            if actif:                                                                   # listePointsGPS : liste de tuples (nom du point, x GCP, y GCP, z GCP, booléen actif ou supprimé, identifiant)
                self.affichePointCalibrationGPS(n,x,y,z,ident,incertitude)		# ajoute une ligne d'affichage

        self.item680.pack()
        self.item653.pack(side='left',padx=20)					    	# affichage des boutons en bas d'onglet
        self.item654.pack(side='left',padx=20)
        self.item655.pack(side='left',padx=20)
        self.item656.pack(side='left',padx=20)

        # placer l'onglet devant l'onglet "Densification"
 
        placeDensification = self.onglets.index("end")-1        # Densification est le dernier onglet
        self.onglets.add(self.item650, text=_("Points GCP"))
        self.onglets.insert(self.item650, placeDensification)   # affichage onglet Points GCP en avant dernière position
		
    def affichePointCalibrationGPS(self,n,x,y,z,ident,incertitude):             # affiche un point
        
        f = ttk.Frame(self.item680,height=5,relief='sunken')			# cadre d'accueil de la ligne
        
        self.listeWidgetGPS.append(
				    (f,						# cadre : [0]
                                    ttk.Entry(f),				# zones de saisie de [1] à [4]
                                    ttk.Entry(f),
                                    ttk.Entry(f),
                                    ttk.Entry(f),
                                    ident,
                                    ttk.Entry(f)
                                    )
				   )
        
        self.listeWidgetGPS[-1][0].pack(side='top')
        if self.onglets.tab(self.onglets.select(), "text")==_("Points GCP") and not self.listeWidgetGPS[-1][0].winfo_viewable():           
            self.item650.configure(height=int(self.item650.cget('height'))+2)

        self.listeWidgetGPS[-1][1].pack(side='left',padx=5)
        self.listeWidgetGPS[-1][1].focus()        
        self.listeWidgetGPS[-1][2].pack(side='left')        
        self.listeWidgetGPS[-1][3].pack(side='left')
        self.listeWidgetGPS[-1][4].pack(side='left')
        self.listeWidgetGPS[-1][6].pack(side='left')
		
        self.listeWidgetGPS[-1][1].insert(0,n)              				        # affichage de la valeur dans le widget                  
        self.listeWidgetGPS[-1][2].insert(0,x)
        self.listeWidgetGPS[-1][3].insert(0,y)
        self.listeWidgetGPS[-1][4].insert(0,z)   
        self.listeWidgetGPS[-1][6].insert(0,incertitude)      
                                        

    def ajoutPointCalibrationGPS(self):
        if self.onglets.tab(self.onglets.select(), "text")=="GCP" and not self.item452.winfo_viewable():                       # controle la visibilité des boutons " valider les options" et "annuler"
            self.infoBulle(_("Agrandissez la fenêtre avant d'ajouter un point GCP !") + "\n" + _("(ou si impossible : supprimer un point)"))
            return
        self.actualiseListePointsGPS()
        if [ e[0] for e in self.listePointsGPS if e[4]].__len__()>=30:                     
            self.infoBulle(_("Soyez raisonnable : pas plus de 30 points GCP !"))
            return
        nom = chr(65+self.listePointsGPS.__len__())
        self.listePointsGPS.append([nom,"","","",True,self.idPointGPS,"1 1 1"])     # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant,incertitude)
        self.idPointGPS += 1						    # identifiant du point suivant
        self.optionsReperes()						    # affichage avec le nouveau point
        self.onglets.select(self.item650)                    		    # active l'onglet (il a été supprimé puis recréé par optionsReperes)  
        self.actualiseListePointsGPS()
        
    def supprPointsGPS(self):       # Suppression des points GCP
        try: self.bulle.destroy()
        except: pass
        if self.nbPointsGCPActifs()==0:                # pas de points actif : on sort
            self.infoBulle(_("Aucun point à supprimer !"))
            return						
        self.actualiseListePointsGPS()                      # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
        listeIdentifiants = [ (e[0],e[5]) for e in self.listePointsGPS if e[4] ] # liste des noms,identifiants si point non supprimé

        self.messageSiPasDeFichier = 0                                           #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto([ f[0] for f in listeIdentifiants],
                                                 titre=_('Points à supprimer'),
                                                 mode='extended',
                                                 message=_("Multiselection possible."),
                                                 objets='points',
                                                 boutonDeux=_("Annuler"))
        self.messageSiPasDeFichier = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return

        listeIdentifiantsASupprimer = [g[1] for g in listeIdentifiants if g[0] in self.selectionPhotosAvecChemin]
        listeIni = list(self.listePointsGPS)     # duplique la liste
        for i in listeIni:                       # on met le flag i[4] à zéro : pour conserver le lien avec les points placés ??
            if i[5] in listeIdentifiantsASupprimer:
                self.listePointsGPS.remove(i)                
                i[4] = False
                self.listePointsGPS.append(i)
        dico = dict(self.dicoPointsGPSEnPlace)  # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
        # supprime les points déjà placés sur les photos              
        [self.dicoPointsGPSEnPlace.pop(i,None) for i in dico if i[2] in listeIdentifiantsASupprimer]                        
        self.optionsReperes()
        self.onglets.select(self.item650)                   # active l'onglet (il a été supprimé puis recréé par optionsReperes)
        # referentiel modifié :
        self.referentielOK = False
        
    def actualiseListePointsGPS(self):                      # actualise les valeurs saisies pour les points GCP
        # n'éxécuter que s'il y a eu saisie de points GCP : self.listeWidgetGPS existe !
        try: self.bulle.destroy()
        except: pass
        dico = dict(self.dicoPointsGPSEnPlace)              # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
        for a,nom,x,y,z,ident,incertitude in self.listeWidgetGPS:
            for i in self.listePointsGPS:                   # listePointsGPS : 6-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
                if i[5] == ident:
                    self.listePointsGPS.remove(i)
                    i[0] = nom.get()
                    i[0] = i[0].replace(" ","_")            # pour corriger une erreur : l'espace est interdit dans les tag d'item de canvas !
                    i[1] = x.get().replace(",",".")         # remplace la virgule éventuelle par un point
                    i[2] = y.get().replace(",",".")
                    i[3] = z.get().replace(",",".")
                    i[6] = incertitude.get().replace(",",".")
                    self.listePointsGPS.append(i)
                    
                for e,v in dico.items():

                    if e[2]==i[5] and i[0]!=e[0]:           # l'identifiant du point placé = identifiant du point GCP mais le nom du point est différent
                                                            # cela signifie que l'utilisateur à modifié le nom
                        self.dicoPointsGPSEnPlace[(i[0],e[1],e[2])] = v  # ajout d'une entrée quicorrige cette anomalie (on devrait utiliser l'identifiant...)
                        try:
                            del self.dicoPointsGPSEnPlace[e]  # suppression de l'ancienne entrée
                        except: pass

                    if e[2]==i[5] and i[4]==False:          # si l'identifiant est identique et le point GCP supprimé alors on supprime le point placé
                        try:
                            del self.dicoPointsGPSEnPlace[e]
                        except: pass
            #############################          
            # sur le modèle pythonique l'élément le plus représenté dans une liste l : x=sorted(set(l),key=l.count)[-1]
            # ou pour avoir toute l'info [(valeur,nombre),...] : [(e,a.count(e)) for e in a]
            # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
            # ce bout de code est dupliqué dans controlePointsGPS et actualiseListePointsGPS
            
            listePointsPlaces=[e[0] for e in self.dicoPointsGPSEnPlace] 
            pointsPlaces = [(e,listePointsPlaces.count(e)) for e in listePointsPlaces]
            self.pointsPlacesUneFois = [f[0] for f,g in set([(e,pointsPlaces.count(e)) for e in pointsPlaces]) if g==1]
            self.pointsPlacesUneFois.sort()

            # Nombre de points placés 2 fois ou plus :
            self.pointsPlacesDeuxFoisOuPlus = [f[0] for f,g in set([(e,pointsPlaces.count(e)) for e in pointsPlaces]) if g>1]
            #############################
        
    def placerPointsGPS(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return
        
        self.actualiseListePointsGPS()

        if self.erreurPointsGPS():           
            return
        
        liste = list ([(n,ident) for n,x,y,z,actif,ident,incertitude in self.listePointsGPS if actif])    # listePointsGPS : 7-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant, incertitude)
        if not liste:
            self.infoBulle(_("Définir au moins un point avant de le placer."))
            return
        
        self.messageSiPasDeFichier  = 0                         #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Choisir une photo pour placer les points GCP : "),
                             mode='single',
                             dicoPoints=self.dicoPointsGPSEnPlace)          # dicoPointsGPSEnPlace key = (nom point, photo avec chemin, identifiant), value = (x,y)
        self.messageSiPasDeFichier  = 1
        
        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
		
        # en retour une liste : self.selectionPhotosAvecChemin
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      self.dicoPointsGPSEnPlace,                                        # les points déjà placés key = nom point, photo avec chemin, identifiant
                                      )                                                                 # value = x,y
        if self.calibre:
            self.dicoPointsGPSEnPlace = self.calibre.dicoPointsJPG                                     # si pas de retour !
            
        # referentiel modifié :
        self.referentielOK = False
       
    def erreurPointsGPS(self):          # regarde si la liste des points GCP comporte une erreur : nom absent ou en double, retourne True si erreur
        try: self.bulle.destroy()
        except: pass
        texte = str()
        ensemble=set(e[0] for e in self.listePointsGPS if e[4])     # listePointsGPS : 6-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant, incertitude)
        liste=list(e[0] for e in self.listePointsGPS if e[4])
        if ensemble.__len__()!=liste.__len__():
            texte = _("Impossible : des points portent le même nom : modifier ou supprimer !")
        if "" in ensemble:
            texte = _("Attention : un point n'a pas de nom. ")+texte
        if texte!=str():
            self.infoBulle(texte)
            return True
        return False
        
    def appliquerPointsGPS(self):

        try: self.bulle.destroy()
        except: pass     
        if orientationKO():
            self.infoBulle(_("Lancer d'abord tapioca/tapas") + "\n" + _("pour obtenir un nuage non densifié."))
            return
       
        if self.erreurPointsGPS():                      # erreur : nom en double ou point sans nom, affiche une info bulle, retourne True si pb
            return                 

        if self.controlePointsGPS()==False:               # les points GCP sont assez nombreux et présents sur assez de photos, retourne False si Pb
            self.infoBulle(_("Points GCP non conformes :") + "\n"+self.etatPointsGPS)            
            return
        
        if self.finCalibrationGPSOK()==False:          # création des fichiers xml qui vont bien (dicoAppuis, mesureAppuis) return False si problème
            self.infoBulle(_("Points GCP non conformes :") + "\n"+self.etatPointsGPS)
            return
      
        self.infoBulle(_("Patienter :") + "\n" + _("le nuage est en cours de calibration"))
        self.orientationCourante = "Arbitrary"
        self.lanceGCPBascule()                 # calibration suivant les points GCP
        
       # Apericloud  crée le nuage 3D des points homologues puis visualisation :

        if self.calculNuageNonDense.get():
            self.lanceApericloud()              # création d'un nuage de points 3D
            self.lanceApericloudMeshlab()       # affiche le nuage 3D si il existe

        try: self.bulle.destroy()
        except: pass  
        
############################ Calibration par axe, plan et métrique
           
    def ligneHorizontale(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return              
        liste = ((_("Origine Ox"),1),(_("Extrémité Ox"),2))           # liste de tuple nom du point et identifiant du widget
        self.messageSiPasDeFichier  = 0                         # pour affichage de message dans choisirphoto, difficile a passer en paramètre
        bulles={}
        if self.dicoLigneHorizontale.__len__():
            bulles={list(self.dicoLigneHorizontale.items())[0][0][1]:""} 
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Placer une ligne horizontale sur une seule photo : "),
                             mode='single',
                             dicoPoints=self.dicoLigneHorizontale,
                             bulles=bulles)
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        self.dicoLigneVerticale = dict()                        # on efface le dico vertical (l'un ou l'autre)              
        horizonVierge = dict()
        try:
            if self.selectionPhotosAvecChemin[0]==list(self.dicoLigneHorizontale.items())[0][0][1]:       # si l'image choisie est la même on conserve le dico
                horizonVierge = self.dicoLigneHorizontale                                               # sinon nouveau dico
        except Exception as e: pass
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      horizonVierge,                                                    # aucun point déjà placé
                                      )                                                              # value = x,y
        #il doit y avoir 2 points placés, sinon erreur :
        try:
            if self.calibre.dicoPointsJPG.__len__()!=2:
                self.infoBulle(_("il faut  placer les 2 points."))
                return
        except Exception as e: pass
        try: self.dicoLigneHorizontale = self.calibre.dicoPointsJPG                                     # si pas de retour on saute
        except Exception as e: pass
        
        # referentiel modifié :
        self.referentielOK = False

    def ligneVerticale(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return          
        self.messageSiPasDeFichier  = 0                  #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        bulles={}
        if self.dicoLigneVerticale.__len__():
            bulles={list(self.dicoLigneVerticale.items())[0][0][1]:""}       
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Placer une ligne verticale sur une seule photo :  : "),
                             mode='single',
                             dicoPoints=self.dicoLigneVerticale,
                             bulles=bulles)
        self.messageSiPasDeFichier  = 1
		
        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        self.dicoLigneHorizontale = dict()                                                              # on efface le dico horizontal (l'un ou l'autre)        
        liste = ((_("Origine Oy"),1),(_("Extrémité Oy"),2))                                                   # liste de tuple nom du point et identifiant du widget
        horizonVierge = dict()
        try:
            if self.selectionPhotosAvecChemin[0]==list(self.dicoLigneVerticale.items())[0][0][1]:       # si l'image choisie est la même on conserve le dico
                horizonVierge = self.dicoLigneVerticale                                                 # sinon nouveau dico
        except: pass        
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      horizonVierge,                                                    # aucun points déjà placé 
                                      )                                                                 # value = x,y
        # il doit y avoir 2 points placés, sinon erreur :)
        try:
            if self.calibre.dicoPointsJPG.__len__()!=2:
                self.infoBulle(_("il faut  placer exactement 2 points."))
                return
        except Exception as e: pass
        try: self.dicoLigneVerticale = self.calibre.dicoPointsJPG                                     # si pas de retour !
        except Exception as e: pass
        
       # referentiel modifié :
        self.referentielOK = False

    def planVertical(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return  
        self.messageSiPasDeFichier  = 0
        bulles={}
        if os.path.exists(self.planProvisoireVertical):   
            bulles = {self.monImage_MaitrePlan:_("Plan vertical sur cette photo")}
        if os.path.exists(self.planProvisoireHorizontal):   
            bulles = {self.monImage_MaitrePlan:_("Plan horizontal sur cette photo")}             
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Une photo pour placer le plan vertical : "),
                             mode='single',
                             bulles=bulles)
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        self.saveAvantPlan()    # en cas d'abandon par l'utilisateur permet de restaurer l'état initial       
        self.monImage_MaitrePlan = self.selectionPhotosAvecChemin[0]
        self.planV = TracePolygone(fenetre,
                                   self.monImage_MaitrePlan,
                                   self.planProvisoireVertical,
                                   labelBouton=_("Délimiter un plan vertical"))                                       # L'utilisateur peut tracer le masque sur l'image maitre 
        if not self.planV.polygone:
            self.restaurePlan()

       # referentiel modifié :
        self.referentielOK = False            

    def planHorizontal(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return       
        self.messageSiPasDeFichier  = 0
        bulles={}
        if os.path.exists(self.planProvisoireVertical):   
            bulles = {self.monImage_MaitrePlan:_("Plan vertical sur cette photo")}
        if os.path.exists(self.planProvisoireHorizontal):   
            bulles = {self.monImage_MaitrePlan:_("Plan horizontal sur cette photo")}          
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Une photo pour placer le plan horizontal : "),
                             mode='single',
                             bulles=bulles)
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        self.saveAvantPlan()        # en cas d'abandon par l'utilisateur permet de restaurer l'état initial  
        self.monImage_MaitrePlan = self.selectionPhotosAvecChemin[0]
        self.planH = TracePolygone(fenetre,
                                   self.monImage_MaitrePlan,
                                   self.planProvisoireHorizontal,
                                   labelBouton=_("Délimiter un plan horizontal"))                                       # L'utilisateur peut tracer le masque sur l'image maitre 
        if not self.planH.polygone:
            self.restaurePlan()

       # referentiel modifié :
        self.referentielOK = False
            
    def saveAvantPlan(self):
        self.saveMaitre = str()
        if os.path.exists(self.planProvisoireHorizontal): (os.replace(self.planProvisoireHorizontal,self.savePlanH))
        if os.path.exists(self.planProvisoireVertical): (os.replace(self.planProvisoireVertical,self.savePlanV))
                                                         
    def restaurePlan(self):
        self.monImage_MaitrePlan = str(self.saveMaitre)
        if os.path.exists(self.savePlanH): (os.replace(self.savePlanH,self.planProvisoireHorizontal))
        if os.path.exists(self.savePlanV): (os.replace(self.savePlanV,self.planProvisoireVertical))

        
    def placer2Points(self):
        if self.photosAvecChemin.__len__()==0:
            self.infoBulle(_("Choisir d'abord les photos du chantier."))
            return  
        liste = (("Début",1),("Fin",2))                                                   # liste de tuple nom du point et identifiant du widget
        self.messageSiPasDeFichier  = 0
        self.choisirUnePhoto(
                             self.photosAvecChemin,
                             message=_("Choisir deux fois une photo pour placer les 2 points  : "),
                             mode='single',
                             dicoPoints=self.dicoCalibre)
        self.messageSiPasDeFichier  = 1
        
        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        
        #Question : il ne faut pas plus de 2 photos avec une distance : s'il s'agit d'une troisième alors on arrête tout :
        
        photosAvecDistance = list(set([os.path.basename(e[1]) for e in self.dicoCalibre.keys() ]))
        ajout(photosAvecDistance,os.path.basename(self.selectionPhotosAvecChemin[0]))

        if photosAvecDistance.__len__()>2:
            self.infoBulle(_("Il y a dèjà 2 images avec des points 'distance'. Supprimer les points sur une des 2 images."))
            return
        
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      self.dicoCalibre                                                  # les points déjà placés key = nom point, photo, identifiant
                                      )                                                                 # value = x,y
        try: self.dicoCalibre = self.calibre.dicoPointsJPG                                              # si pas de retour !
        except: pass
        
       # referentiel modifié :
        self.referentielOK = False        
       
    ################################## LANCEMENT DE MICMAC ########################################################### 
        
    def lanceMicMac(self):          # controles puis Aiguillage en fonction de l'etatDuChanteir
        if self.etatDuChantier==5:  # Chantier terminé
            self.encadre(_("Le chantier %s est terminé après %s") % (self.chantier,self.choixDensification.get()) + ".\n\n"+
                         _("Vous pouvez modifier les options puis relancer MicMac."))
            return
        self.encadre(_("Lance MicMac : controles en cours....")+"\n")   
    # réinitialisation des variables "locales" définies dans le module

        self.zoomI = ""     # pour Malt, inutilisé pour l'instant (voir ZoomIPerso)
   
    # Vérification de l'état du chantier :

    # si pas de photo ou pas de répertoire micmac : retour :
        if self.pasDePhoto():return        
        if self.pasDeMm3d():return
        if self.pasDeExiftool():return
    # Photos ajoutées ou retirées
        if not self.controleCoherenceFichiers():
            message = str()
            if self.jpgAjoutVrai:
                message += _("Des photos ont été ajoutées dans le répertoire du chantier :")+"\n\n"+"\n".join(self.jpgAjoutVrai)+"\n\n"
            if self.jpgRetrait:
                message += _("Des photos ont été retirées dans le répertoire du chantier :")+"\n\n"+"\n".join(self.jpgRetrait)
            message=_("Le répertoire du chantier a été modifié par ajout/retrait de photos.")+"\n\n"+message
            message+="\n\n"+_("solution : Définir un nouveau chantier")
            self.encadre(message)
            return                    
    # controle que les options sont correctes (toutes, même si elles ne doivent pas servir)
    
        retour = self.controleOptions()
        if retour!=True:
            self.encadre(_("Options incorrectes : corriger") + "\n\n"+retour)
            return            
    #  pas assez de photos choisies :
    
        if self.photosAvecChemin.__len__()==2:
            message = _("Avec 2 photos MicMac construira difficilement un nuage de point dense.") + "\n" + _("Utiliser l'échelle -1 dans Tapioca pour obtenir un nuage optimal.") + "\n"   
            retour = self.troisBoutons(titre=_('Avertissement : 2 photos seulement'),
                              question=message,
                                b1=_('Continuer'),b2=_('Abandon'),b3=None)   # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1,
            if retour != 0:
                self.afficheEtat()
                return         

    # pas assez de photos si on retire les photos pour calibration (pour tapas):
        if self.etatDuChantier<=2:
            if self.calibSeule.get():
                nbPhotosPourTapas = self.photosAvecChemin.__len__() - self.photosPourCalibrationIntrinseque.__len__()
                if nbPhotosPourTapas<2:
                    message = _("Nombre de photos insuffisant après retrait des photos pour la calibration : ")+str(nbPhotosPourTapas)
                    self.encadre(message,)
                    return
                
    # les photos de calibration retirées ne doivent pas servir après : mise à l'échelle, points gps, maitresses
    
        if self.calibSeule.get() and self.photosPourCalibrationIntrinseque: # les photos de calibration sont uniquement pour calibration
            calibSansChemin =       set([os.path.basename(e) for e in self.photosPourCalibrationIntrinseque])
            maitressesSansChemin =  set([os.path.basename(e) for e in self.listeDesMaitresses])
            photosAvecPointsGPS =   set([os.path.basename(e[1]) for e in self.dicoPointsGPSEnPlace.keys()])
            photosAvecLigneH =      set([os.path.basename(e[1]) for e in self.dicoLigneHorizontale.keys()])
            photosAvecLigneV =      set([os.path.basename(e[1]) for e in self.dicoLigneVerticale.keys()])
            photosAvecDistance =    set([os.path.basename(e[1]) for e in self.dicoCalibre.keys()])
            
            if calibSansChemin.intersection(maitressesSansChemin):
                message = ( _("Une ou plusieurs photos maitresses ne sont utilisées que pour la calibration : ")+
                            str(calibSansChemin.intersection(maitressesSansChemin))+"\n"+
                            _("Supprimer l'image maitresse"))
                self.etatDuChantier = 3     # pour autoriser l'accès aux options
                self.encadre(message,)
                return
            
            if self.monImage_MaitrePlan:
                if os.path.basename(self.monImage_MaitrePlan) in calibSansChemin: 
                    message = ( _("La photo utilisée pour définir le plan de mise à l'échelle n'est pas utilisable : elle ne sert que pour la calibration  : ")+
                                str(os.path.basename(self.monImage_MaitrePlan))+"\n"+
                                _("Utiliser une autre photo."))
                    self.etatDuChantier = 3     # pour autoriser l'accès aux options
                    self.encadre(message,)
                    return

            if calibSansChemin.intersection(photosAvecLigneH):
                    message = ( _("La photo utilisée pour définir la ligne horizontale de mise à l'échelle n'est pas utilisable : elle ne sert que pour la calibration  : ")+
                                str(photosAvecLigneH)+"\n"+
                                _("Utiliser une autre photo."))
                    self.etatDuChantier = 3     # pour autoriser l'accès aux options
                    self.encadre(message,)
                    return                

            if calibSansChemin.intersection(photosAvecLigneV):
                    message = ( _("La photo utilisée pour définir la ligne verticale de mise à l'échelle n'est pas utilisable : elle ne sert que pour la calibration  : ")+
                                str(photosAvecLigneV)+"\n"+
                                _("Utiliser une autre photo."))
                    self.etatDuChantier = 3     # pour autoriser l'accès aux options
                    self.encadre(message,)
                    return
                                   
            if calibSansChemin.intersection(photosAvecDistance):
                    message = ( _("Les photos utilisées pour définir la distance de mise à l'échelle ne sont pas toutes pas utilisables : elles ne servent que pour la calibration  : ")+
                                str(calibSansChemin.intersection(photosAvecDistance))+"\n"+
                                _("Utiliser d'autres photos."))
                    self.etatDuChantier = 3     # pour autoriser l'accès aux options
                    self.encadre(message,)
                    return

            if calibSansChemin.intersection(photosAvecPointsGPS):
                    message = ( _("Les photos utilisées pour les points GPS ne sont pas toutes pas utilisables : certaines ne servent que pour la calibration  : ")+
                                str(calibSansChemin.intersection(photosAvecPointsGPS))+"\n"+
                                _("Utiliser d'autres photos."))
                    self.etatDuChantier = 3     # pour autoriser l'accès aux options
                    self.encadre(message,)
                    return
                
    # il faut au moins deux photos calibration par appareil photo : vérification
    
        if len(self.photosPourCalibrationIntrinseque)==1: #une seule photo pour la calibration : cela ne marche pas
            message = _("Une seule photo pour la calibration intrinsèque de l'appareil photo. C'est insuffisant.\n")+\
            _("Modifier la liste des photos pour calibration.")
            self.encadre(message)
            return
        nbAppareils = self.nombreDeExifTagDifferents("Model")
        # si un seul appareil : pas de message initial, message final si pas de résultat
      
        if nbAppareils>1:     # plusieurs appareils photos, calibration nécessaire, liste des appareils dans self.lesTags        
            if self.photosPourCalibrationIntrinseque:
                nb = dict()
                message = str()           
                for appareil in self.lesTags:
                    nb[appareil] = 0
                for photo in self.photosCalibrationSansChemin:
                    appareil = self.tagExif("Model",photo)
                    nb[appareil] += 1
                for a in nb:
                    if nb[a]==1:
                        message += _("Une seule photo pour la calibration de l'appareil ")+a+" "+_("c'est insuffisant.\n")
                    if nb[a]==0:
                        message += _("Aucune photo pour la calibration de l'appareil ")+a+" "+_("c'est insuffisant.\n")
                if message:
                    message += "\n\n "+_("Modifier la liste des photos pour calibration.")
                    message += "\n\n "+_("Le menu 'expert/liste des appareils' fournit le nom de l'appareil pour chaque photo.")                    
                    self.encadre(message)
                    return                
            else:     # Plusieurs appareils et Aucune photo pour calibration intrinsèque
                 if len(self.photosPourCalibrationIntrinseque)==0:
                    message = _("Aucune photo pour la calibration intrinsèque des ")+str(nbAppareils)+" "+_("appareils photos.")+\
                              "\n"+_("Cela peut rendre difficile les traitements.")+\
                              "\n\n"+_("Conseil : prendre 2 photos pour la calibration de chaque appareil.")
                    self.ajoutLigne(message)
                    retour = self.troisBoutons(titre=_('Avertissement'),question=message,b1=_('Continuer'),b2=_('Abandon'),b3=None)
                    if retour != 0:
                        self.afficheEtat()
                        return
                
    # pas enregistré : on enregistre on poursuit
    
        if self.etatDuChantier==1:                              # Des photos mais fichier paramètre non encore enregistré, on enregistre et on poursuit
            self.enregistreChantier()                           # sauvegarde du fichier paramètre sous le répertoire du chantier : modif etatduchantier = 2

    # Les photos sont-elles correctes ?

        self.encadre(_("Controle des photos en cours....\nPatienter jusqu'à la fin du controle."))
        self.controlePhotos()   # positionne self.dimensionsOK self.nbFocales
        self.menageEcran()

        message = str()
        if self.dimensionsOK==False:
            message = "\n" + _("Les dimensions des photos ne sont pas toutes identiques.") + "\n"+\
                      _("Le traitement par MicMac est incertain.") + "\n"+\
                      "\n".join([ a+" : "+str(b[0])+" "+str(b[1]) for a, b in self.dimensionsDesPhotos])
            retour = self.troisBoutons(titre=_('Avertissement'),question=message,b1=_('Continuer'),b2=_('Abandon'),b3=None)
            if retour != 0:
                self.afficheEtat()
                return            

        if self.nbFocales==0:               
            retour = self.troisBoutons(titre=_('Absence de focales'),
                              question=_("Certaines photos n'ont pas de focales.") + "\n"+
                                _("Le traitement echouera probablement.") + "\n"+
                                _("Mettre à jour les exifs (menu Outils/mettre à jour l'exif des photos)"),
                                b1=_('Continuer'),b2=_('Abandon du traitement'),b3=None)   # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1,
            if retour != 0:
                self.afficheEtat()
                return            

            
        if self.nbFocales>1 and self.etatDuChantier<3 :
            if self.calibSeule.get()==False:    # plusieurs focales et pas de calibration
                message = _("Les focales des photos ne sont pas toutes identiques.") + "\n"+\
                      _("Dans ce cas une calibration est souhaitable pour chaque focale.")
                retour = self.troisBoutons(titre=_('Avertissement'),question=message,b1=_('Continuer'),b2=_('Abandon du traitement'),b3=None)
                if retour != 0:
                    self.afficheEtat()
                    return

        if self.photosSansChemin.__len__()<2:
            message += _("Pas assez de photos pour le traitement : il en faut au moins 2.")
            self.encadre(message)
            return

        # EtatDuChantier :
        # 0 : pas encore de photos
        # 1 : il y a des photos choisies
        # 2 : des photos, enregistré                              
        # 3 en cours d'exécution de Tapioca/Tapas, a sans doute planté pendant
        # 35 Chantier arrêté aprés tapioca, points homoloques conservés
        # 4 arrêt après tapas,
        # 5 terminé après malt ou c3dc,
        # 6 terminé, redevenu modifiable (??)
        # 7 : la densification a échoué
                     
    # anormal : chantier planté lors de la dernière éxécution de tapioca/Tapas : on propose le déblocage mais on sort dans tous les cas
                
        if self.etatDuChantier==3:	# En principe ne doit pas arriver : plantage en cours de tapas ou Tapioca
            retour = self.troisBoutons(  titre=_("Le chantier %s a été interrompu lors de Tapioca/Tapas.") % (self.chantier),
                                         question=_("Le chantier est interrompu.") + "\n" + _("Vous pouvez le débloquer,")+
                                         _( "ce qui permettra de modifier les options et de le relancer.") + "\n",
                                         b1=_('Débloquer le chantier- effacer les points homologues'),
                                         b2=_('Débloquer le chantier- conserver les points homologues'),
                                         b3=_('Abandon'))
            if retour==-1 or retour==2:                         # 2 ou -1 : abandon ou fermeture de la fenêtre par la croix
                return
            if retour==0:
                self.nettoyerChantier()                          # etat = 2 :  chantier est noté comme de nouveau modifiable, les points homologues sont supprimés
                self.afficheEtat(_("Chantier %s de nouveau modifiable, paramètrable et exécutable pour la recherche des points homologues.") % (self.chantier))                
                return
            if retour==1:
                self.nettoyerChantierApresTapioca()             # etat = 35 le chantier est noté comme de nouveau modifiable, les points homologues sont conservés
                self.afficheEtat(_("Chantier %s de nouveau modifiable, paramètrable et exécutable à partir de l'orientation.") % (self.chantier))                
                return
            
    # anormal : chantier planté lors de la dernière éxécution de Malt/c3dc : on propose le déblocage mais on sort dans tous les cas
                
        if self.etatDuChantier==7:	# La densification a échoué 
            retour = self.troisBoutons( titre=_("Le nuage dense n'a pas été créé."),
                                        question=_("Le chantier est interrompu sans nuage dense")      + "\n" +
                                        _("Pour abandonner fermer cette fenêtre")+ "\n" ,
                                         b1=_('Lancer la densification '),
                                         b2=_('débloquer le chantier - effacer les points homologues'),
                                         b3=_('débloquer le chantier - garder les points homologues'))
            if retour==-1:                                  # 1 ou -1 : abandon ou fermeture de la fenêtre par la croix
                return
            
            if retour==0:            
                self.ajoutLigne(heure()+_("Reprise de la densification, après un premier échec de la densification.")+ "\n")
                self.nettoyerChantierApresTapas()
                self.cadreVide()    # début de la trace                
                self.suiteMicmac()                              # on poursuit par Malt ou C3DC
                return
            if retour==1:                                       # b2 : débloquer le chantier, effacer les points homologues
                self.nettoyerChantier()                         # self.etatDuChantier remis à 2
                self.afficheEtat(_("Chantier réinitialisé : points homologues effacés.")+ "\n")
                return

            if retour==2:                                       # b3 : débloquer le chantier, conserver les points homologues
                self.nettoyerChantierApresTapioca()             # l'etatDuChantier passe à 35 ! prochain départ : Tapas
                self.afficheEtat(_("Chantier réinitialisé aprés Tapioca : points homologues conservés.")+ "\n")
                return 

    # Chantier arrété après tapas : l'utilisateur a pu modifier les options et veut continuer ou reprendre au début suivant les résultats
    # poursuite du traitement ou arrêt suivant demande utilisateur

        if self.etatDuChantier==4:                              # Chantier arrêté après Tapas
            
            retour = self.troisBoutons(  titre=_('Continuer le chantier %s après tapas ?') % (self.chantier),
                                         question =  _("Le nuage non dense de l'orientation est créé. Vous pouvez :") + "\n "+
                                                     _("- lancer la densification") + "\n "+
                                                     _("- débloquer le chantier pour modifier les options des points homologues") + "\n "+
                                                     _("- conserver les points homologues et modifier les paramètres de l'orientation") + "\n"+
                                         _("- ne rien faire : cliquer sur la croix de fermeture de la fenêtre") + "\n ",                                         
                                         b1=_('Lancer la densification '),
                                         b2=_('débloquer le chantier - effacer les points homologues'),
                                         b3=_('débloquer le chantier - garder les points homologues'))
            if retour == -1:                                    # fermeture de la fenêtre
                self.afficheEtat()
                return
            if retour == 0:                                     # b1 : Lancer la densification                  
                self.ajoutLigne(heure()+" "+_("Reprise du chantier %s arrêté après TAPAS - La trace depuis l'origine sera disponible dans le menu édition.") % (self.chantier))
                self.cadreVide()                                # début de la trace : fenêtre texte pour affichage des résultats. 
                self.suiteMicmac()                              # on poursuit par Malt ou C3DC
                return

            if retour==1:                                       # b2 : débloquer le chantier, effacer les points homologues
                self.nettoyerChantier()                         # l'état du chantier passe à 2 !
                self.afficheEtat(_("Chantier réinitialisé. Points homologues effacés."))
                return

            if retour==2:                                       # b3 : débloquer le chantier, conserver les points homologues
                self.nettoyerChantierApresTapioca()             # l'etatDuChantier passe à 35 : Chantier arrêté arrété aprés tapioca, points homoloques conservés
                self.afficheEtat()
                return 

        if self.etatDuChantier==35:                              # Chantier arrété aprés tapioca, points homoloques conservés
            retour = self.troisBoutons(  titre=_('Continuer le chantier %s après recherche des points homologues ?') % (self.chantier),
                                         question =  _("Le chantier est arrêté après la recherche des points homologues. Vous pouvez :") + "\n "+
                                                     _("- relancer la recherche des points homologues") + "\n "+
                                                     _("- rechercher l'orientation des appareils photos") + "\n "+
                                                     _("- ne rien faire : cliquer sur la croix de fermeture de la fenêtre") + "\n",                                         
                                         b1=_('Recherche des points homologues'),
                                         b2=_("Recherche de l'orientation"),
                                         b3=_('Abandon'))        
            if retour==-1 or retour==2:                         # 2 ou -1 : abandon ou fermeture de la fenêtre par la croix
                return
            if retour==0 :                                      # b1 : recherche des points homologues : on met l'état à 2 (avec photo, enregistré)
                self.nettoyerChantier()

            # poursuite du traitement : remettre les photos de calibration sous le répertoire de travail
            
            # si retour == 1 : on laisse l'étatduchantier à 35 : Chantier arrêté arrété aprés tapioca, points homoloques conservés, le temps de sauter tapioca
        
        # L'état du chantier est prêt pour l'exécution de Tapioca (2) ou débloqué (6) : sauvegarde des paramètres actuels puis traitement

        if self.etatDuChantier!=35:    # 35 = Chantier arrêté arrété aprés tapioca, points homoloques conservés
            self.sauveParam()

            # Vérification que les photos, les options et les paramètres  autorisent l'exécution, sinon exit ATTENTION : on efface tout avant de recopier les photos
            
            retourAvantScene = self.avantScene()                    # Efface tout, Prépare le contexte,
                                                                    # crée le répertoire de travail, efface et ouvre les traces

            if retourAvantScene!=None:                              # Préparation de l'éxécution de MicMac
                texte = _("Pourquoi MicMac s'arrête : ") + "\n"+retourAvantScene
                self.encadreEtTrace(texte)                          # si problème arrêt avec explication
                return

            # Prêt : modification de l'état, lancement du premier module Tapioca (recherche des points homologues) arrêt si pas de points homologues
           
            self.etatDuChantier = 3		                        # trés provisoirement (en principe cette valeur est transitoire sauf si avantScène plante)
            self.lanceTapioca()

        # tapioca a-t-il trouvé des points homologues ?
        
        if  not os.path.exists("Homol"):                         # le répertoire Homol contient les points homologues, si absent, pas de points en correspondancce
            message = _("Pourquoi MicMac s'arrête : ") + "\n"+_("Aucun point en correspondance sur 2 images n'a été trouvé par Tapioca.") + "\n\n"+\
                      _("Parmi les raisons de cet échec il peut y avoir :") + "\n"
            if self.photosSansChemin.__len__()>200:
                message += _("Le chantier comporte trop de photos : %s") % (self.photosSansChemin.__len__()) + "\n"+\
                           _("Les maximum connus sont de l'ordre de 250 sous Windows, 400 sous Linux") + "\n\n"
            message +=  _("soit les photos ne se recouvrent pas du tout") + "\n+" +\
                        _("soit l'exif des photos ne comporte pas la focale ou plusieurs focales sont présentes") + "\n+" +\
                        _("Soit l'appareil photo est inconnu de Micmac") + "\n"+\
                        _("soit la qualité des photos est en cause.") + "\n\n"+\
                        _("soit la trace compléte contient : 'Error: -- Input line too long, increase MAXLINELENGTH' .") + "\n\n"+\
                        _("alors tenter, sans certitude, de modifier le fichier /binaire-aux/windows/startup/local.mk") + "\n\n"+\
                        _("Utiliser les items du menu 'outils' pour vérifier ces points.") + "\n\n"
            self.ajoutLigne(message)
            self.messageNouveauDepart =  message
            self.nouveauDepart()                                # lance une fenêtre nouvelle sous windows (l'actuelle peut-être polluée par le traitement) Ecrit la trace  
            return

        # Tapioca a bien trouvé des points homologues : concernant-ils une seule scène ?
        rep="Homol_SRes" if self.modeTapioca.get()=="MulScale" else "Homol"
        if self.plusieursScenes(rep):
            # Plusieurs scènes : demande à l'utilisateur : que faire : continuer avec la plus nombreuse ou abandonner ?
            if self.continuerSurUnGroupe():
                message = "\n"+_("Plusieurs scènes dans les photos. L'utilisateur décide de continuer avec la plus nombreuse.")
                self.ajoutLigne(message)
                if self.modeTapioca.get()=="MulScale":
                    self.menageEcran()                                      # ménage écran        
                    self.cadreVide()                                        # fenêtre texte pour affichage des résultats.           
                    self.lanceTapioca()
            else:
                message = _("Pourquoi MicMac s'arrête : ") + "\n"+_("Les photos définissent plusieurs scènes disjointes") + "\n\n"+\
                          _("MicMac ne peut travailler que sur une seule scène : toutes les photos doivent former une seule scéne.") + "\n"+\
                          _("Les photos se répartissent en :") + str(self.lesGroupesDePhotos.__len__())+" "+_("groupes distincts (consulter la trace) : ")+"\n" +\
                          "\n".join([str(e)[:100] for e in self.lesGroupesDePhotos])            
                self.ajoutLigne(message)
                self.messageNouveauDepart =  message
                self.nouveauDepart()                                # lance une fenêtre nouvelle sous windows (l'actuelle peut-être polluée par le traitement) Ecrit la trace              
                return
        # points homologues trouvés, corrects, second module : Tapas positionne les prises de vue dans l'espace
        # Tapas prend en compte les photos pour la calibration
        # Tapas, si tout va bien, fournit au final une orientation : Arbitrary
        
        self.lanceTapas()
        
        if self.messageRetourTapas:
            self.ajoutLigne(self.messageRetourTapas)
            self.encadre(self.messageRetourTapas)
            return
        
        if os.path.isdir("Ori-Arbitrary")==False:               # Tapas n'a pu mettre en correspondance aucun point entre deux images : échec
            message = _("Pourquoi MicMac s'arrête :") + "\n\n"+self.messageRetourTapas +"\n\n" + _("consulter la trace.")
            self.ajoutLigne(message)
            self.ecritureTraceMicMac()                          # on écrit les fichiers trace
            self.sauveParam()
            self.messageNouveauDepart =  message
            self.nouveauDepart()                                # lance une fenêtre nouvelle sous windows (l'actuelle peut-être polluée par le traitement) Ecrit la trace  
            return
        
        # Tapas OK, orientation trouvée, on applique un référentiel (mise à l'échelle, points GCP ou GPS embarqué) sur "Arbitrary"

        self.referentiel()                                      # mise à l'échelle, points GCP ou BPS embarqué

        # troisième module facultatif : Apericloud  crée le nuage 3D des points homologues puis visualisation :
        
        if self.calculNuageNonDense.get():
            self.lanceApericloud()              # création d'un nuage de points 3D
            self.lanceApericloudMeshlab()       # affiche le nuage 3D si il existe

        # Situation stable, orientation trouvée, changement d'état : 4 = Tapioca et Tapas exécutés, sauvegarde des paramètres

        if orientationOK():   
            self.etatDuChantier = 4		                # état du chantier lors de l'arrêt après tapas
        self.copierParamVersChantier()                          # sauvegarde du fichier paramètre sous le répertoire du chantier        
        self.ecritureTraceMicMac()                              # on écrit les fichiers trace

        # tarama ?
        if self.lancerTarama.get():                             # mosaïque ?
            self.lanceTarama()
            
        # Faut-il poursuivre ?
      
        if self.arretApresTapas.get():                         # L'utilisateur a demandé l'arrêt
            ligne="\n" + _("Arrêt après Tapas ")+heure()+_(". Lancer MicMac pour reprendre le traitement.") + "\n"              
            ligne=ligne+"\n\-------------- " + _("Arrêt après Tapas sur demande utilisateur") + " --------------\n\n"        
            self.ajoutLigne(ligne)
            self.nouveauDepart()                                # sauvegarde les paramètres, écrit la trace, relance "interface" si on est sous nt
            return
        else:
            self.suiteMicmac()                                  # PoursSuite : Malt ou C3DC, pouvant être appelé directement
            
    # Controle si les points homologues définissent plusieurs scènes : si oui : message dans la trace et retour True.
    # le répertoire des points homologues est Homol par défaut ; lors de l'appel après Tapioca MulScale première étape le répertoire est homol_SRes

    def plusieursScenes(self,rep="Homol"):
        nbGroupes = self.regroupementSuivantPointsHomologues(rep)
        if nbGroupes>1 :
            self.ajoutLigne("\n"+_("Les photos représentent plusieurs scènes disjointes.\nLes groupes de photos séparés : ")
                            +"\n"+"\n".join([str(e) for e in self.lesGroupesDePhotos])+"\n")
            
            self.ecritureTraceMicMac()
            return True
        
    def continuerSurUnGroupe(self):
        # 1) trier du plus long au plus petit,
        self.lesGroupesDePhotos.sort(key = lambda e: e.__len__(), reverse=True)
        message =   _("Les photos se répartissent en plusieurs groupes distincts (consulter la trace) :\n\n")+\
                      "\n".join([str(e) for e in self.lesGroupesDePhotos])+\
                    "\n\n"+_("Voulez-vous poursuivre l'éxécution sur le groupe le plus nombreux ?")+\
                    "\n"+_("Si oui les photos inutilisées seront supprimées et le chantier se poursuivra.")
        if MyDialog_OK_KO(fenetre,titre=_("Poursuivre sur moins de photos ou abandonner ?"),texte=message,b1="Continuer",b2="Abandon").retour==1:
            # 2) retirer les groupes sauf le plus long 
            [self.retirerPhotos(e) for e in self.lesGroupesDePhotos[1:]]
            return True
        
    def suiteMicmac(self):  # poursuite après tapas : génération d'un nuage dense 

        # Mise à jour du référentiel (Mise à l'échelle, points GCP ou GPS embarqué ) :

        self.referentiel()
        
        # on ne peut poursuivre que si l'orientation a été trouvée", et une image maîtresse si malt geomimage

        if orientationKO():
            ligne = (_("Tapas n'a pas trouvé d'orientation.") + "\n"+
                     _("Le traitement ne peut se poursuivre.") + "\n"+
                     _("Consulter l'aide/quelques conseils.") + "\n"+                     
                     _("Vérifier la qualité des photos, modifier les paramètres et relancer tapioca-tapas"))
            self.ajoutLigne(ligne)
            self.encadre(ligne)
            return

        if self.choixDensification.get()=="Malt" and not self.existeMaitre2D(): # existeMaitre2D = True si malt geomimage
            ligne = (_("Pas d'image maîtresse pour Malt option geoimage.") + "\n"+
                     _("Le traitement ne peut se poursuivre.") + "\n"+
                     _("Définir une image maîtresse") +"\n"+                     
                     _("ou Changer le mode 'GeomImage' qui impose une image maîtresse") )
            self.ajoutLigne(ligne)            
            self.encadre(ligne)
            return
               
##        # calibrage de l'orientation suivant des points GCP (possiblement modifiés après tapas)
##        # si il existe un fichier XML de points d'appuis : self.mesureAppuis
##              
##        if os.path.exists(self.mesureAppuis):
##            self.orientationCourante = "Arbitrary"
##            self.lanceGCPBascule()

        # recherche le nom du modele3D a créer

        self.modele3DSuivant()
        
        # malt ou D3CD 
        # la production sera self.modele3DEnCours
        
        if self.choixDensification.get()=="C3DC":                               
            self.lanceC3DC()                                    # C3DC crée directement le fichier self.modele3DEnCours
        else:
            self.suiteMicmacMalt()

        # Final : affichage du self.modele3DEnCours, sauvegarde, relance la fenêtre qui a pu être dégradé par le traitement externe

        retour = self.ouvreModele3D()
        texte = ""
        if  retour == -1 :
            if self.choixDensification.get()=="C3DC":    
                texte = _("Pas de nuage de points après C3DC %s.") % (self.modeC3DC.get()) +"\n"+"\n"
                if self.modeC3DC.get()!="BigMac":
                    texte += _("L'usage de photos spécifiques pour calibrer l'appareil photo permet parfois l'obtention d'un nuage dense..")+"\n"+"\n"                    
                    texte += _("Sinon : Essayer de modifier l'option de C3DC : choisir 'BigMac' (sans drapage).")+"\n"+"\n"
                texte += _("Essayer Malt, option ortho si la scène est 'plate' (terrain, façade)")+"\n"
                texte += _("option geoImage si la scène est un objet (statue...)")+"\n"+"\n"
            elif self.modeCheckedMalt.get():
                texte = _("Pas de nuage de points après MALT %s.") % (self.modeCheckedMalt.get())
                texte += _("Essayer Malt avec une autre option ou C3DC option BigMac")+"\n"
            texte += _("Consulter l'aide (menu Aide/Quelques conseils) et la trace.")
            self.etatDuChantier = 7     # 7 : chantier terminé sans génération de nuage dense
        else:
            self.etatDuChantier = 5     # 5 : chantier terminé OK            
        if retour == -2 :
            texte = _("Programme pour ouvrir les .PLY non trouvé.")        
        ligne = texte + "\n\n-------------- " + _("Fin du traitement MicMac ")+heure()+" --------------\n\n"       
        self.ajoutLigne(ligne)
        self.messageNouveauDepart =  texte
        self.nouveauDepart()        # sauvegarde les paramètres, écrit la trace, relance "interface" si on est sous nt (nécessaire : suiteMicmac doit être autonome)
        
    # Que faire après Tapioca et Tapas ? Densification : malt ou D3DC
        
    def suiteMicmacMalt(self):

        if self.etatDuChantier!=4:  	                        # en principe inutile : il faut être juste après tapas 
            self.ajoutLigne(_("Tapas non effectué, lancer MicMac depuis le menu. Etat du chantier = "),self.etatDuChantier)
            return

        # il faut une image maîtresse si le mode est geoimage

        if self.listeDesMaitresses.__len__()==0 and self.modeCheckedMalt.get()=="GeomImage":    # self.photoMaitre : nom de la photo sans extension ni chemin, l'extension est dans self.extensionChoisie
            message = ( _("Pourquoi MicMac est arrêté :")+
                        "\n" + _("Pas d'image maîtresse.")+
                        "\n" + _("Celle-ci est nécessaire pour l'option choisie geomImage de Malt.")+
                        "\n" + _("Pour corriger modifier les options de Malt ou choisissez un masque 3D avec C3DC.")+
                        "\n" + _("Corriger."))
            self.ajoutLigne(message)                
            self.ecritureTraceMicMac()
            self.afficheEtat(message)
            return 

        # mise à jouor du réferentiel si besoin (points gcp, mise à l'échelle, points gps embarqués)

        self.referentiel()

        # si le mode est  UrbanMNE ou Ortho on lance simplement Malt

        if self.modeCheckedMalt.get() in ("UrbanMNE","Ortho"):
            self.lanceMalt()
            self.lanceTawny()
            self.tousLesNuages()
            
             # création de modele3D.ply (self.modele3DEnCours= dernier ply généré par tousLesNuages)
            try: shutil.copy(self.modele3DEnCours,self.modele3DFinal)
            except Exception as e: self.ajoutLigne(_("Erreur copie modele3D.ply")+"\n"+str(e)+"\n")
            self.modele3DEnCours = self.modele3DFinal           # nécessaire pour l'affichage           
            return             

        # si le mode est GeomImage il faut lancer Malt sur chaque Image Maitresse et préparer le résultat

        # Cas GeomImage : il faut traiter toutes les images maitresses :

        if self.modeCheckedMalt.get() in ("GeomImage"):
            self.nuagesDenses = list()                          # liste des nuages denses de tous les masques pour fusion en fin de boucle
            for e in self.listeDesMaitresses:
                self.maitreSansChemin = os.path.basename(e)
                self.MasqueXML()                                # préparation du masque et du maitre
                self.lanceMalt()                                # création du nuage de points
                self.tousLesNuages()                            # création des .ply à tous les niveaux, ajout du plus dense dans la liste
                ajout(self.nuagesDenses,self.modele3DEnCours)   # le dernier modele3dEncours est le plus dense

            # création de modele3D.ply
            self.modele3DEnCours = self.modele3DFinal           # nécessaire pour l'affichage       
            if self.nuagesDenses.__len__()==1:
                try: shutil.copy(self.nuagesDenses[0],self.modele3DEnCours)
                except Exception as e: print(_("erreur malt GeomImage copy de nuage en modele3D : "),str(e)," "+_("pour : "),self.nuagesDenses[0])
            else:            
                try: self.fusionnerPly(self.nuagesDenses,self.modele3DEnCours)     
                except Exception as e: print(_("erreur malt GeomImage fusion des nuages en modele3D : "),str(e)," "+_("pour : "),"\n".join(self.nuagesDenses[0]))
                
    ################################## LES DIFFENTES PROCEDURES MICMAC ###########################################################       

    # ------------------ PREAMBULE --------------------

    def avantScene(self):

        # initialisations 
        self.ecritureTraceMicMac()                              # écriture puis raz de ce qui traîne dans les buffers 
        self.menageEcran()                                      # ménage écran        
        self.cadreVide()                                        # fenêtre texte pour affichage des résultats.

        # vérification nécessaires :
        
        if len(self.photosAvecChemin)==0:                       # photos sans chemin
            texte=_('Aucune photo choisie. Abandon.')
            return texte
        
        if len(self.photosAvecChemin)==1:                       # photos sans chemin
            texte=_('Une seule photo choisie. Abandon.')
            return texte
        retour = self.controleOptions()
        if retour!=True:
            return "\n" + _("Option incorrecte :") + "\n"+str(retour)
                 
        self.lignePourTrace = ("-------------- " + _("TRACE DETAILLEE") + " --------------\n") # première ligne de la trace détaillée        
        self.ligneFiltre = ("-------------- " + _("TRACE SYNTHETIQUE") +  " --------------\n")  # première ligne de la trace synthétique
        
        texte = "-------------- " + _("DEBUT DU TRAITEMENT MICMAC à ")+ heure()+" -------------- \n\n"

        photosPropres=list([os.path.basename(x) for x in self.photosAvecChemin])
        texte = texte+_('Photos choisies :') + " \n\n"+'\n'.join(photosPropres)+'\n\n'           
        texte = texte+_("Ces photos sont recopiées dans le répertoire du chantier :") + "\n\n"+self.repTravail+'\n\n'  
        self.ajoutLigne(texte)



    # ------------------ TAPIOCA --------------------
    
    
    def lanceTapioca(self):
        self.etapeTapioca = 0
        if self.modeTapioca.get()=="All":
            self.echelle1PourMessage = self.echelle1.get()
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle1.get(),
                       self.tapiocaAllPerso.get(),                        
                       "ExpTxt="+self.exptxt,
                       ]
            
        if self.modeTapioca.get()=="MulScale":
            self.echelle1PourMessage = self.echelle2.get()
            self.echelle2PourMessage = self.echelle3.get()            
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle2.get(),      
                       self.echelle3.get(),
                       self.tapiocaMulScalePerso.get(),                        
                       "ExpTxt="+self.exptxt,
                       "NbMinPt=5"
                       ]
            
        if self.modeTapioca.get()=="Line":
            self.echelle1PourMessage = self.echelle4.get()            
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle4.get(),               
                       self.delta.get(),
                       self.tapiocaLinePerso.get(),                       
                       "ExpTxt="+self.exptxt]
            
        self.lanceCommande(tapioca,
                           filtre=self.filtreTapioca,
                           info=(_("Recherche des points homologues sur %s photos.") % (self.photosSansChemin.__len__())))
                                    
    def filtreTapioca(self,ligne):
        try: self.exe.terminate()
        except Exception as e : print("erreur self.exe.terminate=",str(e))
        if ligne[0]=="|":
            return ligne        
        if 'points' in ligne and len(ligne)<=15:            
            return ligne
        if 'mises en' in ligne:
            return ligne
        if 'matches' in ligne:
            return ligne           
        if 'utopano' in ligne and self.etapeTapioca==0:                    # début de la première étape sur la première échelle
            self.etapeTapioca += 1
            return heure()+" : " + _("Recherche des points remarquables et des correspondances sur une image de taille %s pixels.") % (self.echelle1PourMessage)+ "\n\n"
        if 'utopano' in ligne and self.etapeTapioca==1:                    # début de la seconde étape sur la seconde échelle
            self.etapeTapioca += 1 
            if self.plusieursScenes("Homol_SRes"):
                if self.systeme=="posix":
                    try:
                        os.killpg(os.getpgid(self.exe.pid), signal.SIGTERM)
                    except Exception as e: print("erreur killpg : ",str(e))
                if self.systeme=="nt":
# subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=self.exe.pid)) # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/4791612#4791612
                    subprocess.Popen("TASKKILL /F /im mm3d.exe") # https://lecrabeinfo.net/tuer-processus-ligne-de-commande-cmd-windows.html
                return heure()+"\n"+_("Plusieurs scènes : abandon après l'étape 1 de Tapioca")+"\n"
            if self.echelle2PourMessage=="-1":
                return "\n" + heure()+" : " +_("Recherche des points remarquables et des correspondances sur l'image entière.") + "\n\n"
            if self.echelle2PourMessage!="":
                return "\n" + heure()+" : " +_("Recherche des points remarquables et des correspondances sur une image de taille %s pixels.") % (self.echelle2PourMessage) + "\n\n"  
            return ligne
        if 'MAXLINELENGTH' in ligne:
            return "\n"+ligne+"\n"+_("Trop de photos pour Windows. Une idée : Utiliser Linux.")
        
    # ------------------ TAPAS ----------------------- Avec ou sans calibrationj intrinsèque
        
    def lanceTapas(self):        
        self.messageRetourTapas = str()
        def effacerTraceTapas():
            oschdir(self.repTravail)
            if not self.chantierOrigineCalibration: # si le répertoire de calibration est importé : on le garde !
                supprimeRepertoire("Ori-Calib")
            supprimeRepertoire("Ori-Arbitrary")
            supprimeRepertoire("Ori-InterneScan")
            supprimeRepertoire("Ori-Bascul")
            supprimeRepertoire("Ori-echelle3")
            supprimeRepertoire("Tmp-MM-Dir")
            supprimeRepertoire("Ori-nav")            
            supprimeFichier('AperiCloud.ply')
            self.orientationCourante = ""
            self.menageEcran()                                      # ménage écran        
            self.cadreVide()                                        # fenêtre texte pour affichage des résultats.           

        def retirerPhotosInutilesPourCalibration(): # par suppression de l'extension des photos ne servant pas à calibrer :
            if self.calibSeule.get() and self.photosCalibrationSansChemin:    
                [[os.rename(e,os.path.splitext(e)[0]),time.sleep(0.3)] for e in self.photosSansChemin if e not in self.photosCalibrationSansChemin]
                # controle du résultat : il doit rester exactement le nombre de photos pour calibration avec l'extension .JPG                
                self.messageTapas = str()
                lesJpgCalibration = glob.glob(os.path.join(self.repTravail,"*.JPG"))
                if lesJpgCalibration.__len__() != self.photosCalibrationSansChemin.__len__():
                    self.messageRetourTapas = (   _("Problème concernant le renommage des photos avant calibration par Tapas ForCalib.")+"\n"+
                                    _("Vérifier qu'aucune photo n'est ouverte.")+"\n"+
                                    _("Controler les noms et extensions des photos sous le répertoire du chantier : ")+"\n"+
                                    self.repTravail+"\n"+
                                    _("Seules les photos de calibration doivent avoir l'extension .JPG")+"\n"+
                                    _("Les autres photos du chantier doivent être sans extension.")+"\n"+
                                    _("Arrêt du taitement.")                                
                                    )
                    return True

        def remettrePhotosInutilesPourCalibration(): # par remise de l'extension des photos n'ayant pas servies à la calibration
            if self.calibSeule.get() and self.photosCalibrationSansChemin:    
                [[os.replace(os.path.splitext(e)[0],e),time.sleep(0.3)] for e in self.photosSansChemin if e not in self.photosCalibrationSansChemin]  
                # controle du résultat : il doit rester y avoir exactement le nombre de photos total du chantier en .JPG
                tousLesJpg = glob.glob(os.path.join(self.repTravail,"*.JPG"))
                if tousLesJpg.__len__() != self.photosSansChemin.__len__():
                    self.messageRetourTapas = (   _("Problème concernant le renommage des photos après calibration.")+"\n"+
                                    _("Vérifier qu'aucune photo n'est ouverte.")+"\n"+
                                    _("Controler les noms et extensions des photos sous le répertoire du chantier : ")+"\n"+
                                    self.repTravail+"\n"+
                                    _("Toutes les photos doivent avoir l'extension .JPG")+"\n"+
                                    _("Arrêt du traitement.")                                  
                                    )
                    return True            

        def verifierNombrePhotosCalibration():
            if self.photosCalibrationSansChemin.__len__()==1:
                self.messageRetourTapas = _("Une seule photo pour un appareil pour la calibration intrinsèque : insuffisant.") + "\n"
                return True      
            if self.photosSansChemin.__len__()-self.photosCalibrationSansChemin.__len__()<2 and self.calibSeule.get():
                self.messageRetourTapas = (_("Moins de 2 photos pour Tapas (sans les photos de calibration) : insuffisant.") + "\n"+
                                           _("Liste des photos :\n %s") % ("\n".join(self.photosSansChemin))+"\n\n"+
                                           _("Liste des photos de calibration :\n %s") % ("\n".join(self.photosCalibrationSansChemin)))                                            
                return True
            
        def  calibrationKO():
            if os.path.isdir("Ori-Calib")==False:
                self.messageRetourTapas = (_("La calibration intrinsèque n'a pas permis de trouver une orientation.") + "\n"+
                                            _("Calibration intrinsèque effectuée mais pas d'orientation trouvée."))
                return True
            
        def retirerPhotosCalibration(): # après le traitement de calibration par Tapas on déplace les photos utilisées uniquement pour la calibration
            if self.calibSeule.get() and self.photosCalibrationSansChemin:            
                try : os.mkdir(self.repCalibSeule)
                except: pass
                # déplacer les photos pour calibration vers le sous répertoire self.repCalbSeule (replace écrase la destination si elle existe]
                [[os.replace(e,os.path.join(self.repCalibSeule,e)),time.sleep(0.3)]
                 for e in self.photosCalibrationSansChemin if os.path.exists(os.path.join(self.repTravail,e))]  
                ############# Risque : on redéfinit photosAvecChemin et photosSansChemin en gardant le nom !!!! A modifier
                self.photosAvecChemin = [f for f in self.photosAvecChemin if os.path.basename(f) not in self.photosCalibrationSansChemin]
                self.photosSansChemin = [os.path.basename(g) for g in self.photosAvecChemin]
                self.photosPourCalibrationIntrinseque = [os.path.join(self.repTravail,self.repCalibSeule,e) for e in self.photosCalibrationSansChemin]
                # Vérification que le nombre de photos présentessous les répertoires est correct :
                photosSansCalib = glob.glob(os.path.join(self.repTravail,"*.JPG"))
                if photosSansCalib.__len__()!=self.photosSansChemin.__len__():
                    self.messageRetourTapas = _("Problème de nombre de photos après calibration.")
                    return True
                photosPourCalib = glob.glob(os.path.join(self.repTravail,self.repCalibSeule,"*.JPG"))
                if photosPourCalib.__len__()!=self.photosCalibrationSansChemin.__len__():
                    self.messageRetourTapas = _("Problème de nombre de photos pour calibration.")
                    return True                
            
        # Préalables : assez de photos pour calibration et recherche orientation :
        if self.remettrePhotosCalibration(): return             # si les photos de calibration ont été retirées il faut les remettre
        if verifierNombrePhotosCalibration(): return            # au moins 2 photos pour la calib et 2 pour le traitement
        if retirerPhotosInutilesPourCalibration(): return       # limitation aux seules images pour la calibration si il y en a
        effacerTraceTapas()                                     # tout est bon : supprimer les résultats d'un Tapas précédent sauf la calib importée

        if self.photosPourCalibrationIntrinseque:       # s'il y a des photos pour calibration intrinsèque : Lance Tapas pour calibration                                   
            tapas = [self.mm3d,
                     "Tapas",
                     self.modeCheckedTapas.get(),
                     '.*'+self.extensionChoisie,
                     self.tapasPerso.get(),
                     "ForCalib=1",
                     "SauvAutom=NONE",
                     "Out=Calib",
                     "ExpTxt="+self.exptxt]        
            self.lanceCommande(tapas,
                               filtre=self.filtreCalib,
                               info=_(
                               _("Calibration : Recherche des paramètres optiques des appareils sur %s photos.") % (self.photosCalibrationSansChemin.__len__())))          
            if remettrePhotosInutilesPourCalibration(): return      # Remise en état initial des photos n'ayant pas servies à la calibration            
            if calibrationKO(): return                              # controle résultat calibration
            self.orientationCourante = "Calib"                 
            self.ajoutLigne(_("Calibration intrinsèque effectuée."))# bilan : calibration OK, liste des photos modifiées (avec, sans chemin, de calibration)
            
            ######## calibration faite, recherche orientation :  
            if retirerPhotosCalibration(): return   # exclusion des images pour la calibration si elles ne servent plus après                      
            tapas = [self.mm3d,
                     "Tapas",
                     "Figee",        # fige la calibration fixée, sinon "AutoCal" la prend en compte mais la modifie
                     '.*'+self.extensionChoisie,
                     self.tapasPerso.get(),
                     'InCal=Calib',
                     'Out=Arbitrary',
                     "SauvAutom=NONE",
                     "ExpTxt="+self.exptxt]        
            self.lanceCommande(tapas,
                               filtre=self.filtreTapas,
                               info=(_("Calibration effectuée. Recherche de l'orientation sur %s photos.") % (self.photosSansChemin.__len__()))+ "\n" )

        elif self.chantierOrigineCalibration: # la calibration existe déjà, par exemple recopiée d'ailleurs

            tapas = [self.mm3d,
                     "Tapas",
                     "Figee",        # fige la calibration fixée, sinon "AutoCal" la prend en compte mais la modifie
                     '.*'+self.extensionChoisie,
                     self.tapasPerso.get(),
                     'InCal=Calib',
                     'Out=Arbitrary',
                     "SauvAutom=NONE",
                     "ExpTxt="+self.exptxt]        
            self.lanceCommande(tapas,
                               filtre=self.filtreTapas,
                               info=(_("Calibration importée depuis '%s'. Recherche de l'orientation sur %s photos.")
                                     % (self.chantierOrigineCalibration,self.photosSansChemin.__len__()))+ "\n" )
            if os.path.isdir("Ori-Arbitrary"):
                self.orientationCourante = "Arbitrary"      

        else:   # lance Tapas sans calibration préalable :                         
            tapas = [self.mm3d,
                     "Tapas",
                     self.modeCheckedTapas.get(),
                     '.*'+self.extensionChoisie,
                     self.tapasPerso.get(),
                     'Out=Arbitrary',
                     "SauvAutom=NONE",                     
                     "ExpTxt="+self.exptxt]        
            self.lanceCommande(tapas,
                               filtre=self.filtreTapas,
                               info=_("Calibration, pour trouver les réglages intrinsèques de l'appareil photo") + "\n" +
                               _("Recherche l'orientation des %s prises de vue.") % (self.photosSansChemin.__len__())+ "\n" )
       
        if orientationOK():
            self.orientationCourante = "Arbitrary"                      
        else:
            self.messageRetourTapas = _("Tapas n'a pu trouver d'orientation pour les prises de vue.")
            
    def filtreTapas(self,ligne): 
        if ('RESIDU LIAISON MOYENS' in ligne) or ('Residual' in ligne) :   # Residual pour la version 5999
            return ligne
        if ligne[0]=="|":
            return ligne      
        return

    def filtreCalib(self,ligne):
        if ligne[0:3]=="---":
            return ligne         
        return        

    def verifiePresence2PhotosCalibParAppareil(self):
        return
    # les chemins des photos de calibration sont retirées de la liste des photos du chantier aprés avoir été utilisées par tapas
    # Parfois il faut les remettre en place
    
    def remettrePhotosCalibration(self):        # utilisé dans 2 cas : 1) pour relancer Tapioca  aprés Tapas 2) si l'option "uniquement pour calibration" à changé
        if not os.path.exists(self.repCalibSeule):
            return
        oschdir(self.repTravail)
        self.messageRetourTapas = str()
        # déplacer les photos pour calibration vers le répertoire self.repTravail (replace écrase la destination si elle existe]
        try:
            [[os.replace(os.path.join(self.repTravail,self.repCalibSeule,e),e),time.sleep(0.3)]
             for e in self.photosCalibrationSansChemin if os.path.exists(os.path.join(self.repTravail,self.repCalibSeule,e))]
        except Exception as e:
            self.messageRetourTapas = _("Problème avec les photos de calibration.")
            return True                
        ############# Risque : on redéfinit photosAvecChemin et photosSansChemin en gardant le nom !!!! A modifier
        self.photosAvecChemin += [os.path.join(self.repTravail,e) for e in self.photosCalibrationSansChemin
                                  if e not in self.photosSansChemin]
        self.photosSansChemin = [os.path.basename(e) for e in self.photosAvecChemin]
        self.photosPourCalibrationIntrinseque = [os.path.join(self.repTravail,e) for e in self.photosCalibrationSansChemin]    
        toutesLesPhotos = glob.glob(os.path.join(self.repTravail,"*.JPG"))
        if toutesLesPhotos.__len__()!=self.photosSansChemin.__len__():
            self.messageRetourTapas = "remettrePhotosCalibration : "+_("Problème de nombre de photos après calibration.")
            self.ajoutLigne(self.messageRetourTapas)
            return True

    # CenterBascule : mixe orientation Tapas et celle des GPS de l'exif (Ori-Arbitrary et Ori-nav-Brut) dans Ori-nav

    def lanceCenterBascule(self):
        self.ajoutLigne("Patience, prise en compte des coordonnées GPS des photos...")
        pourNuage = self.photosSansCheminPourNuage()
        if pourNuage.__len__()<3:
            message = "\n"+_("Pas assez de photos pour utiliser les coordonnées GPS de navigation")+"\n"
            self.ajoutLigne(message)
            return
        # en fait CenterBascule mixte le résultat de Tapas avec celui de OriConvert qui définit le référentiel GPS embarqué
        # pour produire l'orientation "nav"
        param = [self.mm3d,
                 "CenterBascule",
                 '.*'+self.extensionChoisie,
                 "Arbitrary",  
                 "nav-Brut",
                 "nav"]
        self.lanceCommande(param,
                           info=_("Mixe les orientations de Tapas et des données GPS et positions des exifs des photos prises par drone"))
        if os.path.isdir("Ori-nav"):
            self.orientationCourante = "nav"                      
            self.ajoutLigne(self.messageRepereLocal)
        else:
            self.ajoutLigne(_("La prise en compte des données de navigation du drone a échoué."))

    # ------------------ APERO : orientation par axe, plan et métrique, le nom de l'orientation est "echelle3" (attention : polysème)

    def lanceApero(self):       # l'orientation prise en compte est toujours "Arbitrary" issue de Tapas ! Retourne ori-echelle3

        apero = [self.mm3d,
                 "Apero",
                 os.path.basename(self.miseAEchelle)]
        self.lanceCommande(apero,
                           info=_("Fixe l'orientation (axe, plan et métrique) suivant les options de 'calibration'"))
        if os.path.isdir("Ori-echelle3"):
            self.orientationCourante = "echelle3"        
        
    # ------------------ APERICLOUD :  -----------------------
    # l'orientation en entrée est soit :
    #  - Arbitrary (pas de calibration)
    #  - echelle3 (calibration par axe plan et métrique
    #  - bascul (calibration par points GCP)
    #  - campari_ori ou campari_gps
    
    def lanceApericloud(self):
           
        apericloud=[self.mm3d,
                    "AperiCloud",
                    '.*'+self.extensionChoisie,
                    self.orientationCourante,
                    self.aperiCloudPerso.get(),
                    "Out=AperiCloud.ply",       # c'est d'ailleurs la valeur par défaut pour AperiCloud
                    "ExpTxt="+self.exptxt]
        self.lanceCommande(apericloud,
                           filtre=self.filtreApericloud,
                           info=_("Positionne les appareils photos autour du sujet.") + "\n" + _("Création d'un nuage de points grossier."))
        
    def filtreApericloud(self,ligne):
        if ligne[0]=="|":
            return ligne        
        if "cMetaDataPhoto" in ligne:
            return "\n####" + _("ATTENTION : des metadonnées nécessaires sont absentes des photos. Vérifier l'exif.") + "\n\n" 

    # ------------------ Meslab 1 : ouvre AperiCloud.ply avec l'outil choisi par l'utilisateur --------------------------
    
    def lanceApericloudMeshlab(self):                       # ouvre le ply créé par AperiCloud avec l'outil prévu et le laisse ouvert
     
        if os.path.exists('AperiCloud.ply'):
            if not os.path.exists(self.meshlab):
                open_file('AperiCloud.ply')
                return             
            self.lanceCommande([self.meshlab,'AperiCloud.ply'],
                              info=_("Ouverture du nuage de points après Apericloud"),
                              attendre=False)
        else:
           texte="\n" + _("Pas de fichier AperiCloud.ply généré.") + "\n"
           self.ajoutLigne(texte)
           self.messageNouveauDepart = texte+_("Consulter l'aide (quelques conseils),\nConsulter la trace.") + "\n"
           return -1

    # ------------------ Tarama----------------------- crée TA_LeChantier.tif    sous le répertoire TA

    def lanceTarama(self):
        self.ajoutLigne("\n\n---------------------------\n" + _("Tarama : mosaïque des photos d'après les tie points") + "\n")
        tarama = [self.mm3d,
                    "Tarama",
                    '.*'+self.extensionChoisie,
                    self.orientationCourante,
                  self.taramaPerso.get()
                  ]                 
        self.lanceCommande(tarama)
        
    # ------------------ GCPBascule : utilise les points GCP-----------------------    

    def lanceGCPBascule(self):             # lancé s'il y a des points GCP

        self.ajoutLigne("\n\n---------------------------\n" + _("Prise en compte des points GCP : nécessite au minimum 3 points, chacun sur 2 photos") + "\n")
        if len(self.dicoPointsGPSEnPlace)<6:
            self.ajoutLigne("\n" + _("Le nombre minimum de points placés sur les photos n'est pas atteint. Abandon.") + "\n")
            return
        self.ecartPointsGCPByBascule = heure()+" :\n\n"
        GCPBascule = [self.mm3d,
                        "GCPBascule",
                        '.*'+self.extensionChoisie,
                        self.orientationCourante,           # orientation obtenue après tapas, nuage non densifié
                        "bascul",                           # Orientation calibrée par les points GCP, utilisé par Malt ou C3DC
                        os.path.basename(self.dicoAppuis),                             
                        os.path.basename(self.mesureAppuis),
                        self.gcpBasculPerso.get(),
                        "ShowD=1"]
        self.lanceCommande(GCPBascule,
                           filtre=self.filtreGCPBascule)

        if os.path.isdir("Ori-bascul"):
            self.orientationCourante = "bascul"

        
    def filtreGCPBascule(self,ligne):
        if "MAX" in ligne or "ErrMax" in ligne or "||" in ligne: # dans la version xxxx il y a ERRROR !
            self.ecartPointsGCPByBascule += ligne+"\n"
            return ligne

    # ------------------ CAMPARI : correction après BASCULE (voir mail de Marc le  -----------------------    

    def lanceCampari(self):                       # aprés Tapas, avant Malt
        campari = [self.mm3d,
                        "Campari",
                        '.*'+self.extensionChoisie,
                        self.orientationCourante,                        # orientation obtenue après tapas, nuage non densifié
                        "campari_ori",
                        self.campariPerso.get()
                    ]
        self.lanceCommande(campari,
                           filtre=self.filtreCampari)
        if os.path.isdir("Ori-campari_ori"):
            self.orientationCourante = "campari_ori"
        
    def lanceCampariGCP(self):              # campari après bascule
        try:
            float(self.incertitudeCibleGPS.get())               
            float(self.incertitudePixelImage.get())
        except Exception as e:
            self.ajoutLigne("\n" + _("Campari non lancé : paramètres incorrects : ") + "\n"+
                            "incertitude sur cible GCP : "+self.incertitudeCibleGPS.get() + "\n"+
                            "incertitude sur pixel image : "+self.incertitudePixelImage.get() + "\n"+                            
                            str(e))            
            return
        if not os.path.exists(os.path.join(self.repTravail,"Ori-bascul")):      # orientation obtenue après Tapas et GCPbascule (points GCP OK)
            self.ajoutLigne("\n" + _("Campari non lancé : pas d'orientation 'bascul'") + "\n")            
            return
        
        self.ajoutLigne("\n\n---------------------------\n" + _("Campari : correction points GCP") + "\n")
    # Campari "MyDir\IMG_.*.jpg" OriIn OriOut GCP=[GroundMeasures.xml,0.1,ImgMeasures.xml,0.5]
        campariGCP = [self.mm3d,
                        "Campari",
                        '.*'+self.extensionChoisie,
                        self.orientationCourante,                        # orientation obtenue après tapas, nuage non densifié
                        "campari_gcp",                             # Orientation calibrée par les points GCP, utilisé par Malt ou C3DC
                        self.campariPerso.get(),
                        "GCP=["+os.path.basename(self.dicoAppuis)+","+
                        self.incertitudeCibleGPS.get()+","+
                        os.path.basename(self.mesureAppuis)+","+
                        self.incertitudePixelImage.get()+"]",
                        "DetGCP=1"
                     ]
        self.lanceCommande(campariGCP,
                           filtre=self.filtreCampari)
        if os.path.isdir("Ori-campari_gcp"):
            self.orientationCourante = "campari_gcp"


    def filtreCampari(self,ligne):
        if "MAX" in ligne: 
            return ligne
        if "ErrMax" in ligne:
            return ligne
        if "||" in ligne:
            return ligne   
        
    # ------------------ MALT -----------------------
    
    def lanceMalt(self):    # malt prend les points homologues dans le répertoire "Homol",
                            # et si geoImage : l'image maîtresse dans self.maitreSansChemin (str() si absent)
                            #                  et dans self.photosSansChemin les images autour de l'image maitressse
                            #                  si il y a un masque il faut les 2 fichiers maitre_Masq.xml et maitre_Masq.tif sans les indiquer dans la syntaxe

        self.ajoutLigne("\n\n---------------------------\n" + _("Préparation du lancement de Malt") + "\n")
        aConserver = str()
        self.beginStep = ""        
        if self.modeCheckedMalt.get()=="GeomImage":
            # Les N meilleurs fichiers en correspondances avec la maitresse
            aConserver = self.meilleuresPhotosAutourMaitresse(self.maitreSansChemin,self.photosUtilesAutourDuMaitre.get())
            # on renomme les autres
            if aConserver:
                [os.rename(e,os.path.splitext(e)[0]) for e in self.photosSansChemin if e not in aConserver]
                self.ajoutLigne("\n\n"+_("Photos utiles pour malt GeomImage : ")+aConserver+"\n")
            else:
                self.ajoutLigne("\n\n"+_("Malt sur toutes les photos"))            
            malt = [self.mm3d,
                    "Malt",
                    self.modeCheckedMalt.get(),
                    ".*"+self.extensionChoisie,  # les n meilleures photos en correspondance, les autres étant renommées
                    self.orientationCourante,
                    self.maltGeomImagePerso.get(),   # param perso en premier (les suivants  identiques sont supprimés)                   
                    "NbVI=2",
                    "ZoomF="+self.zoomF.get(),
                    "Master="+self.maitreSansChemin,                   
                    ]                                    

        elif self.modeCheckedMalt.get()=="Ortho":
            if os.path.exists(self.masqueTarama):
                self.ajoutLigne("\n\n"+_("Mosaique et masque: ")+str(self.mosaiqueTaramaTIF)+"\n")
            else:
                self.ajoutLigne("\n\n"+_("Mosaique seule : ")+str(self.mosaiqueTaramaTIF)+"\n")                
            malt = [self.mm3d,
                    "Malt",
                    "Ortho",
                    ".*"+self.extensionChoisie,  # les n meilleures photos en correspondance, les autres étant renommées
                    self.orientationCourante,                    
                    self.maltOrthoPerso.get(),   # param perso en premier (les suivants  identiques sont supprimés)                    
                    "NbVI=2",
                    "ZoomF="+self.zoomF.get(),
                    'DirTA=TA',
                    "DefCor=0",
                    ]            
        elif self.modeCheckedMalt.get()=="UrbanMNE":
            malt = [self.mm3d,
                    "Malt",
                    self.modeCheckedMalt.get(),
                    ".*"+self.extensionChoisie,
                    self.orientationCourante,
                    self.maltUrbanMnePerso.get(),                       
                    "NbVI=2",
                    "ZoomF="+self.zoomF.get(),
                    ]                          # zoom 8,4,2,1 qui correspondent au nuage étape 5, 6, 7, 8
        lesPhotos = glob.glob(os.path.join(self.repTravail,"*.JPG"))
        self.ajoutLigne("\n"+_("lesPhotos pour Malt : ")+",".join(lesPhotos)+"\n")
        self.lanceCommande(malt,
                           filtre=self.filtreMalt,
                           info=_("ATTENTION : cette procédure est longue : patience !"))
        
        if aConserver :     # on renomme correctement les fichiers abandonnés pour le traitement de malt
            [os.rename(os.path.splitext(e)[0],e) for e in self.photosSansChemin if (os.path.exists(os.path.splitext(e)[0]) and not (os.path.exists(e)))]
                     
        
    def filtreMalt(self,ligne):
        if ligne[0]=="|":
            return ligne
        if 'BEGIN STEP' in ligne:
            if self.beginStep!=ligne:
                self.beginStep = ligne
                return ligne.strip(" -")          
        if 'BEGIN BLOC' in ligne:
            return " - "+ligne.strip(" -")        
    
    def reinitialiseMaitreEtMasque(self):                                                       # on conserve si la photo appartient au nouveau lot
        self.masqueSansChemin           =   str()                                               # image masque : en TIF, choisi par l'utilisateur       
        self.maitre                     =   str()        
        self.maitreSansChemin           =   str()                                               # image maîtresse        
        self.fichierMasqueXML           =   str()                                               # nom du fichier XML décrivant le masque
        self.maitreSansExtension        =   str()
        self.monImage_MaitrePlan        =   str()                                               # Nom de l'image maîtresse du plan repere (sans extension)
        self.monImage_PlanTif           =   str()                                               # nom du masque correspondant
        self.listeDesMaitresses         =   list()                                              # liste des images maitresses
        self.listeDesMasques            =   list()                                              # liste Des Masques associès aux maîtresses
        self.miseAJourItem701_703()                                                             # met à jour les windgets de l'onglet Malt

    def reinitialiseMaitreEtMasqueDisparus(self):                                               # on conserve les options si la photo appartient au nouveau lot (photos = liste avec chemins)

        self.masqueSansChemin           =   str()                                               # image masque : en TIF, choisi par l'utilisateur       
        self.maitre                     =   str()        
        self.maitreSansChemin           =   str()                                               # image maîtresse        
        self.fichierMasqueXML           =   str()                                               # nom du fichier XML décrivant le masque
        self.maitreSansExtension        =   str()

        # les axes horizontal et vertical conservé si les photos sont présentes ainsi que les maitresses et les masques et le plan et la distance
        photos = self.photosAvecChemin

        # Ligne horizontale ou verticale
        # axe horizontal, dans le dico : self.dicoLigneHorizontale. key = nom point, photo, identifiant ;Retrouver nom de la photo, coordonnées des points
        # items = liste de tuple (key,values) soit tuple = (point,photo, id),(x1,y1)        
        
        if self.dicoLigneHorizontale.__len__()>0:
            
            photosAvecLigneH = [e[1] for e in self.dicoLigneHorizontale.keys()][0]
            if photosAvecLigneH not in photos:
               self.dicoLigneHorizontale = dict()
               
        if self.dicoLigneVerticale.__len__()>0:
            photosAvecLigneV = [e[1] for e in self.dicoLigneVerticale.keys()][0]
            if photosAvecLigneV not in photos:
               self.dicoLigneVerticale = dict()            

        # maitre plan et image
            
        if self.monImage_MaitrePlan not in photos:
            self.monImage_MaitrePlan        =   str()                                           # Nom de l'image maîtresse du plan repere (sans extension)
            self.monImage_PlanTif           =   str()                                           # nom du masque correspondant            

        # Distance
        # dicoCalibre key = nom point, photo, identifiant, value = x,y         

        if self.dicoCalibre.__len__()>0:
            photosAvecDistance = set([(e[1],e) for e in self.dicoCalibre.keys()])   # ensemble des clés et des noms de fichiers
            for photo,key in photosAvecDistance:
                if not os.path.exists(photo):
                    del self.dicoCalibre[key]


        #Points GCP
        # dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
        # Suppression des points GCP placés sur des photos non choisies dans le nouveau choix
        # l'utilisateur a été prévenu
        
        if self.dicoPointsGPSEnPlace.__len__()>0:
            photosAvecPointsGPS = set([e[1] for e in self.dicoPointsGPSEnPlace.keys()])
            for e in photosAvecPointsGPS:
                if e not in photos:
                    copieDico = dict(self.dicoPointsGPSEnPlace)
                    for f in copieDico.keys():
                        if f[1]==e:
                            del self.dicoPointsGPSEnPlace[f]


        # masques et maitresses
          
        self.listeDesMaitresses         =   [e for e in self.listeDesMaitresses if e in photos] # liste des images maitresses avec chemin
        # liste Des Masques associès aux maîtresses : chemin complet de la maitresse + extension spécifique : _masque.tif
        self.listeDesMasques            =   [e for e in self.listeDesMasques if e.replace('_masque.tif',self.extensionChoisie) in photos]



        # suppression du masque 3 d (qui dépend de apericloud.ply)

        supprimeFichier(self.masque3DSansChemin)                
        supprimeFichier(self.masque3DBisSansChemin)        

        # reconstitution des xml 

        self.finOptionsOK(affiche=False)                                                             # mise à jours des fichiers xml liès aux options
        self.miseAJourItem701_703()                                                             # met à jour les windgets de l'onglet Malt

    # ------------------ Tawny : après Malt, si self.modeCheckedMalt.get() = Ortho et self.tawny.get() = Vrai -----------------------
    # Tawny crée un drapage pour le nuage créé par Malt/Ortho
    
    def lanceTawny(self):

        if self.modeCheckedMalt.get() != "Ortho":
            return
        if not self.tawny.get():
            return
        '''Tawny -help
        *****************************
        * Help for Elise Arg main *
        *****************************
        Unnamed args :
        * string :: {Directory where are the datas}
        Named args :
        * [Name=DEq] INT :: {Degree of equalization (Def=1)}
        * [Name=DEqXY] Pt2di :: {Degree of equalization, if diff in X and Y}
        * [Name=AddCste] bool :: {Add unknown constant for equalization (Def=false)}
        * [Name=DegRap] INT :: {Degree of rappel to initial values, Def = 0}
        * [Name=DegRapXY] Pt2di :: {Degree of rappel to initial values, Def = 0}
        * [Name=RGP] bool :: {Rappel glob on physically equalized, Def = true}
        * [Name=DynG] REAL :: {Global Dynamic (to correct saturation problems)}
        * [Name=ImPrio] string :: {Pattern of image with high prio, def=.*}
        * [Name=SzV] INT :: {Sz of Window for equalization (Def=1, means 3x3)}
        * [Name=CorThr] REAL :: {Threshold of correlation to validate'''
        tawny = [self.mm3d,
                "Tawny",
                "Ortho-MEC-Malt/",
                self.tawnyPerso.get(),
                "Out="+self.orthoMosaiqueTawny]
        self.lanceCommande(tawny,
                           filtre=self.filtreTawny,
                           info=_("lance Tawny"))

    def filtreTawny(self,ligne):
        if "Don't understand" in ligne:
            return ligne
        if "FATAL ERROR" in ligne:
            return ligne+" "+_(": voir la trace complète.")   
        if "KBOX" in ligne:
            return ligne
        
    # ------------------ C3DC : alternative à Malt avec un masque 3D -----------------------
        
    def lanceC3DC(self):
        # Si on a un masque 3D on l'utilise et on ne cherche pas plus loin :
        self.beginStep = ""
        if self.existeMasque3D():            
            C3DC = [self.mm3d,
                    "C3DC",
                    self.modeC3DC.get(),
                    ".*"+self.extensionChoisie,
                    self.orientationCourante,
                    self.C3DCPerso.get(),                    
                    "Masq3D="+self.masque3DSansChemin,
                    "Out="+self.modele3DFinal,
                    "PlyCoul=1",                  
                    ]
        else:
            C3DC = [self.mm3d,
                    "C3DC",
                    self.modeC3DC.get(),
                    ".*"+self.extensionChoisie,                  
                    self.orientationCourante,
                    self.C3DCPerso.get(),                      
                    "Out="+self.modele3DFinal,
                    "PlyCoul=1",
                    ]
            
        self.lanceCommande(C3DC,
                           filtre=self.filtreC3DC,
                           info=_("ATTENTION : cette procédure est longue : patience !"))

    def filtreC3DC(self,ligne):
        if ligne[0]=="|":
            return ligne
        if "long" in ligne:
            return ligne
        if 'BEGIN STEP' in ligne:
            if self.beginStep!=ligne:
                self.beginStep = ligne
                return ligne.strip(" -")          
        if 'BEGIN BLOC' in ligne:
            return " - "+ligne.strip(" -")       
                
    # ------------------ NUAGE2PLY -----------------------
    
    # exemple après GeomImage : C:\MicMac64bits\bin\nuage2ply.exe MM-Malt-Img-P1000556\NuageImProf_STD-MALT_Etape_8.xml Attr=P1000556.JPG Out=self.modele3DEnCours
    # passe d'un nuage (fichier xml pour une maitresse si geomimage) à un ply, Attr = fichier de drapage.
    def tousLesNuages(self): #le zoom est dans self.zoomF.get() et l'étape dans self.etapeNuage : ils sont corrélés comme suit
        
            # étapes = 1,2,3,4,5,6,7,8  zoom = 128,64,32,16,8,4,2,1
            # zoom :   1,2,4,8,16,32,64,128 étapes = 8,7,6,5,4,3,2,1
            
        sauveEtapeNuage = self.etapeNuage
        listeModeles = list()
        for zoom in [[str(8-j),str(pow(2,j))] for j in range(8-int(self.etapeNuage),8)]:
            self.maitreSansExtension = os.path.splitext(self.maitreSansChemin)[0]

        for zoom in [[str(j),str(pow(2,8-j))] for j in range(1,int(sauveEtapeNuage)+1)]:                        
            self.modele3DEnCours = "modele3D_"+self.maitreSansExtension+"_Zoom_"+zoom[1]+".ply"
            listeModeles.insert(0,self.modele3DEnCours)     # liste triée des modèles, le plus précis en tête 
            self.etapeNuage = zoom[0]
            self.zoomNuage = zoom[1]
            self.lanceNuage2Ply()

        self.etapeNuage = sauveEtapeNuage
        
        # dernier modele ayant été créé :
        for e in listeModeles:
            if os.path.exists(e):
                self.modele3DEnCours = e
                return
                       
        
    def lanceNuage2Ply(self):       # nuage2Ply avec un paramètre : self.etapeNuage, et crée le fichier ply : self.modele3DEnCours

        if self.modeCheckedMalt.get() in ("GeomImage"):
            self.lanceNuage2PlyGeom()
        if self.modeCheckedMalt.get() in ("UrbanMNE"):
            self.lanceNuage2PlyUrban()
        if self.modeCheckedMalt.get() in ("Ortho"):
            self.lanceNuage2PlyOrtho()
            
    def lanceNuage2PlyGeom(self):
        arg1 = 'MM-Malt-Img-'+self.maitreSansExtension+'/NuageImProf_STD-MALT_Etape_'+self.etapeNuage+'.xml'
        if os.path.exists(arg1)==False:
            return
        Nuage2Ply = [self.mm3d,
                     "Nuage2Ply",
                     arg1,
                     self.nuage2PlyPerso.get(),                       
                     'Mesh='+self.nuage2Mesh.get(),                                        
                     'Attr='+self.maitreSansChemin,
                     'Out='+self.modele3DEnCours,
                     ]
        self.lanceCommande(Nuage2Ply)
                           
    # exemple après UrbanMNE : mm3d Nuage2Ply "MEC-Malt/NuageImProf_STD-MALT_Etape_8.xml" Scale=8 Attr="MEC-Malt/Z_Num8_DeZoom1_STD-MALT.tif" Out="self.modele3DEnCours"
    # si tawny : ajouter l'attribut : 
    def lanceNuage2PlyUrban(self):
        if int(self.zoomNuage)>32:          # le mode UrbanMNE ne génère apparemment des nuages que pour les zoom de 32 à 1, soit les étapes 3 à 8
            return
        arg1 = "MEC-Malt/NuageImProf_STD-MALT_Etape_"+self.etapeNuage+".xml"
        if os.path.exists(arg1)==False:
            return         

            Nuage2Ply = [self.mm3d,
                     "Nuage2Ply",
                     arg1,
                     self.nuage2PlyPerso.get(),                         
                     'Mesh='+self.nuage2Mesh.get(),
                     'Out='+self.modele3DEnCours,
                     ]
            self.lanceCommande(Nuage2Ply)

    def lanceNuage2PlyOrtho(self):
        arg1 = "MEC-Malt/NuageImProf_STD-MALT_Etape_"+self.etapeNuage+".xml"
        if os.path.exists(arg1)==False:
            return
        orthoMosaique = os.path.join(self.repTravail,"Ortho-MEC-Malt",self.orthoMosaiqueTawny)       # Orthophotomosaic.tif sous le répertoire "Ortho-MEC-Malt/"
        if os.path.exists(orthoMosaique):           
            Nuage2Ply = [self.mm3d,
                         "Nuage2Ply",
                         arg1,
                         self.nuage2PlyPerso.get(),                          
                         'Mesh='+self.nuage2Mesh.get(),                        
                         "Attr="+orthoMosaique,             # pour draper le ply (l'ortho est créée par Tawny)
                         'Out='+self.modele3DEnCours,
                         ]
        else:
            Nuage2Ply = [self.mm3d,
                         "Nuage2Ply",
                         arg1,
                         self.nuage2PlyPerso.get(),                         
                         'Mesh='+self.nuage2Mesh.get(),
                         'Out='+self.modele3DEnCours,
                         ]            
        self.lanceCommande(Nuage2Ply)        
        
    # ------------------ Meslab 2 --------------------------
    
    def ouvreModele3D(self):
        self.chercheModele3D() 
        aOuvrir = os.path.join(self.repTravail,self.modele3DFinal)
        if not os.path.exists(aOuvrir):
           texte=_("Pas de fichier %s généré.") % (self.modele3DFinal)+ "\n\n" + _("Echec du traitement MICMAC") 
           self.ajoutLigne(texte)
           return -1
        if not os.path.exists(self.meshlab):
            open_file(self.modele3DFinal)
            return        
        meshlab = [self.meshlab, aOuvrir]        
        self.lanceCommande(meshlab,
                           info=_("Nuage de points %s généré.") % (self.modele3DFinal),
                           attendre=False)

    def nettoyerChantier(self):     # Le chantier est nettoyé : les fichiers sous self.repTravail sont conservés, les arborescences de calcul effacés
        self.etatDuChantier = 2                
        self.enregistreChantier()
        self.remettrePhotosCalibration()
        listeAConserver  = os.listdir(self.repTravail)
        listeAConserver = [e for e in listeAConserver if not os.path.isdir(e)]
        listeAConserver.append("Ori-nav-Brut")
        listeAConserver.append("Ori-Calib")        
        supprimeArborescenceSauf(self.repTravail,listeAConserver)
        self.sauveParam()
        self.ajoutLigne("\n ****** " + _("Chantier réinitialisé, points homologues supprimés,\n"+
                                         "orientation supprimée, copie calibration et points GPS conservée. Prochain départ : Tapioca.")+"\n")
        self.ecritureTraceMicMac()

    def nettoyerChantierApresTapas(self):     # Le chantier est remis aprés Tapas, prêt pour une nouvelle densification
        self.etatDuChantier = 4                 
        self.enregistreChantier()
        self.sauveParam()
        self.ajoutLigne("\n ****** " + _("Chantier réinitialisé aprés Orientation sur demande utilisateur. Prochain départ : densification")+"\n")
        self.ecritureTraceMicMac()
        
    def nettoyerChantierApresTapioca(self):     # Le chantier est remis aprés Tapioca
        self.etatDuChantier = 35            # 35 = Chantier arrété aprés tapioca, points homoloques conservés      
        self.enregistreChantier()
        self.sauveParam()
        self.ajoutLigne("\n ****** " + " "+_("Chantier réinitialisé aprés points homologues sur demande utilisateur. Prochain départ : Orientation (Tapas)")+"\n")
        self.ecritureTraceMicMac()

    ################################## définir un référentiel à partir d'une mise à l'échelle, de points GCP ou GPS embarqués sur drone

    def referentiel(self):      # le référentiel est dé&fini  après Tapas et Avant génération des nuages
                                # Potentiellement 2 fois : il faut éviter les doublons par la variable self.referentielOK = True
                                # cette variable est réinitialisée lorsque :
                                # - des photos sont retirées (peut-être pas nécessaire : variables réinitialisées ?)
                                # - des points gcp sont modifiés (retirés ou placés; ajouter =inutile, si coordonénes modifiées : à faire...)
                                # - la mise à l'échelle est modifiée (fait suaf si modif de la distance)
                                # - on ferme AperoDeDenis
        # Définition d'un référentiel : 3 possibilités 

        # 1) orientation par données GPS issue des exifs des photos
        # 2) saisie de points GCP (ground control points)
        # 3) calibration par mise à l'échelle (plan, droite, distance) par Apero,         
        # Si une orientation brute a été créée à partir des coordonnées GPS des photos prises par drone (par OriConvert) on mixte avec celle de Tapas
        # la nouvelle orientation sera : Ori-nav

        if self.referentielOK: # inutile de relancer le référentiel est déjà choisi et rien n'a été modifié
            return
        
        self.referentielOK = True # nouveau choix
        
        # PRIORITE 1 : si il existe un fichier XML de points d'appuis GCP  : self.mesureAppuis
        # calibrage de l'orientation suivant des points GCP, un axe ox, un plan déterminé par un masque
              
        if os.path.exists(self.mesureAppuis):
            self.orientationCourante = "Arbitrary"
            self.lanceGCPBascule()         # des points GCP : on calibre dessus, cela remplace la calibration précédente
            # lancement de campari avec points GCP
            self.lanceCampariGCP()
            return     
        

        # PRIORITE 2 : Coordonnées GPS embarquées via Drone, le répertoire Ori-nav-Brut est présent, on l'utilise
        if os.path.isdir("Ori-nav-Brut"):
            self.orientationCourante = "Arbitrary"
            self.lanceCenterBascule()
            self.lanceCampari()                     # Campari sans points GCP            
            return


        # PRIORITE 3 : Si un fichier de mise à l'échelle par axe plan et métrique est valide on lance apero, même s'il y a une mise à l'échelle par points GCP (sera bon si GCP échoue)

        if self.controleMiseALEchelle():            # calibration OK = True   
            self.orientationCourante = "Arbitrary"
            self.lanceApero()                       # exploite un fichier xml et renvoie l'orientation "echelle3"
            self.lanceCampari()                     # Campari sans points GCP
            return

        # si aucun référentiel prévu on lance quand même campari pour préciser la position des points
        
        self.orientationCourante = "Arbitrary"
        self.lanceCampari()

        
    ################################## UTILITAIRES MICMAC ########################################################### 
         
    def exploiterHomol(self):
        self.ajoutLigne("\n ****** " + _("Qualité des photos suite au traitement : "))
        repHomol = self.repTravail+os.path.sep+_('Homol')
        if os.path.exists(repHomol):
            lesRep = os.listdir(repHomol)
            for e in lesRep:
                rep = repHomol+os.path.sep+e
                fichiers = os.listdir(rep)
                for fic in fichiers:
                    fi = rep+os.sep+fic
                    if os.path.exists(fi):
                        with  open(fi) as infile:
                            lignes = infile.readlines()    #lecture dicoCamera.xml

        self.ajoutLigne("\n ****** " + _("Fin d'examen de qualité des photos."))


    def retirerPhotos(self,lesPhotosARetirer=None):
        if lesPhotosARetirer==None: 
            titre = _("Retirer des photos")
            message = _("Choisir les photos a retirer du chantier")        
            self.choisirUnePhoto(self.photosAvecChemin,
                                 titre=titre,
                                 message=message,
                                 messageBouton=_("Valider"))
        else:
            self.selectionPhotosAvecChemin = [ os.path.join(self.repTravail,e) for e in lesPhotosARetirer]
        if len(self.selectionPhotosAvecChemin)>=len(self.photosAvecChemin)-2:
            self.encadre(_("Vous devez laisser au moins 2 photos."))
            return
        if len(self.selectionPhotosAvecChemin)>0:
            [supprimeFichier(photo) for photo in self.selectionPhotosAvecChemin]
            self.photosAvecChemin = [e for e in self.photosAvecChemin if e not in self.selectionPhotosAvecChemin]
            self.photosSansChemin = [os.path.basename(x) for x in  self.photosAvecChemin]
            self.maitreSansChemin = [e for e in self.maitreSansChemin if e in self.photosSansChemin]
            self.masqueSansChemin = [e for e in self.masqueSansChemin if e in self.photosSansChemin]
            dico = dict(self.lesTagsExif)
            [self.lesTagsExif.pop(e,None) for e in dico if e[1] not in self.photosSansChemin] # corrigé le 4/1/20
            # le chemin des photos de calibration dépend de l'état du chantier (déplacées si inutilisées après tapas)
            self.photosPourCalibrationIntrinseque = [e for e in self.photosPourCalibrationIntrinseque if os.path.basename(e) in self.photosSansChemin]
            self.photosCalibrationSansChemin = [os.path.basename(f) for f in self.photosPourCalibrationIntrinseque]
            # le nom de la photo key[1] est avec chemin : on retire du dictionnaire ceux qui ne sont plus dans la liste des photos
            dico = dict(self.dicoPointsGPSEnPlace)
            [self.dicoPointsGPSEnPlace.pop(key,None) for key in dico if key[1] not in self.photosAvecChemin]
            # on met dans la liste des maitresses avec chemin celles qui sont dans la liste des photos
            self.listeDesMaitresses = [e for e in self.listeDesMaitresses if e in self.photosAvecChemin]
            # liste des masques : liste de noms avec chemin mais les masques ont un nom spécifique, suppression des masquesdevenus inutiles
            listeDesMasques = list()
            for e in self.photosSansChemin:
                ajouter = [f for f in self.listeDesMasques if os.path.splitext(e)[0] in f]
                listeDesMasques.extend(ajouter)
            [supprimeFichier(photo) for photo in self.listeDesMasques if photo not in listeDesMasques]
            self.listeDesMasques = listeDesMasques
            # redéfinition si besoin du masque maitre
            if self.listeDesMaitresses: self.maitre = self.listeDesMaitresses[0]
            #mise à jour de la mise à l'échelle
            dico = dict(self.dicoLigneHorizontale)
            [self.dicoLigneHorizontale.pop(key,None) for key in dico if os.path.basename(key[1]) not in self.photosSansChemin]
            dico = dict(self.dicoLigneVerticale)
            [self.dicoLigneVerticale.pop(key,None) for key in dico if os.path.basename(key[1]) not in self.photosSansChemin]
            dico = dict(self.dicoCalibre)
            [self.dicoCalibre.pop(key,None) for key in dico if os.path.basename(key[1]) not in self.photosSansChemin]
            self.encadre(_("Nombre de photos retirées du chantier : %s Consulter la trace") % str(len(self.selectionPhotosAvecChemin))+"\n")
            self.encadrePlus(_("Tous les résultats sont conservés.")+"\n")
            self.encadrePlus(_("Vous pouvez relancer au choix les points homologues ou l'orientation ou la densification."))
            self.ajoutLigne("\n"+_("Les photos suivantes sont retirées du chantier à la demande de l'utilisateur : ")+
                            "\n  - "+"\n  - ".join(self.selectionPhotosAvecChemin)+"\n")
            self.referentielOK = False
            self.ecritureTraceMicMac()
            
###################### création d'un nouveau chantier avec les meilleurs photos

    def outilMeilleuresPhotos(self):
        self.menageEcran()
        repertoireHomol = os.path.join(self.repTravail,"Homol")  # répertoire des homologues
        if os.path.isdir(repertoireHomol)==False:
            self.encadre("Lancer d'abord la recherche des points homologues.")
            return
        self.item9000.pack()
        pass

    def nbMeilleuresOK(self):
        nb=self.item9003.get()
        liste = [os.path.join(self.repTravail,e) for e in self.lesMeilleuresPhotos(int(nb))]
        if self.troisBoutons(titre=_("Nouveau chantier"),question=_("Créer un nouveau chantier avec les photos : ")
                             +"\n"+"\n"+"\n".join(liste)+" ?\n"+"\n"+_("Les paramètres de Tapioca/Malt seront modifiés.")
                             +"\n"+_("Les points homologues et tous les autres résultats seront supprimés."))==0:
            self.nouveauChantier()
            
            # crée le repertoire de travail, copie les photos et renvoit le nombre de fichiers photos "acceptables",
            # met à 1 l'état du chantier crée self.photosAvecChemin et self.photosSansChemin
            # ATTENTION : Supprime l'arborescence et certains résultats.

            self.nombreDExtensionDifferentes(liste)
            self.extensionChoisie = self.lesExtensions[0]                     
            retourExtraire = self.extrairePhotoEtCopier(liste)    

            if retourExtraire.__class__()=='':              # si le retour est un texte alors erreur, probablement création du répertoire impossible
                self.encadre (_("Impossible de créer le répertoire de travail.") + "\n" +
                              _("Vérifier les droits en écriture sous le répertoire des photos") + "\n"+str(retourExtraire))
                return 
            if retourExtraire==0:                           # extraction et positionne  self.repertoireDesPhotos, et les listes de photos avec et sanschemin (photosAvecChemin et photosSansChemin)
                self.encadre (_("Aucun JPG, PNG, BMP, TIF, ou GIF  sélectionné,") + "\n" +
                              _("le répertoire et les photos restent inchangés.") + "\n")
                return
            # paramètres de tapioca : MultiScale 300 * MulScale (Line est disqualifié par la sélection des photos, All est trop lourd)
            self.modeTapioca.set('MulScale')# Mode (All, MulScale, Line)
            self.echelle2.set('300')
            self.echelle3.set('-1')
            # Paramètre de Tapas :
            self.modeCheckedTapas.set('RadialBasic')                # mode par défaut depuis la v 2.23 du 14 mars 2016
            self.arretApresTapas.set(0)                             # 1 : on arrête le traitement après Tapas, 0 on poursuit
            # pas encore suvegardé :
            self.etatSauvegarde = "*"                                     # chantier modifié
            self.etatDuChantier = 1
        self.afficheEtat()

    def nbMeilleuresKO(self):
        self.encadre(_("Abandon"))        
        pass

    ###################### Saisie des paramètres ptionnels des modules python

    def personnaliseOptions(self):
        self.menageEcran()
        self.item9100.pack()
        
    def optionsPersoOK(self):   # attention les valeurs saisies ne sont pas "vérifiées" au sens sémantique; de plus il faut une cohérence entre options
                                # par exemple l'option ExpTxt=1 sur tapioca doit être propagée sur tapass et campari et apericloud

        self.memoPerso()        # enregistre les valeurs saisies dans le dico
        noMatch,ok = self.nettoiePerso()       
        message = (_("Les paramètres nommés personnalisés suivant sont enregistrés pour le chantier en cours :")+"\n\n"+
                     "\n".join([ e[:-5] +" : "+ self.dicoPerso[e]  for e in self.dicoPerso if self.dicoPerso[e]])+"\n\n"+
                     _("Pour les enregistrer pour tous les chantiers, menu :\n Outils/Modifier les paramètres par défaut."))
        if noMatch:
            message += "\n\n"+_("Les saisies suivantes sont incorrectes, effacées :")+"\n"+"\n".join(noMatch)+"\n\n"
            message += _("Forme correcte : param1=toto,param2=tata")
        self.sauveParamChantier()
        if ok: self.encadre (message)
        else:  self.encadre (_("Pas de paramètres personnalisés"))
            
    def optionsPersoKO(self):   # Abandon : on remet comme avant    
        self.restauPerso()      # restaure les valeurs du dico  (qui sert de sauvegarde)
        self.encadre(_("Abandon utilisateur. Valeurs inchangées :") +"\n\n"+
                        "\n".join([ e[:-5] +" : "+ self.dicoPerso[e]  for e in self.dicoPerso if self.dicoPerso[e]]))

    def nettoiePerso(self):     # une seule expression réguière devrait suffire ! Mais laquelle ???
        listeNoMatch = list()
        retour = str()
        for e in self.dicoPerso:            
            self.dicoPerso[e] = self.dicoPerso[e].replace(" ","")
            lesParam = self.dicoPerso[e].split(",")
            for f in lesParam:
                if f.split("=").__len__()==2:
                    param = f.split("=")[0]
                    val = f.split("=")[1]
                    if not(re.match("(\w)",param) and re.match("(.)+",val)):
                        listeNoMatch.append(f)                
                        self.dicoPerso[e] = ""
                    else:
                        retour = "OK"
                elif f:
                    listeNoMatch.append(f)                
                    self.dicoPerso[e] = ""                    
        self.restauPerso()
        return listeNoMatch,retour
    
    def memoPerso(self):
        self.dicoPerso = {
            "tapiocaMulScalePerso" : self.tapiocaMulScalePerso.get(),
            "tapiocaLinePerso" : self.tapiocaLinePerso.get(),
            "tapiocaAllPerso" : self.tapiocaAllPerso.get(),
            "tapasPerso" : self.tapasPerso.get(),
            "maltOrthoPerso" : self.maltOrthoPerso.get(),
            "maltGeomImagePerso" : self.maltGeomImagePerso.get(),
            "maltUrbanMnePerso" : self.maltUrbanMnePerso.get(),
            "C3DCPerso" : self.C3DCPerso.get(),
            "campariPerso" : self.campariPerso.get(),
            "tawnyPerso" : self.tawnyPerso.get(),
            "gcpBasculPerso" : self.gcpBasculPerso.get(),
            "taramaPerso" : self.taramaPerso.get(),
            "aperiCloudPerso" : self.aperiCloudPerso.get(),
            "nuage2PlyPerso" : self.nuage2PlyPerso.get(),
            "divPerso" : self.divPerso.get(),
            "mergePlyPerso" : self.mergePlyPerso.get(),
            }
    def restauPerso(self):
        try:
            self.tapiocaMulScalePerso.set(self.dicoPerso["tapiocaMulScalePerso"])
            self.tapiocaLinePerso.set(self.dicoPerso["tapiocaLinePerso"])
            self.tapiocaAllPerso.set(self.dicoPerso["tapiocaAllPerso"])
            self.tapasPerso.set(self.dicoPerso["tapasPerso"])      
            self.maltOrthoPerso.set(self.dicoPerso["maltOrthoPerso"])
            self.maltGeomImagePerso.set(self.dicoPerso["maltGeomImagePerso"])
            self.maltUrbanMnePerso.set(self.dicoPerso["maltUrbanMnePerso"])                
            self.C3DCPerso.set(self.dicoPerso["C3DCPerso"])       
            self.campariPerso.set(self.dicoPerso["campariPerso"])     
            self.tawnyPerso.set(self.dicoPerso["tawnyPerso"])                        
            self.gcpBasculPerso.set(self.dicoPerso["gcpBasculPerso"])
            self.taramaPerso.set(self.dicoPerso["taramaPerso"])
            self.aperiCloudPerso.set(self.dicoPerso["aperiCloudPerso"])
            self.nuage2PlyPerso.set(self.dicoPerso["nuage2PlyPerso"])
            self.divPerso.set(self.dicoPerso["divPerso"])
            self.mergePlyPerso.set(self.dicoPerso["mergePlyPerso"])
        except Exception as e:
            self.ajoutLigne(_("Erreur lors de la restauration des options personnalisées : ")+str(e))

    def initPerso(self):    # bouton : Effacer tout
        self.tapiocaMulScalePerso.set("")
        self.tapiocaLinePerso.set("")
        self.tapiocaAllPerso.set("")
        self.tapasPerso.set("")      
        self.maltOrthoPerso.set("")
        self.maltGeomImagePerso.set("")
        self.maltUrbanMnePerso.set("")                
        self.C3DCPerso.set("")       
        self.campariPerso.set("")     
        self.tawnyPerso.set("")                        
        self.gcpBasculPerso.set("")
        self.taramaPerso.set("")
        self.aperiCloudPerso.set("")
        self.nuage2PlyPerso.set("")
        self.divPerso.set("")
        self.mergePlyPerso.set("")

    def initDicoPerso(self):
        self.dicoPerso = {
            "tapiocaMulScalePerso" : "",
            "tapiocaLinePerso" : "",
            "tapiocaAllPerso" : "",
            "tapasPerso" : "",
            "maltOrthoPerso" : "",
            "maltGeomImagePerso" : "",
            "maltUrbanMnePerso" : "",
            "C3DCPerso" : "",
            "campariPerso" : "",
            "tawnyPerso" : "",
            "gcpBasculPerso" : "",
            "taramaPerso" : "",
            "aperiCloudPerso" : "",
            "nuage2PlyPerso" : "",
            "divPerso" : "",
            "mergePlyPerso" : "",
            }
        self.restauPerso()
        
    ##################### expression régulière de la liste des meilleures photos autour d'une image maitresse (on explore le répertoire Homol

    def meilleuresPhotosAutourMaitresse(self,maitresse,nombre):
        if nombre==-1:
            return
        repertoireHomol = os.path.join(self.repTravail,"Homol")  # répertoire des homologues     
        if os.path.isdir(repertoireHomol)==False:
            return 
        listeTaille = list()
        oschdir(repertoireHomol)        
        for e in os.listdir():                                  # balaie tous les fichiers contenant les points homologues
            if maitresse.upper() in e.upper():
                oschdir(os.path.join(repertoireHomol,e))            
                for f in os.listdir():
                    listeTaille.append((f, os.path.getsize(f)))   # répertoire, nom du fichier et taille
        oschdir(self.repTravail)        
        listeTaille.sort(key= lambda e:  e[1],reverse=True)     # trie la liste des fichiers par taille
        # supprime l'extension du fichier (toto1234.JPG.dat ou .txt) et garde les N plus grands
        listeCorrigee = [os.path.splitext(e)[0] for e,f in listeTaille[0:nombre] if os.path.exists(os.path.join(self.repTravail,os.path.splitext(e)[0]))]
        listeCorrigee.append(maitresse)
        return "|".join(listeCorrigee)

    ###################### Stratégie APERODEDENIS pour trouver les maitresses et les images associées. (dépend des noms de répertoire et fichiers donnés par micmac)
    # renvoie une liste de tuple : maitresse, liste des photos associées
    # supprime version 5.51 en juin 2020

    ###################### Appareil photo : affiche le nom de l'appareil de la première photo, la focale, la taille du capteur dans dicocamera

    def outilAppareilPhoto(self,silence=None):
        if silence!="oui": self.encadre(_("Patience, recherche des métadonnées des photos..."))
        if self.pasDePhoto():return
        if self.pasDeExiftool():return
              
        texte = " ******\n" + _("Caractéristiques de l'appareil photo : ") + "\n\n"
        self.fabricant =  self.tagExif("Make")
        if self.fabricant!=str():
            texte += _("fabricant : ")+self.fabricant+"\n"
            
        self.nomCamera = self.tagExif("Model")
        if self.nomCamera==str():
            texte += _("Nom de l'appareil photo inacessible.")
        else:
            texte += _("Nom de l'appareil photo : ")+self.nomCamera+"\n"

        self.numeroSerieCamera = self.tagExif("SerialNumber")
        if self.numeroSerieCamera!=str():
            texte += _("Numéro de série de l'appareil photo : ")+self.numeroSerieCamera+"\n"
            
        self.focale35MM = self.tagExif("FocalLengthIn35mmFormat")
            
        self.focale = self.tagExif("FocalLength")
        if self.focale==str():
            texte += ("\n" + _("Pas de focale dans l'exif."))
        else:
            texte += "\n" + _("Focale : ")+ self.focale+"\n"

        if self.focale35MM=="" and "35" not in self.focale:
            texte += ("\n" + _("Pas de focale équivalente 35 mm dans l'exif :") + "\n" + _("Présence de la taille du capteur dans DicoCamera nécesssaire."))
        else:
            if self.focale35MM=="":
                texte += "\n" + _("Focale équivalente 35 mm absente de l'exif") + "\n" 
            else:
                texte += "\n" + _("Focale équivalente 35 mm : ")+ self.focale35MM+"\n"            

        if not os.path.isfile(self.CameraXML):
            texte += "\n" + _("DicoCamera.xml non trouvé : paramètrer au préalable le chemin de MicMac\\bin.")
        else:
            self.tailleCapteurAppareil()
            if self.tailleCapteur==str():
                texte += "\n" + _("L'appareil est inconnu dans DicoCamera.XML.") + "\n"                          
            else:
                texte += "\n" + _("L'appareil est connu dans DicoCamera.XML.") + "\n"+\
                          _("Taille du capteur en mm : ")+"\n\n"+self.tailleCapteur+"."
                
        self.controlePhotos()
        if self.dimensionsDesPhotos:
            if self.dimensionsOK:
                texte += "\nDimensions des photos en pixel :\n"+str(self.dimensionsDesPhotos[0][1][0])+" - "+str(self.dimensionsDesPhotos[0][1][1])   
            else:
                lesDimensions = set([y for (x,y) in self.dimensionsDesPhotos])
                texte += "\n\nPlusieurs dimensions pour les photos :\n"+str(lesDimensions)

        # écriture du résultat dans le fichier trace et présentation à l'écran
        
        self.effaceBufferTrace()
        self.ajoutLigne("\n\n" + _("Appareil photo :") + "\n"+texte)

        if silence=="oui": return        
        self.encadre(texte)

        if self.nombreDeExifTagDifferents("Model")>1:
            message = "\n\n"+_("Attention : les photos proviennent de plusieurs appareils différents.\n Voir l'item 'toutes les focales...' et le menu expert.")
            self.ajoutLigne(message)
            self.encadrePlus(message)

        self.ecritureTraceMicMac()
        
    # tag dans l'exif : renvoi la valeur du tag 'tag' dans l'exif d'une photo
    # si pas de photo précise : la première photo (on suppose qu'elles sont identiques pour toutes les photos)
                          
    def tagExif(self,tag,photo=""):
        if photo=="":photo=self.photosSansChemin[0]
        photo = os.path.basename(photo)
        if (tag,photo) in self.lesTagsExif:
            return self.lesTagsExif[tag,photo]
        self.tag = str()        
        exif = [self.exiftool,
                "-"+tag,
                photo]            
        self.lanceCommande(exif,
                           filtre=self.FiltreTag)
        self.effaceBufferTrace()
        self.lesTagsExif[tag,photo] = self.tag
        print("en principe ne devrait pas se produire, tag absent de l'exif : tagexif recalculé")
        return self.tag
    
    def FiltreTag(self, ligne):                             # ne retourne rien (pour éviter la trace, mais positionne si possible self.tag
        if "can't open" in ligne:
            return _("Erreur dans exiftool : ")+ligne
        try: self.tag = ligne.split(":")[1].strip()         # pour récupérer le nom, et supprimer le retour chariot de fin de ligne
        except Exception as e: print(_("erreur tagExif : "),str(e))
        return None

    # tags dans l'exif : renvoi la valeur du tag 'tag' dans l'exif de toutes les photos
                          
    def tagsExif(self,tag):
              
        self.tags = list()
        if self.systeme=='nt':
            exif = [self.exiftool,
                "-"+tag,
                os.path.join(self.repTravail,"*"+self.extensionChoisie)]
        else:
            exif = [self.exiftool,
                "-"+tag,
                os.path.join(self.repTravail)]         
        self.lanceCommande(exif,
                           filtre=self.FiltreTags)
        return self.tags

    def FiltreTags(self, ligne):
        ajout = afficheChemin(ligne.strip().replace("=",""))
        ajout=ajout.replace(afficheChemin(self.repTravail),"")    # pour ne pas afficher le chemin
        self.tags.append(ajout+"\n")                              # pour récupérer le nom, et supprimer le retour chariot de fin de ligne
        return None

    # Importe tous les tags utiles pour le programme lors du choix des photos : raz puis abonde self.lesTagsExif[tag,photSansChemin]

    def tousLesTagsUtiles(self):
        self.lesTagsExif = dict()
        self.photoEnCours = str()
        exif = [self.exiftool,"-s",]+["-"+e for e in self.tagsExifUtiles]+[os.path.join(self.repTravail),]
        self.lanceCommande(exif,
                           filtre=self.filtreTousLesTags)
        return

    def filtreTousLesTags(self, ligne):      
        if ".JPG" in ligne:
            self.photoEnCours=os.path.basename(ligne[:-1]) # pas très propre (-1 pour supprimer le retour chariot)
        if not self.photoEnCours:
            return
        tag = ligne.split()[0]
        if tag in self.tagsExifUtiles:
            valeur = ligne.split(":")[1].strip()
            self.lesTagsExif[(tag,self.photoEnCours)] = valeur
        return

    ##################### Prise en compte des données GPS des exifs (voir : https://micmac.ensg.eu/index.php/OriConvert )
    # appelé à 3 endroits : 1) choix des photos ; 2) choix du reférentiel (menu expert) 3) ré-utilisation des données GPS embarquées
    # la variable self.repereChoisi indique l'état du repére : adeterminer, absent, supprimé ou le nom du repère choisi
    # ecritureOriTxtInFile() permet de savoir si il y a des données GPS embarquées avant de lancer OriConvert
    # retour False et repereChoisi = Absent si pas de données GPS dans les exifs
    
    def GpsExif(self):
        self.encadre(_("Patience, données GPS en cours d'extraction depuis les exifs des photos"))
        self.messageRepereLocal = str()
        if not  self.ecritureOriTxtInFile():     # s'il n'y a pas d'infos GPS dans les exifs : retour False  =pas de gps"
            self.repereChoisi = self.repereAbsent
            self.messageRepereLocal = self.repereAbsent
            return False
        
        # si repére absent (valeur par défaut) ou supprimé que l'on veut réactiver, on choisit le repére local :
        
        if self.repereChoisi in (self.repereADeterminer,self.repereAbsent,self.repereSupprime):    # s'il n'y a pas encore de reperechoisi on prend un repère local tangent
            self.repereChoisi = self.repereLocalXml

        # si repére local : il faut créer un xml le décrivant :
            
        if self.repereChoisi==self.repereLocalXml: # création du fichier xml repère local tangent si besoin
            self.creationRepereLocal()          # création du système de coordonnée local RTL (repére terrestre local) : SysCoRTL.xml

        # création, à partir des données GPS récupérée par ecritureOriTxtInFile, et du référentiel choisi, d'une orientation provisoire par OriConvert (nav-brut)
        # CenterBascule sera appelé pour transformer cette orientation provisoire en orientation définitive, nav,  lorsque Tapas sera fini
        
        self.lanceOriconvert()              # appel de oriConvert : Création d'une orientation provisoire et brute, suivant le repère choisi (mot clé ou fichier xml)
            
        return True
 
    def creationRepereLocal(self):          # le point origine du repere local est la position du drone lors de la première photo
                                            # les coordonénes sont planes et métriques, l'orientation est celle du wgs84
                                            # on peut considérer que localement il s'agit d'un Lambert93 translaté au point origine avec une bonne approximation
        if self.repereChoisi!=self.repereLocalXml:
            print("repereChoisi=",self.repereChoisi," <> repereLocal = ",self.repereLocalXml)
            return
        pourNuage = self.photosSansCheminPourNuage()
        photo = pourNuage[0]
        latitude = DMS2DD(self.lesTagsExif[("GPSLatitude",photo)])
        longitude = DMS2DD(self.lesTagsExif[("GPSLongitude",photo)])
        altitude = self.lesTagsExif[("AbsoluteAltitude",photo)]
        xml = self.sysCoRTL
        xml = xml.replace("latitude",str(latitude))
        xml = xml.replace("longitude",str(longitude))
        xml = xml.replace("altitude",str(altitude))
        with open(self.repereChoisi,"w") as out:
            out.write(xml)
        x,y = conversionWGS84enRGF93(latitude,longitude)
        self.messageRepereLocal =   ( "----------------------\n"+ 
                     _("Le point origine du repere local est la position du drone lors de la photo : ")+photo+".\n\n"+
                     _("Dans le référentiel WGS84 (EPSG 4326) les coordonnées de ce point sont :")+"\n"+
                     _("latitude : ")+self.lesTagsExif[("GPSLatitude",photo)]+" "+_("soit en degrés décimaux : ")+str(latitude)+"\n"+
                     _("longitude : ")+self.lesTagsExif[("GPSLongitude",photo)]+" "+_("soit en degrés décimaux : ")+str(longitude)+"\n")
        if lambert93OK(latitude,longitude):
            self.messageRepereLocal +=  ( "----------------------\n"+      
                     _("Dans le reférentiel géographique LAMBERT93 (EPSG 2154) les coordonnées de ce point sont :")+"\n"+
                     _("X : ")+str(round(x,2))+"\n"+
                     _("Y : ")+str(round(y,2))+"\n"+
                     _("Les référentiels WGS84 et Lambert93 sont virtuellement identiques : la translation X,Y ci-dessus permet de recaler les nuages en Lambert93.")+"\n"
                    )
        else:
            self.messageRepereLocal +=  ( "----------------------\n"+ _("Le point origine n'est pas situé dans la zone de validité du référentiel Lambert 93"))         
        self.ajoutLigne(self.messageRepereLocal)
        self.ecritureTraceMicMac()

    def creationRepereEpsg(self,epsg):  # Ecriture du fichier xml décrivant le référentiel epsg au format proj4
                                        # code epsg  en paramètre, si erreur ne change pas le repère choisi
        # controle valeur epsg : ce doit être un nombre entier supérieur à 2000 :
        try:
            from pyproj import CRS
            from pyproj import _datadir, datadir            
        except Exception as e:
            self.encadre(_("Pour choisir un ESPG il est nécessaire que le module python 'pyproj' soit installé. Utiliset 'pip install pyproj'.")+
                         "\n"+str(e))
            return
        try: int(epsg)
        except:
            self.encadre(_("Le code ESPG doit être un nombre entier supérieur à 2000 : ")+epsg)
            return False
        if int(epsg)<2000:
            self.encadre(_("Le code ESPG doit être un nombre entier supérieur à 2000 : ")+epsg)
            return False                         
                                        
        self.nomEpsg = str()
        try: crs = CRS.from_epsg(epsg)   # instancie l'objet crs pour la valeur de l'epsg
        except Exception as e:
            self.encadre(_("Problème concernant l'epsg, non trouvé dans proj : ")+epsg+"\nErreur : "+str(e)+"\nPROJ_LIB="+str(os.environ["PROJ_LIB"]))
            return False
        self.nomEpsg = crs.to_string()+"\n"+crs.name # nom de la projection
        proj4 = crs.to_proj4()      # récupère la description du référentiel epsg au format proj4
        
        # controle de proj4 (certaines projections ne sont pas supportées par oriconvert) :
        
        if proj4[:5]!="+proj":
            self.encadre(_("Projection proj4 incorrecte : ")+self.nomEpsg+"\nProj4 = "+proj4)            
            return False            
        if proj4[:13]=="+proj=longlat":        
            self.encadre(_("Projection de type longitude latitude, non supportée, en choisir une autre : ")+self.nomEpsg)            
            return False
        if proj4[:12]=="+proj=sterea":        
            self.encadre(_("Projection de type sterea, non supportée : ")+self.nomEpsg)            
            return False

        # apriori ok pour proj4 :

        SysEpsgChoisi = self.SysCoEpsg.replace("epsg2proj4", proj4) # constitue le corps du fichier xml
        SysEpsgChoisi = SysEpsgChoisi.replace("nomEpsg", self.nomEpsg) # commentaire, constitue le corps du fichier xml           
        with open(self.repereEpsgXml,"w") as out:
            out.write(SysEpsgChoisi)
        self.ajoutLigne(_("Reférentiel EPSG choisi : ")+self.nomEpsg)
        
        return True

    def lanceOriconvert(self):              # crée une orientation brute à partir du fichier self.nomOriGPS créé par self.ecritureOriTxtInFile (données GPS des photos)
                                            # cette orientation est définie dans le repère choisi : local  ou Lambert 93 ou GeoC...
                                            # self.repereChoisi est soit un mot clé (Lambert93, soir le nom d'un fichier xml contenant la description du repère
                                            # cette orientation devra être "mixée" avec l'orientation issue de Tapas par centerBascule
                                            # voir : http://forum-micmac.forumprod.com/first-time-micmac-grandleez-tutorial-t1352-10.html
                                            # datum lambert 93  (http://magrit.cnrs.fr/docs/projection_list_fr.html)
                                            # +proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs                                            
        convert = [self.mm3d,
                "OriConvert",
                "OriTxtInFile",
                self.nomOriGPS,
                "nav-Brut",
                # nom du répertoire  orientation créée par la commande OU nom prédéfini d'un repère (GeoC, WGS84, Lambert93, nom d'un fichier XML)
                "ChSys=DegreeWGS84@"+self.repereChoisi] 
        self.lanceCommande(convert,
                           filtre = self.filtreOriConvert,
                           info = _("Les triplets sont les écarts X,Y,Z par rapport à la photo précédente et T = le délai écoulé"))

    def filtreOriConvert(self,ligne):
        try: self.exe.terminate()
        except Exception as e : print("erreur self.exe.terminate=",str(e))
        if "insuitable" in ligne:
            return ligne

# gestion des données de navigation gps (drones) : choix d'un repère pour calculer le nuage : Local, Lambert, Géocentrique, WGS84

    def choixRepereLocal(self):
        self.choixRepere(self.repereLocalXml," repere tangent local")
            
    def choixRepereGeoC(self):      # repereGeocentrique cartésien
        self.choixRepere(self.repereGeoc)
  
    def choixRepereWGS84(self):     # WGS84 cartésien
        self.choixRepere(self.repereWGS84)        
        
    def choixRepereLambert93(self):
        self.choixRepere(self.repereLambert93)

    def choixRepereEpsg(self):
        epsg = MyDialog(fenetre,_("Code EPSG du référentiel souhaité"),
                        basDePage=_("Les codes epsg se trouvent par exemple sur epsg.org ou epsg.io")+"\n"+
                        "Exemple pour la Réunion : 2975").saisie
        if epsg in (False,""):
            self.encadre(_("Epsg : Abandon utilisateur"))
            return
        # si ok création du fichier XML décrivant le référentiel, sera utilisé par OriConvert
        if self.creationRepereEpsg(epsg):
             self.choixRepere(self.repereEpsgXml," EPSG = "+self.nomEpsg)   
        
    def choixRepere(self,choix,info=""):
        self.referentielOK = False # même si c'est le même...
        if self.repereChoisi==self.repereAbsent:
            self.encadre(self.messageGPSDroneAbsent)
            return
        self.repereChoisi = choix
        if self.GpsExif(): 
            message = _("Référentiel choisi : %s") % choix+"\n"+info
            if self.etatDuChantier == 5:    # si le chantier est fini on le réactive
                self.etatDuChantier=4
        else:
            message = _("Le référentiel choisi n'a pas pu être établi")
        self.ajoutLigne("\n"+message+"\n")
        self.encadre(message)

# Affiche les infos sur le repère choisi

    def afficheMessageRepereLocal(self):

        if self.repereChoisi==self.repereLocalXml:
            self.encadre("'"+self.messageRepereLocal+"'")
        elif self.repereChoisi==self.repereSupprime:
            self.encadre(_("Les données GPS  ne sont pas utilisées sur demande de l'utilisateur."))
        elif self.repereChoisi==self.repereAbsent:
            self.encadre(self.messageGPSDroneAbsent)
        elif self.repereChoisi==self.repereEpsgXml:
            self.encadre(_("Le référentiel choisi est défini par un code : ")+self.nomEpsg)
        else:
            self.encadre(_("Le référentiel choisi est : ")+self.repereChoisi)


# suppression/ajout des données de navigation par l'utilisaeur :
                   
    def swapGPSEmbarque(self):        # suppression ou ajout du fichier des coordonnées GPS des appareils, du repereLocal et du répertoire orientation issu de ces données

        if self.repereChoisi==self.repereAbsent:
             self.encadre(self.messageGPSDroneAbsent)
             return
        if self.repereChoisi == self.repereSupprime:    # le repère a été supprimé : on le remet !
            self.GpsExif()
            message = "\n"+_("Les données GPS embarquées dans les photos du drone sont de nouveau utilisées sur demande de l'utilisateur.")+"\n"
            self.ajoutLigne(message)
            self.encadre(message)            
        else:                                           # repére existe : on le supprime
            self.supOriNavBrut()                        # supprime l'orientation (fichiers xml, répertoire Ori-nav-Brut, affecte repèreChoisi
            self.messageRepereLocal = str()
            message = "\n"+_("Les données GPS embarquées dans les photos du drone ne sont plus utilisées sur demande de l'utilisateur.")+"\n"
            self.ajoutLigne(message)
            self.encadre(message)

        self.miseAJourLibelleNavigationGPS()
        self.afficheEtat()

    def supOriNavBrut(self):
        supprimeFichier(self.nomOriGPS)     # OriGPS.TXT
        supprimeFichier(self.repereLocalXml)# "SysCoRTL.xml"
        retour1 = supprimeRepertoire("Ori-nav-Brut")
        retour = supprimeRepertoire("Ori-nav")
        if self.repereChoisi!=self.repereAbsent:       # s'il y a des données GPS embarquées :
            self.repereChoisi = self.repereSupprime        
        
    def miseAJourLibelleNavigationGPS(self):

        if self.repereChoisi==self.repereADeterminer:
            self.GpsExif()
            
        if self.repereChoisi == self.repereSupprime:
            self.menuNavigationGPS.entryconfig(2, label=_("Navigation GPS : utiliser les données GPS de navigation"),state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(4, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(5, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(6, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(7, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(8, state = tkinter.DISABLED)            
        elif self.repereChoisi == self.repereAbsent:
            self.menuNavigationGPS.entryconfig(2, label=self.messageGPSDroneAbsent,state = tkinter.DISABLED)          
            self.menuNavigationGPS.entryconfig(4, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(5, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(6, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(7, state = tkinter.DISABLED)
            self.menuNavigationGPS.entryconfig(8, state = tkinter.DISABLED)             
        else:
            self.menuNavigationGPS.entryconfig(2, label=_("Navigation GPS : ne pas utiliser les données GPS de navigation"),state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(4, state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(5, state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(6, state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(7, state = tkinter.NORMAL)
            self.menuNavigationGPS.entryconfig(8, state = tkinter.NORMAL)              

    # écriture du fichier des coordonnées gps des photos :

    def ecritureOriTxtInFile(self):         # écrire les données GPS de navigation dans un fichier texte
        if os.path.exists(self.nomOriGPS):  # il y a dèjà un repère (OriGPS.TXT) supprimé si l'utilisateur n'en veut plus
            return True

        # vérification de l'existence des données GPS puis écriture fichier
        # F=N Y X Z K W P
        # image latitude longitude altitude yaw pitch roll
        #                                  "gpslatitude",                                       # les tags pour les photos prises à partir de drones
        #                                  "gpslongitude",                                      
        #                                  "AbsoluteAltitude",
        #                                  "relativealtitude",
        #                                  "gimbalyawdegree",
        #                                  "gimbalpitchdegree",
        #                                  "gimbalrolldegree",
        pourNuage = self.photosSansCheminPourNuage()
        if not pourNuage: return False
        for photo in pourNuage:
            if ("GPSLatitude",photo) not in self.lesTagsExif:         return False
            if ("GPSLongitude",photo) not in self.lesTagsExif:        return False
            if ("AbsoluteAltitude",photo) not in self.lesTagsExif:    return False
            if ("GimbalYawDegree",photo) not in self.lesTagsExif:     return False
            if ("GimbalPitchDegree",photo) not in self.lesTagsExif:   return False
            if ("GimbalRollDegree",photo) not in self.lesTagsExif:    return False
##            if ("FlightYawDegree",photo) not in self.lesTagsExif:     return False
##            if ("FlightPitchDegree",photo) not in self.lesTagsExif:   return False
##            if ("FlightRollDegree",photo) not in self.lesTagsExif:    return False

            
        # les données existent pour toutes les photos, on écrit le fichier :
        with open(self.nomOriGPS,"w",encoding='utf-8') as ori:
            ori.write("#F=N Y X Z K W P\n")
            ori.write("# photo latitude longitude altitude yaw pitch roll de la camera\n")
            for photo in pourNuage:
                yaw = float(self.lesTagsExif[("GimbalYawDegree",photo)])
                pitch = float(self.lesTagsExif[("GimbalPitchDegree",photo)])
                roll = float(self.lesTagsExif[("GimbalRollDegree",photo)])
                ligne = "\t".join([photo,
                          str(DMS2DD(self.lesTagsExif[("GPSLatitude",photo)])),
                          str(DMS2DD(self.lesTagsExif[("GPSLongitude",photo)])),
                          str(self.lesTagsExif[("AbsoluteAltitude",photo)]),
                          str(yaw),
                          str(pitch),
                          str(roll)                           
                                   ])
                ori.write(ligne+"\n")
        return True
                           

# utilitaires : photos pour nuage, coordonnées en degré/minutes/secondes/orientaion vers degrés décimaux
         
    def photosSansCheminPourNuage(self):    # retourne les photos sans chemin sans les photos pour calibration exclusive
        pourNuage = self.photosSansChemin
        if self.calibSeule.get() and self.photosCalibrationSansChemin:
            pourNuage = [e for e in self.photosSansChemin if e not in self.photosCalibrationSansChemin]
        return pourNuage

    
    ##################### Taille du capteur de l"appareil
        
    # retour 1 et positionne la taille du capteur dans self.tailleCapteur, si le nom est connu
    # retour -1 si pas de nom d'appareil
    # retour -2 si pas de fichier dicocamera
    # retour None si appareil absent dans dicocamera

                          
    def tailleCapteurAppareil(self,appareil=""):
        
        self.tailleCapteur = str()                      # par défaut retour ""
        if appareil == str():                           # si pas de nom d'appareil : retour
            appareil=self.nomCamera
        if appareil==str():
            return
        
        self.dicoCamera = str()
        if os.path.exists(self.CameraXML):              # si pas de fichier dicoCamera : retour (il est vrai que la taille pourrait être ailleurs !) 
            with  open(self.CameraXML) as infile:
                self.dicoCamera = infile.readlines()    #lecture dicoCamera.xml
        else: return -2
                          
        texte = str()
        rechercher="<Name>"+appareil+"</Name>"
        rechercher=rechercher.replace(" ","")
        for e in self.dicoCamera:                       # recherche du nom de l'appareil dans dicoCamera
            if texte=="vu":
                if "SzCaptMm" in e:                     # le nom est repéré, voit-on la taille ?
                    self.tailleCapteur = e.replace("<SzCaptMm>","").replace("</SzCaptMm>","").strip().replace(" "," mm - ",1)+" mm"
                    return 1                            # la taille est trouvée : on quitte
                if "</CameraEntry>" in e:               # pas de taille trouvée sous ce nom
                    texte = str()                       # on poursuit
            if rechercher in e.replace(" ",""):                         # le nom de l'appareil est trouvé
                texte="vu"
    # Mise à jour de DicoCamera

    def miseAJourDicoCamera(self):
        
        if self.pasDePhoto():return
        if self.pasDeMm3d():return
        if self.pasDeExiftool():return
        if not os.path.isfile(self.CameraXML):
          self.encadre(_("DicoCamera.xml non trouvé : paramètrer au préalable le chemin de MicMac\\bin."))
          return
        message = str()
        self.encadre("Patience... recherche les noms de tous les appareils photos du chantier...")
        nb = self.nombreDeExifTagDifferents("Model")
        self.menageEcran()
        if nb == 0:
            self.encadre(-("Pas de modèle d'appareil photo dans les exif."))
        self.nomCamera = self.lesTags[0]
        if self.nomCamera==[]:
            message=_("\Pas de nom d'appareil photo dans l'exif")
            self.encadre(message)
        if nb == 1:
            if self.tailleCapteurAppareil()==1:
                message =(   "\n"+_("Le fichier DicoCamera.xml contient déjà la taille du capteur pour l'appareil :") + "\n\n"+
                             self.nomCamera+"\n\n"+ _("taille  = ")+self.tailleCapteur+"\n\n"+_("Pas de modification possible."))
                self.encadre(message)
            else:
                self.menageEcran()
                self.lesAppareilsPourDicocamera = [self.nomCamera]
                self.item1001.configure(text=_("Pour l'appareil ")+self.nomCamera)
                self.item1000.pack()

        if nb > 1:
            self.choisirUnePhoto(
                            self.lesTags,
                            titre=_("Choisir le ou les appareils à mettre à jour"),
                            message=_("Liste des appareils du chantier : \n"),
                            mode='extended',
                            objets='appareils')
            if self.selectionPhotosAvecChemin:
                self.menageEcran()
                self.lesAppareilsPourDicocamera = self.selectionPhotosAvecChemin                
                self.item1001.configure(text=_("Pour les appareils choisis :\n")+"\n".join(self.lesAppareilsPourDicocamera))
                self.item1000.pack()    
     # ne rien ajouter ici qui puisse fermer les boîtes de dialogue

    # écriture des dimensions du capteur dans dicocamera.xml
        
    def dimensionCapteurOK(self): 
        if not os.path.isfile(self.CameraXML):
            self.encadre(_("Paramètrer au préalable le chemin de MicMac\\bin."))
            return
        # controle :
        vals = self.item1003.get().split()
        try:
            float(vals[0])
            float(vals[1])
        except:
            self.encadre("Dimensions capteur incorrectes : "+self.item1003.get()+"\n exemple correct : 7.5 12.3")
            return
        dimension = " ".join(vals)
        # paragraphe à rajouter à DicoCamera  : modif
        modif = str()
        message = str()
        for nomCamera in self.lesAppareilsPourDicocamera:
            if self.tailleCapteurAppareil(nomCamera)==1 and self.tailleCapteur!=" mm":
                message +=("\n"+_("Le fichier DicoCamera.xml contient déjà la taille du capteur pour l'appareil :") + "\n\n"+
                             nomCamera+"\n\n"+ _("taille  = ")+self.tailleCapteur+"\n\n"+_("Pas de modification possible."))
            else:
                texte = self.dicoCameraXMLTaille.replace(_("NomCourt"),nomCamera)          
                texte = texte.replace(_("Nom"),nomCamera)
                texte = texte.replace(_("tailleEnMM"),dimension)
                modif += texte
        #lecture dicocamera.xml :
        with  open(self.CameraXML) as infile:
            self.dicoCamera = infile.readlines()    #lecture dicoCamera.xml
        # ajout du paragraphe enfin de xml : on vérifie d'abord sa présence parmi les 10 dernières lignes du fichier
        if self.dicoCameraXMLFin not in "".join(self.dicoCamera[-10:]):
            self.encadre(_("Fichier DicoCamera.xml invalide : balise de fin manquante : ")+"\n"+self.dicoCameraXMLFin)
            return
        newDico = "".join(self.dicoCamera).replace(self.dicoCameraXMLFin,modif+self.dicoCameraXMLFin)
        if os.path.getsize(self.CameraXML)>0:                       # pour éviter de copier un fichier "vide"
            try: shutil.copy(self.CameraXML,self.CameraXML+".sav")
            except: pass
        if os.path.exists(self.CameraXML+".sav"):
            try:
                with  open(self.CameraXML,mode="w") as outfile:
                    outfile.write(newDico)
            except:
                self.encadre(_("Erreur lors de l'écriture de DicoCamera.xml") + "\n" + _("Une sauvegarde a été créée : DicoCamera.xml.sav"))
                return
        else:
            self.encadre(_("Dimensions du capteur non mis à jour") + "\n")
            return

        self.encadre(_("Mise à jour de dicocamera.xml : ") + "\n"+modif+"\n"+message)
        

    def dimensionCapteurKO(self):
        self.encadre(_("Dimensions du capteur non mis à jour"))

    def toutesLesFocales(self):
        self.encadre(_("Patience, recherche des focales dans les exifs..."))
        if self.pasDePhoto():return
        if self.pasDeExiftool():return        
        texte = _("Les focales, les focales équivalentes en 35mm et le nom des appareils photos :")+"\n\n"
        texte += "\n".join(self.tagsExif("FocalLength"))
        texte += "\n".join(self.tagsExif("FocalLengthIn35mmFormat"))
        texte += "\n".join(self.tagsExif("Model"))        
        self.cadreVide()        
        self.effaceBufferTrace()
        self.ajoutLigne(texte)
        self.texte201.see("1.1")


    ################################## le menu Expert

    def lignesExpert(self):
        self.ecritureTraceMicMac()        
        self.cadreVide()        # ménage écran, ouverture trace
        texte = _("Ceci est une console système : Saisir une ou plusieurs ligne(s) de commande") + "\n"        
        if self.etatDuChantier==0:
            texte+="\n\n"+_("Attention : Le chantier n'existe pas.")                      

        bas = (
               _("Entrer soit une commande MicMac, par exemple : mm3d GCPBascule .*.JPG Arbitrary")+"\n"+             
               _("soit une commande du système, par exemple sous windows : del /S /Q Tmp-MM-Dir")+"\n"+
               _("ou une commande mm3d interactive comme : mm3d vC3DC")+"\n"+               
               _("Possibilité de copier une commande du fichier mm3d-LogFile.txt.")+"\n"+                 
               _("Le tout sous votre responsabilité"))                
        new = MyDialogTexte(fenetre,texte,basDePage=bas,boutonDialogueTexteOk="Exécuter")
        if new.saisie=="":
            return
        lignes = new.saisie.split("\n")
        self.cadreVide()
        self.ecritureTraceMicMac()
        self.ligneCmd  = str()
        for ligne in lignes:
            if ligne:   #si besoin on ajoute le chemin vers mm3d et on retire les "
                if ligne[:4]=="mm3d":ligne=os.path.join(self.micMac,ligne)
                self.ligneCmd += "commande = "+ligne+"\n"
                self.lanceCommande(ligne.replace('"'," ").split(),filtre=self.filtreCmd)
        oschdir(self.repTravail)   # on ne sait pas ce qu'a fait l'utilisateur
        self.ecritureTraceMicMac()         
        self.afficheTexte(self.ligneCmd)        
        
    def filtreCmd(self,ligne):
        self.ligneCmd += ligne
        return ligne

    @decorateTry                # si un fichier n'est pas "lisible"
    def lignesPython(self):
        self.ecritureTraceMicMac()        
        self.cadreVide()        # ménage écran, ouverture trace
        texte = _("Ceci est une console python : Saisir une ou plusieurs ligne(s) de script python") + "\n"        
        if self.etatDuChantier==0:
            texte+="\n\n"+_("Attention : Le chantier n'existe pas.")                      

        bas = (
               _("Entrer soit une commande python, par exemple : locals()")+"\n"+
               _("la commande  sera éxécutée puis évaluée et les résultats affichés dans une fenetre")+"\n"+
               _("et aussi dans la trace synthétique.")+"\n"+                 
               _("Le tout sous votre responsabilité"))                
        new = MyDialogTexte(fenetre,texte,basDePage=bas,boutonDialogueTexteOk="Exécuter")
        if new.saisie=="":
            return
        lignes = new.saisie.split("\n")
        self.cadreVide()
        self.ecritureTraceMicMac()
        entete = "\n"+_("résultat de la commande python : ")+str(lignes)+"\n"
        self.encadre(entete)
        self.ajoutLigne(heure()+entete)
        for ligne in lignes:
            if ligne:   #si besoin on ajoute le chemin vers mm3d et on retire les "
                resul1 = str()
                resul2 = str()
                entete="\n"+_("commande : ")+ligne
                self.encadrePlus("\n"+entete)
                e_exec=e_eval=str()
                try: resul1=exec(ligne)
                except Exception as e:
                    e_exec=str(e)
                    print("erreur exec : ",str(e_exec))
                try: resul2=eval(ligne,globals(),locals())
                except Exception as e:
                    e_eval=str(e)
                    print("erreur eval : ",str(e_eval))              
                if resul1:
                    r="\n"+_("L'exécution de la commande python retourne la valeur : ")+"\n"                     
                    r+="\n".join(wrap(str(resul1),100))   # on coupe tout les 100 caractères                
                else:
                    print("e exec = ",e_exec)
                    r="\n"+_("L'éxécution de la commande python ne retourne pas de valeur")+"\n"+e_exec
                    
                self.encadrePlus("\n"+r)
                if resul2:
                    r="\n"+_("L'évaluation de la commande python retourne la valeur : ")+"\n"                     
                    r+="\n".join(wrap(str(resul2),100))   #on coupe tout les 100 caractères                
                else:                   
                    r="\n"+_("L'évaluation de la commande python ne retourne pas de valeur")+"\n"+e_eval
                self.encadrePlus("\n"+r)
                self.ajoutLigne(r)
                    
        self.ecritureTraceMicMac()                
        oschdir(self.repTravail)   # on ne sait pas ce qu'a fait l'utilisateur
        
    def nbPointsGCPActifs(self):
        # suppression des points supprimés # listePointsGPS : 6-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant, incertitude)
        liste = list(self.listePointsGPS)
        [self.listePointsGPS.remove(e) for e in liste if not e[4]]
        listePoints = [e[0] for e in self.listePointsGPS]
        # suppression des points placés sur les phtos (dicoPointsGPSEnPlace key = nom point, photo avec chemin, identifiant, value = x,y
        dico = dict(self.dicoPointsGPSEnPlace)
        [self.dicoPointsGPSEnPlace.pop(key,None) for key in dico if key[0] not in listePoints]      
        return listePoints.__len__()

############################# Recopie depuis c'autres chantier : points homologues, points GCP, orientation 

    def ajoutPointsGPSAutreChantier(self):  # à revoir : double ouverture du fichier param de l'autre chantier
        self.menageEcran()
        rapport = str()
        nbAjoutPlace = int()
        nbAjout = int()       
      
        bilan = self.choisirUnChantier(_("Choisir le chantier pour ajouter les points GCP."),filtre="GCP")                # boite de dialogue de sélection du chantier à ouvrir, renvoi : self.selectionRepertoireAvecChemin
        if bilan!=None:
            self.encadre(_("Aucun chantier choisi.") + "\n" + bilan + "\n")
            return   
        fichierParamChantierAutre  =   os.path.join(self.selectionRepertoireAvecChemin,self.paramChantierSav)
        if not os.path.exists(fichierParamChantierAutre):
            self.encadre (_('Chantier choisi %s corrompu. Abandon.') % (self.selectionRepertoireAvecChemin))            
            return
               
        try:            # Restauration des points GCP de l'autre chantier :
            sauvegarde1=open(fichierParamChantierAutre,mode='rb')
            r=pickle.load(sauvegarde1)
            sauvegarde1.close()
            listePointsGPS             =   r[12]
            dicoPointsGPSEnPlace       =   r[20]         
            idPointGPS                 =   r[23]

            if listePointsGPS.__len__()==0:
                self.encadre(_("Pas de points GCP dans le chantier %s.") % (os.path.basename(self.selectionRepertoireAvecChemin)))
                return

            # pour assurer la compatibilité ascendante suite à l'ajout de l'incertitude dans la description des points GCP
            # passage vers la version 2.60 de la liste des points GCP (un item de plus dans le tuple)

            if listePointsGPS[0].__len__()==6:  # pour compatibilité avec les version ne comportant pas l'incertitude
                    listePointsGPS = [[a,nom,x,y,z,ident,"1 1 1"] for a,nom,x,y,z,ident in listePointsGPS]

        except Exception as e:
            self.encadre (_('Chantier choisi %s corrompu. Abandon.') % (self.selectionRepertoireAvecChemin))                
            print(_("Erreur restauration points GCP : "),str(e))
            return

        self.ajoutLigne (_('Ajout des points GCP du chantier : %s') % (self.selectionRepertoireAvecChemin)+"\n")         
        # 3 variables : self.dicoPointsGPSEnPlace, self.listePointsGPS et self.idPointGPS pour le chantier en cours et idem (sans self.) pour le chantier a ajouter
        # dicoPointsGPSEnPlace key = nom du point, photo avec chemin, identifiant, value = x,y
        # listePointsGPS : 7-tuples (  nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant,incertitude)
        # idPointGPS : entier, identifiant du dernier point GCP 
            
        if self.nbPointsGCPActifs()!=0:   # il y a des points actifs : on les supprime
            self.supprimerTousLesPointsGCP()
            self.ajoutLigne(_("Suppression des points GCP précédents."))
        
        # 1) Modifier la clé du dico lu : chemin de la photo et identifiant par ajout de la valeur de self.idPointGPS
        # si la photo existe alors ajout dans le dico du chantier en cours       
        for nom,photo,identifiant in dicoPointsGPSEnPlace.keys():
            nouvelId        = identifiant + self.idPointGPS
            nouveauNom      = nom
            nouvellePhoto   = os.path.join(self.repTravail,os.path.basename(afficheChemin(photo)))            
            if os.path.exists(nouvellePhoto):            
                self.dicoPointsGPSEnPlace[nouveauNom,nouvellePhoto,nouvelId] = dicoPointsGPSEnPlace[nom,photo,identifiant]  # la photo existe, on ajoute au dico des points en place l'identifiant change
                nbAjoutPlace += 1
        # 2) Modifier la liste des points GCP : identifiant pat ajout de la valeur de self.idPointGPS, éviter les noms en double
        for nom,x,y,z,actif,identifiant,incertitude in listePointsGPS:
            if actif:
                nouvelId = identifiant + self.idPointGPS
                nouveauNom = nom
                self.listePointsGPS.append([nouveauNom,x,y,z,actif,identifiant,incertitude])
                nbAjout += 1
                rapport += nom+" "+x+" "+y+" "+z+"\n"
        
        self.idPointGPS = 1 + max ([f for a,b,c,d,e,f,g in self.listePointsGPS])    # 3) Trouver la nouvelle valeur de self.idPointGPS
        self.optionsReperes()       # mise à jour de la liste des widgets pour saisie :
        self.finCalibrationGPSOK()  # création des fichiers xml dico-appuis et mesures-appuis
        self.enregistreChantier()   # enregistre le chantier :
        rapport = str(nbAjout)+" "+_("points GCP ajoutés : ")+"\n"+rapport+"\n\n"+str(nbAjoutPlace)+" "+_("points placés sur les photos")

        self.encadre (rapport)   # Affichage de l'état du chantier avec les nouveaux points GCP            
        self.ajoutLigne(heure()+" "+_(": Ajout des %s points GCP du chantier %s.") % (nbAjout,fichierParamChantierAutre) +"\n\n")
        self.ajoutLigne(rapport)
        self.ecritureTraceMicMac()

    def supprimerTousLesPointsGCP(self):
        self.listePointsGPS             =   list()                      # 6-tuples (nom du point, x, y et z GCP, booléen actif ou supprimé, identifiant)
        self.idPointGPS                 =   0				# identifiant des points, incrémenté de 1 a chaque insertion
        self.dicoPointsGPSEnPlace       =   dict()                      # dictionnaire des points GCP placés dans les photos (créé par la classe CalibrationGPS)    
    
    def ajoutPointsGPSDepuisFichier(self):
        # Ajout de points GCP à partir d'un fichier de points : format =
        # #F=N X Y Z Ix Iy Iz
        # PP_5 3.6341 108.5261 38.8897 0.01 0.01 0.01         
        self.menageEcran()
        titre = _("Info sur les fichiers de points GCP")
        rapport = _("Un fichier de points GCP a le format suivant: 7 informations par ligne")+"\n"
        rapport += _("           Nom_du_point  X  Y  Z  dx  dy  dz ")+"\n"
        rapport +=_("C'est un fichier texte, séparateur espace")+"\n"
        rapport +=_("dx dy dz sont les précisions de placement en nombre de pixel, mettre 1 au minimum")+"\n"
        rapport += _("le caractère '#' en début de ligne signale un commentaire")+"\n"
        if not MyDialog_OK_KO(fenetre,titre=titre,texte=rapport,b1="Lancer",b2="Abandon").retour:
            return
        fichierPointsGPS=tkinter.filedialog.askopenfilename(title=_('Liste de points GCP : Nom, X,Y,Z, dx,dy,dz (fichier texte séparteur espace) : '),
                                                  filetypes=[(_("Texte"),("*.txt")),(_("Tous"),"*")],
                                                  multiple=False)
        
        if len(fichierPointsGPS)==0:
            return
        
        if self.nbPointsGCPActifs()!=0:   # il y a des points actifs : on les supprime
            self.supprimerTousLesPointsGCP()
            self.ajoutLigne(_("Suppression des points GCP précédents."))
        
        nbAjout = int()
        rapport = _("Format attendu : Nom X Y Z dx dy dz ")+"\n"
        rapport += _("le caractère '#' en début de ligne signale un commentaire")+"\n"
        with open(fichierPointsGPS, "r") as fichier:              
            for ligne in fichier:
                if ligne[0]!="#":
                    self.idPointGPS += 1
                    try:
                        nom,x,y,z,dx,dy,dz=ligne.split()
                        self.listePointsGPS.append([nom,x,y,z,True,self.idPointGPS,(" ").join([dx,dy,dz])])
                        rapport += _("Point ajouté : ")+ligne
                        nbAjout += 1                         
                    except Exception as e:
                        rapport += _("Ligne lue incorrecte : ")+ligne
                    
        self.idPointGPS += 1        # Déterminer la nouvelle valeur de self.idPointGPS
        self.optionsReperes()       # mise à jour de la liste des widgets pour saisie :
        self.finCalibrationGPSOK()  # création des fichiers xml dico-appuis et mesures-appuis       
        self.enregistreChantier()   # enregistre le chantier :        
        self.ecritureTraceMicMac()           
        if nbAjout>15:
            rapport = str(nbAjout)+" "+_("points GCP ajoutés : c'est beaucoup, sans doute trop.")
        rapport = str(nbAjout)+" "+_("points GCP ajoutés.")+"\n\n"+rapport
        self.encadre (rapport)
        self.ajoutLigne(heure()+" "+_(": Ajout des %s points GCP du fichier %s.") % (nbAjout,fichierPointsGPS) +"\n\n"+rapport)

    def copierPointsHomologues(self):
        self.menageEcran()
        self.selectionRepertoireAvecChemin = str()
    # 0 : en cours de construction, pas encore de photos
    # 1 : photos saisies, répertoire origine fixé, non modifiable
    # 2 : chantier enregistré
    # 3 : micmac lancé, pendant l'exécution de Tapioca et tapas, reste si plantage
    # 35 : arrêté après tapioca, points homologues conservés
    # 4 : arrêt après tapas et durant malt en cours d'exécution
    # 5 : densification terminée OK
    # 7 : densification effectuée mais pas de nuage dense généré
    # - 1 : en cours de suppression      
        # boite de dialogue de sélection du chantier à ouvrir, renvoi : self.selectionRepertoireAvecChemin
        if self.etatDuChantier == 0:
            message = _("Choisir les photos à traiter avant de copier des points homologues.")
            self.encadre(message)
            return message
        # vérification état du chantier
        
        bilan = self.choisirUnChantier(_("Choisir le chantier d'où copier les points homologues. Seuls les chantiers compatibles sont proposés."),filtre="Homol")

        if bilan!=None:
            message = _("Aucun chantier choisi.") + "\n" + bilan + "\n"
            self.afficheEtat(message)
            return message
        fichierParamChantierAutre  =   os.path.join(self.selectionRepertoireAvecChemin,self.paramChantierSav)
        if not os.path.exists(fichierParamChantierAutre):
            message = _('Chantier choisi %s corrompu. Abandon.') % (self.selectionRepertoireAvecChemin)
            self.encadre (message)            
            return message
               
        try:            # Restauration des paramètres de tapioca de l'autre chantier :
            sauvegarde1=open(fichierParamChantierAutre,mode='rb')
            r=pickle.load(sauvegarde1)
            sauvegarde1.close()
            self.modeTapioca.set            (r[6])
            self.echelle1.set               (r[7])
            self.echelle2.set               (r[8])
            self.delta.set                  (r[9])
            self.echelle3.set               (r[10])
        except Exception as e:
            message = _("Ouverture du chantier impossible : %s.") % str(e)
            self.encadre(message)
            return message         
        homolDepart = os.path.join(self.selectionRepertoireAvecChemin,"Homol")
        homolCible = os.path.join(self.repTravail,"Homol")
        bilan = copieRepertoire(homolDepart,homolCible)
        if bilan :
            self.encadre(bilan)
            return bilan                  
        if self.etatDuChantier in[1,2,3]:
            self.etatDuChantier = 35
        self.ajoutLigne ("\n"+_('Copie des points homologues depuis : %s') % (self.selectionRepertoireAvecChemin)+"\n")         
        self.ajoutLigne (_('Paramètres de Tapioca recopiés')+"\n")
        self.ecritureTraceMicMac()
        self.encadre(_("Points homologues copiés.\n Paramètres de Tapioca copiés."))            
        return str()

# l'orientation obtenue après Tapas est Ori-Arbitrary, durant tapas il peut y avoir Ori-Calib                                                                       
    def copierOrientation(self,repertoireInconnu=True):
        self.menageEcran()
        message = str()
        if self.etatDuChantier == 0:
            message = _("Choisir les photos à traiter avant de copier l'orientation.")
            self.encadre(message)
            return message
        # choisir le chantier origine de la copie de l'orientation :
        if repertoireInconnu:
            bilan = self.choisirUnChantier(_("Choisir le chantier d'où copier l'orientation. Seuls les chantiers compatibles sont proposés."),
                                           filtre="Orientation")
            if bilan!=None:
                message = _("Aucun chantier choisi.") + "\n" + bilan + "\n"
                self.afficheEtat(message)
                return message
        orientationACopier  =   os.path.join(self.selectionRepertoireAvecChemin,"Ori-Arbitrary")
        orientationCible = os.path.join(self.repTravail,"Ori-Arbitrary")
        bilan = copieRepertoire(orientationACopier,orientationCible)
        if bilan :
            self.encadre(bilan)
            return bilan
        if not os.path.exists(orientationCible):
            print(_("pas d'orientation copiée depuis %s") % (orientationACopier))
            return (_("pas d'orientation copiée depuis %s") % (orientationACopier))
        if self.etatDuChantier in [1,2,3,35]: # si étatDuChantier avant la fin de Tapas on indique que Tapas est fini
            self.etatDuChantier = 4
        self.ajoutLigne ("\n"+_("Copie de l'orientation depuis : %s") % (self.selectionRepertoireAvecChemin)+"\n")
        self.ecritureTraceMicMac()
        message = _("Orientation copiée")
        self.encadre(message)
        return str()

    def copierMosaiqueTarama(self,repertoireInconnu=True):
        self.menageEcran()
        message = str()
        if self.etatDuChantier == 0:    # vérification état du chantier
            self.encadre(_("Choisir les photos à traiter avant de copier des points homologues."))
            return False
        # choisir le chantier origine de la copie de l'orientation :
        if repertoireInconnu:
            bilan = self.choisirUnChantier(_("Choisir le chantier d'où copier la mosaïque Tarama. Seuls les chantiers compatibles sont proposés."),
                                           filtre="Tarama")
            if bilan!=None:
                message = _("Aucun chantier choisi.") + "\n" + bilan + "\n"
                self.encadre(message)
            return message
        taACopier  =   os.path.join(self.selectionRepertoireAvecChemin,"TA")
        taCible = os.path.join(self.repTravail,"TA")
        bilan = copieRepertoire(taACopier,taCible)
        if bilan :
            self.encadre(bilan)
            return bilan
        self.ajoutLigne ("\n"+_("Copie de la mosaïque tarama depuis : %s") % (self.selectionRepertoireAvecChemin)+"\n")                    
        self.ecritureTraceMicMac()
        message = _("Mosaïque Tarama copiée")
        self.encadre(message)
        return str()
                                                                     
    def copierHomolOriTarama(self):
        self.encadre(_("Patience : copie des points homologues"))
        bilan  = self.copierPointsHomologues()
        if bilan != str():
            self.encadre(bilan)
            return
        self.encadre(_("copie des points homologues effectuée : %s") % bilan +"\n"+_("Patience : copie de l'orientation en cours"))
        bilan += self.copierOrientation(repertoireInconnu=False)
        self.encadre(_("copie des points homologues effectuée,")+
                     "\n"+_("copie de l'orientation en cours")+"\n"+
                     _("bilan %s") % bilan)                    
        bilan += self.copierMosaiqueTarama(repertoireInconnu=False)
        bilan += self.chargerCalibrationIntrinseque(repertoireInconnu=False)
        if bilan:
            self.encadre(_("Copie non totalement effectuée : ")+bilan)
        else:
            self.encadre(_("Copie des points homologues, de l'orientation, de la calibration, et de la mosaïque Tarama effectuées depuis :")+"\n"+
                         self.selectionRepertoireAvecChemin)
            
#######################################
        
    def consulterEcartsGCP(self): #attention : existe pas sur les vieux chantiers
        if not self.ecartPointsGCPByBascule:
            self.encadre(_("Pas de traitement des points GCP."))
            return
        message = (_("Les écarts des points GCP (voir la trace complète pour plus de détails) : ")+"\n\n"+self.ecartPointsGCPByBascule)
        if message.count('\n')>25:
            self.afficheTexte(message)
        else:
            self.encadre(message)
            
    def longueurPrefixe(self):
        new = MyDialog(fenetre,_("Longueur du préfixe actuelle %s") % (self.nbCaracteresDuPrefixe),
                       _("le préfixe est utilisé pour discriminer les appareils photos")+"\n").saisie
        if new.isdigit():
            self.nbCaracteresDuPrefixe = new
            self.encadre(_("Nouvelle longueur du préfixe : %s") % (self.nbCaracteresDuPrefixe) )             
        else:
            self.encadre(_("Valeur inchangée : %s") % (self.nbCaracteresDuPrefixe) )              
    
    def plusieursAppareils(self):
        # y-a-il dans l'exif un numéro de série ?
        nbModif = int()
        nbConserve = int()
        modif = _("AperoDeDenis propose l'ajout du préfixe (3 caractères) du nom des photos au tag model")
        bouton = _("Ajout du préfixe du nom du fichier au tag model de l'exif")
        self.menageEcran()
        message = ( _("Lorque les photos choisies proviennent de plusieurs appareils photos")              + "\n"+
                    _("les TAGS 'model' doivent être différenciés dans l'exif des photos.")                + "\n"+
                    _("La calibration s'effectue alors pour chaque appareil.")                             + "\n\n"+                                 
                    _("AperoDeDenis propose l'ajout du préfixe (%s caractères) du nom des photos au tag model") % (self.nbCaracteresDuPrefixe) + "\n"+
                    _("Le nombre de caractères du préfixe est modifiabe par item du menu Expert")+  "\n"+
                    _("Cet ajout ne sera effectué qu'une seule fois.")+ "\n"+                    
                    _("Le préfixe est un paramètre modifiable propre à chaque appareil photo")+ "\n\n")                          
        if self.etatDuChantier not in [1,2]:                       # 1 = avec photo ; 2 = enregistré, plus = traitement effectué
            message +=_("Cette modification ne sera prise en compte que pour les futurs traitements.")                                
        if self.troisBoutons(_("Plusieurs appareils photos"),message,_("Ne rien faire"),bouton) == 0:
                self.encadre(_("Abandon, le chantier n'est pas modifié."))
                return
        # Modification des tags "model" demandée : 
        self.encadre(_("Modification du modèle de l'appareil photo en cours : ajout du préfixe du nom du fichier.")+"\n"+
                     _("Attention : procédure longue si beaucoup de photos.")+"\n")
        self.lesTagsExif = dict()
        for photo in self.photosAvecChemin:
            if nbModif+nbConserve % 10 ==0:
                self.encadrePlus(str(nbModif+nbConserve))
            else:
                self.encadrePlus(".")
            prefix = os.path.basename(photo)[:int(self.nbCaracteresDuPrefixe)]
            time.sleep(0.01)
            model = self.tagExif("Model",os.path.basename(photo))
            if not prefix in model:
                nbModif += 1
                time.sleep(0.01)
                self.lanceCommande([self.exiftool,"-Model="+model+" "+prefix,photo])
                supprimeFichier(photo+"_original")           # exiftool crée des copies "_original" des fichiers initiaux, on les supprime ;
                time.sleep(0.01)
            else: nbConserve += 1       
        message = "\n"+_("Modéle de l'appareil photo modifié : ajout du préfixe du nom de fichier sur %s caractères.") % (self.nbCaracteresDuPrefixe) +"\n\n"
        message += _("Nombre de fichiers modifiés : %s") % str(nbModif) + "\n"        
        if nbConserve:
             message += _("Nombre de fichiers conservés car déjà modifiés : %s") % str(nbConserve) + "\n"
        self.encadrePlus(message)             
        # controle pour toutes les photos :
        self.encadrePlus(_("Controle des modifications.")+"\n")
        correction = int()
        nbOK = int()
        liste=list()
        self.lesTagsExif = dict()                         
        for photo in self.photosAvecChemin:
            if correction+nbOK % 10 ==0:
                self.encadrePlus(str(correction+nbOK))
            else:
                self.encadrePlus(".")
            prefix = os.path.basename(photo)[:int(self.nbCaracteresDuPrefixe)]
            time.sleep(0.01)
            model = self.tagExif("Model",os.path.basename(photo))
            if not prefix in model:
                correction += 1
                liste+=os.path.basename(photo)
                time.sleep(0.01)
                self.lanceCommande([self.exiftool,"-Model="+model+" "+prefix,photo])
                supprimeFichier(photo+"_original")           # exiftool crée des copies "_original" des fichiers initiaux, on les supprime ;
            else: nbOK += 1
        if correction:
            self.lesTagsExif = dict()
            message = "\n"+ _("liste des photos peut-être mal modifiées : %s") % (liste)+"\n"
            message += _("Veuillez vérifier la liste des appareils photos.\nSi besoin relancer la procédure.")+"\n"
        else:
            message ="\n"+ _("Fin du traitement.")
        self.encadrePlus(message)                        
        self.ajoutLigne(message)
        self.ecritureTraceMicMac()

    def listeAppareils(self):
        self.encadre(_("Recherche des noms d'appareil photos. Patience !."))    
        nb = self.nombreDeExifTagDifferents("Model")
        if nb>1:    message = _("Les photos proviennent de ")+str(nb)+" "+_("appareils photos différents : ")+"\n\n"+"\n".join(self.lesTags)
        elif nb==1: message = _("Les photos proviennent d'un seul appareil : ")+"\n\n"+"\n".join(self.lesTags)
        else:       message = _("L'exif des photos ne contient pas le nom de l'appareil photo.")
        self.encadre(message)
        self.ajoutLigne("Les appareils photos : \n"+message)
        self.ecritureTraceMicMac()
        
    def logMm3d(self):
        oschdir(self.repTravail)
        fichier = "mm3d-LogFile.txt"
        if os.path.exists(fichier):
            self.cadreVide()            
            trace=open(fichier,"r",encoding="utf-8")
            try:
                contenu=trace.read()
            except:                     # pour compatibilité ascendante
                trace.close
                trace=open(fichier,"r",encoding="latin-1")
                contenu=trace.read()
            trace.close
            self.ajoutLigne(contenu)
            self.texte201.see("1.1")            
        else:
            texte = _("Pas de trace du log !")
            self.encadre(texte)

        
    ################################## Les menus AIDE ###########################################################
            
    def commencer(self):
        self.encadre (self.aide3,50,aligne='left')
        
    def aide(self):
        self.afficheTexte(self.aide1)
        
    def conseilsPhotos(self):
        self.afficheTexte(self.aide2)
        
    def conseilsOptions(self):
        self.afficheTexte(self.aide5) 

    def conseilsPlantageNonDense(self):
        self.afficheTexte(self.aide6)

    def conseilsPlantageDense(self):
        self.afficheTexte(self.aide8)
        
    def historiqueDesVersions(self):
        self.afficheTexte(self.aide4)
        
    def aPropos(self):
       
        self.encadre (self.aide7,aligne='center')
        
        # ajout du logo du cerema 
        
        self.canvasLogo.pack(fill='both',expand = 1)
        self.logo.pack()
        self.imgTk_id = self.canvasLogo.create_image(15,0,image = dataLogoCerema,anchor="nw") # affichage effectif de la photo dans canvasPhoto

        # ajout du logo IGN
        
        if self.labelIgn.winfo_manager()!="pack":
            self.labelIgn.pack(pady=5)        
        self.canvasLogoIGN.pack(fill='both',expand = 1)
        self.logoIgn.pack(pady=5)                   
        self.imgTk_idIGN = self.canvasLogoIGN.create_image(0,0,image = dataLogoIGN,anchor="nw") # affichage effectif de la photo dans canvasPhoto

    def aideMetiers(self):
        self.afficheTexte(self.aide9)        
        
    ################################## Le menu FICHIER : nouveau, Ouverture, SAUVEGARDE ET RESTAURATION, PARAMETRES, outils divers ###########################################################       

    def sauveParam(self):                       # La sauvegarde ne concerne que 2 fichiers; fixes, sous le répertoire des paramètres,
                                                #  - pour les paramètres généraux : self.fichierParamMicmac
                                                #  - pour le chantier en cours    : self.fichierParamChantierEnCours
                                                # pour enregistrer le chantier en cours utiliser :
                                                #  - copierParamVersChantier()
        self.sauveParamMicMac()
        self.sauveParamChantier()
    
    def sauveParamChantier(self):
        essai = (self.fichierParamChantierEnCours+"essai")       # pour éviter d'écraser le fichier si le disque est plein
        try:            
            sauvegarde1=open(essai,mode='wb')
            pickle.dump((               
                         self.repertoireDesPhotos,  
                         self.photosAvecChemin,
                         self.photosSansChemin,
                         self.lesExtensions,
                         self.maitreSansChemin,
                         self.masqueSansChemin,
                         self.modeTapioca.get(),
                         self.echelle1.get(),
                         self.echelle2.get(),
                         self.delta.get(),
                         self.echelle3.get(),
                         self.arretApresTapas.get(),
                         self.listePointsGPS,
                         self.modeCheckedMalt.get(),
                         self.fichierMasqueXML,
                         self.repTravail,
                         self.photosAvecChemin,     # a supprimer (doublon avec r2)
                         self.extensionChoisie,
                         self.maitreSansExtension,  # probablement sans intérêt : variable initialisé avant chaque usage
                         self.etatDuChantier,
                         self.dicoPointsGPSEnPlace,                       
                         self.maitre,
                         self.mercurialMicMac,
                         self.idPointGPS,
                         self.dicoLigneHorizontale,
                         self.dicoLigneVerticale,
                         self.dicoCalibre,
                         self.distance.get(),
                         self.monImage_MaitrePlan,                                               # Nom de l'image maîtresse du plan repere (sans extension)
                         self.monImage_PlanTif,                                                   # nom du masque correspondant
                         self.etatSauvegarde,
                         self.modeCheckedTapas.get(),
                         self.echelle4.get(),
                         self.photosPourCalibrationIntrinseque,
                         self.calibSeule.get(),                     # True si photos pour calibration uniquement
                         self.zoomF.get(),
                         self.photosUtilesAutourDuMaitre.get(),
                         self.modele3DEnCours,
                         self.typeDuChantier,
                         self.listeDesMaitresses,
                         self.listeDesMasques,
                         self.choixDensification.get(),
                         self.modeC3DC.get(),
                         self.tawny.get(),
                         self.dicoPerso,
                         version,
                         None,                      # supprimé en v 5.2
                         self.lancerTarama.get(),
                         self.incertitudeCibleGPS.get(),
                         self.incertitudePixelImage.get(),
                         self.chantierNettoye,
                         self.lesTagsExif,
                         self.ecartPointsGCPByBascule,
                         self.choixCalibration.get(),       # calibration par autre chantier ou par photos 
                         self.chantierOrigineCalibration,   # si calibration copiée depuis un autre chantier
                         self.repereChoisi,                 # si navigation GPS (drone) : local ou lambert 93
                         self.messageRepereLocal,
                         self.calculNuageNonDense.get(),    # booléen : faut-il cacluler le nuage non dense
                         self.nuage2Mesh.get(),             # texte : 0 pour obtnir un nuage de points dense, 1 pour obtenir un maillage
                         self.nomEpsg,                      # EPSG choisi pour convertir les données GPS dans l'exif des photos
                         self.modele3DFinal,                # lorsque plusieurs nuages denses sont générés les nom s'incrémentent de _VNN : nom du dernier créé
                         self.masque3DSansChemin,           # nom du fichier XML du masque 3D, fabriqué par Saisie MasqQT (sur AperiCloud ou sur Modele3D)
                         self.masque3DBisSansChemin,        # nom du second fichier XML pour le masque 3D
                         self.tailleDuChantierEnMO,         # taille sous le répertoire racine du chantier, peut comprendre d'autres chantiers, etc
                         ),     
                        sauvegarde1)
            sauvegarde1.close()
            supprimeFichier(self.fichierParamChantierEnCours)
            os.rename(essai,self.fichierParamChantierEnCours)
            self.etatSauvegarde=""
        except Exception as e:
            print (_('erreur sauveParamChantier : '),str(e))

       
    def sauveParamMicMac(self):
        essai = (self.fichierParamMicmac+"essai")       # pour éviter d'écraser le fichier si le disque est plein
        try:
            sauvegarde2=open(essai,mode='wb')
            repertoire = self.verifParamRep()   # [self.micMac, self.meshlab, self.exiftool, self.mm3d, self.convertMagick, self.ffmpeg]
            pickle.dump((repertoire[0],
                         repertoire[1],
                         self.indiceTravail,
                         self.tousLesChantiers,
                         repertoire[2],
                         repertoire[3],
                         repertoire[4],
                         self.tacky,
                         version,
                         langue,
                         repertoire[5],
                         versionInternet,               # dernière version lue sur Internet
                                                        # permet de repérer les nouvelles versions et de réactiver le message
                         self.avertirNouvelleVersion,   # bool : si vrai on prévient l'utilisateur qu'il y a une nouvelle version (si pas la même, sinon pas
                         self.mercurialMicMac,          # version de micmac 
                         ),     
                        sauvegarde2)
            sauvegarde2.close()
            supprimeFichier(self.fichierParamMicmac)
            os.rename(essai,self.fichierParamMicmac)
        except Exception as e:              # Controle que le programme a accès en écriture dans le répertoire d'installation
            print (_('erreur sauveParamMicMac : '),str(e))
            texte = _("L'interface doit être installée dans un répertoire ou vous avez les droits d'écriture.") + "\n\n"+\
                    _("Installer l'interface AperoDeDenis à un emplacement ou vous avez ce droit.") + "\n\n"+\
                    _("Répertoire actuel : ")+self.repertoireData+".\n\n"+\
                    _("Erreur rencontrée : ")+str(e)+str(repertoire)
            self.troisBoutons(titre=_("Problème d'installation"),question=texte,b1='OK',b2='')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1            
            fin(1)


    def verifParamRep(self):  #Vérifie s'il existe un répertoire pour les outils de micmac et gère leur absence lors de la sauvegarde.
        repertoire = [self.micMac, self.meshlab, self.exiftool, self.mm3d, self.convertMagick, self.ffmpeg]
        cpt = 0
        while(cpt < 6):
            if(repertoire[cpt] == self.noRep[cpt]):
               repertoire[cpt] = "N\\A" ##Empêche de se retrouver avec une langue inconnue dans ses paramètres.
            cpt +=1
        return repertoire

    ###### Restauration paramètres :
            
    def restaureParamEnCours(self):
        self.restaureParamChantier(self.fichierParamChantierEnCours)       
        self.restaureParamMicMac()

    def restaureParamMicMac(self):
        try:
            sauvegarde2 = open(self.fichierParamMicmac,mode='rb')
            r2=pickle.load(sauvegarde2)
            sauvegarde2.close()
            r3 = []
            r3 = self.verifNARep(r2)                        # sépare ce qui doit être traduit ou pas
            self.micMac                     =   r3[0]
            self.meshlab                    =   r3[1]
            self.indiceTravail              =   r2[2]
            self.tousLesChantiers           =   r2[3]
            self.exiftool                   =   r3[2]
            self.mm3d                       =   r3[3]                               # spécifique linux/windows
            self.convertMagick              =   r3[4]
            self.tacky                      =   r2[7]
            #r2[8] est la version : inutile pour l'instant (v3.00)
            #r2[9] est la langue
            self.ffmpeg                     =   r3[5]
            self.versionInternetAncienne    =   r2[11]  # ne sert plus
            self.avertirNouvelleVersion     =   r2[12]
            self.mercurialMicMac            =   r2[13]
        except Exception as e: print(_("Avertissement : restauration param généraux : "),str(e))

        threading.Thread(target=self.verifieVersion).start() # supprimé version 5.43 remis en version 5.49

        # détermination du chemin pour dicocamera, de la version de mm3d, de la possibilité d'utiliser C3DC
        
        self.CameraXML      = os.path.join(os.path.dirname(self.micMac),self.dicoCameraGlobalRelatif)
        #self.mercurialMicMac= mercurialMm3d(self.mm3d)          # voir si cela va durer !
        self.mm3dOK         = verifMm3d(self.mm3d)              # Booléen indiquant si la version de MicMac permet la saisie de masque 3D

        # après plantage durant Malt ou fusion des photos ou ply peuvent manquer : on tente une restauration
        try:
            [os.rename(os.path.splitext(e)[0],e) for e in self.photosAvecChemin if (os.path.exists(os.path.splitext(e)[0]) and not (os.path.exists(e)))]
            [os.rename(e,os.path.splitext(e)[0]+".ply") for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".pyl"]  # remise à l'état initial
        except Exception as e:
            print("erreur tentative restauration après plantage : ",str(e))
        # il reste le pb des photos déplacées pour la calibration

    def verifNARep(self, r2): 
        cpt = 0
        if r2.__len__()>10: repFfmpeg = r2[10]              # pour assurer la compatibilité avec les anciennes versions ou self.ffmpeg n'était pas sauvé
        else:               repFfmpeg = self.ffmpeg
        r3 = [r2[0], r2[1], r2[4], r2[5], r2[6], repFfmpeg]
        while(cpt < 6):
            if(r3[cpt] == "N\\A"):
                r3[cpt] = self.noRep[cpt]
            cpt +=1
        return r3


    ######  la restauration d'un chantier peut concerner un chantier archivé,
    #      dans ce cas on restaure un fichier dont le nom est passé en paramètre
                        
    def restaureParamChantier(self,fichier):                                        # permet de restaurer les paramètres d'un chantier si besoin
        
        try:                                                                        # s'il y a une sauvegarde alors on la restaure
            sauvegarde1=open(fichier,mode='rb')
            r=pickle.load(sauvegarde1)
            sauvegarde1.close()
            self.repertoireDesPhotos        =   r[0]
            self.photosAvecChemin           =   r[1]
            self.photosSansChemin           =   r[2]
            self.lesExtensions              =   r[3]
            self.maitreSansChemin           =   r[4]
            self.masqueSansChemin           =   r[5]           
            self.modeTapioca.set            (r[6])
            self.echelle1.set               (r[7])
            self.echelle2.set               (r[8])
            self.delta.set                  (r[9])
            self.echelle3.set               (r[10])
            self.arretApresTapas.set        (r[11])
            self.listePointsGPS             =   r[12]
            self.modeCheckedMalt.set        (r[13])
            self.fichierMasqueXML           =   r[14]
            self.repTravail                 =   r[15]
            self.chantier                   =   os.path.basename(self.repTravail)        
            photosAvecChemin                =   r[16]       # a supprimer (doublon avec r2)
            self.extensionChoisie           =   r[17]
            self.maitreSansExtension        =   r[18]
            self.etatDuChantier             =   r[19]
            self.dicoPointsGPSEnPlace       =   r[20]         
            self.maitre                     =   r[21]       # 22 disparu
            self.mercurialMicMacChantier    =   r[22]       # attention : différent de la variable sauvée : self.mercurialMic%ac
            self.idPointGPS                 =   r[23]
            self.dicoLigneHorizontale       =   r[24]
            self.dicoLigneVerticale         =   r[25]
            self.dicoCalibre                =   r[26]
            self.distance.set               (r[27])
            self.monImage_MaitrePlan        =   r[28]                                               # Nom de l'image maîtresse du plan repere (sans extension)
            self.monImage_PlanTif           =   r[29]                                               # nom du masque correspondant
            self.etatSauvegarde             =   r[30]
            self.modeCheckedTapas.set       (r[31])
            self.echelle4.set               (r[32])
            self.photosPourCalibrationIntrinseque = r[33]
            self.calibSeule.set             (r[34])
            self.zoomF.set                  (r[35])
            self.photosUtilesAutourDuMaitre.set(r[36])
            self.modele3DEnCours            =   r[37]
            self.typeDuChantier             =   r[38]
            self.listeDesMaitresses         =   r[39]
            self.listeDesMasques            =   r[40]
            self.choixDensification.set     (r[41])
            self.modeC3DC.set               (r[42])
            self.tawny.set                  (r[43])
            self.dicoPerso                  = r[44]
            # r[45] est la version : inutile pour l'instant (v2.61]
            # r[46] devenu inutile v5.2   
            self.lancerTarama.set           (r[47])
            self.incertitudeCibleGPS.set    (r[48]),
            self.incertitudePixelImage.set  (r[49]),
            self.chantierNettoye            = r[50]
            self.lesTagsExif                = r[51]
            self.ecartPointsGCPByBascule    = r[52]
            self.choixCalibration.set       (r[53]) # calibration par autre chantier ou par photos 
            self.chantierOrigineCalibration = r[54]  # si calibration copiée depuis un autre chantier
            self.repereChoisi               = r[55]
            self.messageRepereLocal         = r[56]
            self.calculNuageNonDense.set    (r[57])
            self.nuage2Mesh.set             (r[58])
            self.nomEpsg                    = r[59]
            self.modele3DFinal              = r[60]
            self.masque3DSansChemin         = r[61] # nom du fichier XML du masque 3D, fabriqué par Saisie MasqQT (sur AperiCloud ou sur Modele3D)
            self.masque3DBisSansChemin      = r[62] # nom du second fichier XML pour le masque 3D                         
            self.tailleDuChantierEnMO       = r[63] # taille sous la racine du chantier (juin 2020)
        except Exception as e: print(_("Erreur restauration param chantier : "),str(e))
        
        # pour assurer la compatibilité ascendante suite à l'ajout de l'incertitude dans la description des points GCP
        # passage vers la version 2.60 de la liste des points GCP (un item de plus dans le tuple)
    
        if self.listePointsGPS.__len__()>0:
            if self.listePointsGPS[0].__len__()==6:
                self.listePointsGPS=[[a,nom,x,y,z,ident,"10 10 10"] for a,nom,x,y,z,ident in self.listePointsGPS]

        try: self.definirFichiersTrace()                 # attention : peut planter a juste titre si reptravail
        except: print(_("erreur définir fichier trace, est normale lors d'une importation."))
        
        # zoom OK, les valeurs 8,4,2,1 correspondent au nuage étape 5, 6, 7, 8 (la valeur 8 est initialisée par défaut
        try:
            if self.zoomF.get()=="8":self.etapeNuage = "5"
            if self.zoomF.get()=="4":self.etapeNuage = "6"
            if self.zoomF.get()=="2":self.etapeNuage = "7"
            if self.zoomF.get()=="1":self.etapeNuage = "8"
        except: pass

        # chemin constants pour la mosaique tarama

        self.mosaiqueTaramaTIF = os.path.join(self.repTravail,"TA","TA_LeChantier.tif")      
        self.mosaiqueTaramaJPG = os.path.join(self.repTravail,"TA","TA_LeChantier.JPG")
        self.masqueTarama = os.path.join(os.path.splitext(self.mosaiqueTaramaJPG)[0]+"_Masq.tif") 

        # Mise à jour des widgets pour les options de Malt (dépendent de la présence/absence de masques)
        
        self.miseAJourItem701_703()
        self.photosCalibrationSansChemin = [os.path.basename(f) for f in self.photosPourCalibrationIntrinseque]

        # Restauration des paramètres nommés personnalisés : si pas alors initialisation
        if type(self.dicoPerso)!=dict(): self.restauPerso()
        
    ########################### affiche les messages à l'écran : cadre, état, boites de dialogues standards, ménage                

    def encadreEtTrace(self,texte,nbLignesMax=40,aligne='center'):
        self.ajoutLigne(texte)
        self.ecritureTraceMicMac()                          # on écrit la trace        
        self.encadre(texte,nbLignesMax,aligne)

    def encadre(self,texte,nbLignesMax=44,aligne='center',nouveauDepart='non'):
       
        if texte.__class__==tuple().__class__:
            texte=' '.join(texte)
        if texte.__class__==list().__class__:
            texte=' '.join(texte)

        if texte.count('\n')>nbLignesMax:                           # limitation à nbLignesMax du nombre de lignes affichées 
            texte='\n'.join(texte.splitlines()[0:nbLignesMax-5]) +'\n.......\n'+'\n'.join(texte.splitlines()[-3:])
        self.menageEcran()
        if nouveauDepart=='oui':
            self.nbEncadre+=1
        if self.nbEncadre>=6 and nouveauDepart=='oui' and self.systeme=='nt':
            self.messageNouveauDepart =  texte
            self.nouveauDepart()    # lance une fenêtre  nouvelle sous windows (l'actuelle peut-être se polluer par certains traitements sous windows)
            return
        self.texte101.configure(text=texte,justify=aligne)
        self.texte101Texte = texte  # pour encadrePlus
        self.resul100.pack()
        fenetre.title(self.etatSauvegarde+self.chantier+" - "+self.titreFenetre)
        fenetre.focus_force()       # force le focus (it is impolite !)
        fenetre.update()

    def encadrePlus(self,plus,nbLignesMax=40):
        try:
            self.texte101Texte+=plus
            if len(self.texte101Texte.split("\n")[-1])>60:
                self.texte101Texte+="\n"
            if self.texte101Texte.count('\n')>nbLignesMax:                           # limitation à nbLignesMax du nombre de lignes affichées
                self.texte101Texte='\n'.join(self.texte101Texte.splitlines()[0:nbLignesMax-5]) +'\n-------\n'+'\n'.join(self.texte101Texte.splitlines()[-3:])            
            self.texte101.configure(text=self.texte101Texte)
            fenetre.update()
        except Exception as e:
            print("erreur encadre plus : "+str(e))
        
    def menageEcran(self):                                          # suppression écran (forget) de tous les FRAMES

        # fermeture des écrans de saisie encore ouvert :
        
        self.fermerLaBoiteAOnglets()
        self.fermerOptionsGoPro()
        self.fermerModifExif()

        # fermeture des frames et notebook
        
        if self.item400.winfo_manager()=="pack":
           self.item400.pack_forget()
        if self.item450.winfo_manager()=="pack":
           self.item450.pack_forget()
        if self.item460.winfo_manager()=="pack":
           self.item460.pack_forget()
        if self.item470.winfo_manager()=="pack":
           self.item470.pack_forget()
        if self.item480.winfo_manager()=="pack":
           self.item480.pack_forget()
           
        if self.item500.winfo_manager()=="pack":
           self.item500.pack_forget()
        if self.item510.winfo_manager()=="pack":
           self.item510.pack_forget()
        if self.item535.winfo_manager()=="pack":
           self.item535.pack_forget()             
        if self.item540.winfo_manager()=="pack":
           self.item540.pack_forget()           
        if self.item520.winfo_manager()=="pack":
           self.item520.pack_forget()

        if self.item600.winfo_manager()=="pack":
           self.item600.pack_forget()     
        if self.item700.winfo_manager()=="pack":
           self.item700.pack_forget()
        if self.item710.winfo_manager()=="pack":
           self.item710.pack_forget()
        if self.item720.winfo_manager()=="pack":
           self.item720.pack_forget()
        if self.item725.winfo_manager()=="pack":
           self.item725.pack_forget()           
        if self.item730.winfo_manager()=="pack":
           self.item730.pack_forget()

        if self.item800.winfo_manager()=="pack":
           self.item800.pack_forget()

        if self.item950.winfo_manager()=="pack":
           self.item950.pack_forget()
        if self.item960.winfo_manager()=="pack":
           self.item960.pack_forget()
        if self.item965.winfo_manager()=="pack":
           self.item965.pack_forget()
        if self.item970.winfo_manager()=="pack":
           self.item970.pack_forget()
        if self.item975.winfo_manager()=="pack":
           self.item975.pack_forget()           
        if self.item980.winfo_manager()=="pack":
           self.item980.pack_forget()
        if self.item990.winfo_manager()=="pack":
           self.item990.pack_forget()  

        if self.item1000.winfo_manager()=="pack":
           self.item1000.pack_forget()           
        if self.item2000.winfo_manager()=="pack":
           self.item2000.pack_forget()
        if self.item3000.winfo_manager()=="pack":
           self.item3000.pack_forget()

        if self.item9000.winfo_manager()=="pack":
           self.item9000.pack_forget()

        if self.item9100.winfo_manager()=="pack":
           self.item9100.pack_forget()
           
        if self.resul100.winfo_manager()=="pack":
           self.resul100.pack_forget()
        if self.resul200.winfo_manager()=="pack":
           self.resul200.pack_forget()           
        if self.onglets.winfo_manager()=="pack":
           self.onglets.pack_forget()
           
        if self.logo.winfo_manager()=="pack":
           self.logo.pack_forget()           
        if self.logo1.winfo_manager()=="pack":
           self.logo1.pack_forget()
        if self.logoIgn.winfo_manager()=="pack":
           self.logoIgn.pack_forget()
           
        try:
            if self.frame.winfo_manager()=="pack":
                self.frame.pack_forget()              
            self.bulle.destroy()
        except: pass

        try:
            if InitialiserLangue.frame.winfo_manager()=="pack":
                InitialiserLangue.frame.frame.pack_forget()              
        except: pass           
##
##    def listeFrames(self):                                          # CREE LA LISTE DE TOUS LES FRAMES de la fenetre self
##        self.l=list()
##        for v,t in self.__dict__.items():                           # un print (v,t) ici affiche l'identifiant arborescent des widgets (fenetre/frame/widget)
##            if t.__class__ in [ttk.Frame().__class__,ttk.Notebook().__class__]:
##                self.l.append(v)


    def fermerLaBoiteAOnglets(self):    # palliatif
        # la boite à oglet n'est pas une fenêtre modale mais une frame..
        # on pallie à cela en proposant de la sauver ou pas lorsque l'on fait du ménage
        # pour éviter de fermer brutalement
        # la vraie solution serait de mettre la frame dans une fenêtre toplevel, modale, elle.
        # le try récupére l'erreur si jamais l'interface n'existe plus.
        try:
            if self.fermetureOngletsEnCours == True:
                return
            if self.onglets.winfo_manager()=="":
                return
        # modif version 5.47 : on enregistre systématiquement            
            self.finOptionsOK()
            self.fermetureOngletsEnCours = False
            return
        except: pass
        
    def fermerOptionsGoPro(self):
        if self.fermetureOptionsGoProEnCours == True:
            return
        if self.item2000.winfo_manager()=="":
            return
        self.fermetureOptionsGoProEnCours = True        
        if self.troisBoutons(_("Fermer les options vidéo."),_("Enregistrer les options vidéos saisies ?"),b1=_("enregistrer"),b2=_("abandon"))==0:
            self.optionsGoProOK()
        else:
            self.optionsGoProKO()
        self.fermetureOptionsGoProEnCours = False        

    def fermerModifExif(self):
        if self.fermetureModifExif == True:
            return
        if self.item3000.winfo_manager()=="":
            return
        self.fermetureModifExif = True        
        if self.troisBoutons(_("Fermer la modification des exifs."),_("Enregistrer les valeurs saisies ?"),b1=_("enregistrer"),b2=_("abandon"))==0:
            self.exifOK()
        else:
            self.exifKO()
        self.fermetureModifExif = False

######################### recherche de la dernière version d'aperodedenis sur le net

    def verifieVersion(self):   # Procédure éxécutée lors de la restauration des paramètres de Micmac
                                # va lire la version dans la page GitHub : doit être au début du fichier readme.txt
                                # Affiche un message si besoin.
                                # lancé par un thread (pour éviter le retard éventuel de connexion à internet si pas de connexion
                                # un seul lancement par session
        
        if compteur>1 or self.avertirNouvelleVersion==False:    # inutile si relance de l'interface ou si l'utilisateur ne veut pas être averti
            return
        if self.versionOkInGitHub():
            return
        self.avertissementNouvelleVersion()


    def verifVersion(self):     # procédure lancée sur demande utilisateur (menu outils)
        self.encadre(_("Recherche sur internet en cours, patience..."))        
        
        # Y-a-t-il une nouvelle version sur internet ? Si oui faut-il un message ?
        
        if not self.versionOkInGitHub():             # version utilisateur trouvée dans version GitHub
            self.avertissementNouvelleVersion()
            self.encadre(_("Il existe une version plus récente sur GitHub"))            
        else:
            self.avertissementVersionAJour()
            self.encadre(_("Version actuelle à jour"))            

    def avertissementNouvelleVersion(self): # n'apparait qu'une fois par session (role de avertirNouvelleVersion)

        retour = self.troisBoutons(titre=_("Nouvelle version de l'interface AperoDeDenis"),
                                   question=_("Nouvelle version disponible sur Internet : ")+"\n"+
                                            _("Téléchargement à l'adresse : ")+"\n\n"+
                                            "https://github.com/micmacIGN/InterfaceCEREMA/tree/master/InterfaceCEREMA",                                       
                                   b1=_("OK"),
                                   b2=_("Ouvrir la page web"),
                                   b3=_("Lire le readme.txt"
                                   ))            
        if retour == 1:
            ouvreInterfaceCeremaGItHub()
        if retour == 2:
            ouvreReadMeGitHub()

    def avertissementVersionAJour(self): # n'apparait qu'une fois par session (role de avertirNouvelleVersion)
        # version OK, on propose à l'utilisateur d'aller voir :
        retour = self.troisBoutons(titre=_("Version de l'interface AperoDeDenis à jour"),
                                   question=_("Version à jour : ")+version,                                    
                                   b1=_("OK"),
                                   b2=_("Ouvrir la page web"),
                                   b3=_("Lire le readme.txt"),                                       
                                   )
        if retour == 1:
            ouvreInterfaceCeremaGItHub()
        if retour == 2:
            ouvreReadMeGitHub()
         
    def versionOkInGitHub(self): # retour = true or False
        try:
            sock = urllib.request.urlopen("https://github.com/micmacIGN/InterfaceCEREMA/blob/master/InterfaceCEREMA/readme.txt")
            htmlLu = str(sock.read(100000))
            sock.close
        except:
            return
        # Y-a-t-il une nouvelle version sur internet ?  Le readme.txt comporte " V N.nn " pour la version en cours
        positionVersion = htmlLu.find(" V ")
        premiereVersion = htmlLu[positionVersion:positionVersion+10]
        if "." not in premiereVersion: # pour éviter les éventuelles confusions avec un autre " V "
            return
        print("premiereVersion=",premiereVersion)
        versionGitHub = premiereVersion.split()[1]
        print("versionGitHub = '",versionGitHub,"' numéro version = '",numeroVersion,"'")
        if versionGitHub.strip() == numeroVersion.strip():             # version utilisateur sous la forme : " V 5.43 " non trouvée dans version GitHub (espace V majuscule espace numéro espace)
            return True
        else:
            return False
        
    #################################### Ménage : Supprime les répertoires de travail : appel par item de menu 
    
    def supprimeRepertoires(self): 
        self.menageEcran()

        # Y-a-t-il des chantiers ?
        
        if len(self.tousLesChantiers)==0:
                texte='\n' + _("Tous les chantiers sont déjà supprimés.") + "\n"
                self.encadre(texte)
                return

        # Oui il y a des chantiers !
        
        supprime = list()
        conserve = list()
        texte = str()
        attention = str()
        espaceGagne = int()
        chantierEnCours = self.repTravail
        
        self.choisirUnePhoto(self.tousLesChantiers,
                             titre=_('Chantiers à nettoyer ou à supprimer'), 
                             mode='extended',
                             message=_("Multi sélection possible"),
                             boutonDeux=_("Annuler"),
                             objets=_('repertoires'),
                             testPresenceRepertoire=False)      # renvoi  : self.selectionPhotosAvecChemin
        # rien à faire
        
        if len(self.selectionPhotosAvecChemin)==0:
            return

        # Nettoyage effectif à faire

        if len(self.selectionPhotosAvecChemin)==1:
            self.troisBoutons(_('Suppression du chantier ou nettoyage des répertoires de travail superflus'),
                             _('Le chantier suivant va être supprimé ou nettoyé :') + '\n\n'+'\n'.join(self.selectionPhotosAvecChemin),
                             _('Supprimer totalement le chantier'),
                             _('Nettoyer le chantier, conserver les résultats'),                            
                             _('Annuler'))
        if len(self.selectionPhotosAvecChemin)>1:
            if self.repTravail in self.selectionPhotosAvecChemin:
                attention=_("ATTENTION : le chantier en cours est dans la liste.") + "\n\n"
            else:
                attention=""

            self.troisBoutons(_('Suppression des chantiers ou nettoyage des répertoires de travail superflus'),
                             attention+_('Les chantiers suivant vont être supprimés ou nettoyés :') + '\n\n'+'\n'.join(self.selectionPhotosAvecChemin),
                             _('Supprimer totalement les chantiers,\ny compris tous les sous-répertoires présents sous la racine'),
                             _('Nettoyer les chantier,\nconserver les résultats et les sous-répertoires indépendants du chantier'),                              
                             _('Annuler'))
            
        if self.bouton==2 or self.bouton==-1:       # abandon par annulation (1) ou par fermeture de la fenêtre (-1)
            return

        # suppression totale des répertoires
        
        if self.bouton==0:       
            self.encadre(_("Suppression en cours....")  + "\n")      
            for e in self.selectionPhotosAvecChemin:
                if os.path.exists(e):
                    espaceGagne+=sizeDirectoryMO(e)
                    if self.repTravail==e:
                        self.etatDuChantier = -1
                        texte=_("Le chantier en cours %s est supprimé. Un nouveau chantier est proposé") % (self.chantier)+ "\n"                    
                        self.nouveauChantier()
                        time.sleep(0.1)
                    try: shutil.rmtree(e)   # suppression arborescence sous racine, la racine reste présente il faut ensuite la supprimer
                    except: pass
                    try:    os.rmdir(e)     # suppression racine
                    except: pass
                    time.sleep(0.01)
                if os.path.exists(e):
                    ajout(conserve,e)       # dossier non supprimé (en cours d'utilisation ?)
                else:
                    try:
                        ajout(supprime,e)
                        self.tousLesChantiers.remove(e)
                    except: pass
                    self.encadrePlus("...")
            if len(supprime)>=1:            
                texte = texte+_("Compte rendu de la suppression :") + "\n\n" + _("les chantiers supprimés :") + "\n\n"+'\n'.join(supprime)+"\n"               
            if len(conserve)==0:
                    texte = texte+'\n\n' + _('Tous les chantiers demandés sont supprimés.')
            elif len(conserve)==1:
                    texte = texte+'\n\n' + _('Il reste un chantier impossible à supprimer maintenant : ') + '\n\n'+'\n'.join(conserve)
            else:
                    texte = texte+'\n\n' + _('Il reste des chantiers impossibles à supprimer maintenant : ') + '\n\n'+'\n'.join(conserve)
            texte+="\n\n"+_("Espace disque récupéré : ")+str(espaceGagne)+" MO" 
            self.sauveParam()                                   # mémorisation de la suppression
            self.encadre(texte)
            return

        # nettoyage des répertoires suppression des répertoires de travail, temporaires, conservation des résultats
        
        if self.bouton==1:    
            listeDesRepertoiresSupprimes = list()
            self.encadre(_("Suppression des sous-répertoires en cours...."))          
            for chantier in self.selectionPhotosAvecChemin:
                if os.path.exists(chantier):
                    # conserver les résultats qui se trouvent dans des sous-répertoires : recopie sous la racine du chantier
                    conserverFichiers = [(os.path.join(chantier,e),os.path.join(chantier,os.path.basename(e))) for e in self.resultatAConserver]
                    for e,f in conserverFichiers:
                        if os.path.exists(e):
                            shutil.copy(e,f)
                    # les sous-répertoires du chantier, pas les fichiers
                    lesSousRepertoires = [f for f in os.listdir(chantier) if os.path.isdir(os.path.join(chantier, f))]                   
                    lesRepertoiresASupprimer = list()
                    for r in lesSousRepertoires:
                        for s in self.listeRepertoiresASupprimer:
                            if r[:len(s)-1]==s[:len(s)-1]:
                                lesRepertoiresASupprimer.append(r)
                    for nom in lesRepertoiresASupprimer:
                        # le                     
                        cheminASupprimer = os.path.join(chantier,nom)
                        if cheminASupprimer not in self.tousLesChantiers:   # ne pas supprimer les chantiers qui seraient sous-répertoire de ce chantier 
                            taille = sizeDirectoryMO(cheminASupprimer)
                            try:                    # la suppression peut planter pour moult raison                                                            
                                shutil.rmtree(cheminASupprimer)
                                espaceGagne += taille
                                listeDesRepertoiresSupprimes += [nom + " : "+ str(taille)+" MO",]
                                ajout(supprime,nom)
                            except Exception as erreur:
                                ajout(conserve,nom+" : "+erreur)
                    nouvelleTailleChantier = sizeDirectoryMO(chantier)
                    fichierParam = os.path.join(chantier,self.paramChantierSav)
                    sauveUnParametre(fichierParam,63,nouvelleTailleChantier) 
                    
            texte = "Ménage effectué"
            texte += "\n\n"+_("Espace disque récupéré : ")+str(espaceGagne)+" MO"
            if listeDesRepertoiresSupprimes:
                texte += "\n\n"+_("Les répertoires supprimés : ")
                texte += "\n"+"\n".join(listeDesRepertoiresSupprimes)
            if conserve:
                texte += "\n\n"+_("Les répertoires qui n'ont pas pu être supprimés : ")
                texte += "\n"+"\n".join(conserve)                
            if not conserve and not supprime:
                texte += "\n\n"+_("Aucun répertoire à supprimer")
            self.chantierNettoye = True # chantier marqué comme nettoyé
            self.etatDuChantier = 1     # état du chantier remis à : photos choisies
            self.encadre(texte)
            return
        
    ############################### Message proposant une question et deux, trois ou 4 Boutons
    # si b2="" alors pas de second bouton    retour : 0, 1, 2, 3 : numéro du bouton
    def troisBoutons(self,titre=_('Choisir'),question=_("Choisir : "),b1='OK',b2='KO',b3=None,b4=None):

        # positionne self.bouton et le renvoie : b1 = 0, b2 = 1 b3 = 2 b4 = 3; fermer fenetre = -1, 
        try:
            self.bouton = -1
            self.resul300 = tkinter.Toplevel(height=50,relief='sunken')
            fenetreIcone(self.resul300)          
            self.resul300.title(titre)
            if question.count('\n')>15:                           # limitation à nbLignesMax du nombre de lignes affichées 
                question='\n'.join(question.splitlines()[0:10]) +'\n.......\n'+'\n'.join(question.splitlines()[-3:])            
            self.texte301=ttk.Label(self.resul300, text=question)
            self.texte301.pack(pady=10,padx=10)        
            self.texte302=ttk.Button(self.resul300, text=b1,command=self.bouton1)
            self.texte302.pack(pady=5)
            if b2!="":                     # autorise un seul bouton
                self.texte303=ttk.Button(self.resul300, text=b2,command=self.bouton2)
                self.texte303.pack(pady=5)
            if b3!=None:                    # autorise un seul bouton
                self.texte304=ttk.Button(self.resul300, text=b3,command=self.bouton3)
                self.texte304.pack(pady=5)
            if b4!=None:                    # autorise un seul bouton
                self.texte305=ttk.Button(self.resul300, text=b4,command=self.bouton4)
                self.texte305.pack(pady=5)                
            self.resul300.transient(fenetre)                                    # 3 commandes pour définir la fenêtre comme modale pour l'application
            self.resul300.grab_set()
            self.resul300.focus_force()
            fenetre.wait_window(self.resul300)
            self.resul300.destroy()
            return self.bouton
        except:
            return self.bouton      # pour le cas ou Aperodedenis est fermé avec ce module en cours !
        
    def bouton1(self):
        self.bouton = 0
        self.resul300.destroy()
    
    def bouton2(self):
        self.bouton = 1
        self.resul300.destroy()   

    def bouton3(self):
        self.bouton = 2
        self.resul300.destroy()

    def bouton4(self):
        self.bouton = 3
        self.resul300.destroy()
        
    ############################### Prépare un cadre pour Afficher une trace dans la fenêtre
        
    def cadreVide(self):
        self.menageEcran()
        fenetre.update()                                  # rafraichissement avant agrandissement
        self.texte201.delete("0.0","end")
        self.resul200.pack()
        
    def yviewTexte(self, *args):
        if args[0] == 'scroll':
            self.texte201.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.texte201.yview_moveto(args[1])

    ################################## lance une procédure, attends ou non le résultat, éxécute un filtre sur chaque ligne de l'output ################################################

    def lanceCommande(self,commande,filtre=lambda e: e,info="",attendre=True):
        def nettoyerLaCommande(commande):
            listeParam = list()
            listeNomParam = list()
            commande = [e for e in commande if e.__len__()>0]       # suppression des arguments "vides"
            listeParamNommes = [ e.split("=")[0] for e in commande if e!=e.split("=")]
            for e in commande:
                nomParam = e.split("=")[0]
                if nomParam not in listeNomParam:    
                    listeParam.append(e)        # paramètre nouveau : on le garde
                    listeNomParam.append(nomParam)
            commandeTexte=" ".join(listeParam)                        # Format concaténé des arguments
            # limitation à 8191 caractère de la ligne de commande sous windows : mais pas sur que cela marche
            # par exemple pour exiftool les paramètres sont dépendants les uns des autres : il vont par groupe
            # aussi avertissement utilisateur :       
            if len(commandeTexte)>8000 and os.name=="nt":
                texte = (_("Sous Windows la longueur d'une ligne de commande est limitée à 8191 caractères") +"\n"+
                         _("AperoDeDenis essaie d'éxécuter la une commande dont la longueur est de %s") % len(commandeTexte) +"\n"+
                         _("Il est possible que ce soit un échec : dans ce cas il faut utiliser un autre système d'exploitation") +"\n"+
                         _("ou diminuer le nombre de photos, la longueur des chemins...") +"\n"+
                         _("Voici les 200 premiers caractères de la commande :") +"\n"+
                         commandeTexte[:200]+"\n"+
                         _("Toute la commande se trouve dans la trace"))
                self.troisBoutons(titre=_("Problème de longueur de commande"),question=texte,b1='OK')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1                            
                d = commande[1:]
                while 1:
                    if len(d):
                        c = commande[0]
                        chaine=str()
                        while len(chaine)<8000:
                            if len(d):
                                if len(d[0])+len(chaine)<8000:
                                    c.append(commande[i])   # ajout à la commande
                                    chaine+=commande[i]     # ajout à la chaine pour controler la longueur
                                    del d[0]                # pour s'arrêter si tout est épuisé
                                self.lanceCommande(self,c,filtre,attendre)
            return listeParam
        ########################
        commande = nettoyerLaCommande(commande)
        commandeTexte = " ".join(commande)                        # Format concaténé des arguments
        self.ajoutLigne("\n\n"+heure()+" "+_(": lancement de ")+commandeTexte+"\n\n"+info+"\n")
        self.ecritureTraceMicMac()                            
        # lance la commande                               
        try:
            self.exe = subprocess.Popen(commande,
                                   shell=self.shell,
                                   stdout=subprocess.PIPE,      # ne pas définir stdin car sinon il faut le satisfaire
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True)
        except Exception as e:
            self.ajoutLigne("\n"+_("erreur lors de l'éxécution de la commande :") + "\n"+str(e)+"\n")
            self.ajoutLigne("\n"+heure()+" "+_(": fin de ")+commandeTexte+"\n")
            return
        
        if not attendre:                                # par exemple pour lancer meshlab on n'attend pas la fin du process
            return
            
        ligne = self.exe.stdout.readline()              # boucle sur l'output (y compris stderr)
        
        while ligne:                
            if ligne.__class__!=str().__class__:        # doit être une chaine
                break                                   # sinon pb majeur : on arrête            
            self.ajoutTraceComplete(ligne)        # on ajoute la ligne et la ligne filtrée dans les traces
            self.ajoutTraceSynthese(filtre(ligne))

            try:
                ligne = self.exe.stdout.readline()      # ligne suivante, jusqu'à la fin du fichier, sauf décès (anormal) du processus père
            except:
                break                                   # si la lecture ne se fait pas c'est que le processus est "mort", on arrête
        
        self.ajoutLigne("\n"+heure()+" "+_(": fin de ")+commandeTexte+"\n")
        self.ecritureTraceMicMac()
        
    ########################## Opérations sur les Fichiers TRACE

    def definirFichiersTrace(self):     # affectation des noms des fichiers trace. pas de création : en effet le plus souvent ils existent déjà, il faut seulement les retrouver
        if  self.typeDuChantier[0]=='metier':       # 0 : metier, 1 : fichier pour répertoire 2 : nom du fichier trace
            repertoire = os.path.dirname(self.typeDuChantier[1])  
            self.TraceMicMacSynthese = os.path.join(repertoire,"Trace_AperoDeDenis_"+self.typeDuChantier[2]+".txt")
            self.TraceMicMacComplete = ""
            oschdir(repertoire)                                                       # on se met dans le répertoire de travail, indispensable
        elif self.repTravail != "":
            self.TraceMicMacSynthese = os.path.join(self.repTravail,'Trace_MicMac_Synthese.txt')
            self.TraceMicMacComplete = os.path.join(self.repTravail,'Trace_MicMac_Complete.txt')
            oschdir(self.repTravail)                                                       # on se met dans le répertoire de travail, indispensable

    def initialisationFichiersTrace(self):                      # vide les fichiers et ecrit une nouvelle entête avec le nom des photos
        open(self.TraceMicMacSynthese,'w').close()              # création d'un fichier de trace, vide
        open(self.TraceMicMacComplete,'w').close()              # création d'un fichier de trace, vide
        self.effaceBufferTrace()                                # RAZ d'un ahjoutLigne éventuel (notamment par affichage de la trace )
        self.ajoutLigne(heure()+" : "+self.titreFenetre+"\n-----------------------\n")
        self.ajoutTraceComplete(_("Trace complète"))
        self.ajoutTraceSynthese(_("Trace synthétique"))
        self.ajoutLigne("\n-----------------------\n\n")
        if len(self.photosAvecChemin)>0:
            self.ajoutLigne(heure()+ "\n\n" + _("Choix des photos :") + "\n"+"\n".join(self.photosAvecChemin))
        self.ajoutLigne("\n\n" + _("répertoire du chantier :") + "\n"+self.repTravail+"\n\n")
        self.ajoutLigne(_("Version MicMac : ")+self.mercurialMicMac+"\n")
        self.ecritureTraceMicMac()
                    
    # ajout de lignes dans les traces

    def ajoutLigne(self,ligne):
        if not ligne: return
        self.ajoutTraceComplete(ligne)                                # toutes les lignes vont dans la trace compléte
        self.ajoutTraceSynthese(ligne)                            # la ligne filtrée est mise dans la trace synthétique 

    def ajoutTraceComplete(self,lue):
        if not lue: return         

        self.lignePourTrace += str(lue)      # la trace détaillée en fin de MicMac, dans le répertoire de travail, sous le nom traceTotale

        # Si la ligne devient trop lourde on enregistre le fichier :
        if self.lignePourTrace.__len__()>1000000:
            self.ecritureTraceMicMac()
           
    def ajoutTraceSynthese(self,filtree):
        if not filtree: return
        if filtree[0:2]=="**": return       # commentaires micmac
        self.ligneFiltre += str(filtree)    # la trace synthétique

        # affichage en live pendant les traitements :        
        if self.resul200.winfo_manager()=="pack":    
            self.texte201.insert('end',str(filtree))                  
            self.texte201.update()
            self.texte201.see('end') 

    def effaceBufferTrace(self):    # raz l'écran d'affichage de la trace
        self.lignePourTrace = str()
        self.ligneFiltre = str()
    # écrire dans les traces

    def ecritureTraceMicMac(self):                                 # écriture en Ajout des fichiers trace
        self.definirFichiersTrace()
        try:
            with open(self.TraceMicMacSynthese,'a', encoding='utf-8') as infile:
                infile.write(self.ligneFiltre)
            if self.TraceMicMacComplete:
                with open(self.TraceMicMacComplete,'a', encoding='utf-8') as infile: # erreur si tracemicmaccomplete ="" (cas du volume)
                    infile.write(self.lignePourTrace)
        except Exception as e: 
            print (_('erreur ecritureTraceMicMac : '),str(e),"\ntraces : ",self.TraceMicMacSynthese," et ",self.TraceMicMacComplete)
            
        self.effaceBufferTrace()    
            
    ############################### Choix d'une image dans la liste des images retenues avec scrollbar : charge self.selectionPhotosAvecChemin, gadgets
        
# choix simple ou multiple dans une liste
# en retour une liste : self.selectionPhotosAvecChemin
            
    def choisirUnePhoto(self,                                               # en retour liste : self.selectionPhotosAvecChemin
                        listeAvecChemin,                                    # liste des noms  de fichiers ou répertoires à afficher pour le choix
                        titre=_('Choisir une photo'),                          # titre de la fenêtre
                        message=_("Cliquer pour choisir une ou plusieurs photos : "), # entête de la liste 
                        mode='extended',                                    # par défaut sélection multiple, autre mode = "single"
                        messageBouton=_("OK"),                                 # message sur le premier bouton
                        boutonDeux=None,                                    # texte d'un second bouton : fermeture, renvoyant une liste vide
                        dicoPoints=None,                                    # dictionnaire de points à afficher :  key = (nom point, photo, identifiant), value = (x,y)
                        objets='photos',                                    # par défaut la liste est une liste de fichiers, alternative : répertoires, ply
                        bulles=dict(),                                       # dictionnaires d'info bulle : key = photo, value = infobulle
                        testPresenceRepertoire=True):                                   # ne pas vérifier l'existence du répertoire de travail self.repTravail (cas : ménage)
        self.selectionPhotosAvecChemin = list()                             # sélection : vide pour l'instant !
        if len(listeAvecChemin)==0:                                         # pas de photos : on sort
            self.encadre(_("Pas de photos pour cette demande."))
            return
        if testPresenceRepertoire and not os.path.exists(self.repTravail):
            self.encadre(_("Le répertoire du chantier n'est pas accessible. Relancer l'ouverture d'un chantier"))
            return
        self.cherche = str()                                                # recherche
        self.fermerVisu = False                                             # permet d'identifier la sortie par le second bouton si = True (!= sortie par fermeture fenêtre)
        l = [ e for e in listeAvecChemin if not (os.path.exists(e))]        # BIS : si des photos ou répertoires manquent encore : abandon !
        if len(l)>0 and objets in ('photos','ply'):
            # les fichiers absents peuvent être des fichiers "pour calibration" : ils doivent alors être retirés de la liste             
            noCalib = [f for f in l if os.path.basename(f) not in [os.path.basename(g) for g in self.photosPourCalibrationIntrinseque]]
            if len(noCalib)>0:
                texte=_("Les fichiers suivants sont absents du disque :") + "\n\n"+"\n".join(l)+"\n\n" + _("Dossier corrompu. Traitement interrompu.")
                self.encadre(texte)
                return
            # restriction de la liste aux fichiers non calibrant :
            listeAvecChemin = [ h for h in listeAvecChemin if os.path.basename(h) not in [os.path.basename(i) for i in self.photosPourCalibrationIntrinseque]]
        self.dicoPointsAAfficher = dicoPoints                               # pour passer l'info à afficherTousLesPointsDuDico
        self.dicoInfoBullesAAfficher = bulles                               # pour passer l'info à afficherLesInfosBullesDuDico
        self.fermerVisuPhoto()                                              # pour éviter les fenêtres multiples
        self.listeChoisir = list(set(listeAvecChemin))                      # liste de choix par copie de la liste ou du tuple paramètre, sans doublons
        self.listeChoisir.sort(key=os.path.basename)                                            # tri alpha
        listeSansChemin = [os.path.basename(e) for e in self.listeChoisir]       
        self.topVisuPhoto = tkinter.Toplevel(fenetre,relief='sunken')               # fenêtre principale de choix de la photo (maitre, ou autre)
        self.topVisuPhoto.title(titre)
        self.topVisuPhoto.geometry("400x450+200+300")
        fenetreIcone(self.topVisuPhoto)           
        self.invitePhotoMessageInitial = message
        self.invitePhotoMessage = tkinter.StringVar()
        self.invitePhotoMessage.set(self.invitePhotoMessageInitial)
        self.invitePhoto = ttk.Label(self.topVisuPhoto,textvariable=self.invitePhotoMessage)                  # message entête
        self.invitePhoto.pack(padx=5,pady=5,ipadx=5,ipady=5)
        
        frameSelect = ttk.Frame(self.topVisuPhoto)                          # cadre dans la fenêtre: pour afficher la boite à liste        
        scrollbar = ttk.Scrollbar(frameSelect, orient='vertical')           # barre de défilement
        
        self.selectionPhotos = tkinter.Listbox(frameSelect,
                                               selectmode=mode,
                                               yscrollcommand=scrollbar.set,
                                               width=min(250,(5+max([0]+[len (r) for r in listeSansChemin]))))
        self.selectionPhotos.select_set(1)
        self.selectionPhotos.bind("<KeyRelease-Up>", self.upDown)
        self.selectionPhotos.bind("<KeyRelease-Down>", self.upDown)
        self.selectionPhotos.bind("<KeyRelease-Prior>", self.upDown)
        self.selectionPhotos.bind("<KeyRelease-Next>", self.upDown)
        self.selectionPhotos.bind("<Key>", self.lettre)
        self.selectionPhotos.pack(side='left', fill='both', expand=1)        
        self.selectionPhotos.focus_set()
                
        scrollbar.config(command=self.yview)
        scrollbar.pack(side='right', fill='y')
        
        for i in listeSansChemin:                                           # remplissage de la liste
            self.selectionPhotos.insert('end',i)
            l=[os.path.basename(e) for e in list(self.dicoInfoBullesAAfficher.keys())]
            if i in l:
                 self.selectionPhotos.itemconfig("end",bg='yellow')   
        frameSelect.pack()                                                  # fin de la boite à liste
        
        self.b1 = ttk.Button(self.topVisuPhoto,text=messageBouton,command=self.validPhoto)  # le premier bouton (fermer ou OK
        if boutonDeux!=None:
            c = ttk.Button(self.topVisuPhoto,text=boutonDeux,command=self.cloreVisuPhoto)   # le second bouon si demandé
            self.b1.pack(pady=5)
            c.pack(pady=5)
        else:
            self.b1.pack(pady=5)
            
        foto = ttk.Frame(self.topVisuPhoto)                                     # cadre dans la fenetre ; affiche la photo sélectionnée              
        self.canvasPhoto = tkinter.Canvas(foto,width = 200, height = 200)       # Canvas pour revevoir l'image
        self.canvasPhoto.pack(fill='both',expand = 1)
        foto.pack()
        if bulles==dict():
            self.selectionPhotos.select_set(0)                                  # si pas de dictionnaire sélection de la première photos (sinon colorisation &éventuelle de la première photo)
        else:
            self.retailleEtAffichePhoto(self.listeChoisir[0])                   # pour afficher la première photo, même s'il n'y a pas de sélection
        self.current = self.selectionPhotos.curselection()                      # sélection courante
        self.list_has_changed(self.current)                                     # la sélection est définie : on réagit

        ##########################################################
        # poll : lance retaille et affiche la photo (retailleEtAffichePhoto), qui lance afficherTousLesPointsDuDico et afficherLesInfosBullesDuDico
        # affiche les points du dictionnaire et une info bulle indiquant le nombre de points
        # affiche les infos bulles de 'bulles' 
        # réagit aux changements de sélection par l'utilisateur
        if objets in ('photos','ply',_("repertoires")):
            self.poll()                                                             # essentiel : lance la boucle infinie d'attente                                                                

        ##########################################################
        self.topVisuPhoto.protocol("WM_DELETE_WINDOW", self.fermerVisuPhoto)    # Fonction a éxécuter lors de la sortie du programme
        self.topVisuPhoto.transient(fenetre)                                    # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.topVisuPhoto.grab_set()
        fenetre.wait_window(self.topVisuPhoto)
        try : self.bulle.destroy()
        except: pass

########################################## Traitement des données GoPro ##############################################

    # saisie des options de la GoPro

    def optionsGoPro(self):
        self.sauveOptionsGoPro()        # en cas d'annulation par l'utilisateur
        self.menageEcran()
        self.item2000.pack()        

    # après saisie des options de la GoPro :

    def optionsGoProOK(self):
        self.item2000.pack_forget()     # fermer l'item (pour évitr la question par menageEcran)
        self.encadre(_("Options GoPro modifiées"))

    def optionsGoProKO(self):   # l'utilisateur abandonne les modifs
        
        self.goProMaker.set(self.goProMakerSave)
        self.goProFocale35.set(self.goProFocale35Save)
        self.goProFocale.set(self.goProFocaleSave)
        self.goProNomCamera.set(self.goProNomCameraSave)
        self.goProNbParSec.set(self.goProNbParSecSave)          # taux de conservation des photos pour DIV
        self.goProEchelle.set(self.goProEchelleSave)            # pour tapioca 
        self.goProDelta.set(self.goProDeltaSave)
        self.item2000.pack_forget()     # fermer l'item (pour évitr la question par menageEcran)
        self.encadre(_("Abandon : options GoPro inchangées."))

    def sauveOptionsGoPro(self):  # l'utilisateur valide les modifs

        self.goProMakerSave     =   self.goProMaker.get()        
        self.goProFocale35Save  =   self.goProFocale35.get()
        self.goProFocaleSave    =   self.goProFocale.get()
        self.goProNomCameraSave =   self.goProNomCamera.get()
        self.goProNbParSecSave  =   self.goProNbParSec.get()    # taux de conservation des photos pour DIV
        self.goProEchelleSave   =   self.goProEchelle.get()     # pour tapioca 
        self.goProDeltaSave     =   self.goProDelta.get()           
        
    # Choix d'une vidéo et extraction des photos :

    def laVideo(self):                                  #  choix de la video
        
        self.fermerVisuPhoto()                          #  s'il y a une visualisation en cours des photos ou du masque on la ferme             
        if verifierSiExecutable(self.ffmpeg)==False:
            self.encadre(_("L'outil ffmpeg n'est pas installé sur votre ordinateur. Traitement des vidéo GoPro impossible."))
            return
        
        repIni = ""                                     # répertoire initial de la boite de dialogue
        if os.path.isdir(self.repertoireDesPhotos):
            repIni = self.repertoireDesPhotos
        
        video = tkinter.filedialog.askopenfilename(title=_("Choisir la video issue d'un appareil {GoProMaker} {GoProName} (sinon modifier les options)"
                                                           ).format(GoProMaker=self.goProMaker.get(), GoProName= self.goProNomCamera.get()),
                                                  initialdir=repIni,
                                                  filetypes=[(_("Video"),("*.mp4","*.MP4","*.MOV","*.mov")),(_("Tous"),"*")],
                                                  multiple=False)
        
        if len(video)==0:
            self.encadre(_("Abandon, aucune sélection,\n le chantier res(te inchangé.") + "\n")
            return 

        if os.path.splitext(video)[1].upper() not in ".MP4":
            self.encadre(_("La version actuelle ne traite que les videos au format MP4, or le format des photos est %s. Désolé.") % (os.path.splitext(video)[1]))
            #return

        # Quel répertoire pour le chantier ?
        
        self.nouveauChantier()                  # Enregistre le chantier précédent, réinitialise les valeurs par défaut prépare un chantier vide avec le répertoire de travail par défaut   
        retour = self.quelChantier(video)       # positionne un nouveau self.repTravail en fonction du répertoire de la video, donne un nom au chantier
        if retour!=None:
                self.encadre(retour)
                return        # y a un pb
        oschdir(self.repTravail)
        
        if retour!=None:
            self.encadre(retour)
            return

        # ouverture de la trace

        self.cadreVide()
        self.ajoutLigne(_("Décompacte la vidéo"))

        # décompactage : extraction de toutes les photos :
        self.extensionChoisie = ".JPG"   # ou png        
        if self.lanceFfmpeg(video)==-1:         # sous les noms : "\Im_0000_%5d_Ok"+self.extensionChoisie %5d = 5 chiffres décimaux
            self.encadre(_("L'outil ffmpeg est absent.") + "\n" + _("Il convient de l'associer.") )
            return

        self.photosAvecChemin = [x for x in os.listdir(self.repTravail) if self.extensionChoisie in str(x) and os.path.isfile(x)]    # listes des photos conservées
        self.photosSansChemin = list([os.path.basename(x) for x in self.photosAvecChemin])   # liste des noms de photos copiès, sans le chemin. [tuple]            

        if self.photosSansChemin.__len__()==0:
            self.encadre(_("Aucune image décompactée : consulter la trace."))
            self.ecritureTraceMicMac()          # on écrit les fichiers trace
            return            

        # ajout de l'exif :

        self.ajoutExifGoPro()
        
        self.etatDuChantier = 2
    # Type de chantier : c'est une liste de string (on pourrait aussi mettre un dictionnaire), avec :
    # [0] = s'il s'agit de 'photos' ou d'une 'vidéo' 
    # [1] = s'il s'agit d'un chantier 'initial' ou 'renommé'
    # [2] = 'original' ou "importé"        
        self.typeDuChantier [0] = 'vidéo'
        self.copierParamVersChantier()      # effectue d'abord sauveparam()
        self.ecritureTraceMicMac()          # on écrit les fichiers trace

        # charge les options pour Tapioca : les valeurs d'échelle et de Line sont celles par défaut  

        self.modeTapioca.set('Line')# Mode (All, MulScale, Line)
      
        # charge les options pour Tapas :
        
        self.modeCheckedTapas.set('FishEyeBasic')

        # Message final :

        self.encadre(_("Les images de la video sont décompactées sous le répertoire :") + "\n\n" + self.repTravail+
                     "\n\n" + _("Il y a %s images décompactées.") % (str(self.photosSansChemin.__len__())) +
                     "\n\n" + _("Lancer 'Sélection des images' pour sélectionner %s images par seconde de film.") % (self.goProNbParSec.get())+
                     "\n\n" + _("La sélection choisira les 'meilleures' images")+
                     "\n\n" + _("Les options Tapioca et Tapas ont été positionnées pour des images GoPro : modifier si besoin"),nouveauDepart='oui') 

        return          # fin : on a obtenu les photos avec un exif à partir d'une vidéo

    def ajoutExifGoPro(self):

        # mise à jour de l'exif des images décompactées :
        
        self.ajoutLigne(_("met à jour l'exif des JPG décompactés :") + "\n"+
                        "F35="+self.goProFocale35.get()+"\n"+
                        "F="+self.goProFocale.get()+"\n"+
                        "Model="+self.goProNomCamera.get()+"\n"+
                        "Make="+self.goProMaker.get())                                                
##        # pour format png
##        if self.extensionChoisie=="png":
##            setExif = [self.mm3d,
##                   "SetExif",
##                   ".*"+self.extensionChoisie,
##                   "F35="+self.goProFocale35.get(),
##                   "F="+self.goProFocale.get(),
##                   "Cam="+self.goProNomCamera.get()]
        # pour format jpg            
        if self.extensionChoisie.upper()==".JPG":        
            setExif  = [self.exiftool,
                    "-Make="+self.goProMaker.get(),
                    "-Model="+self.goProNomCamera.get(),
                    "-FocalLength="+self.goProFocale.get(),
                    "-FocalLengthIn35mmFormat="+self.goProFocale35.get(),
                    "*"+self.extensionChoisie]
        
        self.lanceCommande(setExif)

        # SetExit crée des copies "original" des fichiers initiaux, on les supprime ;
   
        [supprimeFichier(x) for x in os.listdir(self.repTravail) \
         if os.path.splitext(x)[1]!=self.extensionChoisie  \
         and os.path.splitext(x)[0] not in self.photosSansChemin]
        
    def selectionGoPro(self):

        if self.typeDuChantier[0]!='vidéo':
            self.encadre(_("Cette sélection de photos est réservé  aux chantiers vidéos"))
            return
                         
        # on sélectionne un nombre d'image à la seconde en fonction de la qualité des images 

        ################## Bizarrerie (bogue) : l'extension doit être png, même si le format est jpg##################
        [os.rename(a,os.path.splitext(a)[0]+".png") for a in os.listdir(self.repTravail) if self.extensionChoisie in a]
        ########################################################
        self.cadreVide()        # ouvre la trace
        self.ajoutLigne(_("Sélection d'un sous ensemble des images GoPro décompactées."))
        div = [self.mm3d,
               "DIV",
               "Im_0000_.*png",
               self.divPerso.get(),
               "Rate="+self.goProNbParSec.get()]
        self.lanceCommande(div)

        ################## Bizarrerie (bogue) : l'extension doit être png, même si le format est jpg##################
        [os.rename(a,os.path.splitext(a)[0]+self.extensionChoisie) for a in os.listdir(self.repTravail) if 'png' in a]
        ########################################################
        
        # on supprime les intrus (les noms des fichiers intrus ont été marqué d'un N1, les autres d'un _Ok
        self.ajoutLigne("\n".join([(" "+_("a supprimer : ")+x) for x in os.listdir(self.repTravail) if "Nl" in str(x)]))
                
        nbSuppressions = [supprimeFichier(x) for x in os.listdir(self.repTravail) if "Nl" in str(x)].__len__()            
        self.photosAvecChemin = [x for x in os.listdir(self.repTravail) if self.extensionChoisie in str(x) and os.path.isfile(x)]    # listes des photos conservées
        self.photosSansChemin = list([os.path.basename(x) for x in self.photosAvecChemin])   # liste des noms de photos copiès, sans le chemin. [tuple]            
        self.etatDuChantier = 2
        self.ecritureTraceMicMac()                              # on écrit les fichiers trace
        if nbSuppressions==0:
            self.encadre(_("Aucune sélection effectuée. La version de micmac ne propose peut-être pas cette fonction.") + "\n"
                         + _("Consulter la trace.") + "\n\n" +
                         _("Vous pouvez utiliser le menu 'outils/qualité des photos line'") + "\n" +
                         _("puis effectuer une sélection manuelle."))
        else:
            self.afficheEtat(_("Images sélectionnées.") + "\n\n" + _("Vous pouvez lancer MicMac."))                                      

    ###################### Sélection des meilleures JPG (futur)

    def selectionJPG(self):

        if self.typeDuChantier[0]!='photos':
            self.encadre(_("Cette sélection de photos est réservé  aux chantiers photos"))
            return
                         
        # on sélectionne un nombre d'image à la seconde en fonction de la qualité des images 

        ################## Bizarrerie (bogue) : l'extension doit être png, même si le format est jpg##################
        [(os.rename(a,os.path.splitext(a)[0]+".png")) for a in os.listdir(self.repTravail) if self.extensionChoisie in a]
        ########################################################
        self.cadreVide()        # ouvre la trace
        self.ajoutLigne(_("Sélection d'un sous ensemble des images GoPro décompactées."))
    
        div = [self.mm3d,
               "DIV",
               "DSC.*png",
               self.divPerso.get(),
               "Rate="+self.goProNbParSec.get()]
        self.lanceCommande(div)

        ################## Bizarrerie (bogue) : l'extension doit être png, même si le format est jpg##################
        [(os.rename(a,os.path.splitext(a)[0]+self.extensionChoisie)) for a in os.listdir(self.repTravail) if 'png' in a]
        ########################################################
        
        # on supprime les intrus (les noms des fichiers intrus ont été marqué d'un N1, les autres d'un _Ok
        self.ajoutLigne("\n".join([(" "+_("a supprimer : ")+x) for x in os.listdir(self.repTravail) if "Nl" in str(x)]))
                
        nbSuppressions = [supprimeFichier(x) for x in os.listdir(self.repTravail) if "Nl" in str(x)].__len__()            
        self.photosAvecChemin = [x for x in os.listdir(self.repTravail) if self.extensionChoisie in str(x) and os.path.isfile(x)]    # listes des photos conservées
        self.photosSansChemin = list([os.path.basename(x) for x in self.photosAvecChemin])   # liste des noms de photos copiès, sans le chemin. [tuple]            
        self.etatDuChantier = 2
        self.ecritureTraceMicMac()                              # on écrit les fichiers trace
        if nbSuppressions==0:
            self.encadre(_("Aucune sélection effectuée.") + "\n" + _("Consulter la trace.") + "\n\n" +
                         _("Vous pouvez utiliser le menu 'outils/qualité des photos line'\npuis effectuer une sélection manuelle."))
        else:
            self.afficheEtat(_("Images sélectionnées.") + "\n\n" + _("Vous pouvez lancer MicMac."))                                      


########################################## ffmpeg : extraction images d'une video -----------------------
        
    def lanceFfmpeg(self,video):

        if os.path.exists(self.ffmpeg)==False:
            return -1
        # Si on a un masque 3D on l'utilise et on ne cherche pas plus loin :
        ffmpeg = [self.ffmpeg,
                "-i",
                video,
                self.repTravail+"\Im_0000_%5d_Ok"+self.extensionChoisie]
        self.lanceCommande(ffmpeg,
                           filtre=self.filtreFfmpeg,
                           info=_("ATTENTION : cette procédure est longue : patience !"))

    def filtreFfmpeg(self,ligne):
        #if ligne[0:5]=="frame":
            return ligne

########################################## Quel nom pour le modéle qui va être créé ? on renomme le modèle3D pour éviter de l'écraser
    @decorateTry
    def modele3DSuivant(self): # premier modèle libre
        for i in range(1,100):
            new = "modele3D_V"+str(i)+".ply"
            if not os.path.exists(new):
                self.modele3DFinal = new
                return
 
    def chercheModele3D(self):  # suppose le répertoire courant = self.repTravail; renvoi le plus récent des modeles 3D dans self.modele3DFinal
        for i in range(50,0,-1):
            self.modele3DFinal = "modele3D_V"+str(i)+".ply"
            if os.path.exists(self.modele3DFinal):
                return
        test = "modele3D.ply"   # pour compatibilité avec les versions antérieures
        if os.path.exists(test):
            self.modele3DFinal = test  
                
########################################## Outils divers (raccourcis clavier, infobulle, afficher un dico de points....)

    def lettre(self,event):
        if event.char.isdigit():                            # sinon on annule la recherche digit = chiffre
            self.cherche = self.cherche+event.char
            trouve = False
            for i in range(self.listeChoisir.__len__()):
                if self.cherche in os.path.basename(self.listeChoisir[i]):
                    self.selectionPhotos.selection_clear(self.current)
                    self.list_has_changed((i,))
                    self.selectionPhotos.select_set(self.current)
                    self.selectionPhotos.activate(self.current)
                    trouve = True
                    break
            if trouve:
                self.invitePhotoMessage.set(self.invitePhotoMessageInitial+"\n" + _("Trouvé : ")+self.cherche)
            else:
                self.invitePhotoMessage.set(self.invitePhotoMessageInitial+"\n" + _("Non trouvé : ")+self.cherche)
        else:
            self.cherche=str()
            self.invitePhotoMessage.set(self.invitePhotoMessageInitial)
            
    def poll(self):                                                             # boucle scrutant la valeur sélectionnée en cours, 10 fois par seconde
        try:
            now = self.selectionPhotos.curselection()
            if now != self.current:
                self.list_has_changed(now)                                      # la valeur a changé : on modifie l'affichage de la photo
            self.after(100, self.poll)
        except:
            pass
        
    def list_has_changed(self, selection):
        if len(selection)>0:
            self.current = selection
            try:
                if self.retailleEtAffichePhoto(self.listeChoisir[selection[0]])=="KO":  # prend l'image, la retaille et l'affiche
                    if self.messageSiPasDeFichier==1:
                        self.infoBulle(_("Pas de fichier pour ")+os.path.basename(self.listeChoisir[selection[0]]))  # message si pas de photo
            except: pass
            self.selectionPhotos.see(self.current)
            
    def infoBulle(self,texte=""):                                                   # affiche une infobulle sous le curseur.
        try: self.bulle.destroy()
        except: pass
        try:
            self.bulle = tkinter.Toplevel()                                         # nouvelle fenêtre
            self.bulle.overrideredirect(1)                                          # sans le bordel tout autour
            x,y = self.winfo_pointerx(),self.winfo_pointery()                       # self.winfo_pointerxy() # marche pas la première fois car x,y
            self.bulle.geometry("+%d+%d"%(x+15,y))                                  # position du coin nw de la fenêtre par rapport au curseur
            l=ttk.Label(self.bulle,
                        text = texte,
                        background="#ffffaa",
                        relief='solid')                                             # texte, la taille de la fenêtre s'adapte au texte, style infobulle
            l.pack()
            self.bulle.update()
        except Exception as e:
            print(_("erreur infobulle : "),str(e))
        
    def yview(self, *args):
        if args[0] == 'scroll':
            self.selectionPhotos.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.selectionPhotos.yview_moveto(args[1])

    def validPhoto(self):
        self.photosEnCours = self.selectionPhotos.curselection()
        for e in self.photosEnCours:
            ajout(self.selectionPhotosAvecChemin,self.listeChoisir[int(e)])
        self.fermerVisuPhoto()

    def cloreVisuPhoto(self):                       
        self.fermerVisu = True                                                  # fermeture par le second bouton
        self.fermerVisuPhoto()
        
    def fermerVisuPhoto(self):                                                  # fermer la fenêtre de visualisation des photos, du masque 2D, du masque 3D
        try:
            self.imagePhoto.close()                                             # fermer la photo ouverte et affichée
            del self.imagePhoto
        except: pass
        try: self.topVisuPhoto.destroy()                                        # fermer la fenêtre de visu des photos
        except: pass
        try: self.topMasque3D.destroy()                                         # fermer la fenêtre de visu du masque 3D (le subprocess C3DC subsiste)
        except: pass
        
    def upDown(self,event=None):                                                # modifie la sélection en cours après appui sur les flèches up ou Down (qui modifient seulement l'item "ACTIVE")
        if self.selectionPhotos.curselection():
            self.selectionPhotos.selection_clear(self.selectionPhotos.curselection())           
        self.selectionPhotos.selection_set(self.selectionPhotos.index('active'))

    def afficherTousLesPointsDuDico(self):                                      # affiche les points de l'imager en cours sur le canvas en cours
        if self.dicoPointsAAfficher==None:
            return
        nbpts = 0                                                               # (info dans le dico self.dicoPointsJPG)
        for cle in self.dicoPointsAAfficher:
            photo=os.path.basename(cle[1])
            if photo==self.enCours:
                self.xyJPGVersCanvas(self.dicoPointsAAfficher[cle][0],
                                     self.dicoPointsAAfficher[cle][1],
                                     bouton=cle[0])
                nbpts+=1

        if nbpts==0:
            self.infoBulle(_("Aucun point placé sur cette photo"))
        if nbpts==1:
            self.infoBulle(_("Un point placé sur cette photo"))
        if nbpts>1:
            self.infoBulle(nbpts.__str__()+" "+_("points placés sur cette photo"))

    def afficherLesInfosBullesDuDico(self):
        if self.dicoInfoBullesAAfficher==None:
            return
        for e in self.dicoInfoBullesAAfficher:
            if os.path.basename(e)==self.enCours:
                message = str(self.dicoInfoBullesAAfficher[e])
                if message!=str():
                    self.infoBulle(message)
            
 
    def xyJPGVersCanvas(self,xJPG,yJPG,bouton=None):                         # xJPG,yJPG : position dans l'image originale (Jpeg)
        couleurTexte = 'black'
        xFrame = xJPG * self.scale             # xFrame,yFrame : position dans l'image dans le cadre
        yFrame = yJPG * self.scale
        self.canvasPhoto.create_text(xFrame-10, yFrame+10, text = bouton,tag=bouton,fill=couleurTexte)
        self.canvasPhoto.create_oval(xFrame-5, yFrame-5,xFrame+5, yFrame+5,fill='yellow',tag=bouton)
        
    ######################################## Retaille et Affiche : prépare une photo pour affichage dans une petite fenêtre 200*200 max
    # attention : appelle  afficherTousLesPointsDuDico et afficherLesInfosBullesDuDico qui nécessitent des variables existantes
    
    def retailleEtAffichePhoto(self,photo):                                             # charge le canvas self.canvasPhoto
        self.enCours = os.path.basename(photo)

        if not os.path.exists(photo):                                                   # erreur de paramétrage
            try: self.canvasPhoto.delete(self.imgTk_id)                                 # supprimer la photo dans le canvas si elle existe
            except: return "KO"
        self.dimMaxiCanvas = 200
        self.hauteurCanvas = 200
        self.largeurCanvas= 200
        self.imagePhoto = Image.open(photo)        
        self.largeurImageFichier, self.hauteurImageFichier = self.imagePhoto.size
        if self.hauteurImageFichier>self.largeurImageFichier:                           # plus haut que large : on calcule l'échelle sur la hauteur
            self.hauteurCanvas = self.dimMaxiCanvas
            self.scale = self.hauteurCanvas/self.hauteurImageFichier
            self.largeurCanvas = int(self.largeurImageFichier * self.scale)             # largeur correspondante pour conserver les proportions
        else:                                                                           # plus large que haut :
            self.largeurCanvas = self.dimMaxiCanvas
            self.scale = self.largeurCanvas/self.largeurImageFichier                    # on cale sur l'échelle sur la largeur
            self.hauteurCanvas = int(self.hauteurImageFichier * self.scale)             # hauteur correspondante pour conserver les proportions        
        self.img = self.imagePhoto.resize((self.largeurCanvas,self.hauteurCanvas))
        self.imgTk = ImageTk.PhotoImage(self.img)
        self.imgTk_id = self.canvasPhoto.create_image(0,0,image = self.imgTk,anchor="nw") # affichage effectif de la photo dans canvasPhoto

        #affichage des info bulles
        try: self.bulle.destroy()
        except: pass        
        self.afficherLesInfosBullesDuDico()
        self.afficherTousLesPointsDuDico()

    ############################### Choix d'un répertoire dans la liste des répertoires de travail, avec scrollbar : charge self.selectionPhotosAvecChemin
    # les filtres opèrent une sélection sur les chantiers proposés :
    # filtres possibles : "GCP" avec GCP, ou "CALIB" avec Ori_Calib, ou "Homol" pour copier les points homologues, ou orient pour l'orientation
    # retour : a
    def choisirUnChantier(self,titre,mode='single',filtre=None):              # mode="single" ou 'extended'
        def compatibleChantierEnCours():    # élimine des chantiers proposés ceux qui ne contiennent pas les photos du chantier en cours
            try:
                liste = list(self.fichierProposes)
                for e in liste:
                    with open(os.path.join(e,self.paramChantierSav),mode='rb') as sauvegarde1:
                        r = pickle.load(sauvegarde1)
                    photosSansChemin = r[2]
                    # les photos du chantier en cours doivent être un sous ensemble des photos du chantier à copier  
                    if not set(self.photosSansChemin).issubset(photosSansChemin):
                         self.fichierProposes.remove(e)                         
            except Exception as e:
                pass

        # traitement :
            
        self.retourChoixRepertoire=_("Abandon")
        self.fichierProposes = list()
        chantierSansParametre = list()
        chantierSansRepertoire = list()
        self.restaureParamMicMac()
        for e in self.tousLesChantiers:                             # suppression des répertoires inexistants (parce que supprimés)
            if os.path.exists(e):
                fichierParamChantier  =   os.path.join(e,self.paramChantierSav)
                if os.path.exists(fichierParamChantier):            # le fichier paramètre existe :on le propose
                    ajout(self.fichierProposes,e)
                else:
                    chantierSansParametre.append(e)
            else:
                chantierSansRepertoire.append(e)            
        if len(self.fichierProposes)==0:
            return _("Aucun chantier mémorisé.")

        # filtres GCP et Calib
        
        if filtre == "CALIB": # il faut un répertoire Ori-Calib", les photos peuvent être différentes (il faut que ce soit le même appareil)
            
            self.fichierProposes = [ e for e in self.fichierProposes if os.path.exists(os.path.join(e,"Ori-Calib"))]            
            if len(self.fichierProposes)==0:  return _("Aucun chantier avec calibration.")
                     
        if filtre == "GCP": # il faut des points GCP
            try:            # Restauration des points GCP de l'autre chantier : définition et position dans les images 
                liste = list(self.fichierProposes)
                for e in liste:
                    sauvegarde1=open(os.path.join(e,self.paramChantierSav),mode='rb')
                    r=pickle.load(sauvegarde1)
                    sauvegarde1.close()
                    listePointsGPS = r[12]
                    if listePointsGPS.__len__()==0:
                        self.fichierProposes.remove(e)
            except Exception as e: pass
            if len(self.fichierProposes)==0:
                return _("Aucun chantier avac points GCP.")
                     
        if filtre == "Homol": 
            compatibleChantierEnCours() # il faut des points homologues et que les photos du chantier en cours soit un sous ensemble des photos du chantier de départ
            self.fichierProposes = [ e for e in self.fichierProposes if os.path.exists(os.path.join(e,"Homol"))]
            if len(self.fichierProposes)==0:
                message=_("Aucun chantier avec les mêmes photos et des points homologues.")
                self.encadre(message)
                return message
            
        if filtre == "Orientation":
            compatibleChantierEnCours() # il faut des points homologues et que les photos du chantier en cours soit un sous ensemble des photos du chantier de départ
            self.fichierProposes = [ e for e in self.fichierProposes if os.path.exists(os.path.join(e,"Ori-Arbitrary"))]
        if len(self.fichierProposes)==0:
            message=_("Aucun chantier avec les mêmes photos et une orientation.")
            self.encadre(message)
            return message
        
        self.selectionRepertoireAvecChemin=str()
        # création fenêtre
        self.topRepertoire = tkinter.Toplevel(fenetre)
        self.topRepertoire.title(titre)
        self.topRepertoire.geometry("800x600+100+200")
        fenetreIcone(self.topRepertoire)   
        f = self.topRepertoire                                      #ttk.Frame(self.topRepertoire)       
        frameSelectRep = ttk.Frame(self.topRepertoire)
        invite = ttk.Label(self.topRepertoire,text=_("Choisir le chantier :"))
        invite.pack(pady=10,padx=10,ipadx=5,ipady=5)
        scrollbarV = ttk.Scrollbar(frameSelectRep, orient='vertical')       
        scrollbarH = ttk.Scrollbar(frameSelectRep, orient='horizontal')
        self.selectionRepertoire = tkinter.Listbox(frameSelectRep,
                                                   selectmode=mode,
                                                   xscrollcommand=scrollbarH.set,
                                                   yscrollcommand=scrollbarV.set,
                                                   height= min(15,len(self.fichierProposes)),
                                                   width=  min(150,min(500,(70+max(len (r) for r in self.fichierProposes))))
                                                   )       
        self.selectionRepertoire.select_set(0)
        self.fichierProposes.sort(key=os.path.basename)
        for i in self.fichierProposes: # recherche de la taille dans le fichier paramètre
            chemin = os.path.dirname(i)
            chantier = os.path.basename(i)
            fichierParam = os.path.join(i,self.paramChantierSav)
            taille = restaureUnParametre(fichierParam,63) #renvoi la valeur du paramètre ou None si pas trouvé
            if  taille==None:
                taille = "???"
                #taille = sizeDirectoryMO(afficheChemin(os.path.dirname(i)))
                #sauveUnParametre(fichierParam, 63, taille)
            texte=format3Colonnes(os.path.basename(i),str(taille)+" MO ",afficheChemin(os.path.dirname(i)),100)
            self.selectionRepertoire.insert('end',texte)  
        scrollbarV.config(command=self.yviewRepertoire)
        scrollbarV.pack(side='right', fill='y')            
        scrollbarH.config(command=self.xviewRepertoire)
        scrollbarH.pack(side='bottom', fill='y')
        self.selectionRepertoire.pack(side='left', fill='both', expand=1)          
        frameSelectRep.pack()         
        self.selectionRepertoire.select_set(0)
        b = ttk.Button(f,text=_("Ouvrir"),command=self.validRepertoire)
        b.pack(pady=5)
        c = ttk.Button(f,text=_("Annuler"),command=self.cancelRepertoire)
        c.pack(pady=5)
        if len(chantierSansParametre)>0:
            d = ttk.Label(f,text=_("Il y a des chantiers incomplets,") + "\n " + _("le fichier %s est absent.") % (self.paramChantierSav)+ "\n" + 
                          _("Ces chantiers ne peuvent être ouverts mais peuvent être supprimés :") + "\n\n"+"\n".join(chantierSansParametre))
            d.pack(pady=5)
        if len(chantierSansRepertoire)>0:
            f = ttk.Label(f,text="\n\n"+_("Il y a des chantiers sur disque externe non connecté ou dont le répertoire a été supprimé,") + "\n" + 
                          _("Ces chantiers ne peuvent être ouverts mais peuvent être supprimés :") + "\n\n"+"\n".join(chantierSansRepertoire))
            f.pack(pady=5)

        self.topRepertoire.protocol("WM_DELETE_WINDOW", self.cancelRepertoire)    # Fonction a éxécuter lors de la sortie du programme
        self.topRepertoire.transient(fenetre)                            # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.topRepertoire.grab_set()
        fenetre.wait_window(self.topRepertoire)    
        return self.retourChoixRepertoire

    def yviewRepertoire(self, *args):
        if args[0] == 'scroll':
            self.selectionRepertoire.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.selectionRepertoire.yview_moveto(args[1])

    def xviewRepertoire(self, *args):
        if args[0] == 'scroll':
            self.selectionRepertoire.xview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.selectionRepertoire.xview_moveto(args[1])            

    def validRepertoire(self):
        self.repertoireEnCours = self.selectionRepertoire.curselection()
        self.topRepertoire.destroy()
        self.selectionRepertoireAvecChemin = str(self.fichierProposes[self.repertoireEnCours[0]])
        self.retourChoixRepertoire=None

    def cancelRepertoire(self):
        self.topRepertoire.destroy()
        self.retourChoixRepertoire=_("Abandon utilisateur.")


    ########## pour renommer homol    

    def repertoireHomol(self,homol):
                                                    # le paramètre permet d'utiliser un autre répertoire
        try: os.rename(_("Homol"),_("HomolTemporaire"))
        except Exception as e:
            print(_("erreur renommage Homol en HomolTemporaire : "),str(e))
            return
        try:
            os.rename(homol,_("Homol"))
            self.homolActuel = homol                # Pour retourner à la situation originale si besoin
        except Exception as e: print(_("erreur renommage %s en Homol : ") % (homol),str(e))

    def retourHomol(self):      # pour l'instant inutilisé
        
        if self.homolActuel==str(): return
        try: os.rename(_("Homol"),self.homolActuel)
        except  Exception as e:
            print(_("erreur renommage Homol en : %s : ") % (self.homolActuel),str(e))
            return        
        try: os.rename(_("HomolTemporaire"),"Homol")
        except  Exception as e:
            print(_("erreur renommage HomolTemporaire en Homol : "),str(e))
            return
        self.homolActuel = str()
        
    #################### Examen du nombre de points homologues  dans le répertoire homol sous le répertoire passé en paramètre, affichage
    # n'est appelé que par l'item de menu : le paramètre est prévu pour usage ultérieur

    def nombrePointsHomologues(self,rep="Homol"):
        message = ""
        nbGroupes = self.regroupementSuivantPointsHomologues(rep)
        if nbGroupes>1 :
            message = _("ATTENTION : Les photos définissent plusieurs scènes disjointes") + "\n"+\
                      _("MicMac ne peut travailler que sur une seule scène : toutes les photos doivent former une seule scéne.") + "\n"+\
                      _("Les photos se répartissent en :") + str(nbGroupes)+" "+_("groupes distincts (consulter la trace) : ")+"\n" +\
                      "\n".join([str(e)[:100] for e in self.lesGroupesDePhotos])
            self.ajoutLigne(_("Les groupes de photos séparés : ")+"\n"+"\n".join([str(e) for e in self.lesGroupesDePhotos]))
            self.ecritureTraceMicMac()
        self.menageEcran()         
        repertoireHomol = os.path.join(self.repTravail,rep) # répertoire des homologues
        if os.path.isdir(repertoireHomol)==False:
            self.encadre(_("Lancer MicMac avant de pouvoir évaluer la qualité des photos."))
            return
        if os.path.isdir(repertoireHomol)==False:
            self.encadre(_("Le traitement n'a donné aucun point homologue.") + "\n\n" + message+ "\n\n"+ _("Consulter la trace."))
            return
        
        # somme des scores de chaque photo : préparation des données
        homol = dict()
        nb = dict()
        moyenne = dict()
        for photo in self.photosSansChemin:
            homol[photo] = 0                    # nombre total des points homologue de l'image
            nb[photo] = 0                       # nombre d'images "comparées" 
            moyenne[photo] = 0

        oschdir(repertoireHomol)
        nbPoints = 0
        for e in os.listdir():                   # balaie tous les fichiers contenant les points homologues         
            oschdir(os.path.join(repertoireHomol,e))
            for f in os.listdir():
                if os.path.isfile(f):           # fichier : on calcule le nombre de points homologues dans le fichier
                    nbPoints = 0
                    if f[-3:]=="dat":
                        taille = os.path.getsize(f)
                        nbPoints = (taille-8)/44    # fichier binaire : 44 octets par point homologue
                    if f[-3:]=="txt":               # fichier texte : une ligne par point homologue
                        with  open(f) as infile:    # il faut lire de fichier (longueur variable)
                            nbPoints = infile.readlines().__len__()
                    for photo in self.photosSansChemin:
                        if photo in e: # nom de la photo dans le nom du répertoire : on incrémente le nb points
                            homol[photo] += nbPoints
                            nb[photo] += 1
                            moyenne[photo] = homol[photo]/nb[photo]
        
    # on crée le rapport : nombre moyen de points homologues, trié du + grand au plus petit : dans ajouLigne

        listeHomol = list(moyenne.items())
        listeHomol.sort(key=lambda e: e[1],reverse=True)
        cas = _("dernier traitement : ")+self.modeTapioca.get()
        self.effaceBufferTrace()        # efface ajoutligne
        self.ajoutLigne("\n" + _("Classement des photos par nombre de points homologues :") + "\n\n"+cas+"\n\n")
        self.ajoutLigne(chr(9)+_("Photo                 ")+chr(9)+_("score")+chr(9)+_("nb photos en correspondance") + "\n\n")
        for e in listeHomol:
            self.ajoutLigne(e[0]+chr(9)+str(int(e[1]))+chr(9)+chr(9)+chr(9)+str(nb[e[0]])+"\n")
        if len(listeHomol)==0:
            self.ajoutLigne(_("Aucune photo n'a de point analogue avec une autre.") + "\n")            
        self.ajoutLigne("\n"+heure()+" "+_(": fin de la recherche sur la qualité des photos."))
        self.ajoutLigne("\n\n ******")
        ligneFiltre = self.ligneFiltre  # l'écriture de la trace efface self.ligneFiltre et encadre doit être en fin de paragraphe
        self.ecritureTraceMicMac()
        oschdir(self.repTravail)       
        self.encadre(message+ligneFiltre)

    #################### Regroupement des photos reliées par des points homologues : renvoi le nombre de groupes
    ## s'il y a plusieurs groupes isolés les uns des autres alors : pas d'orientation possible
    # attention : lors de la commande Tapioca MulScale lors du premier passage il est créé un répertoire pour chaque photo dans Homol_SRes
    #             ce qui peut créer des groupes "vides"
    #             lors du second passage il n'est créé un répertoire que s'il y a des points homologues avec une autre photo
    # Modif du premier avril 2020 : le répertoire Homol existe toujours, toujours faire le regroupement sur ce répertoire sauf 
    def regroupementSuivantPointsHomologues(self,rep = "Homol"):        
        def ajout(groupe,liste):                       
            for p in liste:
                if p in dico and p not in exclure:
                    exclure.append(p)
                    ajout(groupe,dico[p])
                    if p not in groupe:
                        groupe.append(p)
            
        repertoireHomol = os.path.join(self.repTravail,rep)
        if os.path.isdir(repertoireHomol)==False:
            return 0
        groupe = dict()     # dico : [photo : liste des photos participant à la même scène]
        dico = dict()       # dico : [photo : liste des photos ayant des points homologues] (à partir du répertoire rep)  
        exclure = list()    # liste des photos apparaisssant dans un groupe, chaque photo n'étant que dans un seul groupe
        for e in os.listdir(repertoireHomol):   # balaie tous les sous-répertoires de rep : crée une liste par répertoire
            photo = e[6:]   # nom de la photo
            dico[photo] = list()        
            for f in os.listdir(os.path.join(repertoireHomol,e)): # sous-répertoire
                dico[photo].append(f[:-4])          # nom des photos (sans prefixe/suffixe) dans un dictionnaires de listes
        if rep=="Homol_SRes":                       # Tapioca MulScale lors du premier passage il est créé un répertoire pour chaque photo dans Homol_SRes
                                                    # ce qui n'est pas le cas pour Tapioca All : pas de répertoire si pas de photo en correspondance !
            dico = {k: v for k, v in dico.items() if v} # retire les photos isolées
        for p in self.photosSansChemin:             # recherche pour chaque photo du groupe d'appartenance
            groupe[p] = list()                      # chaque photo n'appartient qu'à un seul groupe
            if p in dico :
                ajout(groupe[p],dico[p]) # récursivité sur les listes de photos ayant des points homologues
            else:
                groupe[p] = [p,]                     # il faut ajouter les groupes avec une seule photo isolée (ignorés dans le répertoire rep):
                
        # ajout de p si p est isolé (dico[p] =  vide)
        for p in dico:
            if dico[p]==list():
                 groupe[p]=[p]
        # Suppression des photos qui ne servent que pour la calibration intrinsèque, les photos uniquement pour calibration ne peuvent former une scéne
        if self.calibSeule.get():
            for p in groupe:
                try:
                    [groupe[p].remove(e) for e in self.photosCalibrationSansChemin if e in groupe[p]]
                except:
                    pass
        # les regroupements sont faits : la variable groupe[p] est soit une liste vide, soit la liste de tous les éléments du groupe      
        self.lesGroupesDePhotos = [e for e in groupe.values() if e]
        return self.lesGroupesDePhotos.__len__()            
                
################## Sélection des N meilleures photos en fonction de leur nombre de points homologues....
################## remarque : on sélectionne les meilleurs couples, avec un petit effort sur le premier item des éléments de listeTaille
################## Attention : suppose que les points homologues soient dans des fichiers .dat ( si variable self.exptxt="0") sinon des .txt
        
    def lesMeilleuresPhotos(self,nombre=0): # retourne la liste des N = nombre meilleures photos en nombre de points homologues.
        self.menageEcran()    
        listeTaille = list()
        repertoireHomol = os.path.join(self.repTravail,"Homol")  # répertoire des homologues
        if os.path.isdir(repertoireHomol)==False:
            self.encadre(_("Lancer d'abord Tapioca/Tapas"))
            return
        
        oschdir(repertoireHomol)        
        for e in os.listdir():                                  # balaie tous les fichiers contenant les points homologues
            oschdir(os.path.join(repertoireHomol,e))            
            for f in os.listdir():
                listeTaille.append((e,f, os.path.getsize(f)))   # répertoire, nom du fichier et taille
        oschdir(self.repTravail)
        
        listeTaille.sort(key= lambda e:  e[2],reverse=True)     # trie la liste des fichiers par taille
        if self.exptxt =="0" : typeFichier=".dat"
        if self.exptxt =="1" : typeFichier=".txt"        
        liste = [(e[1].split(typeFichier)[0],e[0].split("Pastis")[-1]) for e in listeTaille]    # liste des noms des plus gros fichiers des fichiers de l'arborescence Homol
        listeSet=set()                                          # chaque nom peut apparaitre plusieurs fois : on va utiliser un ensemble (set)
        for e in liste :                                        # on ne conserve que les n premiers
             listeSet.add(e[0])                                 # ajout nom du répertoire = premiere photo(la lecture de la liste conserve l'ordre des tailles)
             listeSet.add(e[1])                                 # ajout seconde photo  
             if len(listeSet)>=nombre:                          # le passage par un ensemble fait perdre l'ordre des tailles (sans importance : on ne retient que les meilleures)
                 break
        listeOk = [e for e in listeSet if os.path.exists(e)]    # liste limitée aux fichiers effectivement présents sous le répertoire de travail
        return listeOk

####################    Lister les fichiers Ply générés:

    def lister3DPly(self):
        listePly = [e for e in os.listdir() if os.path.splitext(e)[1]==".ply"]
        if listePly==list():
            self.encadre(_("Aucun nuage de points dans ce chantier."))
            return
        self.choisirUnePhoto(listePly,
                             titre=_("Liste des nuages de points du chantier"),
                             message=_("les nuages (fichiers ply) :"),
                             messageBouton=_("Visualiser"),
                             boutonDeux=_("Fermer"),
                             mode='single')
        if self.selectionPhotosAvecChemin.__len__()==1:
            self.lanceCommande([self.meshlab,self.selectionPhotosAvecChemin[0]],attendre=False)

    ####################    Fusionner des fichiers Ply :

    def choisirPuisFusionnerPly(self):

        listePly = [e for e in os.listdir() if os.path.splitext(e)[1]==".ply"]
        if listePly==list():
            self.encadre(_("Aucun nuage de points dans ce chantier."))
            return
        self.choisirUnePhoto(listePly,
                             titre=_("Fusion de nuages"),
                             message=_("Choisir les fichiers à fusionner :"),
                             messageBouton=_("Fusionner et visualiser"),                             
                             boutonDeux=_("Fermer"),
                             mode='extended')
        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        if self.selectionPhotosAvecChemin.__len__()==1:
            self.encadre(_("Choisir au moins 2 nuages pour la fusion."))
            return
        liste = "|".join([os.path.splitext(os.path.basename(x))[0] for x in self.selectionPhotosAvecChemin])
        self.mergePly = 'fusion.ply'
        i = 0
        while os.path.exists(os.path.join(self.repTravail,self.mergePly))==True and i<20:
            i+=1
            self.mergePly = 'fusion_'+str(i)+".ply"        
        self.fusionnerPly(self.selectionPhotosAvecChemin,self.mergePly)

    def fusionnerPly(self,liste,nomFinal):
        
        if liste.__len__()==0:      
            return
        if liste.__len__()==1:
            self.encadre(_("Choisir au moins 2 nuages pour la fusion."))
            return
        if os.path.exists(liste[0])==False or os.path.exists(liste[1])==False:     # la liste comprend au moins 2 fichiers : existent-t-ils ?
            self.encadreEtTrace(_("Les ply attendus n'ont pas été créé.") + "\n" + _("Consulter la trace."))
            return
            
        supprimeFichier(nomFinal)   # tentative de suppression du fichier résultat
        # on va fusionner tous les ply, on dénomme ceux qui ne doivent pas l'être :           
        [os.rename(e,os.path.splitext(e)[0]+".pyl") for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]=='.ply' and e not in liste]  # pour ne traiter que le nécessaire (self.)
          
        mergePly = [self.mm3d,
                    "MergePly",
                    '.*.ply',
                    self.mergePlyPerso.get(),
                    "Out="+nomFinal]
        self.lanceCommande(mergePly)            # fusion des ply : attention si types différents (xyz,xyzrgb), plante 
        [os.rename(e,os.path.splitext(e)[0]+".ply") for e in os.listdir(self.repTravail) if os.path.splitext(e)[1]==".pyl"]  # remise à l'état initial        
        if os.path.exists(nomFinal):
            self.lanceCommande([self.meshlab,nomFinal],attendre=False)
            self.encadreEtTrace(_("Nuage fusionné :") + "\n\n" + nomFinal + "\n\n" + _("ajouté à la liste des nuages.") + "\n" + _("résultat de la fusion de :") + "\n\n"
                        +"\n"+"\n".join(liste)+"\n")
        else:
            self.encadreEtTrace(_("La fusion n'a pu se réaliser.") + "\n" + _("Consulter la trace."))

    def demandePlyChantierPourInfo(self):
        listePly = [e for e in os.listdir() if os.path.splitext(e)[1]==".ply"]
        if listePly==list():
            self.encadre(_("Aucun nuage de points dans ce chantier."))
            return
        self.choisirUnePhoto(listePly,
                             titre=_("Information sur un fichier PLY"),
                             message=_("Choisir le fichier:"),
                             messageBouton=_("Rechercher les infos"),                             
                             boutonDeux=_("Fermer"),
                             mode='extended')
        if len(self.selectionPhotosAvecChemin)==0:
            return
        ply = self.selectionPhotosAvecChemin[0]        
        self.infoSurPly(ply)

    def demandePlyPourInfo(self):

        ply = tkinter.filedialog.askopenfilename( initialdir="",                                                 
                                                filetypes=[(_("ply"),"*.ply"),(_("Tous"),"*")],
                                                multiple=False,
                                                title = _("Info sur le fichier Ply"))
    
        self.infoSurPly(ply)


    def infoSurPly(self, ply):
        if not os.path.exists(ply):
            return
        self.encadre(_("Patience : lecture du fichier :\%s") % (ply))
        info = typePly = typeDePly(ply)
        if typePly in ("nuage de points ascii","mesh ascii","mesh binary"):
            info = _("Type du fichier ply :\n%s\n %s") % (ply,typePly)
        if typePly == None:
            info = _("Le contenu de ce fichier n'est pas du type Ply")
        if typePly in ("nuage de points binaire","mesh binary"):
            mnt = extraireLesXyzDuPly(ply)
            if type(mnt) != type(dict()):
                self.encadre(_("Abandon : %s") % (ply))
                return
            info  = _("Nom du fichier : %s") %(ply)
            info +=  "\n\n"+_("Nombre de points dans le nuage : %s") % (mnt["nb"])
            info +=  "\n\n"+_("Surface couverte : %s") % (round(mnt["surface"],2))
            info +=  "\n\n"+_("Nombre de points par unité de surface : %s") % (int(mnt["nb"]/mnt["surface"]))
            info +=  "\n\n"+_("X minimum : %s") % (round(mnt["min_x"],2))
            info +=  "\n"+_("X maximum : %s") % (round(mnt["max_x"],2))
            info +=  "\n\n"+_("Y minimum : %s") % (round(mnt["min_y"],2))
            info +=  "\n"+_("Y maximum : %s") % (round(mnt["max_y"],2))
            info +=  "\n\n"+_("Z minimum : %s") % (round(mnt["min_z"],2))
            info +=  "\n"+_("Z maximum : %s") % (round(mnt["max_z"],2))
            info +=  "\n\n"+_("Volume : %s") % (round(mnt["volume"],2))
            info +=  "\n\n"+_("Nombre de points par unité de volume : %s") % (int(mnt["nb"]/mnt["volume"]))
                      
        self.encadre(info)
        self.ajoutLigne(info)


    ################### Conversion au format jpg, information de l'Exif

    def conversionJPG(self,liste=list()):

        if self.pasDeConvertMagick():
            self.ajoutLigne(_("Le programme de conversion n'est pas présent."))
            return
        if liste==list():
            liste = self.photosSansChemin
        if liste.__len__()==0:
            return
        curdir = os.getcwd()
        oschdir(os.path.dirname(liste[0]))
        for e in liste:
            if os.path.isfile(e):
                i=os.path.basename(e)
                nouveauJPG = os.path.splitext(i)[0]+".JPG"                
                convert = [self.convertMagick,i,'-quality 100',nouveauJPG]
                os.system(" ".join(convert))
        oschdir(curdir)
        
    # mise à jour de l'exif :
                
    def majExif(self,liste=list()):
        if self.pasDeExiftool():return
        self.menageEcran()        
        self.encadre(_("Recherche des exifs des photos en cours.\nPatience...."))
        self.outilAppareilPhoto(silence='oui')
        self.exifMaker.set(self.fabricant)
        self.exifNomCamera.set(self.nomCamera)
        self.exifFocale.set(self.focale)
        self.exifFocale35.set(self.focale35MM)
        self.menageEcran()          
        self.item3000.pack()
        return

    # lancé par item3000 :
    
    def exifOK(self):
        if self.pasDeExiftool():return
        listeTag = [('Make',                    self.exifMaker.get()     ),
                    ('Model',                   self.exifNomCamera.get() ),
                    ('FocalLength',             self.exifFocale.get()    ),
                    ('FocalLengthIn35mmFormat', self.exifFocale35.get()  )
                    ]
                     
        self.encadre(_("Modification des exifs des photos en cours.\nPatience...."))
        self.informerExif(self.exiftool,self.photosSansChemin,listeTag)
        self.item3000.pack_forget()     # pour éviter la question par menageEcran
        self.encadreEtTrace(_("Exifs mis à jour") + "\n"+
                            _("Fabricant = ")+self.exifMaker.get()+"\n"+
                            _("Modèle = ")+self.exifNomCamera.get()+"\n"+
                            _("Focale = ")+self.exifFocale.get()+"\n"+
                            _("Focale eq 35mm = ")+self.exifFocale35.get()+"\n")
        self.nbFocales = 1       # une seule focale pour toutes les photos
        self.lesTagsExif = dict() # supprimer les anciennes mémorisations des tags
        self.sauveParamChantier()
        # suppression des fichiers créés par exiftool
        [supprimeFichier(x) for x in os.listdir(self.repTravail) \
        if os.path.splitext(x)[1]==".JPG_original"]
        
    def exifKO(self):
        self.item3000.pack_forget()     # pour éviter la question par menageEcran        
        self.encadre(_("Abandon de la mise à jour des exifs"))
        
    # après saisie de l'exif :

    def informerExif(self,exiftool,listeFichiers,listeTagInfo): # la liste peut être relative ou absolue, taginfo est une liste de tuple (tag,info)

        if self.pasDeExiftool():return

        if listeFichiers.__len__()==0:
            return _("Aucune photo à mettre à jour.")

        if self.nombreDExtensionDifferentes(listeFichiers)!=1:
            return _("La liste des fichiers comporte plusieurs extensions différentes : abandon.")+\
                   "\n".join(listeFichiers)

        extension = os.path.splitext(listeFichiers[0])[1]
        if extension.upper() not in ".JPG.JPEG":
            interface.encadre(_("La version actuelle ne traite que les exif des photos au format JPG, or le format des photos est %s. Désolé, abandon.") % (extension) )
            return
                  
        # Controle de l'existence des fichiers :
        for e in listeFichiers:
            if os.path.isfile(e)==False:
                return _("Le fichier %s n'existe pas. Abandon") % (e)
                    
        # mise à jour de l'exif des images décompactées :
        
        message = _("met à jour l'exif de ")+"\n".join(listeFichiers)+"\n"
                      
        # Les fichiers sont ok on va pouvoir les traiter :

        listeModifs = ["-"+tag+"="+info for tag,info in listeTagInfo]

        # pour format jpg            
  
        setExif  = [exiftool]+listeModifs+["-ext .JPG", self.repTravail] # ["*"+extension]
    
        self.lanceCommande(setExif)
                    
        # SetExit crée des copies "original" des fichiers initiaux, on les supprime ;
   
        [supprimeFichier(x) for x in os.listdir(self.repTravail) \
        if os.path.splitext(x)[1]!="."+extension  \
        and os.path.splitext(x)[0] in listeFichiers]

        return ""
           
    #################### Utilitaires : tests de la présence de photos, de mm3d, d'exiftool, envoi retour chariot
    # et compte le nombre d'extensions différentes dans une liste, affiche un texte long et scroll

    def pasDePhoto(self,avecMessage=True):
        if self.photosAvecChemin.__len__()==0:
            if avecMessage: self.encadre(_("Choisir des photos au préalable."))
            return True
##        repertoireInitial = os.path.dirname(self.photosAvecChemin[0])
##        if not os.path.isdir(repertoireInitial):
##            self.encadre(_("Répertoire du chantier non accessible"))
##            return
##        liste = [e for e in self.photosAvecChemin if os.path.exists(e)==False]
##        if liste.__len__()>0:
##            self.photosAvecChemin = [e for e in self.photosAvecChemin if os.path.exists(e)]
##            self.photosSansChemin = [os.path.basename(x) for x in  self.photosAvecChemin]
##            if self.photosAvecChemin:
##                repertoireInitial = os.path.dirname(self.photosAvecChemin[0])
##                texte=_("Attention les photos suivantes sont absentes sur disque : ") + "\n"+"\n".join(liste)+"\n" + _("Elles sont supprimées du chantier.")
##                self.troisBoutons(titre=_("Problème de fichiers"),question=texte,b1='OK',b2='')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1            
##            else:           
##                texte=_("Attention toutes les photos  sont absentes sur disque et retirées du chantier: ")
##                self.troisBoutons(titre=_("Problème de fichiers"),question=texte,b1='OK',b2='')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1            
             
    def pasDeMm3d(self):
        if not os.path.exists(self.mm3d):
             self.encadre("\n" + _("Bonjour !") + "\n\n" + _("Commencer par indiquer où se trouve MicMac :") + "\n\n "+
                         _("- menu Paramétrage/Associer le répertoire bin de MicMac") + "\n\n"+
                         _("Ensuite consulter l'aide, item 'pour commencer'.") + "\n\n"+
                         _("Si besoin :") + "\n "+
                        _( "- Associer convert et exiftool s'ils ne sont pas trouvés automatiquement sous micmac/binaire-aux")+"\n "+
                        _("- Associer un outil (CloudCompare ou Meshlab) pour afficher les nuages de points 3D") + "\n\n "+
                         _("- Consulter la notice d'installation et de prise en main"),
                         aligne='left')
             return True

    def pasDeExiftool(self):
        if not os.path.exists(self.exiftool):
            self.encadre(_("Désigner le fichier exiftool (menu paramétrage)."))            
            return True
        
    def pasDeConvertMagick(self):
        if not os.path.exists(self.convertMagick):
            self.encadre(_("Désigner le fichier convert, ou avconv, d'image Magick") + "\n" +
                         _("en principe sous micmac\\binaire-aux (menu paramétrage)."))            
            return True

    def pasDeFfmpeg(self):
        if not os.path.exists(self.ffmpeg):
            self.encadre(_("Désigner le fichier ffmpeg (possible sous micmac\\binaire-aux (menu paramétrage)."))            
            return True

    def nombreDExtensionDifferentes(self,liste):
        lesExtensions=set([os.path.splitext(x)[1].upper() for x in liste])                  # on vérifie l'unicité de l'extension :
        self.lesExtensions=list(lesExtensions)                                              # liste pour être slicable
        return len(self.lesExtensions)

    def nombreDePrefixes(self,liste,longueurPrefixe=3):
        lesPrefixes=set([x[0:longueurPrefixe].upper() for x in liste])                  # on vérifie l'unicité des préfixes :
        self.lesPrefixes=list(lesPrefixes)                                              # liste pour être slicable
        return len(self.lesPrefixes)

    def nombreDeExifTagDifferents(self,tag="SerialNumber"):     # on vérifie l'unicité des valeurs pour un tag (numéros de série par défaut)
        lesTags = [[self.encadrePlus("."),self.tagExif(tag,photo)] for photo in self.photosSansChemin]
        lesTags = set([e1 for e0,e1 in lesTags])
        self.lesTags=[ tag for tag in lesTags if tag !=""]      # abonde la liste des valeurs trouvées dans self.lesTags    
        return len (self.lesTags)                               # renvoie le nombre de valeurs différentes : 0, 1 , plus

    def afficheTexte(self,texte):
        self.cadreVide()
        self.listePositions201 = list()
        self.ending_index = "1.0"
        self.effaceBufferTrace()        
        self.ajoutLigne(texte)
        fenetre.state('zoomed')
        self.texte201.see("1.1")
        self.texte201.focus_set()
        
        
########################################################   Modifier les options par défaut

    def majOptionsParDefaut(self):                  # Si les options ont déjà été modifiées
        if os.path.exists(self.fichierSauvOptions):
            retour = self.troisBoutons(titre=_("Modifier les options par défaut"),
                                       question=self.messageSauvegardeOptions,                                       
                                       b1=_("Revenir aux options par défaut d'AperoDeDenis"),
                                       b2=_("Utiliser les options du chantier en cours"),
                                       b3=_("Ne rien changer"))
            if retour == 0: 
                supprimeFichier(self.fichierSauvOptions)
                self.encadre(_("Options par défaut réinitialisées"))
            elif retour == 1:
                optionsOK = self.sauveOptions()
                if optionsOK==True:
                    self.encadre(_("Les options par défaut seront  désormais celles du chantier en cours"))
                else:
                    self.encadre(optionsOK)
            else:
                self.afficheEtat()
                
        else:                                   # Si les options n'ont pas été modifiées
            retour = self.troisBoutons(titre=_("Modifier les options par défaut"),
                                       question=self.messageSauvegardeOptions+
                                       _("Les options par défaut actuelles sont les options par défaut d'AperoDeDenis"),                                      
                                       b1=_("Utiliser les options du chantier en cours"),
                                       b2=_("Ne rien changer"))
            if retour == 0: # choix b1 
                optionsOK = self.sauveOptions()
                if optionsOK==True:
                    self.encadre(_("Les options par défaut seront  désormais celles du chantier en cours"))
                else:
                    self.encadre(optionsOK)
            else:
                self.afficheEtat()                    
                
    def sauveOptions(self):     # les options par défaut modifiées par l'utilisateur
        retour = self.controleOptions()
        if retour!=True:
            message = _("Options par défaut non sauvegardées car les options du chantier en cours sont invalides :") + "\n"+retour
            return message
        try:
            sauvegarde3=open(self.fichierSauvOptions,mode='wb')
            pickle.dump((   self.echelle1.get(),                # nécessaire pour définir la variable obtenue le widget
                            self.echelle2.get(),             
                            self.echelle3.get(),
                            self.echelle4.get(),             
                            self.delta.get(),    
                            self.fileTapioca.get(),             # pour usage futur   
                            self.modeTapioca.get(),
                            self.modeCheckedMalt.get(),
                            self.modeCheckedTapas.get(),
                            self.arretApresTapas.get(),
                            self.photosUtilesAutourDuMaitre.get(),
                            self.calibSeule.get(),
                            self.zoomF.get(),
                            self.modeC3DC.get(),
                            self.tawny.get(),
                            self.dicoPerso,    
                            version,
                            self.lancerTarama.get(),
                            self.incertitudeCibleGPS.get(),
                            self.incertitudePixelImage.get(),
                            self.choixDensification.get(),
                            self.calculNuageNonDense.get(),
                            self.nuage2Mesh.get(),
                            self.tolerance,
                            self.arrondi,
                            ),
                        sauvegarde3)
            sauvegarde3.close()
        except Exception as e:              # Controle que le programme a accès en écriture dans le répertoire d'installation
            print (_('erreur sauveOptions : '),str(e))
            texte = _("Erreur rencontrée lors de la sauvegarde des options : ")+str(e)
            return texte
        return True
            
    def restaureOptions(self):
        if not os.path.exists(self.fichierSauvOptions): return
        try:                                                                        # s'il y a une sauvegarde alors on la restaure
            sauvegarde4 = open(self.fichierSauvOptions,mode='rb')
            r = pickle.load(sauvegarde4)
            sauvegarde4.close()
            self.echelle1.set(r[0])               # nécessaire pour définir la variable obtenue le widget
            self.echelle2.set(r[1])             
            self.echelle3.set(r[2])
            self.echelle4.set(r[3])             
            self.delta.set(r[4])    
            self.fileTapioca.set(r[5])           
            self.modeTapioca.set(r[6])
            self.modeCheckedMalt.set(r[7])          
            self.modeCheckedTapas.set(r[8])
            self.arretApresTapas.set(r[9])
            self.photosUtilesAutourDuMaitre.set(r[10])
            self.calibSeule.set(r[11])
            self.zoomF.set(r[12])
            self.modeC3DC.set(r[13])
            self.tawny.set(r[14])
            self.dicoPerso=r[15]  
            # R16 est la version d'aperodedenis, inutile pour l'instant
            self.lancerTarama.set(r[17])
            self.incertitudeCibleGPS.set(r[18])
            self.incertitudePixelImage.set(r[19])
            self.choixDensification.set(r[20])
            self.calculNuageNonDense.set(r[21])
            self.nuage2Mesh.set(r[22])
            self.tolerance=r[23]
            self.arrondi=r[24]
        except Exception as e:
            print(_("erreur restauration options : ")+str(e))
        # Restauration des paramètres nommés personnalisés : si pas alors initialisation
        if type(self.dicoPerso)!=dict(): self.initPerso() 
        else: self.restauPerso()
              
    ########################################################   nouvelle fenêtre (relance utile pour vider les traces d'exécution de mm3d et autres)

    def nouveauDepart(self):
        try: self.copierParamVersChantier()                          # sauvegarde du chantier, des param...
        except: pass
        try: self.ecritureTraceMicMac()                              # on écrit les fichiers trace
        except: pass

    # faut-il différencier linux et windows ?
        if self.systeme=='posix':
            if self.messageNouveauDepart==str():
                self.afficheEtat()
            else:
                self.encadre(self.messageNouveauDepart,nouveauDepart='oui')
            self.messageNouveauDepart = str()
            
        if self.systeme=='nt':       
           global messageDepart
           messageDepart = self.messageNouveauDepart            # ce message sera repris dans la nouvelle "interface"
           if "fenetre" in globals():
                time.sleep(0.2)
                try:
                    fenetre.destroy()                                # relance une nouvelle "interface"
                except: pass
            
    # quitter
            
    def quitter(self):
        self.ecritureTraceMicMac()                      # enegistre la trace
        self.enregistreChantier()                       # enregistre systématiquement (modifier ?)
        print(heure()+" "+_(": fin normale d'aperodedenis."))
        self.sauveParam()
        global continuer                                # pour éviter de boucler sur un nouveau départ
        continuer = False                               # termine la boucle mainloop
        fenetre.destroy()

    ########################################################   Pour gérer de multiples instances d'AperoDeDenis

    # vérifie sous windows qu'il n'y a pas déjà un AperoDeDenis lancé !
    
    def lancementMultiple(self):
        # lancement unique d'aperodedenis sous WINDOWS : (pas trouvé d'équivalent sous Linux/Ubuntu) premier lancement seulement
        # titles = créé au départ, liste des fenetres sous windows, pour éviter de relancer l'appli si déjà lancée 
        if os.name=="nt" and compteur==1:                
            liste = [e for e in titles  if "AperoDeDenis V "in e]   # apero déjà ouvert sous WIndows ?
            nb = liste.__len__()
            if nb:
                titre="AperoDeDenis dèjà lancé !"
                if nb==1:
                    texte = _("AperoDeDenis est déjà lancé dans la fenêtre :")+"\n\n"+liste[0]+"\n\n"+\
                            _("'Lancer' pour lancer une seconde instance d'AperoDeDenis.")+"\n"+\
                            _("Dans ce cas un nouveau chantier sera ouvert.")+"\n\n"+\
                            _("Eviter de traiter le même dossier dans les 2 instances.")
                else:
                    texte = _("AperoDeDenis est déjà lancé dans les %s fenêtres :") % (nb) +"\n\n"+\
                            "\n".join(liste)+"\n\n"+\
                            _("'Lancer' pour lancer une nouvelle instance d'AperoDeDenis.")+"\n\n"+\
                            _("Eviter de traiter le même dossier dans plusieurs instances.")
                if MyDialog_OK_KO(fenetre,titre=titre,texte=texte,b1="Lancer",b2="Abandon").retour:
                    self.nouveauChantier()    
                else:
                    fin()                    

    # Ajoute le chantier en cours directement dans le fichier des paramètres généraux (ceci pour gérer de multiples  instances de AperoDeDenis)

    def ajoutChantier(self):
        sauvegarde2 = open(self.fichierParamMicmac,mode='rb')
        r2 = pickle.load(sauvegarde2)
        sauvegarde2.close()
        self.tousLesChantiers           =   r2[3]            
        if self.repTravail in self.tousLesChantiers:    # controle que le chemin n'existe pas déjà, sinon : rien
            self.encadre(_("Ajout de chantier : le chantier existe déjà."))
            return
        ajout(self.tousLesChantiers,self.repTravail)    # Ajout du chantier :
        self.sauveParamMicMac()                         # sauve les param en cours du chantier dans les param généraux (peux mieux faire ?)       

    ########################################### Conversion d'un PLY en fichier X Y Z (séparateur espace
    #@decorateTry
    def ecrireXYZ(self):
        fichierPlyPourXyz =tkinter.filedialog.askopenfilename(title=_('Fichier .PLY à convertir en XYZ : '),
                                                  filetypes=[(_("fichier ply"),("*.ply")),(_("Tous"),"*")],
                                                  multiple=False)
        self.encadre(_("Patience : lecture du fichier en cours."))
        semisDePoints = extraireLesXyzDuPly(fichierPlyPourXyz)
        if "semisDePoints" not in locals():
            self.encadre(_("Erreur sur le fichier \n %s")) % (fichierPlyPourXyz)
            return            
        if type(semisDePoints)!=type(dict()):
            self.encadre(_("Erreur sur le fichier \n %s \n  %s") % (fichierPlyPourXyz,str(semisDePoints)))
            return
        fichierXYZ   = os.path.splitext(fichierPlyPourXyz)[0]+".XYZ"    # fichier xyz
        xyz = [ " ".join((str(x),str(y),str(z))) for x,y,z in semisDePoints["lesXyz"]]   # voir la commande zip peut être utile : https://stackoverflow.com/questions/12142133/how-to-get-first-element-in-a-list-of-tuples
               
        with open (fichierXYZ,"w") as f:
            f.write ("\n".join(xyz))
        message = _("Fichier XYZ, séparateur espace \n %s \n écrit.") % (fichierXYZ)            
        self.encadre(message)
        self.ajoutLigne(message)
                                        
    ########################################### Conversion PLY en XYZ puis en MNT, MNT IGN et MNT Grass

    def ply2Mnt(self):
                
        self.toMnt("ply")

    def xyz2Mnt(self):
        self.toMnt("xyz")

    #@decorateTry   
    def toMnt(self,typeFichier):
##        
##        # cette fonction n'est pas disponible aprés cx-freese : numpy ne peut pas être chargé par cx-freeze 
##
##        if ".exe" in sys.argv[0]:
##            self.encadre(_("La construction des MNT doit être effectuée à partir du script python, impossible à partir de l'éxécutable."))
##            return
        def controleFichier():
            if len(fichierPourMnt)==0:
                return False
            typePly=False

            if not os.path.exists(fichierPourMnt):
                self.encadre(_("Ce fichier n'est pas trouvé : ")+"\n"+fichierPourMnt)
                return False
            
            if fichierPourMnt[-4:].upper() in (".ASC",".XYZ",".CSV",".TXT"):
                with open(fichierPourMnt) as f:
                    ligne = f.readline()
                    if "cols" in ligne:
                        self.encadre("\n"+_("Le fichier\n %s \nest déjà un mnt.\n\n") % (fichierPourMnt))
                        return False
                    typePly = "ASC"
                    
            elif fichierPourMnt[-4:].upper() in (".PLY"):
                typePly = typeDePly(fichierPourMnt)
                if typePly==None:                      
                    erreur = _("erreur : le fichier\n %s \nn'a pas un contenu de type ply.") % (fichierPourMnt)
                    self.encadre(erreur)
                    return False                                               # Abandon si pas fichier ply
                if typePly in ("nuage de points ascii"):
                    erreur = _("Désolé : le fichier %s \nest de type %s. \nFormat non traité dans cette version d'AperoDeDenis.\n\n"+
                               "Utiliser CloudCompare pour l'enregistrer au format mesh ascii ou nuage de point binary.") %(fichierPourMnt,typePly)
                    self.encadre(erreur)
                    return False                                               # Abandon si pas fichier ply
            else:
                erreur = _("Le fichier\n %s \nn'a pas une extension ASC, XYZ,CSV,TXT ou PLY. Abandon") % (fichierPourMnt)
                self.encadre(erreur)
                return False                                               # Abandon si pas fichier ply                
            self.ajoutLigne(heure()+_("Fichier a écrire en MNT : %s") % (fichierPourMnt))
            return typePly
        
        # Traitement
                
        # OK, on essaie :
        # demande le fichier :
        self.menageEcran()
        if typeFichier=="ply":
            extensions = ("*.ply",)
            message = _("Choisir le nuage PLY a écrire au format MNT :")

        if typeFichier=="xyz":
            extensions = ("*.asc","*.xyz","*.txt")
            message = _("Choisir le nuage XYZ a écrire au format MNT : ")
                          
        fichierPourMnt=tkinter.filedialog.askopenfilename(title=message,
                                                            initialdir=self.repTravail,
                                                            filetypes=[(_("fichier ply ou asc"),extensions),(_("Tous"),"*")],
                                                            multiple=False)
        
        typePly = controleFichier()
        if typePly==False: return
        if typePly=="nuage de points binaire":
            retour = self.ecrireMNTPlyNuage(fichierPourMnt)
        if typePly=="mesh ascii":
            retour = self.ecrireMNTPlyMesh(fichierPourMnt)
##        if typePly=="mesh binary": # a écrire pour lire des mesh binaires
##            retour = self.ecrireMNTPlyMeshBinaryMesh(fichierPourMnt)            
        if typePly=="ASC":
            retour = self.ecrireMNTPlyNuage(fichierPourMnt)
            
    ####### Ecrire un mnt
    @decorateTry
    def ecrireMNTPlyNuage(self,fichierPourMnt):
        
        def mggrille(min_x,max_x,lePas, min_y,max_y): # ne sert pas : pour remplacer mgrid de numpy, afin de se passer de numpy
            nb_x=int((max_x-min_x)/lePas)+1
            ix = range(nb_x)
            gx=[min_x+e*lePas for e in ix]
            nb_y=int((max_y-min_y)/lePas)+1
            iy = range(nb_y)
            gy=[min_y+e*lePas for e in iy]
            grid_x = [ [e]*nb_y for e in gx]
            grid_y = [gy]*nb_x
            return grid_x,grid_y


        def messageFin():

            message = "\n\n "+self.debutEcrireMnt
            if self.fichierIgnASC:
                message += "\n\n"+_("Ecriture du fichier :")+"\n"+self.fichierIgnASC
##            if self.fichierGrassASC:
##                message += "\n\n"+("Ecriture du fichier :")+"\n"+self.fichierGrassASC
                
            message += "\n\n"+_("%s Fin de l'écriture du MNT.") % (heure())
            if not self.fichierIgnASC+self.fichierGrassASC:
                message += "\n\n"+_("Pas de fichier écrit")
            self.encadre(message)
            traceMetier(message,fichierPourMnt,"MNT")            
        
        def demandeLePas(surface,nb_points): # demande la taille de la maille
            lePas = False
            texte  = _("Fichier : %s") % (fichierPourMnt)
            texte += "\n\n"+_("Indiquer la taille de la maille utilisée pour le MNT, en mètres :\n par exemple 0.5 pour une maille de 50 cm : ")
            texte += "\n\n"+_("Le nombre de points est de %s, la surface couverte est de %s m2.") % (nb_points,int(surface))
            texte += "\n\n"+_("Il y a %s points au m2.") % (round(nb_points/surface))
            texte += "\n\n"+_("Une taille de %s m correspond à 1 point du nuage par maille.") % (round((surface/nb_points)**0.5,2))

            bas = ( _("Remarque : l'unité de longueur supposée est le mètre"))
            new = MyDialog(fenetre,texte,basDePage=bas)
            if new.saisie in (False,""):
                return
            lePas = new.saisie        
            if not isNumber(lePas):
                self.encadre(_("Taille de la maille invalide : ")+str(new.saisie))
                return
            if float(lePas)<=0:
                self.encadre(_("Taille de la maille négative ou nulle : ")+str(new.saisie))
                return
            self.ajoutLigne(_("Taille de la maille : %s.") % (lePas))
            return lePas
        
        def ecrireMntGrass():
            # Ecriture entête MNT GRASS ASC (suppose mnt et tableauTexte dans le contexte et self.fichierGrassASC)
            return #abandon pour l'instant
            with open(self.fichierGrassASC,"w") as grass:
                grass.write("cols "+str(mnt["mnt"].shape[1])+"\n")
                grass.write("rows "+str(mnt["mnt"].shape[0])+"\n")
                grass.write("west "+str(round(float(mnt["min_x"]),3))+"\n")
                grass.write("south "+str(round(float(mnt["min_y"]),3))+"\n")
                grass.write("north "+str(round(float(mnt["max_x"]),3))+"\n")
                grass.write("east "+str(round(float(mnt["max_y"]),3))+"\n")
                grass.write(tableauTexte)
            self.ajoutLigne(_("Mnt Grass écrit : %s.") % (self.fichierGrassASC))
                
        def ecrireMntIgn():
            # Ecriture entête MNT GRASS ASC (suppose mnt et tableauTexte dans le contexte, self.lePas et self.fichierIgnASC)
            with open(self.fichierIgnASC,"w") as ign:
                ign.write("ncols "+str(mnt["mnt"].shape[1])+"\n")
                ign.write("nrows "+str(mnt["mnt"].shape[0])+"\n")
                ign.write("xllcorner "+str(round(float(mnt["min_y"]),3))+"\n")
                ign.write("yllcorner "+str(round(float(mnt["min_x"]),3))+"\n")
                ign.write("cellsize "+str(self.lePas)+"\n")
                ign.write("NODATA_value "+str("-9999")+"\n")
                ign.write(tableauTexte)
            self.ajoutLigne(_("Mnt IGN écrit : %s.") % (self.fichierIgnASC))

        def prealableKO():
            if not os.path.exists(fichierPourMnt):
                message=_("Pas de fichier ply ou xyz.")
                self.encadre(message)
                return True
            # Si utilisation sous cx-freeze l'importation plante 
            # pour ne pas imposer scipy à tous...       
            try:
                from scipy.interpolate import griddata      # Pour l'interpolation
                from numpy import mgrid           
            except Exception as e :
                message = (_("Cette fonction nécessite la présence du module scipy  : ")+"\nErreur : "+str(e)+"\n")
                message += (_("Si AperoDeDenis a été installé à partir du fichier msi cette fonction 'MNT' n'est pas fonctionnelle."))
                self.encadre(message)
                return True
            if not isNumber(lePas):
                message=_("Taille de la maille incorrecte : %s.") % (lePas)
                self.encadre(message)
                return True
            return False
            
        def initialisation():
            self.debutEcrireMnt=heure()
            message = "\n"+self.debutEcrireMnt+" "+_("Lancement du calcul des MNT IGN et GRASS")           
            # OK, Initialisation des variables utiles, affichage message départ du traitement
            self.lePas = float(lePas)                          
            self.fichierIgnASC   = os.path.join(os.path.dirname(fichierPourMnt),"maillage_"+str(lePas)+"_IGN_"+
                                   os.path.basename(fichierPourMnt)+".ASC")    # MNT IGN ASC
            self.fichierGrassASC = os.path.join(os.path.dirname(fichierPourMnt),"maillage_"+str(lePas)+"_GRASS_"+
                                   os.path.basename(fichierPourMnt)+".ASC")    # MNT GRASS ASC
            message = "\n"+_("Patience : procédure longue, création d'un MNT à partir du fichier : ")+"\n"+fichierPourMnt+"\n" +_("taille de la maille : ")+lePas+"\n"
            message +=" "+_("Le MNT est en cours de création.")+"\n"
            self.encadre(message) 

        def mntVersTableauTexte(mnt):   # Conversion de la grille en tableau de nombres arrondis, avec valeur de remplissage ok  :       
            tableArrondie = list()

            for uneLigne in mnt["mnt"]:    # le mailage est une liste de listes : découpe est une ligne du mnt
                ligneTexte = list()            
                for f in uneLigne:       # f est une valeur de z, on l'arrondit
                    val = round(float(f),3)
                    if val==-9999:
                        val="-9999"
                    ligneTexte.append(str(val))
                tableArrondie.insert(0," ".join(ligneTexte))
            return "\n".join(tableArrondie) # ajout des sauts de ligne

        def choixUtilisateur(taille):       # demande ce qu'il faut écrire les "gros fichiers" (plus de 50 MO)
            tailleMO = int(taille / 1000000)
            if tailleMO>=30:                #plus de 50 MO : que choisit l'utilisateur (sinon on écrit IGN et GRASS
                texte = _("La taille du fichier MNT est de %s MO.\n Voulez poursuivre le traitement ?") % tailleMO
                texte += "\n\n"+(_("Mnt au format IGN = 1,\n 0 ne rien écrire, autre réponse = formaIGN")+"\n")
                new = MyDialog(fenetre,texte)
                return new.saisie
            return 1
        

        def extraireLesXyz(fichierPourMnt):
            self.encadre(_("Lecture du fichier\n %s \nen cours.\nPatientez.") % (fichierPourMnt))
            semisDePoints = dict()
            if fichierPourMnt[-4:].upper()==".PLY":
                semisDePoints = extraireLesXyzDuPly(fichierPourMnt)
            elif fichierPourMnt[-4:].upper() in (".ASC",".XYZ",".TXT",".CSV") :
                semisDePoints = extraireLesXyzDuAsc(fichierPourMnt)
            else:
                self.encadre(_("Fichier d'extension inattendue : ni ply, xyz, txt, asc, csv :\n %s \n extension : %s") % (fichierPourMnt,fichierPourMnt[-4:].upper()))
                return
            return semisDePoints
                
######################## le traitement :

        semisDePoints = extraireLesXyz(fichierPourMnt) # récupére le semis de points x y z dans l'asc ou le ply
        if "surface" not in semisDePoints: return      
        lePas = demandeLePas(semisDePoints["surface"],semisDePoints["nb"])
        if prealableKO(): return
        initialisation()                            # variable utiles : nom des fichiers, message dé
        mnt = creerMnt(semisDePoints,self.lePas)    # création mnt numérique ; LesXYZ : dictionnaire comportant les entrées :
                                                    #  mnt : liste de tuples de la forme ((x,y),z)
                                                    #  nb,min_x, max_x, min_y, max_yn : nombre de points,  min, max..
        tableauTexte = mntVersTableauTexte(mnt)     # création tableau texte
        if choixUtilisateur(len(tableauTexte))!=1:
            return      # si gros fichier on demande à l'utilisateur ce qu'il veut en faire 
        ecrireMntIgn()                              #
        messageFin()

####################### Passage d'un maillage ply au format MNT

    def ecrireMNTPlyMesh(self,fichier):
        import numpy
        def demandeLePas(fichier): # demande la taille de la maille
            lePas = False
            texte  = _("Fichier : %s") % (fichier)
            texte += "\n\n"+_("Indiquer la taille de la maille utilisée pour le MNT, en mètres :\n par exemple 0.5 pour une maille de 50 cm : ")
            texte += "\n\n"+_("Le fichier est un maillage (mesh) qui définit une altitude en tout point du terrain.")

            bas = ( _("Remarque : l'unité de longueur supposée est le mètre"))
            new = MyDialog(fenetre,texte,basDePage=bas)
            if new.saisie in (False,""):
                return
            lePas = new.saisie        
            if not isNumber(lePas):
                self.encadre(_("Taille de la maille invalide : ")+str(new.saisie))
                return
            if float(lePas)<=0:
                self.encadre(_("Taille de la maille négative ou nulle : ")+str(new.saisie))
                return
            self.ajoutLigne(_("Taille de la maille : %s.") % (lePas))
            return lePas
        
        def lireMesh(fichier,lePas):
            mesh = dict()
            with open (fichier,"r") as f:
                lignes = f.readlines()
            for i in range(30):
                if "element vertex " in lignes[i]:
                    nbSommets = int(float(lignes[i].split()[2]))
                    mesh["nbSommets"] = nbSommets
                if "element face " in lignes[i]:
                    nbFaces = int(float(lignes[i].split()[2]))
                    mesh["nbFaces"] = nbFaces
                if "end_header" in lignes[i]:
                    debut = i+1
                    mesh["debut"] = i+1
            lesSommets = [ [float(f) for f in e.split()] for e in lignes[debut:debut+int(nbSommets)]]
            mesh["lesSommets"] = lesSommets
            mesh["lesTriangles"] = [[ int(f) for f in e.split()]for e in lignes[debut+int(nbSommets):debut+int(nbSommets+nbFaces)]]
            minX,maxX,minY,maxY = minMaxXY(lesSommets)
            mesh["iMax"] = int(1 + (maxX-minX)/lePas)
            mesh["jMax"] = int(1 + (maxY-minY)/lePas)
            mesh["minX"] = minX
            mesh["minY"] = minY
            mesh["lePas"]=lePas
            return mesh
            
        def minMaxXY(lesSommets):
            minX = min([x for x,y,z in lesSommets])
            maxX = max([x for x,y,z in lesSommets])
            minY = min([y for x,y,z in lesSommets])
            maxY = max([y for x,y,z in lesSommets])
            return float(minX),float(maxX),float(minY),float(maxY)

        def zNumpyVersTexte(z):
            tableArrondie = list()
            z = mesh["z"]
            lignes,cols = z.shape
            for i in range(lignes) :    # le mailage est une liste de listes : découpe est une ligne du mnt            
                ligneTexte = list()            
                for j in range(cols):       # f est une valeur de z, on l'arrondit
                    val = round(z[i,j],3)
                    if val==-9999:
                        val="-9999"
                    else:
                        val = str(round(z[i,j],3))
                    ligneTexte.append(val)
                tableArrondie.insert(0," ".join(ligneTexte))
            return "\n".join(tableArrondie) # ajout des sauts de ligne        

        def calculDesZ(mesh):
            # création tableau vide Numpy initialisé à -9999 :
            z=  numpy.full((mesh["jMax"],mesh["iMax"]), -9999, dtype=float)
            pool = cycle(mesh["lesTriangles"])
            t = next(pool)
            lesSommets = mesh["lesSommets"]
            minX = mesh["minX"]
            minY = mesh["minY"]
            lePas = mesh["lePas"]
            nbFaces = mesh["nbFaces"]
            jMax=mesh["jMax"]
            thermo = 40*"..........................................................................................................\n"
            thermoCoupe = thermo[:jMax]
            patience = _("procédure longue... patience...\n"+thermoCoupe)
            self.encadre(patience)
            for i in range (mesh["jMax"]):  # lignes
                for j in range (mesh["iMax"]): # colonnes
                    xij = minX+j*lePas
                    yij = minY+i*lePas
                    for e in range(nbFaces):
                        A = tuple(lesSommets[t[1]])
                        B = tuple(lesSommets[t[2]])
                        C = tuple(lesSommets[t[3]])
                        retour = pointDansTriangle(A,B,C,(xij,yij))                
                        if retour:  # calcul de la valeur du Z : raison barycentrique sur A ! 
                                    # retour = les 3 valeurs barycentriques
                            z[i,j] = A[2]*retour[0]+B[2]*retour[1]+C[2]*retour[2]
                            break
                        t = next(pool)
                thermoCoupe = thermoCoupe.replace(".","*",i)
                patience = _("procédure longue... patience...\n"+thermoCoupe)                
                self.encadre(_(patience))
            mesh["z"] = z
            
        def ecrireMntIgnMesh(fichier,mesh):
            # Ecriture entête MNT GRASS ASC (suppose mnt et tableauTexte dans le contexte, self.lePas et self.fichierIgnASC)      
            z= mesh["z"]
            ncols = str(z.shape[1])
            nrows = str(z.shape[0])
            xllcorner = str(round(mesh["minX"],3))
            yllcorner = str(round(mesh["minY"],3))
            lePas = str(mesh["lePas"])
            with open(fichier,"w") as ign:
                ign.write("ncols "+ncols+"\n")
                ign.write("nrows "+nrows+"\n")
                ign.write("xllcorner "+xllcorner+"\n")
                ign.write("yllcorner "+yllcorner+"\n")
                ign.write("cellsize "+lePas+"\n")
                ign.write("NODATA_value "+str("-9999")+"\n")
                tableau = zNumpyVersTexte(z)
                ign.write(tableau)

    ################### traitement
        lePas = float(demandeLePas(fichier))
        if not lePas:
            self.encadre(_("Abandon"))
            return
        mesh = lireMesh(fichier,lePas)
        calculDesZ(mesh)
        zNumpyVersTexte(mesh)
        fichierIgn   = os.path.join(os.path.dirname(fichier),"maillage_BaseMesh_"+str(lePas)+"_IGN_"+
                        os.path.basename(fichier)+".ASC") # MNT IGN ASC  
        ecrireMntIgnMesh(fichierIgn,mesh)
        message = _("Mnt IGN écrit à partir d'un maillage :\n %s \n taille de la maille : %s m.") % (fichierIgn,str(lePas))
        self.ajoutLigne(message)
        self.encadre(message)
        


######################################## Fin du calcul des MNT        

########################################
####### recherche dans la zone texte 201

    def find201(self,event):
        self.find201 = "un"
        self.texte201.tag_delete("search")
        self.cherche = MyDialog(self.texte201,"chaine a rechercher (sensible à la casse)").saisie
        self._search_(index=self.texte201.index(tkinter.INSERT))
        
    def suivant201(self,event):
        if self.find201 == "un":
            self.texte201.tag_delete("search")        
            self._search_(self.ending_index)
        if self.find201 == "tous":
            if self.suite201>=0:
                self.suite201 += 1         
                if self.listePositions201.__len__()<=self.suite201:
                    self.suite201 = -1
                    return
                self.texte201.tag_delete("enCours")
                self.texte201.tag_add("enCours",self.listePositions201[self.suite201][0],self.listePositions201[self.suite201][1])
                self.texte201.tag_configure("enCours", background="red", foreground="yellow")                
                self.texte201.see(self.listePositions201[self.suite201][0])            
        
    def _search_(self,index="1.0"):
        try:
            if self.cherche:
                countvar = tkinter.StringVar()
                f = self.texte201.search(self.cherche, index, count=countvar)
                self.starting_index = f         
                self.ending_index = "{}+{}c".format(self.starting_index, countvar.get())
                self.texte201.tag_add("search", self.starting_index, self.ending_index)
                self.texte201.tag_configure("search", background="skyblue", foreground="red")
                self.texte201.see(self.starting_index)
            else:
                return None
        except: pass

####### recherche TOUT dans la zone texte 201
        
    def findAll201(self,event):
        self.find201 = "tous"
        self.texte201.tag_delete("search")
        self.cherche = MyDialog(self.texte201,"chaine a rechercher").saisie
        self._search_all_(self.cherche)
        self.suite201 = 0        
        self.texte201.see(self.listePositions201[self.suite201][0])
        
    def _search_all_(self, word):
        self.listePositions201 = list()        
        index="1.0"
        if word:
            while True:
                f = self.texte201.search(word, index, stopindex=tkinter.END)
                if not f:	break
                starting_index =int(f.split(".")[0])
                ending_index  = len(word)+int(f.split(".")[1])
                coordinates = "{}.{}".format(starting_index, ending_index)
                self.texte201.tag_add("search", f, coordinates)
                self.texte201.tag_configure("search", background="skyblue", foreground="red")
                index = coordinates
                self.listePositions201.append([f,index])
            return True
        else:
            return None

####### Définition des 3 jeux de photos pour la syntaxe des commandes micmac :
#       - toutes les photos
#       - les photos pour la calibration
#       - les photos sans la calibration
    def les3JeuxDePhotos(self):
        self.jeuToutesLesPhotos = '".*('+"|".join(self.photosSansChemin)+')"'
        self.jeuToutesLesPhotos = '".*.(DS105055|DS105056|DS105057).JPG"'
        self.jeuCalibration = '"('+"|".join(self.photosCalibrationSansChemin)+')"'
        sansCalibration = [e for e in self.photosSansChemin if e not in self.photosCalibrationSansChemin]
        self.jeuSansCalibration = '"'+"|".join(sansCalibration)+'"'
        print("self.jeuToutesLesPhotos=",self.jeuToutesLesPhotos)
        print("jeuCalibration=",self.jeuCalibration)
        print("self.jeuSansCalibration=",self.jeuSansCalibration)
            
################################## FIN DE LA CLASSE INTERFACE ###########################################################
    
################################## Outils divers et outils POUR DEBUG ###########################################################

def pv(variable):       # affiche le nom de la variable, sa classe et sa valeur (pour debug uniquement)
    stack = traceback.extract_stack(limit=2)
    print('\n------------------')
    if '))' in stack[0][3]:
        nomVariable = stack[0][3].replace('pv(', '').replace('))', ')')
        typeVariable = _("fonction")
        valeurVariable = _("valeur en retour : ")
    else:
        nomVariable = stack[0][3].replace('pv(', '').replace(')', '')
        typeVariable = _("variable")
        valeurVariable = _("valeur : " )       
    print (_("Détail de la %(typeVar)s : %(nomVar)s") % {"typeVar" : typeVariable, "nomVar" : nomVariable},
           '\n', _('Identifiant : '),id(variable),
           '\n', _('Type : '),type(variable),
           '\n', _('class = '),variable.__class__,
           '\n', _('Les attributs : '),dir(variable),
           '\n\n',str(valeurVariable),str(variable))
    print('\n------------------')

def copieRepertoire(source,cible): #copie d'une arborescence de répertoire après suppression 
    retour=supprimeRepertoire(cible)
    if retour: return retour                                             
    try: shutil.copytree(source,cible)
    except Exception as e:
        interface.encadre(_("la copie a échouée : %s.") % (str(e)))
        return _("la copie a échouée : %s.") % (str(e))                                           

def supprimeFichier(fichier):
    try:    os.remove(fichier)
    except Exception as e:
        return _("Erreur suppression fichier :")+str(e)

def supprimeRepertoire(repertoire):
    if not os.path.exists(repertoire):     
        return
    try:
        shutil.rmtree(repertoire)
    except Exception as e:
        erreur = _("Erreur lors de la suppression du répertoire : %s\n%s") % (repertoire,str(e))
        print(erreur)
        return erreur
    if os.path.exists(repertoire):
        erreur=_("Erreur répertoire non supprimé : %s" % (repertoire))
        print(erreur)        
        return erreur
    
def supprimeMasque(repertoire,masque):
    for e in os.listdir(repertoire):
        if masque in e:
            supprimeFichier(e)

def blancAuNoir(p):
    if p == 255:
        return 0
    else:
        return 255

def ajout(liste,item):                                  # ajout d'un item dans une liste en s'assurant qu'il n'y a pas de doublons et avec un tri:
    if liste.__class__()==list():
        try:
            liste.append(item)
            c=list(set(liste))
            c.sort()
            liste.clear()
            for e in c:
                liste.append(e)
        except Exception as e:
            print (_("erreur ajout : "),str(e))

def supprimeArborescenceSauf(racine,sauf=list()):   # supprime toute une arborescence, sauf une liste de fichiers et répertoires sous la racine
    sauf = [os.path.basename(e) for e in sauf]      # sans chemin
    for item in os.listdir(racine):
        chemin = os.path.join(racine,item)
        if item not in sauf:    # si item est dans sauf c'est un fichier a garder sauf sion essaie 
            if os.path.isfile(chemin):
                try:
                    supprimeFichier(chemin)
                except Exception as e:
                    print(_("erreur remove = "),str(e))
            else:
                shutil.rmtree(chemin)           # on supprime tous les sous répertoires 'calculs, temporaires...)

def zipdir(path):                                                   # path = chemin complet du répertoire à archiver,
                                                                    # crée un zip qui contient tous les fichiers sauf les exports                                                                   # avec un nouveau nom de chantier = ancienNom(export)
    try:
        archive = os.path.join(path,os.path.basename(path)+".exp")  #  archive : nom du fichier dans lequel mettre l'archive 
        racine = os.path.dirname(path)                              # racine pour dezip
        zipf = zipfile.ZipFile(archive, 'w')
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if not os.path.splitext(archive)[1]==os.path.splitext(file)[1]:     # les archives ne sont pas incluses dans le zip
                    fichier = os.path.join(root, file)                              # nom complet du fichier à archiver
                    cheminDezip = fichier.partition(racine)[2]                      # nom pour le dezippage (on change le nom du répertoire de travail relatif dans le chantier
                    cheminDezip = cheminDezip.replace(interface.chantier,interface.chantier+interface.suffixeExport,1)
                    zipf.write(fichier,
                               arcname=cheminDezip,
                               compress_type=zipfile.ZIP_DEFLATED )
                    interface.encadrePlus(".")
        zipf.close()
        return os.path.getsize(archive)
    except  Exception as e:
        print(_("erreur zip = "),str(e))
        return -1
               
def afficheChemin(texte):                               # avant d'afficher un chemin on s'assure que le séparateur est bien le bon suivant l'OS
    # normcase supprimé le 26 avril 2016 : affectait les noms de fichiers en minuscule
    texte = str(texte)   
    texte = os.path.normpath(texte)
    return texte.replace(interface.separateurAutre,interface.separateurChemin)

def format2Colonnes(col1,col2,largeurCol1EnPixels): # en principe : col1 = nom du chantier, col2 = chemin du chantier
    lab=tkinter.Label(text=col1)
    long=lab.winfo_reqwidth()
    while long<largeurCol1EnPixels:
        col1=col1+" "
        lab=tkinter.Label(text=col1)
        long=lab.winfo_reqwidth() 
    return col1+" "+col2

def format3Colonnes(col1,col2,col3,largeurCol1EnPixels): # en principe : col1 = nom du chantier, col2 = taille du chantier en KO, col3 = chemin du chantier
    col2=str(col2)
    lab=tkinter.Label(text=col1)
    long=lab.winfo_reqwidth()
    while long<largeurCol1EnPixels:
        col1=col1+" "
        lab=tkinter.Label(text=col1)
        long=lab.winfo_reqwidth()
    while long<2*largeurCol1EnPixels:
        col2=" "+col2
        lab=tkinter.Label(text=col1+col2)
        long=lab.winfo_reqwidth()
    retour = str(col1)+" "+str(col2)+str(col3)
    return retour

def verifMm3d(mm3D):            # Il faudrait que la version de MicMac autorise la saisie de masque en 3D, sinon ancienne version, susceptible de donner des erreurs.
    if os.path.exists(mm3D)==False: return False
    try:
        helpMm3d = subprocess.check_output([mm3D,"-help"],universal_newlines=True)
    except Exception as e:
        return False
    if "SaisieMasqQT" in helpMm3d: return True
    else: return False

def mercurialMm3d(mm3D):            # Il faudrait que la version de MicMac autorise la saisie de masque en 3D, sinon ancienne version, susceptible de donner des erreurs.
    if os.path.exists(mm3D)==False: return False
    try:
        mercurialMm3d = subprocess.check_output([mm3D,"CheckDependencies"],universal_newlines=True)
    except Exception as e:
        return _("pas de version identifiée de MicMac")
    else: return mercurialMm3d.splitlines()[0]

def orientationOK():
    return os.path.isdir("Ori-Arbitrary")

def orientationKO():
    return not orientationOK()

def verifierSiExecutable(exe):
    try:
        subprocess.check_call(exe)
        return True
    except Exception as e:
        try:
            subprocess.check_call([exe,"-h"])
            return True
        except Exception as f:
            return False
    
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def fenetreIcone(fenetre=""):       # Icone au format GIF pour être géré par tkinter sans utiliser Pillow
    if fenetre=="":
         return
    fenetre.tk.call('wm', 'iconphoto', fenetre._w, dataIcone)

def sizeDirectoryMO(path):  
    size = 0  
    for root, dirs, files in os.walk(path):  
        for fic in files:  
            size += os.path.getsize(os.path.join(root, fic)) 
    return round(size/1000000)

def ouvrirPageWEBAperoDeDenis():
    webbrowser.open("https://github.com/micmacIGN/InterfaceCEREMA/tree/master/InterfaceCEREMA")  

def lireReadMe():
    webbrowser.open("https://raw.githubusercontent.com/micmacIGN/InterfaceCEREMA/master/InterfaceCEREMA/readme.txt")  


def ouvreInterfaceCeremaGItHub():
    threading.Thread(target=ouvrirPageWEBAperoDeDenis).start()  # ouverture de la page WEB dans un thread (join=0 pour désynchroniser si besoin)

def ouvreReadMeGitHub():
    threading.Thread(target=lireReadMe).start()  # ouverture de la page WEB dans un thread                                       

def oschdir(rep):
    if rep==os.getcwd():
        return
    if os.path.isdir(rep):
        os.chdir(rep)
    else:
        texte = _("Répertoire non trouvé : %s .") % (rep)
        #*tkinter.messagebox.showwarning("AperoDeDenis : Avertissement",texte)

def isNumber(s):       # https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    try:
        float(s)
        return True
    except:
        return False

##### Quelques outils pour : manipuler les ply et les XYZ, créer un MNT :
    # format d'échange commun : LesXYZ : liste de tuples de float de la forme (x,y,z)
    # lesXYZ est ancapsulé dans un dictionnaire qui comporte aussi des métadonnées.
    # 0) détermine le type de ply : mesh ou nuage, binary ou ascii
    # 1) extraireLesXyzDuPly,  : décode les fichiers PLY en mode binaire
    # 2) lireFichierXYZ 
    # 3) creerMnt : appel de la fonction scipy mgrid qui construit le maillage

@decorateTry
def typeDePly(fichier):              # retour :
    nbFaces = 0
    with open (fichier,"r",encoding="latin-1") as f:
        lignes = f.readlines(1000)
    if lignes[0][:3]!="ply":
        return _("%s \nn'est pas un fichier ply") % (fichier)
    for i in range(min(20,lignes.__len__())):
        if "ascii" in lignes[i]:
            format = "ascii"
        if "binary" in lignes[i]:
            format = "binary"            
        if "element vertex " in lignes[i]:
            nbSommets = int(float(lignes[i].split()[2]))
        if "element face " in lignes[i]:
            nbFaces = int(float(lignes[i].split()[2]))
        if "end_header" in lignes[i]:
            debut = i+1

    if format=="binary" and nbFaces==0:
        return ("nuage de points binaire")  #_("nuage de points binaire") serait mieux mais pas traité plus loin
    if format=="binary" and nbFaces==0:
        return ("nuage de points ascii")
    if format=="ascii" and nbFaces>0:
        return ("mesh ascii")
    if format=="binary" and nbFaces>0:
        return ("mesh binary")
@decorateTry  
def extraireLesXyzDuPly(fichierPly):    # retour : lesXyz ou False : LesXYZ : liste de float de la forme (x,y,z)  
    endian = "@"                                                    # valeur par défaut : endian du système
    fmt = str()                                                     # format de codage des données dans le ply ce format est utilisé par struct
    i = int()
    taille = int(os.path.getsize(fichierPly)/1000000)
    
    if taille>=50:
        if not tkinter.messagebox.askokcancel(
                    _("Gros fichier, traitement long.Continuer ?"),
                    _("Le fichier\n%s\nest gros, le traitement sera LONG... : %s MO.\nFaut-il continuer ?") % (fichierPly,int(taille))
                    ):
            erreur = _("Fichier trop gros : %s MO. Arrêt par l'utilisateur.") % (int(taille))
            interface.encadre(erreur)
            return erreur        
                                                              
    with open(fichierPly, 'rb') as infile:                          # lecture du fichier en mode "binaire"
        ligne = infile.read()

    lignes = ligne.splitlines()                                     # coupure du flux binaire en "lignes"
    if lignes[0]!=b'ply':                                           # vérification que le tag "ply" est présent en entête de fichier
        erreur = "erreur : le fichier\n"+fichierPly+"\nn'est pas un fichier de type ply."
        return erreur                                               # Abandon si pas fichier ply

    if b"ascii" in lignes[1]:                                        # pas prévu pour lire les fichiers ply "ASCII" choisir binary lors de l'écriture
        erreur = _("erreur : le fichier\n%s\nest un fichier de type ply au format ASCII.\nUtiliser CloudCompare pour l'enregister au format Binary.") %(fichierPly)
        return erreur

    nombre_faces = 0    # si absent ! correction version 5.111
    nombre_points = 0   # si absent ! correction version 5.111

    for e in lignes:                                                # décodage des lignes d'entête qui indique la structure du fichier
        i+=1
        if e==b'end_header':
            break                                                   # tag de fin d'entête on connait la structure, fin du décodage de la structure
        s=str(e)             
        if "little_endian" in s:                                    # boutisme
            endian="<"
        if "big_endian" in s:
            endian=">"
        if "element vertex" in s:                                   # nombre de points
            nombre_points = int(s.split(" ")[-1][0:-1])
        if "element face" in s:                                     # nombre de faces, cela termine la lecture : on ignore les faces
            nombre_faces = int(s.split(" ")[-1][0:-1])
            break
        if "property" in s:                                         # property : liste les éléments de la structure des données pour chaque point
            cType = s.split(" ")[1]
            if cType=="float":                                      # Micmac n'utilise que les valeurs float et uchar pour les nuages
               fmt += "f"                                           # indique qu'il y a un float à lire
            elif cType=="uchar":
               fmt += "B"                                           # indique qu'il y a un octet à lire
            elif cType=="char":
               fmt += "c"                                           # indique qu'il y a un octet à lire
            elif cType=="short":
               fmt += "h"                                           # indique qu'il y a deux octet à lire 
            elif cType=="ushort":
               fmt += "H"                                           # indique qu'il y a deux octet à lire
            elif cType=="int":
               fmt += "i"                                           # indique qu'il y a 4 octet à lire 
            elif cType=="uint":
               fmt += "I"                                           # indique qu'il y a 4 octet à lire
            elif cType=="double":
               fmt += "d"                                           # indique qu'il y a 8 octet à lire                              
            elif cType!="list":                                     # la valeur list est aussi utilisée, s'il s'agit d'une autre valeur : abandon
                erreur=(_("format de donnée non prévu pour les ply issus de micmac, abandon : ")+cType)
                return erreur

    fmt = endian+fmt                                                # le format est complété par le boutisme
    debutData = ligne.find(b"end_header",0,1000)+11                 # on extrait la zone des données utiles dans la varible "ligne" : début = aprés l'entête
    longueurData = nombre_points*struct.calcsize(fmt)               # on prend juste la longueur nécessaire (nombre de point * longueur des données du point)
    finData = debutData + longueurData
    plageData = ligne[debutData:finData]
    
    # extraction des Y,X,Z du ply :
    valeur=tuple([e for e in fmt])
    try:
        # list comprehension extrayant les xyz de la structure décodée :  (X,Y,Z
        lesXyz = [(valeur[1],valeur[0],valeur[2]) for [*valeur] in struct.iter_unpack(fmt,plageData).__iter__() ]

        mnt = dict()
        mnt["min_x"]  = min([x for x,y,z in lesXyz])     # bornes
        mnt["max_x"]  = max([x for x,y,z in lesXyz])
        mnt["min_y"]  = min([y for x,y,z in lesXyz])
        mnt["max_y"]  = max([y for x,y,z in lesXyz])
        mnt["nb"]     = len(lesXyz)
        mnt["lesXyz"] = lesXyz
        mnt["surface"]= (mnt["max_x"]-mnt["min_x"])*(mnt["max_y"]-mnt["min_y"])

# ajout pour infos :

        lesZ = [z for x,y,z in lesXyz]
        mnt["min_z"]  = min(lesZ)
        mnt["max_z"]  = max(lesZ)
        mnt["volume"] = mnt["surface"]*(mnt["max_z"]-mnt["min_z"])
    except Exception as e:
        print( _("Erreur lors du décodage des données du fichier Ply, le ply ne provient pas de micmac. Erreur = ")+str(e))
        return False

    # extraction des triangles
    fmtTriangles = endian+"BIII" # un entier pour pour le nombre de points (=3 pour un triangle) et 2 long pour les numéros des sommets du triangle
    finTriangles = finData + nombre_faces * struct.calcsize(fmtTriangles)
    plageDataTriangles = ligne[finData:finTriangles]
    valeur = tuple([e for e in fmtTriangles])
       # pour extraire les triangles
    try:       
        lesTriangles = [(valeur[1],valeur[2],valeur[3]) for [*valeur] in struct.iter_unpack(fmtTriangles,plageDataTriangles).__iter__() ]
    except Exception as e:
        print( _("Erreur lors du décodage des triangles du fichier Ply, le ply ne provient pas de micmac. Erreur = ")+str(e))
        return False
    mnt["lesTriangles"] = lesTriangles    
    return mnt

def extraireLesXyzDuAsc(fichierASC):# fichier texte semis de points 3D comportant sur chaque ligne X Y Z
                                    # séparateur de champ recherché : espace ou ; ou virgule
                                    # séparateur décimal recherché : . ou ,
                                    # si # en tête de ligne = commentaire, éventuellement rvb derrière (ignoré)
                                    # retourne : LesXYZ : liste de tuples de float de la forme ((x,y),z)
    def rechercheSeparateur(ligne):
        separateurDecimal = ","
        separateurDeChamp = str()
        if ligne.count(".") and not ligne.count(","):
            separateurDecimal = "."
        elif ligne.count(","):
            separateurDecimal = ","
        if ligne.count(" "):
            separateurDeChamp = " "
        elif ligne.count(";"):
            separateurDeChamp = ";"
        elif ligne.count("\t"):
            separateurDeChamp = "\t"
        elif ligne.count(","):
            separateurDeChamp = ","
            separateurDecimal = "."
        return separateurDecimal,separateurDeChamp

    ##### Début traitement
                          
    lesXyz = list()
    if not os.path.exists(fichierASC):
        self.message=_("Pas de fichier XYZ.")
        return False
    with open (fichierASC) as asc:
        xyz = asc.readlines()
        separateurDecimal,separateurDeChamp = rechercheSeparateur(xyz[-3])   # -2 mieux que 1 qui peut être spéciale, si pas 3 ligne, dommage
        if separateurDecimal==separateurDeChamp:
            message = _("Format de fichier incorrect : le fichier doit comporter las valeur X,Y et Z sur chaque ligne : \n"+ligne)
            self.encadre(message)
            return False
        if separateurDecimal==",":      # remise du point comme séparateur décimal
            xyz = [ligne.replace(",",".") for ligne in xyz]
        # OK
        for ligne in xyz:
            if ligne[0]=="#": continue      # commentaire possible
            ligneXyz = ligne.split(separateurDeChamp)[:3]
            if len(ligneXyz)<3: continue    # moins de 3 valeurs
            try:
                point = (float(ligneXyz[1]),float(ligneXyz[0]),float(ligneXyz[2])) # pour tromper l'ennemi : transposition y,x
                lesXyz.append(point)
            except Exception as e:
                erreur = (" erreur ligne"+ligneXyz+" : "+str(e))
                return erreur
    if not lesXyz: return _("erreur dans la lecture du fichier")
    mnt = dict()    
    mnt["min_x"]  = min([x for x,y,z in lesXyz])     # bornes
    mnt["max_x"]  = max([x for x,y,z in lesXyz])
    mnt["min_y"]  = min([y for x,y,z in lesXyz])
    mnt["max_y"]  = max([y for x,y,z in lesXyz])
    mnt["nb"]     = len(lesXyz)
    mnt["lesXyz"] = lesXyz
    mnt["surface"]= (mnt["max_x"]-mnt["min_x"])*(mnt["max_y"]-mnt["min_y"])
    return mnt

    
def creerMnt(semisDePoints,lePas): # méthode linéaire, remplissage -9999 ; LesXYZ : liste de tuples de la forme ((x,y),z)
    from scipy.interpolate import griddata      # Pour l'interpolesXyzlation
    from numpy import mgrid     
    # création de la grille régulière : générer un maillage avec un pas régulier,
    # au format grid de numpy les couples (x,y) sont éclatés en 2 listes [x] et [y]
    
    ################ ATTENTION : si les valeurs de x ou y sont trop grandes alors la précision du résultat est faible (voir pb mauchassat mnt TN1 471 687)
    # il faut donc tranlater les valeurs pour améliorer la précision : on limite localement à 4 chiffres au dessus de la virgule, sans toucher au mnt initial
    deltaX = round(semisDePoints["max_x"],-4)
    deltaY = round(semisDePoints["max_y"],-4)
    minX = round(semisDePoints["min_x"],4)-deltaX
    maxX = round(semisDePoints["max_x"],4)-deltaX
    minY = round(semisDePoints["min_y"],4)-deltaY
    maxY = round(semisDePoints["max_y"],4)-deltaY
    
    #################
    
    grid_x, grid_y = mgrid[minX:maxX+lePas:lePas, #constitue la grille demandée de minx, miny à maxX,maxY, au pas de lePas
                           minY:maxY+lePas:lePas]
    
    grid  = griddata( [(x-deltaX,y-deltaY) for x,y,z in semisDePoints["lesXyz"]],
                      [z  for x,y,z in semisDePoints["lesXyz"]],
                      (grid_x, grid_y),
                      method='linear',          # alternative : nearest ou linear ou cubic mais nearest ne fonctionne pas !!!!
                      fill_value="-9999")
                      
    semisDePoints["mnt"]=grid
    return semisDePoints
##Pour insérer une image, ou un logo, dans un script, utilisable ensuite par Tkinter :
##1) Convertir l'image au format GIF (sinon il faudra utiliser PIL) voir (les images dans http://tkinter.fdex.eu/doc/sa.html#images)
##2) Convertir le binaire GIF en texte encodé en 64 bits par le bout de code suivant :
##3) Copier le contenu du fichier sauf le 'b' initial dans le script et l'affecter à une variable :
##monGif = 'RRARAFVA....'
##4) Transformer cette chaine en objet image utilisable par tkinter par PhotoImage  avec l'option data :
##   imageLogo = tk.PhotoImage(data=logoCerema)
##5) Utiliser cet objet dans une commande Tkinter, par exemple :
##imgTk_id = canvasLogo.create_image(0,0,image = imageLogo,anchor="nw") 
##(le passage par une variable imageLogo est obligatoire)

def gif2txt(fichier):
    with open(fichier, 'rb') as image_file: 
        encoded_string = base64.b64encode(image_file.read())
        with open(os.path.basename(fichier)+'.txt', 'w') as image_txt: 
             image_txt.write(str(encoded_string))

##################################### Calcul du volume entre 2 MNT

def infoVolume():
    avertissement  = _("Avertissement sur les calculs de volume entre 2 MNT :")+"\n\n"
    avertissement += _("Les MNT sont obtenus à partir des nuages de points PLY ou XYZ par 2 items du menu Outils_métier.")+"\n\n"
    avertissement += _("Les fichiers PLY ou XYZ sont des semis de points 3D irréguliers.")+"\n"
    avertissement += _("Le MNT enregistre les valeurs d'altitude suivant une grille 2D carrée régulière, par exemple un point tous les 50 cm.")+"\n"
    avertissement += _("La taille de la maille est un paramètre crucial pour un MNT : elle conditionne sa précision spatiale.")+"\n"
    avertissement += _("La taille de la maille doit être évaluée suivant la densité de points du fichier origine (PLY ou XYZ).")+"\n"
    avertissement += _("Une trop petite maille ne pourra améliorer la précision initiale du PLY ou du XYZ.")+"\n\n"
    avertissement += _("Le calcul du volume entre 2 MNT ne s'effectuera (dans cette version) que si les tailles des mailles sont identiques.")+"\n"               
    avertissement += _("Si les mailles sont identiques l'outil recherche la zone de recouvrement des 2 MNT.")+"\n"
    avertissement += _("Les 2 grilles sont alors ajustées et le calcul se fait pour les mailles ayant une valeur dans chaque MNT.")+"\n"
    avertissement += _("Un paramètre de 'tolerance' permet d'ignorer les écarts trop faibles, inférieurs à cette tolérance, dans l'épaisseur du trait.")+"\n\n"
    avertissement += _("Un nuage de points 3D des écarts est produit, au format XYZ : un item du menu permet de le visualiser dans Cloud Compare.")+"\n\n"
    avertissement += _("Remarques :")+"\n"    
    avertissement += " "+_("- Ces fonctions 'métiers' sont indépendantes de l'utilisation de l'outil MicMac")+"\n"    
    avertissement += " "+_("- lorsque AperoDeDenis est installé sous windows  par l'installateur AperoDeDenis.msi la création des MNT n'est pas opérationnelle.")+"\n"    
    interface.encadre(avertissement)    

@decorateTry
def calculVolumeMnt():
    interface.menageEcran()
    fond = tkinter.filedialog.askopenfilename( initialdir="",                                                 
                                                filetypes=[(_("asc"),"*maillage*.asc"),(_("Tous"),"*")],
                                                multiple=False,
                                                title = _("Calcul du volume d'un MNT"))
    if fond==str():
        interface.encadre(_("Calcul de volume abandonné."))
        return

    infoMnt = dict()
    erreur = str()
    infoMnt["fichierFond"]=fond
    infoMnt["avertissement"]=list()
    arrondi = interface.arrondi

    with open (fond) as p:
        try:
            l6 = [next(p) for x in range(6)]
        except Exception as e:
            erreur = _("erreur : le fichier %s n'est pas un MNT") % (fond) +str(e)

    if "cols" in l6[0]: 
        infoMnt["colsFond"] = int(l6[0].split()[1])
    else:
        erreur += "cols fond incorrecte"
        
    if "nrows" in l6[1]: 
        infoMnt["nrowsFond"] = int(l6[1].split()[1])
    else:
        erreur += "nrows fond incorrecte"            
    
    if "xllcorner" in l6[2]:    # ll = lower left
        infoMnt["xllcornerFond"] = round(float(l6[2].split()[1]),arrondi)
    else:
        erreur += "xllcorner fond incorrecte"            

    
    # anomalie possible : valeur négative :

    if infoMnt["xllcornerFond"]<0:
        infoMnt["avertissement"].append(_("xllcornerFond est négatif"))
    
    if "yllcorner" in l6[3]: 
        infoMnt["yllcornerFond"] = round(float(l6[3].split()[1]),arrondi)
    else:
        erreur += "yllcorner fond incorrecte"
        
    # anomalie possible : valeur négative :

    if infoMnt["yllcornerFond"]<0:
        infoMnt["avertissement"].append(_("yllcornerFond est négatif"))
              
    if "cellsize" in l6[4]:
        sizF = float(l6[4].split()[1])
        infoMnt["cellsizeFond"] = sizF
    else:
        erreur += "cellsize fond incorrecte"
        
    if "NODATA_value" in l6[5]: 
        infoMnt["remplissage"] = l6[5].split()[1]
    else:
        erreur += "NODATA_value fond incorrecte"

    if erreur:
        interface.encadre(erreur)
        return 
                                                          
    with open (fond) as p:
        lignes=p.readlines()
        
    tableFond = list()
    for ligne in lignes[6:]:
        tableFond.append(ligne.split())

    # reherche mini et maxi du Mnt :
    mini  = 99999999
    maxi = -mini
    for i in range(infoMnt["colsFond"]):       
        for j in range(infoMnt["nrowsFond"]):        
            val = tableFond[j][i]          
            if val!=infoMnt["remplissage"]:
                mini = min(mini,float(val))
                maxi = max(maxi,float(val))

    ######### demande la cote de base

    coteDeBase = MyDialog(fenetre,_("Altitude Z de base"),
                    basDePage=_("Le calcul du volume de fera par rapport à une altitude Z 'de base'.")+"\n"+
                    _("Le Z mini du MNT est %s m. Le Z maxi du Mnt est %s m.") % (round(mini,arrondi),round(maxi,arrondi))+"\n\n"+
                    _("Indiquer la valeur de l'altitude servant de plancher au calcul du volume, zéro par défaut :")+"\n"                             
                    ).saisie
    print("coteDeBase=",coteDeBase)
    if coteDeBase == False:
        interface.encadre(_("Abandon."))        
        return
    if coteDeBase == "":
        coteDeBase = 0
    if not isNumber(coteDeBase):
        interface.encadre(_("Valeur non numérique : %s. abandon.") % (coteDeBase))
        return        
    coteDeBase = float(coteDeBase)           
    ######### somme des valeurs du fond sur l'emprise :
    
    nbRemplissageFond = 0
    nbValFond = 0
    sommeFond = 0

    infoMnt["xurcornerFond"]   = round(infoMnt["xllcornerFond"] + (infoMnt["cellsizeFond"]*(infoMnt["colsFond"]-1)),arrondi)
    infoMnt["yurcornerFond"]   = round(infoMnt["yllcornerFond"] + (infoMnt["cellsizeFond"]*(infoMnt["nrowsFond"]-1)),arrondi)
    infoMnt["Emprise fond"] = (( infoMnt["xllcornerFond"], infoMnt["xurcornerFond"]) ,( infoMnt["yllcornerFond"], infoMnt["yurcornerFond"]) )           

    for i in range(infoMnt["colsFond"]):       
        for j in range(infoMnt["nrowsFond"]):
            val = tableFond[j][i]          
            if val==infoMnt["remplissage"]:
                nbRemplissageFond += 1
            else:
                val = float(val) - coteDeBase
                sommeFond += val
                nbValFond += 1

    infoMnt["nbRemplissageFond"]=nbRemplissageFond
    infoMnt["sommeFond"]=round(sommeFond,arrondi)
    infoMnt["nbValFond"]=nbValFond
    infoMnt["moyenneFond"] = -9999
    if nbValFond: infoMnt["moyenneFond"]=round(sommeFond/nbValFond,arrondi)
    infoMnt["surfaceCouverteFond"]=round(nbValFond*infoMnt["cellsizeFond"]**2,arrondi)
    infoMnt["volumeFond"] = round(infoMnt["sommeFond"]*infoMnt["cellsizeFond"]**2,arrondi)

    rapport  = _("Calcul du volume d'un MNT : rapport final.")+"\n\n"
    rapport += _("Mnt      :\n %s") % (infoMnt["fichierFond"])+"\n\n"
    empfond=str(infoMnt['Emprise fond'])
    rapport += _("Emprise : %s m2" % empfond)+"\n"
    rapport += _("Surface utile : %s m2") % (infoMnt["surfaceCouverteFond"]  )  +"\n\n"                                       
    rapport += _("Volume entre le MNT et la cote de base %s m : %s m2") % (coteDeBase,infoMnt["volumeFond"])  +"\n\n"
    rapport += _("Remarque : l'unité de mesure du MNT est présumée être le mètre.")  +"\n"

    
    print("rapport=",rapport)
    interface.encadre(rapport)
    traceMetier(rapport,fond,'volume')

def calculVolumeEntre2Mnt():
    def lectureInfoFichiers(fond,dessus):
        
        def controleCompatibles(fond,dessus):
            infoMnt = dict()
            erreur = str()
            infoMnt["fichierFond"]=fond
            infoMnt["fichierDessus"]=dessus
            infoMnt["avertissement"]=list()

            with open (fond) as p:
                try:
                    l6 = [next(p) for x in range(6)]
                except Exception as e:
                    return "erreur : "+str(e)

            if "cols" in l6[0]: 
                infoMnt["colsFond"] = float(l6[0].split()[1])
            else:
                erreur += "cols fond incorrecte"
                return erreur
                
            if "nrows" in l6[1]: 
                infoMnt["nrowsFond"] = float(l6[1].split()[1])
            else:
                erreur += "nrows fond incorrecte"            
                return erreur
            
            if "xllcorner" in l6[2]:    # ll = lower left
                infoMnt["xllcornerFond"] = round(float(l6[2].split()[1]),arrondi)
            else:
                erreur += "xllcorner fond incorrecte"            
                return erreur
            
            # anomalie possible : valeur négative :

            if infoMnt["xllcornerFond"]<0:
                infoMnt["avertissement"].append(_("xllcornerFond est négatif"))
            
            if "yllcorner" in l6[3]: 
                infoMnt["yllcornerFond"] = round(float(l6[3].split()[1]),arrondi)
            else:
                erreur += "yllcorner fond incorrecte"
                
            # anomalie possible : valeur négative :

            if infoMnt["yllcornerFond"]<0:
                infoMnt["avertissement"].append(_("yllcornerFond est négatif"))
                      
            if "cellsize" in l6[4]:
                sizF = float(l6[4].split()[1])
                infoMnt["cellsizeFond"] = sizF
            else:
                erreur += "cellsize fond incorrecte" 

            # Enfin on arrondit les valeurs des xll et yll à un multiple de la taille de la cellule :
            # les 2 MNT seront "raccords" s'il ont la même taille de cellule
            # petit pb : le résultat est un flottant, pas un décimal...

            infoMnt["xllcornerFond"] = round(round(infoMnt["xllcornerFond"]/infoMnt["cellsizeFond"])*infoMnt["cellsizeFond"],arrondi)
            infoMnt["yllcornerFond"] = round(round(infoMnt["yllcornerFond"]/infoMnt["cellsizeFond"])*infoMnt["cellsizeFond"],arrondi)
                       
            if "NODATA_value" in l6[5]: 
                infoMnt["NODATA_valueFond"] = l6[5].split()[1]
            else:
                erreur += "NODATA_value fond incorrecte"             
                

            ############# dessus
            
            with open (dessus) as p:
                try:
                    l6 = [next(p) for x in range(6)]
                except Exception as e:
                    return "erreur : "+str(e)
                
            if "cols" in l6[0]: 
                infoMnt["colsDessus"] = float(l6[0].split()[1])
            else:
                erreur += _("cols dessus incorrecte : %s") %(l6[0])                        
                return erreur
            
            if "nrows" in l6[1]: 
                infoMnt["nrowsDessus"] = float(l6[1].split()[1])
            else:
                infoMnt["nrowsDessus"] = -9999
                erreur += _("nrows dessus incorrecte : %s") % (l6[1])                                
                return erreur               
            
            if "xllcorner" in l6[2]: 
                infoMnt["xllcornerDessus"] = round(float(l6[2].split()[1]),arrondi)
            else:
                infoMnt["xllcornerDessus"] = -9999
                erreur += "xllcorner dessus incorrecte"                                     
                return erreur
            
            # anomalie possible : valeur négative :

            if infoMnt["xllcornerDessus"]<0:
                infoMnt["avertissement"].append(_("xllcornerDessus est négatif"))
                
            if "yllcorner" in l6[3]: 
                infoMnt["yllcornerDessus"] = round(float(l6[3].split()[1]),arrondi)
            else:
                infoMnt["yllcornerDessus"] = -9999
                erreur += "yllcorner dessus incorrecte"
                return erreur

            # anomalie possible : valeur négative :

            if infoMnt["yllcornerDessus"]<0:
                infoMnt["avertissement"].append(_("yllcornerDessus est négatif"))

                
            if "cellsize" in l6[4]:
                sizD = float(l6[4].split()[1])
                infoMnt["cellsizeDessus"] = sizD
            else:
                erreur += "cellsize dessus incorrecte"
                return erreur

            # les tailles des 2 mailles doivent être égales :

            if infoMnt["cellsizeDessus"]!= infoMnt["cellsizeFond"]:
                erreur += _("Les tailles des mailles des MNT sont différentes : %s et %s. Abandon") % (infoMnt["cellsizeFond"],infoMnt["cellsizeDessus"])
                return erreur                

            # Enfin on arrondit les valeurs des xll et yll à un multiple de la taille de la cellule :
            # les 2 MNT seront "raccords" s'il ont la même taille de cellule
            # petit pb : le résultat est un flottant, pas un décimal...

            infoMnt["xllcornerDessus"] = round(round(infoMnt["xllcornerDessus"]/infoMnt["cellsizeDessus"])*infoMnt["cellsizeDessus"],arrondi)
            infoMnt["yllcornerDessus"] = round(round(infoMnt["yllcornerDessus"]/infoMnt["cellsizeDessus"])*infoMnt["cellsizeDessus"],arrondi)

            if "NODATA_value" in l6[5]: 
                infoMnt["NODATA_valueDessus"] = l6[5].split()[1]
            else:
                erreur += "NODATA_value dessus incorrecte"
                   
            if erreur: return erreur        
            
            ####### Controle cohérence :

            if infoMnt["NODATA_valueDessus"]!=infoMnt["NODATA_valueFond"]:
                erreur += "nodata_value incohérentes"

            if infoMnt["cellsizeDessus"]-infoMnt["cellsizeFond"]!=0:        # ce n'est pas un vrai problème mais un avertissement
                infoMnt["avertissement"].append(["cellsize incohérentes",]) # dans ce cas pas de calcul de volume entre les couches
            
            ####### Controle intersection xy

            # examen des valeurs : il se peut qu'une des valeurs soit conforme au référentiel (en millions de mètres)
            # et que l'autre soit tronquée des chiffres les plus significatifs ; auquel cas il faut réagir

            # différence sur les X : la différence doit être < 10000 (on est en mètres)
            # le delta appliqué est la valeur arrondie à 10000 de deltaX dessus - fond : ajouter  au Fond pour rétablir les valeurs homogène

            # Contrainte : il faut que les valeurs des ooordonnées restent positives
            # effectuer la translation pour avoir des référentiels cohérents : ajout de delta aux coordonnées du desssus ou du fond

            # sur les X :

            deltaX = round(infoMnt["xllcornerFond"] - infoMnt["xllcornerDessus"],-4)
            if deltaX>=0:
                infoMnt["xllcornerDessus"] += deltaX
            else:
                infoMnt["xllcornerFond"] -= deltaX

            # sur les Y :
            deltaY = round(infoMnt["yllcornerFond"] - infoMnt["yllcornerDessus"],-4)
            if deltaY>=0:
                infoMnt["yllcornerDessus"] += deltaY
            else:
                infoMnt["yllcornerFond"] -= deltaY

            # le delta de fond vers dessus est bien celui ci, mais la transforamtion est une addition pour remettre le référentiel correct

            infoMnt["deltaXYFondVersDessus"] = (deltaX,deltaY)

            # coin haut droit fond : upper right

            infoMnt["xurcornerFond"]   = round(infoMnt["xllcornerFond"] + (infoMnt["cellsizeFond"]*(infoMnt["colsFond"]-1)),arrondi)
            infoMnt["yurcornerFond"]   = round(infoMnt["yllcornerFond"] + (infoMnt["cellsizeFond"]*(infoMnt["nrowsFond"]-1)),arrondi)

            infoMnt["xurcornerDessus"] = round(infoMnt["xllcornerDessus"] + (infoMnt["cellsizeDessus"]*(infoMnt["colsDessus"]-1)),arrondi)
            infoMnt["yurcornerDessus"] = round(infoMnt["yllcornerDessus"] + (infoMnt["cellsizeDessus"]*(infoMnt["nrowsDessus"]-1)),arrondi)

            # Zone de recouvrement : max des min, min des max

            xrecouvreInf = round(max(infoMnt["xllcornerFond"],infoMnt["xllcornerDessus"]),arrondi)
            xrecouvreSup = round(min(infoMnt["xurcornerFond"],infoMnt["xurcornerDessus"]),arrondi)
            yrecouvreInf = round(max(infoMnt["yllcornerFond"],infoMnt["yllcornerDessus"]),arrondi)
            yrecouvreSup = round(min(infoMnt["yurcornerFond"],infoMnt["yurcornerDessus"]),arrondi)
            
            infoMnt["xrecouvreInf"] = xrecouvreInf
            infoMnt["xrecouvreSup"] = xrecouvreSup
            infoMnt["yrecouvreInf"] = yrecouvreInf
            infoMnt["yrecouvreSup"] = yrecouvreSup        

    
            infoMnt["Emprise fond"] = (( infoMnt["xllcornerFond"], infoMnt["xurcornerFond"]) ,( infoMnt["yllcornerFond"], infoMnt["yurcornerFond"]) )           
            infoMnt["Emprise dessus"] = (( infoMnt["xllcornerDessus"], infoMnt["xurcornerDessus"]) ,( infoMnt["yllcornerDessus"], infoMnt["yurcornerDessus"]) )           
            infoMnt["Emprise recouvrement"] = ((xrecouvreInf,xrecouvreSup ),(yrecouvreInf,yrecouvreSup))
            if (xrecouvreSup-xrecouvreInf )<= 0 or (yrecouvreSup-yrecouvreInf) <=0 :
                erreur = _("Les 2 MNT ne se recouvrent pas !")
                return erreur
            infoMnt["Surface recouvrement"] = round((xrecouvreSup-xrecouvreInf )*(yrecouvreSup-yrecouvreInf),arrondi)
            # indices i,j du fond pour la zone de recouvrement :

            infoMnt["iminFond"] = int((xrecouvreInf-infoMnt["xllcornerFond"])/sizF)
            infoMnt["imaxFond"] = int((xrecouvreSup-infoMnt["xllcornerFond"])/sizF)
            infoMnt["jminFond"] = (infoMnt["nrowsFond"]-1)-int((yrecouvreSup-infoMnt["yllcornerFond"])/sizF)   # -1 : les tableaux commencent à zéro/ nb de colonne qui commence à 1        
            infoMnt["jmaxFond"] = (infoMnt["nrowsFond"]-1)-int((yrecouvreInf-infoMnt["yllcornerFond"])/sizF)          

            # limité à l'emprise
            
            infoMnt["iminFond"] = int(max(0,infoMnt["iminFond"]))
            infoMnt["imaxFond"] = int(min((infoMnt["colsFond"]-1),infoMnt["imaxFond"]))
            infoMnt["jminFond"] = int(max(0,infoMnt["jminFond"]))
            infoMnt["jmaxFond"] = int(min((infoMnt["nrowsFond"]-1),infoMnt["jmaxFond"]))

            # indices i,j du dessus pour la zone de recouvrement :
            
            infoMnt["iminDessus"] = int((xrecouvreInf-infoMnt["xllcornerDessus"])/sizD)
            infoMnt["imaxDessus"] = int((xrecouvreSup-infoMnt["xllcornerDessus"])/sizD)
            infoMnt["jminDessus"] = (infoMnt["nrowsDessus"]-1)-int((yrecouvreSup-infoMnt["yllcornerDessus"])/sizD)  # -1 : les tableaux commencent à zéro/ nb de colonne qui commence à 1                  
            infoMnt["jmaxDessus"] = (infoMnt["nrowsDessus"]-1)-int((yrecouvreInf-infoMnt["yllcornerDessus"])/sizD)
            
            # limité à l'emprise
            
            infoMnt["iminDessus"] = int(max(0,infoMnt["iminDessus"]))
            infoMnt["imaxDessus"] = int(min((infoMnt["colsDessus"])-1,infoMnt["imaxDessus"]))
            infoMnt["jminDessus"] = int(max(0,infoMnt["jminDessus"]))        
            infoMnt["jmaxDessus"] = int(min((infoMnt["nrowsDessus"])-1,infoMnt["jmaxDessus"]))
           
            # comment faire correspondre le fond et le dessus :
            # si la maille est identique et le référentiel aussi : vecteur de passage "fond vers dessus" : (I,J)

            if infoMnt["cellsizeFond"]==infoMnt["cellsizeDessus"]:
                infoMnt["vecteurPassageFondVersDessus"]=((infoMnt["iminFond"]-infoMnt["iminDessus"]),(infoMnt["jminFond"]-infoMnt["jminDessus"]))
            else:
                infoMnt["vecteurPassageFondVersDessus"]=tuple()                
            return infoMnt
        # traitement
            
        return controleCompatibles(fond,dessus)

    #@decorateTry
    def calculDesVolumesFondEtDessus (fond,dessus):

        # lire le mnt du fond :
        
        with open (fond) as p:
            lignes=p.readlines()
            
        tableFond = list()
        for ligne in lignes[6:]:
            tableFond.append(ligne.split())
                    
        ######### somme des valeurs du fond sur l'emprise commune fond/dessus:
        
        nbRemplissageFond = 0
        nbValFond = 0
        sommeFond = 0
        for i in range(infoMnt["iminFond"],infoMnt["imaxFond"]):       
            for j in range(infoMnt["jminFond"],infoMnt["jmaxFond"]):
                val = tableFond[j][i]          
                if val==remplissage:
                    nbRemplissageFond += 1
                else:
                    sommeFond += float(val)
                    nbValFond += 1

        infoMnt["nbRemplissageFond"]=nbRemplissageFond
        infoMnt["sommeFond"]=round(sommeFond,arrondi)
        infoMnt["nbValFond"]=nbValFond
        infoMnt["moyenneFond"] = -9999
        if nbValFond: infoMnt["moyenneFond"]=round(sommeFond/nbValFond,arrondi)
        infoMnt["surfaceCouverteFond"]=round(nbValFond*infoMnt["cellsizeFond"]**2,arrondi)
        infoMnt["volumeFond"] = round(infoMnt["sommeFond"]*infoMnt["cellsizeFond"]**2,arrondi)
        
        # lire le mnt du dessus :

        with open (dessus,"r") as q:
                lignes=q.readlines()
                
        tableDessus = list()
        for ligne in lignes[6:]:
            tableDessus.append(ligne.split())
                    
        ######### somme des valeurs du dessus sur l'emprise commune fond/dessus:
             
        nbRemplissageDessus = 0
        nbValDessus = 0
        sommeDessus = 0
        for i in range(infoMnt["iminDessus"],infoMnt["imaxDessus"]):      # imindessus et imaxdessus sont pour la zone de recouvrement
            for j in range(infoMnt["jminDessus"],infoMnt["jmaxDessus"]):
                val = tableDessus[j][i]             
                if val==remplissage:
                    nbRemplissageDessus += 1
                else:
                    sommeDessus += float(val)
                    nbValDessus += 1
        
        infoMnt["nbRemplissageDessus"]=nbRemplissageDessus
        infoMnt["sommeDessus"]=round(sommeDessus,arrondi)
        infoMnt["nbValDessus"]=nbValDessus
        infoMnt["moyenneDessus"] = -9999 # valeur par défaut
        if nbValDessus: infoMnt["moyenneDessus"]=round(sommeDessus/nbValDessus,arrondi)
        infoMnt["surfaceCouverteDessus"]=round(nbValDessus*infoMnt["cellsizeDessus"]**2,arrondi)
        infoMnt["volumeDessus"] = round(infoMnt["sommeDessus"]*infoMnt["cellsizeDessus"]**2,arrondi)

        #volume entre les 2 Mnt :
        infoMnt["volumeEntreFondEtDessus"] = round(infoMnt["volumeDessus"] - infoMnt["volumeFond"],arrondi)

    def calculEcart(fond,dessus):

        if infoMnt["cellsizeFond"]!=infoMnt["cellsizeDessus"]:
            return False
        nbRemplissageFond = 0
        nbValFond = 0
        sommeFond = 0
        maxFond = -999999
        minFond =  999999
        maxDessus = -999999
        minDessus =  999999    
        nbRemplissageDessus = 0
        nbValDessus = 0
        sommeDessus = 0
        sommeEcarts = 0
        nbEcartsTotal = 0
        nbEcartSupPositifs = 0
        sommeDesEcartsSignificatifsPositifs = 0
        nbEcartSupNegatifs = 0    
        sommeDesEcartsSignificatifsNegatifs = 0
        histogrammeDesEcarts = [0 for e in range(len(limitesHistogrammeDesEcarts)+1)]
        ecartMax = -99999
        ecartMin = +99999
        positionXEcartMax = None
        positionXEcartMin = None
        positionYEcartMax = None
        positionYEcartMin = None
        tableFond = list()
        tableDessus = list()
        cols = infoMnt["imaxDessus"]-infoMnt["iminDessus"]
        rows = infoMnt["jmaxDessus"]-infoMnt["jminDessus"]    
        infoMnt["dimensionRecouvrement"] = (cols,rows)
        xllDessus = infoMnt["xllcornerDessus"]
        yllDessus = infoMnt["yllcornerDessus"]
        cellsize = infoMnt["cellsizeFond"]
        surfaceCellule = cellsize**2
        yurDessus = infoMnt["yurcornerDessus"] # le haut des y upper left

        ####### tableEcart = [[-9999]*(cols+1)]*(rows+1) # piège !!! on duplique le même élément, qui sera modifié..... pour toutes les lignes
        tableEcart = [[-9999 for i in range (cols+1)] for j in range(rows+1)]
        with open (fond) as p:
            lignesFond=p.readlines()

        for ligneFond in lignesFond[6:]:
            tableFond.append(ligneFond.split())
            
        with open (dessus) as q:
            lignesDessus=q.readlines()

        for ligneDessus in lignesDessus[6:]:
            tableDessus.append(ligneDessus.split())

        di,dj = infoMnt["vecteurPassageFondVersDessus"]
      
        for i in range(infoMnt["iminDessus"],infoMnt["imaxDessus"]):     # d'abord les x  
            for j in range(infoMnt["jminDessus"],infoMnt["jmaxDessus"]): # les y vont en décroissants dans le tableau
                try:
                    valDessus = tableDessus[j][i]
                except: continue
                try:                
                    valFond   = tableFond[j+dj][i+di]
                except:
                    print("erreur j+dj : i,j,dj =",i,j,dj)
                    continue
                if valFond==remplissage:
                    nbRemplissageFond += 1
                else:
                    nbValFond += 1
                    if float(valFond)>maxFond:
                        maxFond = float(valFond)
                        xMaxFond = round(xllDessus+i*cellsize,arrondi)
                        yMaxFond = round(yllDessus+j*cellsize,arrondi)
                    if float(valFond)<minFond:
                        minFond = float(valFond)
                        xMinFond = round(xllDessus+i*cellsize,arrondi)
                        yMinFond = round(yllDessus+j*cellsize,arrondi)
                    
                if valDessus==remplissage:
                    nbRemplissageDessus += 1
                else:
                    nbValDessus += 1
                    if float(valDessus)>maxDessus:
                        maxDessus = float(valDessus)
                        xMaxDessus = round(xllDessus+i*cellsize,arrondi)
                        yMaxDessus = round(yurDessus-j*cellsize,arrondi)
                    if float(valDessus)<minDessus:
                        minDessus = float(valDessus)
                        xMinDessus = round(xllDessus+i*cellsize,arrondi)
                        yMinDessus = round(yurDessus-j*cellsize,arrondi)
                        
                    
                if valFond!=remplissage and valDessus!=remplissage:
                    ecart = float(valDessus) - float(valFond)
                    iTableEcart = i-infoMnt["iminDessus"]
                    jTableEcart = j-infoMnt["jminDessus"]
                    tableEcart[jTableEcart][iTableEcart] = round(ecart,arrondi)
                    sommeEcarts += ecart
                    nbEcartsTotal += 1
                    
                    if ecart>tolerance:
                        nbEcartSupPositifs += 1
                        sommeDesEcartsSignificatifsPositifs += ecart
                    if ecart<-tolerance:
                        nbEcartSupNegatifs += 1
                        sommeDesEcartsSignificatifsNegatifs += ecart
                    # histogramme : les écarts sont égaux, les valeurs hors de l'intervamme min,max sont ignorées                    
                    histogrammeDesEcarts[len([a for a in limitesHistogrammeDesEcarts
                                              if a<ecart
                                              and limitesHistogrammeDesEcarts[0]<ecart<=limitesHistogrammeDesEcarts[-1]])]+=1
                    
                    if ecart>ecartMax:
                        ecartMax = ecart
                        positionXEcartMax = xllDessus+i*cellsize
                        positionYEcartMax = yurDessus-j*cellsize
                    if ecart<ecartMin:
                        ecartMin = ecart
                        positionXEcartMin = xllDessus+i*cellsize
                        positionYEcartMin = yurDessus-j*cellsize
                        
        if nbEcartsTotal==0:    # aucune valeur d'altitude commune : abandon !!!
            erreur=_("Aucun recouvrement avec altitude entre les 2 MNT\n %s\n%s\n Abandon.") % (fond,dessus)
            for a in infoMnt:
                if a!="tableEcart":
                    print(a,infoMnt[a])            
            return erreur
            
        infoMnt["tableEcart"] = tableEcart
        infoMnt["nbRemplissagesFond"] = nbRemplissageFond
        infoMnt["nbRemplissageDessus"] = nbRemplissageDessus
        infoMnt["nbValeursComparées"] = nbEcartsTotal
        infoMnt["nbEcartReelSupérieursATolerance"] = ("tolerance",tolerance,
                                                     "surface > tolerance",round(nbEcartSupPositifs*surfaceCellule,arrondi),
                                                     " volume concerné : ",round(sommeDesEcartsSignificatifsPositifs*surfaceCellule,arrondi))
        infoMnt["nbEcartReelInférieursATolerance"] = ("tolerance",tolerance,
                                                     "surface < -tolérance ",round(nbEcartSupNegatifs*surfaceCellule,arrondi),
                                                     " volume concerné : ",round(sommeDesEcartsSignificatifsNegatifs*surfaceCellule,arrondi))
        infoMnt["surfaceHorsTolerance"] = infoMnt["nbEcartReelSupérieursATolerance"][3]+infoMnt["nbEcartReelInférieursATolerance"][3]
        infoMnt["surfaceComparée"] = round(nbEcartsTotal*surfaceCellule,arrondi)
        infoMnt["surfaceEgalité"] = round(infoMnt["surfaceComparée"] - infoMnt["surfaceHorsTolerance"],arrondi)      
        infoMnt["volumeEcart"] = round(sommeEcarts*surfaceCellule,arrondi)
        if infoMnt["surfaceComparée"]: infoMnt["ecartMoyen"] = round(infoMnt["volumeEcart"]/infoMnt["surfaceComparée"],arrondi)
        infoMnt["ecartMax"] = (round(ecartMax,arrondi),(round(positionXEcartMax,arrondi),round(positionYEcartMax,arrondi)))
        infoMnt["ecartMin"] = (round(ecartMin,arrondi),(round(positionXEcartMin,arrondi),round(positionYEcartMin,arrondi))) 
        infoMnt["limitesHistogrammeDesEcarts"]=limitesHistogrammeDesEcarts
        infoMnt["histogrammeDesEcarts"]=histogrammeDesEcarts    
        infoMnt["(X,Y)_MinFond recouvrement"] = ((xMinFond,yMinFond),minFond)
        infoMnt["(X,Y)_MinDessus recouvrement"] = ((xMinDessus,yMinDessus),minDessus)    
        infoMnt["(X,Y)_MaxFond recouvrement"] = ((xMaxFond,yMaxFond),maxFond)
        infoMnt["(X,Y)_MaxDessus recouvrement"] = ((xMaxDessus,yMaxDessus),maxDessus)

      

    ########################## écrire les écarts
        
    def ecrireTableDesEcarts(infoMnt):
        sizF = infoMnt["cellsizeFond"]
        sizD = infoMnt["cellsizeDessus"]
        if sizF!=sizD:
            return
        fichierFond = infoMnt["fichierFond"]
        fichierDessus = infoMnt["fichierDessus"]
        base = ("ecart_tolerance_"+str(tolerance)+"_"+
                os.path.splitext(os.path.basename(fichierFond))[0]+"__"+
                os.path.splitext(os.path.basename(fichierDessus))[0]+".XYZ")
        fichierEcart = os.path.join(os.path.dirname(fichierFond),base)
        infoMnt["fichierEcart"] = fichierEcart
        # point de départ : xrecouvreinf
        xinf = infoMnt["xrecouvreInf"]
        yinf = infoMnt["yrecouvreInf"]
        xsup = infoMnt["xrecouvreSup"]
        ysup = infoMnt["yrecouvreSup"]
        cols,rows = infoMnt["dimensionRecouvrement"]
        table = infoMnt["tableEcart"]
        with open(fichierEcart,"w") as f:
            for i in range(cols+1):
                for j in range(rows+1):
                    x = xinf + i * sizF
                    y = ysup - j * sizF
                    v = table[j][i]
                    if v!=float(remplissage):

                        if -tolerance<v<tolerance:
                            v=0         # on annule les "petits écarts", dans l'épaisseur du trait.
                        t = (str(round(x,arrondi)),str(round(y,arrondi)),str(round(v,arrondi)))
                        f.write(" ".join(t)+"\n")
                
    ##################################################################################################### Début    

    interface.menageEcran()
    fond = tkinter.filedialog.askopenfilename( initialdir="",                                                 
                                                filetypes=[(_("asc"),"*maillage*.asc"),(_("Tous"),"*")],
                                                multiple=False,
                                                title = _("MNT constituant le territoire initial, le socle, le fond"))
    if fond==str():
        interface.encadre(_("Calcul de volume abandonné."))
        return

    dessus = tkinter.filedialog.askopenfilename( initialdir="",                                                 
                                                filetypes=[(_("asc"),"*maillage*.asc"),(_("Tous"),"*")],
                                                multiple=False,
                                                title = _("MNT constituant le territoire final, le dessus"))
    if dessus==str():
        interface.encadre(_("Calcul de volume abandonné."))
        return
                                
    #initiatisations  
    remplissage = "-9999"
    arrondi = interface.arrondi         # les valeurs de volume seront arrondies (nb chiffres)
    tolerance = interface.tolerance     # on compte les écarts supérieurs à cette valeur
    limitesHistogrammeDesEcarts = interface.limitesHistogrammeDesEcarts

    interface.encadre("\n"+_("Patience, le calcul du volume peut sembler long....\n"))

    # recherche des infos,  calcul du volume
    infoMnt = lectureInfoFichiers( fond, dessus)  # exploite les 6 premières lignes du MNT, calcule la zone de recouvrement
    if type(infoMnt) != type(dict()):
        interface.encadre("Erreur : "+str(infoMnt))
        return
    calculDesVolumesFondEtDessus( fond, dessus) # calcul du volume de chaque couche, indépendamment de l'autre 
    retourCalcul =calculEcart (fond, dessus)   # calcul de l'écart, uniquement sur les valeurs communes
    if retourCalcul!=None:
        interface.encadre("Erreur : "+str(retourCalcul))
        return        
    ecrireTableDesEcarts(infoMnt)    # retour :

    rapport  = _("Calcul du volume entre 2 MNT : rapport final.")+"\n\n"
    rapport += _("Mnt socle     : %s") % (str(infoMnt["fichierFond"]))+"\n"   
    rapport += _("Mnt supérieur : %s") % (infoMnt["fichierDessus"])+"\n\n"
    rapport += _("Emprise commune : %s m2") % (str(infoMnt['Emprise recouvrement']))+"\n"
    rapport += _("Surface commune : %s m2") % (infoMnt["Surface recouvrement"]  )  +"\n"                                       
    rapport += _("Le volume est calculé lorsque l'altitude est connue pour les 2 MNT.")+"\n"
    rapport += _("En tenant compte de ce principe la surface comparable est de %s m2") % (infoMnt["surfaceComparée"])+"\n"                                            
    rapport += _("Le  calcul du volume dépend d'un paramètre : la tolérance qui vaut %s m. (modifiable par menu)")% (tolerance)+"\n"
    rapport += _("Un écart d'altitude inférieur à la tolérance est ignoré, considéré comme nul, dans l'épaisseur du trait.")+"\n\n"
    surfaceInchangee = infoMnt["surfaceEgalité"]
    pourCentInchange = round(100*surfaceInchangee/infoMnt["surfaceComparée"],arrondi)
    rapport += (_("Ainsi les 2 MNT sont égaux sur %s m2, soit %s %% de la surface comparable") % (surfaceInchangee,pourCentInchange)) +"\n\n"
    rapport += _("Le volume calculé est composé d'un volume positif (Mnt supérieur > Mnt Socle) : %s m3") % (str(infoMnt["nbEcartReelSupérieursATolerance"][5]))  +"\n"                
    rapport += _("et d'un volume négatif (Mnt supérieur < Mnt Socle) : %s m3") % (str(infoMnt["nbEcartReelInférieursATolerance"][5]))  +"\n\n"
    rapport += _("Informations complémentaires")+"\n"   
    rapport += " "+_("- l'écart maximum est de %s m, au point %s.") % (infoMnt["ecartMax"][0],infoMnt["ecartMax"][1])  +"\n"    
    rapport += " "+_("- l'écart minimum est de %s m, au point %s.") % (infoMnt["ecartMin"][0],infoMnt["ecartMin"][1])  +"\n"
    rapport += " "+_("- globalement l'écart moyen entre les 2 MNT est de %s m.") % (infoMnt["ecartMoyen"])  +"\n"     
    rapport += " "+_("- sans prendre en compte la tolérance le volume total de l'écart est de %s m3") % (infoMnt["volumeEcart"])+"\n\n"    
    rapport += " "+_("- le fichier 'Trace_AperoDeDenis_volume.txt' mémorise ces résultats.")+"\n"
    rapport += (" "+_("- le nuage de points XYZ des écarts est consultable par le menu 'Outil_Metier\Visualiser l'écart'"))              
    interface.ecartXyz = infoMnt["fichierEcart"]
    message = "\n********************** CALCUL VOLUME \n\n"+heure()+"\n"+rapport+"\n\n********************** FIN DU CALCUL VOLUME\n"
    traceMetier(message,fond,'volume')
    interface.ecritureTraceMicMac() 
    interface.encadre(rapport)
##    for a in infoMnt:
##        if a!="tableEcart":
##            print(a,infoMnt[a])

def traceMetier(message,fichier,nom_trace):     # écrire le message dans la trace nom sous le répertoire de fichier
    interface.ecritureTraceMicMac()             # vider la liste d'attente
    precedente = interface.typeDuChantier       #mémoriser l'état initial
    interface.typeDuChantier = ['metier',fichier,nom_trace] # pour définir le fichier trace    
    interface.ajoutLigne(message)               # ajouter dans la file d'attente 
    interface.ecritureTraceMicMac()             # écrire effectivement
    interface.typeDuChantier = precedente       # remettre en l'état initial

##################################### Fonctions de géométrie euclidienne: équation d'une droite (A,B),
##################################### distance point droite, point dans triangle, produit scalaire

def pointDansTriangle(A,B,C,M): # chaque point est un tuple X,Y, qui peut être complété par Z, inutilisé)
    # position de M entre C et la droite AB :
    dAB = droite(A,B)
    pC = distanceALaDroite(C,*dAB)
    pMC = distanceALaDroite(M,*dAB)
    if pC!=math.copysign(pC,pMC) : return False     # pas du même côté de la droite : pas dans le triangle
    if abs(pMC)>abs(pC):         return False       # M plus éloigné que C : pas dans le triangle

    # position de M entre B et la droite AC :
    dAC = droite(A,C)
    pB = distanceALaDroite(B,*dAC)
    pMB = distanceALaDroite(M,*dAC)
    if pB!=math.copysign(pB,pMB) : return False     # pas du même côté de la droite : pas dans le triangle
    if abs(pMB)>abs(pB):           return False     # M plus éloigné que C : pas dans le triangle
   
    # position de M entre A et la droite BC :
    dBC = droite(B,C)
    pA = distanceALaDroite(A,*dBC)
    pMA = distanceALaDroite(M,*dBC)
    if pA!=math.copysign(pA,pMA) : return False     # pas du même côté de la droite : pas dans le triangle
    if abs(pMA)>abs(pA):           return False     # M plus éloigné que C : pas dans le triangle

    # cas particulier : A=B=C et M différent
    if A==B==C and M!=A:
        print("a=b=c point M en dehors du triangle nul ABC")        
        return False
    return pMA/pA,pMB/pB,pMC/pC # renvoie les coeficient barycentriques du point dans le triangle

    
def produitScalaire(O,U,V):        
    return (U[0]-O[0])*(V[0]-O[0])+(U[1]-O[1])*(V[1]-O[1])

def droite(A,B): # renvoi a,b,c les coef de la droite ax+by+c=0 : choix de -1 pour le coef de y afin que a = pente et c = abscisse à l'origine
    if A[0]!=B[0]:
        a =(A[1]-B[1])/(A[0]-B[0])
        b =-1
        c = A[1]-a*A[0]
    elif A[1]!=B[1]:
        a = -1
        b = 0
        c = A[1]
    else:
        a=0
        b=0
        c=0
    return a,b,c
    
def distanceALaDroite(M,a,b,c): # retourne la valeur axm+bym+c : position du point par rapport à la droite
    return a*M[0]+b*M[1]+c

################### Lecture ponctuele, Modification ponctuelle d'une sauvegarde pickle

def restaureUnParametre(fichierPickle, numeroParam):         # permet de restaurer un seul paramètre d'un chantier si besoin ou d'un pickle
    try:
        with open(fichierPickle,mode='rb') as f:
            r = pickle.load(f)
        return r[numeroParam]
    except Exception as e:
        return None

def sauveUnParametre(fichierPickle, numeroParam, valeur):  # permet de sauver un seul paramètre d'un pickle, si possible
    try:
        with open(fichierPickle,mode='rb') as f:
            r = pickle.load(f)      #r est un tuple                
    except Exception as e:
        print("erreur lire sauveUnParametre : ",str(e))
        return
    if numeroParam<len(r):
        l = list(r)            
        l[numeroParam]=valeur
        r = tuple(l)
    elif len(r)==numeroParam:
        l = list(r)             
        l.append(valeur)
        r = tuple(l)            
    else:
        print("pas assez de paramètres pour sauvegarder la valeur dans le numéro %s, longueur tuple = %s chantier %s" % (numeroParam,len(r),fichierPickle))
        return
    try:
        with open(fichierPickle,mode='wb') as f:          
            pickle.dump(r,f)               
    except Exception as e:
        print("erreur dump sauveUnParametre : ",str(e))
        return

# vérificatio ndu paramètre de centrage de saisieMasqQT

@decorateTrySilencieux
def verifParametresSaisieMasqQT():
    valeurActuelle = queryRegistre(interface.cleMasqQT,interface.sousCleMasqQT)
    if len(valeurActuelle):
        print("valeur actuelle=",valeurActuelle)
        if "0x2" in valeurActuelle[0]: # centre = origine
            ecrireRegistre(interface.majCleMasqQT)
    

# Ecrire une clé de registre

@decorateTrySilencieux
def ecrireRegistre(script):
    if os.name=="nt":
        with open("reg.reg",mode="w") as r:
            r.write(script)
        time.sleep(0.01)
        interface.lanceCommande(["regini.exe","reg.reg"],
                          info=_("Modification clé registre %s" % (script)),
                          attendre=True)        
        supprimeFichier("reg.reg")

# liste une clé de registre : renvoi une liste

@decorateTrySilencieux
def queryRegistre(cle,sousCle):
    if os.name=="nt":    
        retour=list()
        def filtreQuery(ligne):
            if sousCle in ligne:
                retour.append(ligne)
        query = ["reg",
                    "query",
                    cle,
                    "/v",
                    sousCle
                    ]
        interface.lanceCommande(query,
                                info=_("Modification clé registre SaisieMasqQT"),
                                filtre=filtreQuery,
                                attendre=True)
        return retour
    
'''################################## Crée un fichier contenant l'icone de l'application et en renvoie le nom conserver pour exemple de ficheir temporaire

def iconeGrainSel():
    iconeTexte = "AAABAAIAIC....
    iconeBin = base64.b64decode(iconeTexte)                 # décodage pour revenir au binaire du fichier icone :
    with tempfile.NamedTemporaryFile(delete=False) as f:    # écriture de ce binaire dans un fichier temporaire
        f.write(iconeBin)
    return f.name
'''

################################## Classe : Dialogue minimum modal : demande une chaine de caractères ###########################"

class MyDialog:
   
    def __init__(self,parent,titre=_("Nouveau nom pour le chantier : "),basDePage='none'):
        self.saisie=str()
        top = self.top = tkinter.Toplevel(parent,width=500,relief='sunken')
        top.transient(parent)
        top.geometry("500x320+100+100")
        fenetreIcone(self.top)                
        l=ttk.Label(top, text=titre)
        l.pack(pady=10,padx=10)
        top.bind("<Return>",self.ok)
        self.e = ttk.Entry(top,width=60)
        self.e.pack()
        self.e.focus_set()
        b = ttk.Button(top, text=_("OK"), command=self.ok)
        b.pack(pady=5)
        c = ttk.Button(top, text=_("Annuler"), command=self.ko)
        c.pack(pady=5)
        if basDePage!="none":
            d = ttk.Label(top, text=basDePage)
            d.pack(pady=5)
        top.grab_set()
        fenetre.wait_window(top)
        
    def ok(self,event='none'):
        self.saisie=self.e.get()
        self.top.destroy()
        return

    def ko(self):
        self.top.destroy()
        self.saisie=False
        return

################################## Classe : Dialogue modale : demande un texte sur plusieurs lignes #########################"

class MyDialogTexte:
   
    def __init__(self,parent,titre=_("Console"),basDePage='none',boutonDialogueTexteOk='OK'):
        self.saisie=str()
        top = self.top = tkinter.Toplevel(parent,width=250,relief='sunken')
        top.transient(parent)
        top.geometry("600x400+100+100")
        fenetreIcone(self.top)                
        l=ttk.Label(top, text=titre)
        l.pack(pady=10,padx=10)
        self.resul200 = ttk.Frame(top,height=100,relief='sunken')  # fenêtre texte pour afficher le bilan
        self.scrollbar = ttk.Scrollbar(self.resul200)
        self.scrollbar.pack(side='right',fill='y',expand=1)              
        self.scrollbar.config(command=self.yviewTexte)
        self.texte201 = tkinter.Text(self.resul200,width=60,height=5,yscrollcommand = self.scrollbar.set,wrap='word')
        self.resul200.pack()
        self.texte201.pack()
        self.texte201.focus_set()
        b = ttk.Button(top, text=_(boutonDialogueTexteOk), command=self.ok)
        b.pack(pady=5)
        c = ttk.Button(top, text=_("Abandon"), command=self.ko)
        c.pack(pady=5)
        if basDePage!="none":
            d = ttk.Label(top, text=basDePage)
            d.pack(pady=5)
        top.grab_set()
        fenetre.wait_window(top)
        
    def ok(self,event='none'):
        self.saisie=self.texte201.get("0.0",'end')
        self.top.destroy()
        return
        
    def ko(self):
        self.top.destroy()
        return

    def yviewTexte(self, *args):
        if args[0] == 'scroll':
            self.texte201.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.texte201.yview_moveto(args[1])

################################## Classe : Dialogue minimum modal : choix dans une liste ###########################"

class choisirDansUneListe:              # mode="single" ou 'extended'

    def __init__(self,fenetreParent,listeDeChoix,titre,mode='extended',boutonOk="supprimer"):
        if len(listeDeChoix)==0:
            return
        self.lesChoix = listeDeChoix    
        self.topChoix = tkinter.Toplevel(fenetreParent)         # boite de dialogue
        self.topChoix.transient(fenetreParent)
        self.topChoix.title(titre)
        self.topChoix.geometry("400x250+100+100")
        fenetreIcone(self.topChoix)   
        f = self.topChoix                          # ttk.Frame(self.topChoix)       
        frameSelectRep = ttk.Frame(self.topChoix)
        invite = ttk.Label(self.topChoix,text=("Choisir :"))
        invite.pack(pady=10,padx=10,ipadx=5,ipady=5)
        scrollbarV = ttk.Scrollbar(frameSelectRep, orient=('vertical'))          
        scrollbarH = ttk.Scrollbar(frameSelectRep, orient=('horizontal'))
        self.selection = tkinter.Listbox(frameSelectRep,
                                                   selectmode=mode,
                                                   xscrollcommand=scrollbarH.set,
                                                   yscrollcommand=scrollbarV.set,
                                                   height= min(10,len(listeDeChoix)),
                                                   width=  min(70,min(300,(5+max(len (r) for r in listeDeChoix)))))
                                                        
        self.selection.select_set(1)
        listeDeChoix.sort()
        for i in listeDeChoix:
            self.selection.insert('end',i)
        if len(listeDeChoix)>10:
            scrollbarV.config(command=self.yview)
            scrollbarV.pack(side='right', fill='y')            
        self.selection.pack(side='left', fill='both', expand=1)          
        frameSelectRep.pack()         
        self.selection.select_set(0)
        b = ttk.Button(f,text=(boutonOk),command=self.valid)
        b.pack(pady=5)
        c = ttk.Button(f,text=("Annuler"),command=self.cancel)
        c.pack(pady=5)
        self.topChoix.grab_set()
        fenetre.wait_window(self.topChoix)    

    def yview(self, *args):
        if args[0] == 'scroll':
            self.selection.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.selection.yview_moveto(args[1])

    def xview(self, *args):
        if args[0] == 'scroll':
            self.selection.xview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.selection.xview_moveto(args[1])            

    def valid(self):
        selectionEnCours = self.selection.curselection()
        self.topChoix.destroy()
        self.selectionFinale = [self.lesChoix[e] for e in selectionEnCours]


    def cancel(self):
        self.topChoix.destroy()
        self.selectionFinale = list()

################################## Classe : Dialogue minimum modal : deux boutons OK KO si b2="" alors pas de second bouton ###########################"
 
class MyDialog_OK_KO:
    def __init__(self,parent=None,titre="Question",texte="texte",b1="OK",b2="KO"):
        self.retour = -1
        if parent==None:
            parent = tkinter.Tk()
        self.top = tkinter.Toplevel(parent,width=200,relief='sunken')
        self.top.transient(parent)
        self.top.geometry("600x250+100+100")
        try: fenetreIcone(self.top)
        except Exception as e: print("erreur fenetre icone : ",str(e))
        self.top.title(titre)
        l=ttk.Label(self.top, text=texte)
        l.pack(pady=10,padx=10)
        b = ttk.Button(self.top, text=b1, command=self.ok)
        b.pack(pady=5)
        if b2:
            c = ttk.Button(self.top, text=b2, command=self.ko)
            c.pack(pady=5)
        self.top.grab_set()
        parent.wait_window(self.top)

    def ok(self,event='none'):
        self.retour = 1
        self.top.destroy()
        
    def ko(self,event=None):
        self.retour = 0
        self.top.destroy()
        

################################## Style pur TTK  ###########################"

def monStyle():
    ttk.Style().configure("TButton", padding=6, relief="flat",background="#ccc")

# Message indiquant le lancement de l'outil dans le shell

print(heure()+" "+_("lancement d'aperodedenis")+version+".")

################################### boucle sur l'interface tant que continuer est vrai :

if __name__ == "__main__":
    while continuer:
        compteur += 1           # pour n'exécuter qu'un fois les fonctions à lancer au lancement de l'interface                
        fenetre = tkinter.Tk()  # fenêtre principale
        # les icones en variables globales : icone cerema, fleche droite, gauche (saisie points gcp)
        # la commande photoImage ne être appelée qu'après création de la fenêtre Tk        
        dataIcone        = tkinter.PhotoImage(data=iconeTexte)
        dataFlecheDroite = tkinter.PhotoImage(data=flecheDroite)
        dataFlecheGauche = tkinter.PhotoImage(data=flecheGauche)        
        dataLogoCerema   = tkinter.PhotoImage(data=logoCerema)
        dataLogoIGN      = tkinter.PhotoImage(data=logoIGN)        
        # création de l'interface : menu, widgets...        
        interface = Interface(fenetre)
        # parfois l'interface doit se rafraichir :  relance :
        if messageDepart==str():
            interface.afficheEtat()
        else:
            interface.encadre(str(messageDepart))   # affiche les infos restaurées :     
        try: fenetre.mainloop()                     # boucle tant que l'interface existe
        except: pass


