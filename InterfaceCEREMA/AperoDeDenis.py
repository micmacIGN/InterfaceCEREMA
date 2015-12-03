#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PEP 0008 -- Style Guide for Python Code

import tkinter                              # gestion des fenêtre, des boutons ,des menus
import tkinter.filedialog                   # boite de dialogue "standards" pour demande fichier, répertoire
import tkinter.ttk as ttk                   # amélioration de certains widgets de tkinter : le comportement est géré indépendamment de l'apparence : c'est mieux ! mais différent !
import pickle                               # pour la persistence
import os.path                              # pour les noms de fichier
import os                                   # gestion du système, des path 
import shutil                               # copie des fichiers, gestions répertoires
import time
import sys                                  # info système
import subprocess                           # appel des procédures MicMac
import traceback                            # uniquement pour pv : affiche les propriétés des variables (qui sert pour débug)
from   PIL import Image                     # pour travailler sur les images, définir le masque, placer les points GPS : PIL
from   PIL import ImageTk
from   PIL import ImageDraw
import base64
import tempfile
import inspect

########################### Classe pour tracer les masques

class TracePolygone():
    def __init__(self, fenetre, image, masque,labelBouton='Tracer le masque'):  # fenetre : root de l'appli ; image : fichier image sur lequel tracer le polygone ; masque = nom du fichier à créer
        self.root = tkinter.Toplevel()                      #fenêtre spécifique à la saisie du masque
        self.root.title("Saisie sur la photo : "+image)     # titre
        fenetreIcone(self.root)
        self.root.geometry( "900x900" )                     # Taille
        self.dimMaxiCanvas = 600                            # dimension max du canvas accueillant l'image       
        self.facteurZoom = 2                                # valeur du changement de niveau de zoom lorsque l'utilisateur "zoom" (par la molette de la souris)
        self.maxScale = 8                                   # Nb de zooms maximum autorisé
        self.listeSauveImages = list()                      # mémorisation des images zoomées pour accélérer le retour en arrière (deZoom)
        self.listePointsJPG = list()                        # liste des points du polygone
        self.polygone = False                               # deviendra vrai lorsque le polygone sera effectif
        self.file = image                                   # nom du fichier partagé, devient attribut de la classe
        self.nomMasque = masque                             # nom du fichier masque partagé (en principe : os.path.splitext(self.file)[0]+"_mask.tif")
        
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
        self.boutonQuitter = ttk.Button(self.frame2, text="Valider",command = self.quitter)
        self.boutonAbandon = ttk.Button(self.frame2, text="Abandon",command = self.abandon)        
        self.boutonTracer = ttk.Button(self.frame2, text=labelBouton,command = self.tracerMasqueBis)
        self.boutonAide = ttk.Label (self.frame2,
                                     text=  "\nmolette de la souris = zoom,\n"+\
                                            "utilisable avant ET pendant le tracé\n"+\
                                            "glisser-déposer actif avant le tracé\n\n"+\
                                            "Tracer :\n"+\
                                            "Clic gauche : ajouter un point;\n clic droit : fermer le polygone,\n"+\
                                            "Touche Del pour supprimer un point ou le polygone,\n")       
        self.boutonAide.pack(side='left',pady=2,padx=2)
        self.boutonTracer.pack(side='left',pady=2,padx=8)
        self.boutonQuitter.pack(side='left',pady=2,padx=8)
        self.boutonAbandon.pack(side='left',pady=2,padx=8)
        self.frame2.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.quitter)    # Fonction a éxécuter lors de la sortie du programme
        self.root.transient(fenetre)                            # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.root.grab_set()
        fenetre.wait_window(self.root)                          
        
    def quitter(self):                                          # libère les ressources images pour ne pas les "bloquer"
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
                self.infoBulle(event,"Il faut au moins 2 points dans le polygone.")
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
             self.infoBulle(event,texte="Zoom maximum atteint") # l'utilisateur est informé
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
        try: self.canvas.delete(self.imgTk_id)                  #si jamais il n'y a pas encore d'image
        except: pass
        self.imgTk = ImageTk.PhotoImage(self.img)      
        self.imgTk_id = self.canvas.create_image(0,0,image = self.imgTk,anchor="nw")
        self.afficheMasque()
                
    def tracerMasqueBis(self):                                  # appui sur un bouton "tracermasque" : on active le tracé
        if self.frame.cget("cursor").string=="plus":            # Nouvel appui sur le bouton : on arrête la saisie
            self.frame.config(cursor="arrow")                   # on remet le cursor "normal"
            return
        self.listePointsJPG=list()                              # nouvelles données
        self.polygone = False                                     # pas de polygone fini
        self.menagePol()
        self.fermerMasque()                                     # efface le masque affiché en cours
        self.frame.config(cursor="plus")                        # curseur en mode ajout          
        self.boutonTracer.state(["pressed","!focus",'selected']) # etat séléctionné du bouton

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
        except: pass
        self.bulle = tkinter.Toplevel()                                 # nouvelle fenêtre pour l'info bulle
        self.bulle.overrideredirect(1)                                  # sans le bordel tout autour
        self.bulle.geometry("%dx%d%+d%+d" % (l+10,h+6,event.x_root+15,event.y_root))  # position du coin nw de la fenêtre par rapport au curseur
        ttk.Label(self.bulle,text = texte,background="#ffffaa",relief = 'solid').pack()    # texte, la taille de la fenêtre s'adapte au texte, style infobulle
        #self.bulle.mainloop()                                           # boucle d'attente d'événement sur la fenêtre (pas de pack possible)

    def sauverMasque(self):                                             # création d'une image 200x200 avec un fond de couleur noire        
        img = Image.new("1",self.imageFichier.size)                     # 1 bit par pixel (noir et blanc (la couleur par défaut est le noir (http://pillow.readthedocs.org/en/latest/reference/Image.html)
        dessin = ImageDraw.Draw(img)                                    # création d'un objet Draw
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
    
    def __init__(self,fenetre,image,points,dejaPlaces):        
        # controle présence photo :
        
        if image.__len__()==0:              # pas d'image
            return
        if image.__class__()==list():
            image = image[0]
            
        self.file = image                   # nom de la photo avec chemin (au moins relatif)        
        self.root = tkinter.Toplevel()
        self.root.title( "Calibration GPS "+image)
        self.root.title("Position des points sur la photo  : "+image)       # titre
        fenetreIcone(self.root)
        self.root.geometry( "900x900" )    
        self.dimMaxiCanvas = 600            # dimension max du canvas accueillant l'image
        self.facteurZoom = 2                # valeur du changement de niveau de zoom lorsque l'utilisateur "zoom" (par la molette de la souris)
        self.maxScale = 8                   # zoom max autorisé
        self.couleurTexte = 'white'
        self.xyInfo = True
        self.listeSauveImages = list()      # mémorisation des images zoomés pour accélérer le retour en arrière (deZoom)
        self.xDrag = -1
        self.yDrag = -1
        self.imgTk_id = 'none'
        self.dicoBoutons = dict()           # key = nom du point, value = référence du bouton correspondant dans la fenêtre, dico utile localement        
        self.dicoPointsJPG = dejaPlaces     # key = (nom du point,nom de la photo), value = tuple à 2 valeurs : (x,y dans le jpeg) dico utile globalement
        self.retourSiAbandon = dejaPlaces
        self.boutonActif = ttk.Button()
        self.tempo = 0
        
        # initialisations de l'affichage de l'image, dimesions du cadre, positionnement :
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
        
        # Initialisation des boutons de la souris, du gestionnaire d'événements, des boutons pour placer les points
        self.placerBoutons(points)

        # boutons de controle :
        
        self.frame3 = ttk.Frame(self.root,borderwidth = 2,relief = "sunken")
        self.boutonQuitter = ttk.Button(self.frame3, text="Valider",command = self.quitter)
        self.boutonSupprimerTousLesPoints = ttk.Button(self.frame3, text="Supprimer tous les points",command = self.supprimerTousLesPoints)
        self.boutonAbandon = ttk.Button(self.frame3, text="Abandon",command = self.abandon)
        self.boutonQuitter.pack(side='left',pady=2,ipady=2)
        self.boutonSupprimerTousLesPoints.pack(side='left',pady=2,ipady=2,padx=5)
        self.boutonAbandon.pack(side='left',pady=2,ipady=2,padx=5)
        self.frame3.pack(pady=10)
        self.frame4 = ttk.Frame(self.root,borderwidth = 2,relief = "sunken")        
        self.boutonchangerCouleurTexte = ttk.Button(self.frame4, text="Changer la couleur des libellés",command = self.changerCouleurTexte)        
        self.boutonchangerCouleurTexte.pack(pady=2,ipady=2,padx=5)
        self.frame4.pack(pady=10)

        # message d'inforamtion

        self.frame5 = ttk.Frame(self.root,borderwidth = 2)
        ttk.Label(self.frame5,text="Utiliser la molette pour zoomer/dezoomer pendant la saisie.").pack()
        self.frame5.pack()
        
        # évènements

        self.root.bind("<Button-1>",self.bouton1)
        self.root.bind("<ButtonRelease-1>",self.finDrag)
        self.root.bind("<MouseWheel>",self.molette)
        self.root.bind("<B1-Motion>",self.b1Move)
        self.root.bind("<4>",self.moletteLinux4)
        self.root.bind("<5>",self.moletteLinux5)                        
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)    # Fonction a éxécuter lors de la sortie du programme
        self.root.transient(fenetre)                            # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.root.grab_set()
        fenetre.wait_window(self.root)
                                            
    def placerBoutons(self,listePoints):                        # Place les boutons correspondants aux points de listePoints
        for e in listePoints:                                   # un bouton pour chaque référence de la liste des boutons;
            b = ttk.Button(self.frame2, text="Placer le point "+e[0],cursor="plus",command = lambda i = (e[0],e[1]) :self.activerBouton(i))              
            self.dicoBoutons.update({e[0]:b})                      # mémo dans un dico du nom du point / références du bouton
            b.pack(side="left",padx=5)

        
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
             self.infoBulle(event,texte="Zoom maximum atteint")                         # l'utilisateur est informé
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
        self.canvas.create_text(self.xFrame, self.yFrame+20,text = bouton+" x="+str(xJPG)+" y="+str(yJPG),tag=bouton,fill=self.couleurTexte)
      
    def activerBouton(self,boutonChoisi):                                                               # appui sur un bouton "ajouter un point"
        self.boutonActif.state(["!active","!focus","!pressed",'!selected'])                             # RAZ état de l'ancien bouton
        if self.boutonActif==self.dicoBoutons[boutonChoisi[0]]:                                            # réappuie sur le bouton actif : on le désactive  et on quitte
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
        if self.couleurTexte=='white':
            self.couleurTexte = 'black'
        else:
            if self.couleurTexte=='black':
                self.couleurTexte = 'blue'
            else:
                if self.couleurTexte=='blue':
                    self.couleurTexte = 'white'
        self.afficherTousLesPoints()
        
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

    def abandon(self):
        self.dicoPointsJPG = self.retourSiAbandon
        self.quitter()

    def supprimerTousLesPoints(self):
        aSupprimer = dict(self.dicoPointsJPG)
        for cle in aSupprimer:
            if cle[1]==self.file:
               del self.dicoPointsJPG[cle]
        self.afficheImage()
        
################# Classe Principale : la fenêtre maître de l'application, le menu, l'IHM

class Interface(ttk.Frame):
        
    ################################## INITIALISATIONS - MENU - VALEURS PAR DEFAUT - EXIT ###########################################################
    
    def __init__(self, fenetre, **kwargs):
 
        # initialise les "constantes"

        self.initialiseConstantes()

        #affiche le logo durant 5 secondes
        try:
            global compteur
            if compteur==1:
                self.logo1 = ttk.Frame(fenetre)                                     # cadre dans la fenetre ; affiche la photo sélectionnée              
                self.canvasLogo = tkinter.Canvas(self.logo1,width = 560, height = 200)       # Canvas pour revevoir l'image
                self.canvasLogo.pack(fill='both',expand = 1)
                self.logo1.pack()
                self.imageLogo = Image.open(self.logoCerema) 
                self.img = self.imageLogo.resize((560,200))
                self.imgTk = ImageTk.PhotoImage(self.img)
                self.imgTk_id = self.canvasLogo.create_image(0,0,image = self.imgTk,anchor="nw") # affichage effectif de la photo dans canvasPhoto
                fenetreIcone(fenetre)
                for i in range(len(self.titreFenetre+" : Une interface graphique pour MicMac...")+8):
                    fenetre.title((self.titreFenetre+" : Une interface graphique pour MicMac...")[0:i])        
                    fenetre.update()
                    time.sleep(0.1)
                self.logo1.destroy()
        except Exception as e:
            print(str(e))

        # initialise les variables "chantier"
                
        self.initialiseValeursParDefaut()               # valeurs par défaut pour un nouveau chantier (utile si pas encore de chantier)                                                                                                                       # pour les paramètres du chantier sous le répertoire chantier, aprés lancement Micmac
        
        # On restaure la session précédente
        
        self.restaureParamEnCours()                                                             # restaure les paramètres locaux par défaut

        # Fenêtre principale : fenetre
       
        ttk.Frame.__init__(self, fenetre, **kwargs)
        self.pack(fill='both')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        fenetreIcone(fenetre)
        fenetre.title(self.titreFenetre)                                                        # Nom de la fenêtre
        fenetre.geometry("600x600+100+200")          

        # construction des item du menu

        mainMenu = tkinter.Menu()                                                               # Barre de menu principale

        # Fichier
        
        menuFichier = tkinter.Menu(mainMenu,tearoff = 0)                                        ## menu fils : menuFichier, par défaut tearOff = 1, détachable 
        menuFichier.add_command(label="Nouveau chantier", command=self.nouveauChantier)           
        menuFichier.add_command(label="Ouvrir un chantier", command=self.ouvreChantier)
        menuFichier.add_separator()        
        menuFichier.add_command(label="Enregistrer le chantier en cours", command=self.enregistreChantier)
        menuFichier.add_command(label="Renommer le chantier en cours", command=self.renommeChantier)         
        menuFichier.add_separator()
        menuFichier.add_command(label="Du ménage !", command=self.supprimeRepertoires)        
        menuFichier.add_separator()        
        menuFichier.add_command(label="Quitter", command=self.quitter)

        # Edition

        menuEdition = tkinter.Menu(mainMenu,tearoff = 0)                                        ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuEdition.add_command(label="Afficher l'état du chantier", command=self.afficheEtat)
        menuEdition.add_separator()        
        menuEdition.add_command(label="Visualiser toutes les photos sélectionnées", command=self.afficherToutesLesPhotos)
        menuEdition.add_command(label="Visualiser les points GPS", command=self.afficherLesPointsGPS)        
        menuEdition.add_command(label="Visualiser le masque 2D et l'image maitre", command=self.afficherMasqueEtMaitre)
        menuEdition.add_command(label="Visualiser le masque 3D", command=self.afficheMasqueC3DC)
        menuEdition.add_command(label="Visualiser la ligne horizontale/verticale", command=self.afficherLigneHV)
        menuEdition.add_command(label="Visualiser la zone plane", command=self.afficherZonePlane)
        menuEdition.add_command(label="Visualiser la distance", command=self.afficherDistance)        
        menuEdition.add_separator()
        menuEdition.add_command(label="Afficher la trace complete du chantier", command=self.lectureTraceMicMac)
        menuEdition.add_command(label="Afficher la trace synthétique du chantier", command=self.lectureTraceSynthetiqueMicMac)
        menuEdition.add_separator()
        menuEdition.add_command(label="Afficher l'image 3D aprés Tapas", command=self.afficheApericloud)      
        menuEdition.add_command(label="Afficher l'image 3D aprés Malt ou C3DC", command=self.affiche3DNuage)
        
        # menuMaintenance.add_command(label="Vérifier les dépendances",command=self.verifierDependances)

        # MicMac
                
        menuMicMac = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuMicMac.add_command(label="Choisir des photos", command=self.lesPhotos)
        menuMicMac.add_command(label="Options", command=self.optionsOnglet)
        menuMicMac.add_separator()     
        menuMicMac.add_command(label="Lancer MicMac", command=self.lanceMicMac)                 ## Ajout d'une option au menu fils menuFile

        # Outils

        menuOutils = tkinter.Menu(mainMenu,tearoff = 0)                                         ## menu fils : menuFichier, par défaut tearOff = 1, détachable

        menuOutils.add_command(label="Nom et focale de l'appareil photo", command=self.OutilAppareilPhoto)
        menuOutils.add_command(label="Toutes les focales des photos", command=self.toutesLesFocales)          
        menuOutils.add_command(label="Mettre à jour DicoCamera.xml", command=self.miseAJourDicoCamera)        
        menuOutils.add_separator()         
        menuOutils.add_command(label="Qualité des photos 'line'", command=self.OutilQualitePhotosLine)        
        menuOutils.add_command(label="Qualité des photos 'All' ", command=self.OutilQualitePhotosAll)
        
        # Paramètrage       

        menuParametres = tkinter.Menu(mainMenu,tearoff = 0)
        menuParametres.add_command(label="Afficher les paramètres", command=self.afficheParam)              ## Ajout d'une option au menu fils menuFile
        menuParametres.add_separator()         
        menuParametres.add_command(label="Associer le répertoire bin de MicMac'", command=self.repMicmac)   ## Ajout d'une option au menu fils menuFile
        menuParametres.add_command(label="Associer 'exiftool'", command=self.repExiftool)                   ## Exiftool : sous MicMac\bin-aux si Windows, mais sinon ???   
        menuParametres.add_command(label="Associer 'Meshlab' ou 'CloudCompare'", command=self.repMeslab)    ## Meslab   
      
        # Aide
        
        menuAide = tkinter.Menu(mainMenu,tearoff = 0)                                           ## menu fils : menuFichier, par défaut tearOff = 1, détachable
        menuAide.add_command(label="Pour commencer...", command=self.commencer)           
        menuAide.add_command(label="Aide", command=self.aide)           
        menuAide.add_command(label="Quelques conseils", command=self.conseils)         
        menuAide.add_command(label="A Propos", command=self.aPropos) 
        
        # ajout des items dans le menu principal :
        
        mainMenu.add_cascade(label = "Fichier",menu=menuFichier)
        mainMenu.add_cascade(label = "Edition",menu=menuEdition)        
        mainMenu.add_cascade(label = "MicMac",menu=menuMicMac)
        mainMenu.add_cascade(label = "Outils",menu=menuOutils)
        mainMenu.add_cascade(label = "Paramètrage",menu=menuParametres)        
        mainMenu.add_cascade(label = "Aide",menu=menuAide)
        
        # affichage du menu principal dans la fenêtre

        fenetre.config(menu = mainMenu)       
        
        # Fonction a éxécuter lors de la sortie du programme

        fenetre.protocol("WM_DELETE_WINDOW", self.quitter)

        # zone de test éventuel :

    #initialise les valeurs par défaut au lancement de l'outil
        
    def initialiseConstantes(self):
       


       # initialisation variables globales et propre au contexte local :

        self.repertoireScript           =   repertoire_script                                   # là où est le script et les logos cerema et IGN
        self.repertoireData             =   repertoire_data                                     # là ou l'on peut écrire des données
        self.systeme                    =   os.name                                             # nt ou posix
        self.version                    =   " V 1.55"
        self.nomApplication             =   os.path.splitext(os.path.basename(sys.argv[0]))[0]  # Nom du script
        self.titreFenetre               =   self.nomApplication+self.version                    # nom du programme titre de la fenêtre
        self.tousLesChantiers           =   list()                                              # liste de tous les réchantiers créés

        # Les 3 chemins utiles : mecmac\bin, meshlab et exiftool :  

        self.micMac                     =   'Pas de répertoire désigné pour MicMac\\bin'        # oar défaut il n'y a pas de répertoire micMac, sauf si restauration ligne suivante
        self.meshlab                    =   'Pas de fichier désigné pour ouvrir les .PLY'
        self.exiftool                   =   "Pas de chemin pour ExifTool"
        self.mm3d                       =   "Pas de fichier pour mm3d"

        # Les noms des fichiers xml

        self.masque3DSansChemin         =   "AperiCloud_selectionInfo.xml"                      # nom du fichier XML du masque 3D, fabriqué par 
        self.masque3DBisSansChemin      =   "AperiCloud_polyg3d.xml"                            # nom du second fichier XML pour le masque 3D
        self.dicoAppuis                 =   "Dico-Appuis.xml"                                   # nom du fichier XML des points d'appui (nom, X,Y,Z,incertitude) pour Bascule
        self.mesureAppuis               =   "Mesure-Appuis.xml"                                 # nom du XML positionnant les points d'appuis dans les photos
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
        
        # Les variables, Widgets et options de la boite à onglet :

        # Pour tapioca

        self.echelle1           = tkinter.StringVar()                # nécessaire pour définir la variable obtenue le widget
        self.echelle2           = tkinter.StringVar()
        self.echelle3           = tkinter.StringVar() 
        self.echelle4           = tkinter.StringVar()        
        self.delta              = tkinter.StringVar()
        self.file               = tkinter.StringVar()         
        self.modeTapioca        = tkinter.StringVar()
        self.modeMalt           = tkinter.StringVar()                          

        # Pour tapas :

        self.modeCheckedTapas = tkinter.StringVar()                   # nécessaire pour définir la variable obtenue par radiobutton
        self.arretApresTapas  = tkinter.IntVar()

        #pour la calibration

        self.distance           = tkinter.StringVar()

        # L'onglet :

        self.modeMalt           = tkinter.StringVar()
        
        self.onglets = ttk.Notebook(fenetre)                           # create Notebook in "master" : boite à onglet, supprimé par menageEcran() comme les frames
        
        #   tapioca : 400
        
        self.item400=ttk.Frame(self.onglets,borderwidth=5,height=50,relief='sunken',padding="0.3cm")        

        self.item401 = ttk.Radiobutton(self.item400, text="All",      variable=self.modeTapioca, value='All',     command=self.optionsTapioca)
        self.item402 = ttk.Radiobutton(self.item400, text="MulScale", variable=self.modeTapioca, value='MulScale',command=self.optionsTapioca)
        self.item403 = ttk.Radiobutton(self.item400, text="Line",     variable=self.modeTapioca, value='Line',    command=self.optionsTapioca)
        self.item404 = ttk.Radiobutton(self.item400, text="File",     variable=self.modeTapioca, value='File')
        self.item401.pack(anchor='w')
        self.item402.pack(anchor='w')
        self.item403.pack(anchor='w')
        self.item404.pack(anchor='w')
        self.item404.state(['disabled'])                # dans cette version de l'outil

        # tapioca Echelle 1
        
        self.item480  = ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")        
        self.item481  = ttk.Label(self.item480, text="Echelle image (-1 pour l'image entière) :")
        self.item482  = ttk.Entry(self.item480,textvariable=self.echelle1)
        self.item481.pack()
        self.item482.pack()

        # tapioca Echelle2 (MultiScale)

        self.item460=ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")        
        self.item461=ttk.Label(self.item460, text="Echelle image réduite : ")
        self.item462=ttk.Entry(self.item460,textvariable=self.echelle2)
        self.item461.pack()
        self.item462.pack()
        self.item463=ttk.Label(self.item460, text="Seconde Echelle (-1 pour l'image entière) :")
        self.item464=ttk.Entry(self.item460,textvariable=self.echelle3)
        self.item463.pack()
        self.item464.pack()
        
        # tapioca Delta

        self.item470=ttk.Frame(self.item400,height=50,relief='sunken',padding="0.3cm")
        self.item471=ttk.Label(self.item470, text="Echelle image (-1 pour l'image entière) :")
        self.item472=ttk.Entry(self.item470,textvariable=self.echelle4)
        self.item473=ttk.Label(self.item470, text="Delta (nombre d'images se recouvrant, avant et après) : ")
        self.item474=ttk.Entry(self.item470,textvariable=self.delta)
        self.item471.pack()
        self.item472.pack()
        self.item473.pack()
        self.item474.pack()


        #   Tapas : 500
        
        self.item500=ttk.Frame(self.onglets,height=150,relief='sunken',padding="0.3cm")                               
        modesTapas=[('RadialExtended','RadialExtended','active'),('RadialStd','RadialStd','active'),('RadialBasic','RadialBasic','active'),
                    ('Fraser','Fraser','disabled'),('FraserBasic','FraserBasic','disabled'),('FishEyeEqui','FishEyeEqui','disabled'),
                    ('HemiEqui','HemiEqui','disabled'),('AutoCal','AutoCal','disabled'),('Figee','Figee','disabled')]        # déconnexion texte affichée, valeur retournée
        for t,m,s in modesTapas:
            b=ttk.Radiobutton(self.item500, text=t, variable=self.modeCheckedTapas, value=m)
            b.pack(anchor='w')
            b.state([s])       
        self.modeCheckedTapas.set('RadialExtended')                  # valeur par défaut nécessaire pour définir la variable obtenue par radiobutton    
        self.item510 = ttk.Frame(self.item500,height=50,relief='sunken',padding="0.3cm")      # pour le check button, fera un encadrement       
        self.item511 = ttk.Checkbutton(self.item510, variable=self.arretApresTapas, text="Arrêter le traitement après TAPAS")
        self.item511.pack()
        self.item510.pack()         

        
        # Calibration : 950
        
        self.item950 = ttk.Frame(  self.onglets,
                                   height=5,
                                   relief='sunken')

        # Cadre définition des axes :
        
        self.item960 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")
        
        self.item961 = ttk.Label(self.item960,
                                  text='Choisir entre :')
        
        self.item962 = ttk.Button(self.item960,
                                  text='Ligne horizontale',
                                  command= self.ligneHorizontale)            

        self.item963 = ttk.Label(self.item960,
                                  text='ou')        

        self.item964 = ttk.Button(self.item960,
                                  text='Ligne verticale',
                                  command= self.ligneVerticale)

        self.item961.pack(ipadx=5,padx=5,ipady=2)
        self.item962.pack(side='left',ipadx=15,padx=5)        
        self.item963.pack(side='left',padx=5)
        self.item964.pack(side='left',ipadx=5)
        
        self.item960.pack(padx=5,pady=10,ipady=2,ipadx=15)
        
        # conjonction de coordination :
        
        self.item965 = ttk.Frame(  self.item950)
        self.item966 = ttk.Label(self.item965,text='ET :')
        self.item966.pack()
        self.item965.pack()
        
        #cadre définition des plans :

        self.item970 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")
        
        self.item971 = ttk.Label(self.item970,
                                  text='Choisir entre :')
        
        self.item972 = ttk.Button(self.item970,
                                  text='Zone plane horizontale',
                                  command= self.planHorizontal)   

        self.item973 = ttk.Label(self.item970,
                                  text='ou') 

        self.item974 = ttk.Button(self.item970,
                                  text='Zone plane verticale',
                                  command= self.planVertical)
        
        self.item971.pack(ipadx=5,padx=5,ipady=2)               
        self.item972.pack(side='left',ipadx=15,padx=5)        
        self.item973.pack(side='left',padx=5)
        self.item974.pack(side='left',ipadx=5)
        self.item970.pack(padx=5,pady=10,ipady=2,ipadx=15)
        
        # conjonction de coordination :
        
        self.item975 = ttk.Frame(self.item950)
        self.item976 = ttk.Label(self.item975,text='ET :')
        self.item976.pack()            
        self.item975.pack()
        
        # Cadre pour la distance entre 2 points :

        self.item980 = ttk.Frame(  self.item950,
                                   height=5,
                                   relief='sunken',
                                   padding="0.3cm")        
        self.item981 = ttk.Label(self.item980,
                                  text='Distance entre les 2 points :')        

        self.item982 = ttk.Entry(self.item980,textvariable=self.distance)          # distance

        self.item983 = ttk.Button(self.item980,
                                  text='Placer 2 points identiques sur 2 photos',
                                  command= self.placer2Points)

        self.item981.pack()
        self.item982.pack()
        self.item983.pack(pady=10)
        self.item980.pack()

        self.item990 = ttk.Frame(  self.item950,
                                   relief='sunken') 
        self.item991 = ttk.Label(self.item990,text='\nPour annuler la calibration mettre la distance = 0')       
        self.item991.pack()
        
        # Malt 

        self.item700 = ttk.Frame(self.onglets,height=5,relief='sunken',padding="0.3cm")                      
 
        self.modesMalt=[('Ortho pour orthophotos','Ortho'),('UrbanMNE pour photos urbaine','UrbanMNE'),('GeomImage pour photos du sol','GeomImage')]
        for t,m in self.modesMalt:
            b=ttk.Radiobutton(self.item700, text=t, variable=self.modeMalt, value=m)
            b.pack(anchor='w')
            if self.modesMalt==m:
                b.state(['selected'])
                self.modeMalt.set(m)                        # positionne la valeur initiale sélectionnée
                
        self.item710=ttk.Frame(self.item700,height=50,relief='sunken',padding="0.2cm")      # pour le check button, fera un encadrement
        self.item701=ttk.Label(self.item710,text="image maitresse = ")
        self.item702=ttk.Button(self.item710,text="Choisir l'image maîtresse",command=self.imageMaitresse)
        self.item703=ttk.Label(self.item710,text="Pas de masque.")
        self.item704=ttk.Button(self.item710,text='Tracer le masque',command=self.traceMasque) 
        self.item705=ttk.Label(self.item700,text="Attention :\nLe masque 3D de C3DC a la priorité sur Malt\nTracer le masque supprime le masque précédent")
        self.item701.pack()        
        self.item702.pack(ipady=2,pady=10)
        self.item703.pack()                
        self.item704.pack(ipady=2,pady=10)
        self.item705.pack()    
        self.item710.pack(pady=15)
       
        
        # C3DC
        
        self.item800 = ttk.Frame(self.onglets,height=5,relief='sunken',padding="0.3cm")
       
        self.item801 = ttk.Button(self.item800,text='Tracer le masque 3D sur le nuage AperiCloud',command=self.affiche3DApericloud)              
        self.item801.pack(ipady=2,pady=10)
        self.item802 = ttk.Label(self.item800, text= "Tapas doit avoir créé un nuage de points.\n\n"+\
                                                   "Dans l'outil : \n"+\
                                                   "Définir le masque : F9 \n"+\
                                                   "Ajouter un point : clic gauche\n"+\
                                                   "Fermer le polygone : clic droit\n"+\
                                                   "Sélectionner : touche espace\n"+\
                                                   "Sauver le masque : Ctrl S.\n"+
                                                   "Quitter : Ctrl Q.\n\n"+
                                                   "Supprimer le masque : Ctrl Q (sans saisie préalable).\n\n"+                               
                                                   "Attention : C3DC a la priorité sur le masque 2D de Malt")
        self.item802.pack(ipady=2,pady=10)

 
        #Ajout des onglets dans la boite à onglet :
        
        self.onglets.add(self.item400,text="Tapioca")               # add onglet to Notebook        
        self.onglets.add(self.item500,text="Tapas")                 # add onglet to Notebook
        self.onglets.add(self.item950,text="Calibration")           # add onglet to Notebook
        self.onglets.add(self.item700,text="Malt")
        self.onglets.add(self.item800,text="C3DC")


        # boutons  généraux à la boite à onglet :

        self.item450 = ttk.Frame(fenetre)                           # frame pour bouton de validation, permet un ménage facile
        self.item451 = ttk.Button(self.item450,
                                text=' Valider les options',
                                command=self.finOptionsOK)          # bouton permettant de tout valider
        self.item452 = ttk.Button(self.item450,
                                text=' Annuler',
                                command=self.finOptionsKO)          # bouton permettant de tout annuler
        
        # les 2 boutons globaux :
   
        self.item451.pack(side='left')
        self.item452.pack(side='left')

        # La boite de dialogue pour demander les dimensions du capteur de l'appareil photo

        self.item1000 = ttk.Frame(fenetre)
        self.item1001 = ttk.Label(self.item1000)
        self.item1002 = ttk.Label(self.item1000,
                                  text= "Indiquer les dimensions du capteur, en mm.\n"+\
                                        "par exemple :\n\n                                  5.7  7.6  \n\n"+\
                                        "Le site :\n \http://www.dpreview.com/products\n"+\
                                        "fournit les dimensions de tous les appareils photos.")
        self.item1003 = ttk.Entry(self.item1000)
        self.item1004 = ttk.Button(self.item1000,
                                text=' Valider',
                                command=self.dimensionCapteurOK)          # bouton permettant de tout valider
        self.item1005 = ttk.Button(self.item1000,
                                text=' Annuler',
                                command=self.dimensionCapteurKO)          # bouton permettant de tout annuler
        self.item1001.pack(pady=15)
        self.item1002.pack(pady=15)
        self.item1003.pack(pady=15)
        self.item1004.pack(pady=15)
        self.item1005.pack(pady=15)
        
        # Les fichiers XML :

    # fichier XML de description du masque

        self.masqueXML                  =   (   '<?xml version="1.0" ?>\n'+
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
    
    # Fichier de persistance des paramètres
        
        self.paramChantierSav           =   'ParamChantier.sav'
        self.fichierParamMicmac         =   os.path.join(self.repertoireData,'ParamMicmac.sav')       # sauvegarde des paramètres globaux d'AperodeDenis
        self.fichierParamChantierEnCours=   os.path.join(self.repertoireData,self.paramChantierSav)   # pour les paramètres du chantier en cours


    # Divers

        self.logoCerema                 =       os.path.join(self.repertoireScript,'logoCerema.jpg')
        self.logoIGN                    =       os.path.join(self.repertoireScript,'logoIGN.jpg')
        self.messageNouveauDepart       =       str()   # utilisé lorsque l'on relance la fenêtre
        self.nbEncadre                  =       0       # utilisé pour relancer la fenetre

    ####################### initialiseValeursParDefaut du défaut : On choisit de nouvelles photos : on oublie ce qui précéde, sauf les paramètres généraux de aperodedenis (param micmac)
       
    def initialiseValeursParDefaut(self):

    # Numéro du chantier : pour indicer le numéro du répertoire de travail : un nouveau est créé à chaque éxécution
    
        try: self.indiceTravail         +=   1                         # on incrémente s'il existe
        except: self.indiceTravail      =   1                           # sinon met à 1 sinon
        
    # le chantier : variable self.etatDuChantier
    
    # 0 : en cours de construction, pas encore de photos
    # 1 : photos saisies, répertoire origine fixé, non modifiable
    # 2 : chantier enregistré
    # 3 : micmac lancé, pendant l'exécution de Tapioca et tapas
    # 4 : arrêt aprés tapas et durant malt en cours d'exécution
    # 5 : malt terminé
    # 6 : rendu modifiable aprés une première exécution
    # - 1 : en cours de suppression
        
        self.etatDuChantier             =   0

    # La sauvegarde : self.etatSauvegarde
    # ""  : lorsque le chantier est sauvegardé sous son répertoire de travail, l'exécution de micMac sauve le chantier
    # "*" : lors de sa création avant sauvegarde et lorsque le chantier a été modifié par l'utilisateur.

        self.etatSauvegarde             =   ""                                                 # Indicateur du caractère sauvegardé ("") ou à sauvegarder ("*") du chantier. utile pour affichage title fenetre
            
    # les photos :


    
        self.repertoireDesPhotos        =   'Pas de répertoire pour les photos'
        self.photosAvecChemin           =   list()                                              # liste des noms des fichiers photos avec chemin complet
        self.photosSansChemin           =   list()                                              # nom des photos sans le chemin
        self.photosPropresAvecChemin    =   list()                                              # les photos propres = photos à copier : on remplace les photos "sales" par les "propres" (nettoyées)            
        self.lesExtensions              =   str()                                               # l'utilisateur pourrait sélectionner des photos avec des extensions différentes
        self.repTravail                 =   self.repertoireData                                 # répertoire ou seront copiés les photos et ou se fera le traitement,Pour avoir un répertoire valide au début
        self.chantier                   =   str()                                               # nom du chantier (répertoire sosu le répertoire des photos)
        self.extensionChoisie           =   str()                                               # extensions des photos (actuellement JPG obligatoire)
        
    # Malt : Mode, Maitre et Masque :

        self.modeMalt.set('GeomImage')
        self.masque                     =   str()                                               # nom du fichier image représentant le masque sur l'image maitresse
        self.masqueSansChemin           =   str()                                               # image masque : en TIF, choisi par l'utilisateur       
        self.masqueSansCheminProvisoire =   str()
        self.maitre                     =   str()        
        self.maitreSansChemin           =   str()                                               # image maitresse
        self.maitreSansCheminProvisoire =   str()
        self.item701.config(text="Pas d'image maitresse.")
        self.item703.config(text="Pas de masque")                                               # réinitialise le masque        
        self.maitreCommentaire          =   str()                                               # indique si l'image maitresse est choisie automatiquement
        self.fichierMasqueXML           =   str()                                               # nom du fichier XML décrivant le masque
        self.nomMaitreSansExtension     =   str()
        self.monImage_MaitrePlan        =   str()                                               # Nom de l'image maitresse du plan repere (sans extension)
        self.monImage_PlanTif           =   str()                                               # nom du masque correspondant
        self.planProvisoireHorizontal   =   "planHorizontal.tif"
        self.planProvisoireVertical     =   "planVertical.tif"
        
        # mieux que Mic Mac qui prend par défaut le masque de l'image maitre avec le nom prédéfini masq
                                               

    # Tapioca

        self.modeTapioca.set('MulScale')
        self.echelle1.set('500')        
        self.echelle2.set('500')
        self.echelle3.set('1500')        
        self.echelle4.set('1500')        
        self.delta.set(1)

    # TAPAS

        self.modeCheckedTapas.set('RadialExtended')
        self.arretApresTapas.set(1)                                                   # 1 : on arrête le traitement après Tapas, 0 on poursuit

    # Malt

        self.modeMalt.set('GeomImage')
            
    # Calibration

        self.listePointsGPS             =   list()                      # 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
        self.idPointGPS                 =   0				# identifiant des points, incrémenté de 1 a chaque insertion
        self.dicoPointsGPSEnPlace       =   dict()                      # dictionnaire des points GPS placés dans les photos (créé par la classe CalibrationGPS)
        self.dicoLigneHorizontale       =   dict()                      # les deux points de la ligne horizontale (sur 2 photos)              
        self.dicoLigneVerticale         =   dict()                      # les 2 points décrivant une ligne horizontale
        self.dicoCalibre                =   dict()                      # les 2 points décrivant un segment de longueur donnée
        
    # pour la trace :
    
        self.lignePourTrace             =   str()
        self.ligneFiltre                =   str()
        self.TraceMicMacComplete        =   str()
        self.TraceMicMacSynthese        =   str()
        self.fichierParamChantier       =   ""                                  #fichier paramètre sous le répertoire du chantier
        
    # divers 

        self.messageSiPasDeFichier      =   1                                   #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        if self.systeme=="posix":                                               #  dépend de l'os, mais valeur par défaut nécessaire
            self.shell                  =   False
        if self.systeme=="nt": 
            self.shell                  =   True                                

    ################# Le Menu FICHIER : Ouvre un nouveau chantier avec les valeurs par défaut, ouvre un chantier existant, enregistrer, renommer, supprimer
        
    def nouveauChantier(self):                                                  # on conserve : micMac,meshlab,tousLesRepertoiresDeTravail
        texte=""
        if self.etatDuChantier == 1 :
            if self.deuxBoutons("Enregistrer le chantier ?",
                                "Chantier non encore enregistré. Voulez-vous l'enregistrer ?",
                                "Enregistrer",
                                "Ne pas enregistrer.") == 0:
                self.enregistreChantier()
                texte="Chantier précédent enregistré : "+self.chantier+"\n"
            
        if self.etatDuChantier >= 2 and self.etatSauvegarde =="*":
            if self.deuxBoutons("Enregistrer le chantier "+self.chantier+" ?",
                                "Chantier modifé depuis la dernière sauvegarde. Voulez-vous l'enregistrer ?",
                                "Enregistrer",
                                "Ne pas enregistrer.") == 0:
                self.copierParamVersChantier()
                texte = "Chantier précédent enregistré : "+self.chantier+"\n"                
        self.initialiseValeursParDefaut()                           
        os.chdir(self.repTravail)                                               # lors de la création d'un chantier il s'agir du répertoire de l'appli
        self.afficheEtat(texte)
        
            
    def ouvreChantier(self):
        texte=""
        if self.etatDuChantier == 1 :
            if self.deuxBoutons("Enregistrer le chantier ?",
                                "Chantier non encore enregistré. Voulez-vous l'enregistrer ?",
                                "Enregistrer",
                                "Ne pas enregistrer.") == 0:
                self.enregistreChantier()
                texte="Chantier précédent enregistré : "+self.chantier+"\n"
        if self.etatDuChantier >= 2 and self.etatSauvegarde =="*":
            if self.deuxBoutons("Enregistrer le chantier "+self.chantier+" ?",
                                "Chantier modifé depuis la dernière sauvegarde. Voulez-vous l'enregistrer ?",
                                "Enregistrer",
                                "Ne pas enregistrer.") == 0:
                self.copierParamVersChantier()
                texte="Chantier précédent enregistré : "+self.chantier+"\n"
                
        bilan = self.choisirUnRepertoire("Choisir un chantier.")                # boite de dialogue de sélection du chantier à ouvrir, renvoi : self.selectionRepertoireAvecChemin
        if bilan!=None:
            self.afficheEtat("Aucun chantier choisi.\n"+bilan+"\n")
            return   
        self.fichierParamChantier  =   self.selectionRepertoireAvecChemin+os.sep+self.paramChantierSav         
        if os.path.exists(self.fichierParamChantier):        
            self.restaureParamChantier(self.fichierParamChantier)
            self.etatSauvegarde = ""            
            self.sauveParam()                                                   # pour assurer la cohérence entre le chantier en cours et le chantier ouvert (écrase le chantier en cours)
            self.afficheEtat(texte)
        else:
            self.encadre ('Chantier choisi "'+self.selectionRepertoireAvecChemin+'" corrompu. Abandon.')


    def enregistreChantier(self):               # Correspond simplement à la copie du fichier paramètre sous le répertoire de travail et à l''apparition du nom
        if self.etatDuChantier == 0:		# pas de photo : pas d'enregistrement
            self.encadre("Indiquer les photos à traiter avant d'enregistrer le chantier.")
            return
        if self.etatDuChantier == 1:		# des photos, pas encore enregistré : on mote l'enregistrement : etat = 2
            self.etatDuChantier = 2
        self.copierParamVersChantier()          # on enregistre, ou on réenregistre 

    def renommeChantier(self):
        if self.etatDuChantier==0:
            self.encadre("Le chantier est en cours de définition.\nIl n'a pas encore de nom, il ne peut être renommé.\n\nCommencer par choisir les photos")
            return                        
        texte = "Nouveau nom pour le chantier "+self.chantier+" :\n"
        bas = "Un chemin, absolu ou relatif, est un nom valide\n\nAucun fichier de l'arborecence du chantier ne soit être ouvert."
        if self.etatSauvegarde=="*":
            bas = bas+"\nLe chantier, actuellement modifié, sera enregistré."
        new = MyDialog(fenetre,texte,basDePage=bas)
        if new.saisie!="":
            nouveauRepertoire = os.path.join(self.repertoireDesPhotos,new.saisie)
            if os.path.splitdrive(nouveauRepertoire)[0].upper()!=os.path.splitdrive(self.repTravail)[0].upper():
                self.encadre("Le nom \n\n"+new.saisie+"\n\nimplique un changement de disque.\nCette version ne permet pas cette opération.")
                return 
            if os.path.exists(nouveauRepertoire):
                self.encadre("Le nom \n"+new.saisie+"\npour le chantier est déjà utilisé.\nChoississez un autre nom.")
                return               
            self.fermerVisuPhoto()                                                      # fermer tous les fichiers potentiellement ouvert.
            os.chdir(self.repertoireData)                                             # quitter le répertoire courant
            try:
                self.meshlabExe1.kill()
                time.sleep(0.1)
            except: pass                                                                # fermer meshlab si possible
            try:
                self.meshlabExe2.kill()
                time.sleep(0.1)
            except: pass        
            try:
                time.sleep(0.1)
                os.rename (self.repTravail,nouveauRepertoire)                               # RENOMMER
            except Exception as e:
                self.encadre("Le renommage du chantier ne peut se faire actuellement,\nsoit le nom fourni est incorrect,\n"+
                             "soit un fichier du chantier est ouvert par une autre application.\n"+
                             "soit l'explorateur explore l'arborescence.\nerreur : \n\n"+str(e))
                return
            self.tousLesChantiers.remove(self.repTravail)                               # retirer de la liste des répertoires de travail
            ajout(self.tousLesChantiers,nouveauRepertoire)                              # ajouter le nouveau
            ancienChantier = self.chantier 
            self.repTravail = nouveauRepertoire                                         # maj des paramètres

            #redéfinir les chemins des images maitre et masques
            
            if self.maitre!=str():
                self.maitre                 = os.path.join(self.repTravail,self.maitreSansChemin)
            if self.masque!=str():
                self.masque                 = os.path.join(self.repTravail,self.masqueSansChemin)
            if self.fichierMasqueXML!=str():
                self.fichierMasqueXML       = os.path.join(self.repTravail,os.path.basename(self.fichierMasqueXML))
            if self.monImage_MaitrePlan!=str():
                self.monImage_MaitrePlan    = os.path.join(self.repTravail,os.path.basename(self.monImage_MaitrePlan))
                self.monImage_PlanTif       = os.path.join(self.repTravail,os.path.basename(self.monImage_PlanTif))

            self.photosPropresAvecChemin    = [os.path.join(self.repTravail,os.path.basename(e)) for e in self.photosPropresAvecChemin]
            
            # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y          
            dico=dict()
            for  e in self.dicoPointsGPSEnPlace.keys():
                f = (e[0],os.path.join(self.repTravail,os.path.basename(e[1])),e[2])
                dico[f]=self.dicoPointsGPSEnPlace[e]
            self.dicoPointsGPSEnPlace = dict(dico)

            # axe horizontal, dans le dico : self.dicoLigneHorizontale. key = nom point, photo, identifiant ;Retrouver nom de la photo, coordonnées des points
            # items = liste de tuple (key,values) soit tuple = (point,photo, id),(x1,y1)
           
            dico=dict()
            for  e in self.dicoLigneHorizontale.keys():
                f = (e[0],os.path.join(self.repTravail,os.path.basename(e[1])),e[2])
                dico[f]=self.dicoLigneHorizontale[e]
            self.dicoLigneHorizontale = dict(dico)           
            dico=dict()
            for  e in self.dicoLigneVerticale.keys():
                f = (e[0],os.path.join(self.repTravail,os.path.basename(e[1])),e[2])
                dico[f]=self.dicoLigneVerticale[e]
            self.dicoLigneVerticale = dict(dico)           
            dico=dict()
            for  e in self.dicoCalibre.keys():
                f = (e[0],os.path.join(self.repTravail,os.path.basename(e[1])),e[2])
                dico[f]=self.dicoCalibre[e]
            self.dicoCalibre = dict(dico)
            
            self.chantier = new.saisie
            self.definirFichiersTrace()                                                 #positionne sous le répertoire de travail
            self.copierParamVersChantier()                                              # sauve param puis copie on enregistre, ou on réenregistre
            self.afficheEtat("Chantier :\n"+ancienChantier+"\nrenommé en :\n"+self.chantier+"\n")
            
    def copierParamVersChantier(self):                                                  # copie du fichier paramètre sous le répertoire du chantier, pour rejouer et trace
        try:
            self.etatSauvegarde = ""                                                    # Pour indiquer que le chantier sauvegardé sous le répertoire du chantier
            self.sauveParam()
            try: shutil.copy(self.fichierParamChantierEnCours,self.repTravail)        # pour éviter de copier un fichier sur lui même
            except Exception as e: print("erreur copie : ",self.fichierParamChantierEnCours," vers ",self.repTravail," erreur=",str(e))
            fenetre.title(self.etatSauvegarde+self.titreFenetre)            
        except Exception as e:
            self.ajoutLigne("Erreur lors de la copy du fichier paramètre chantier \n"+self.fichierParamChantierEnCours+"\n vers \n"+self.repTravail+"\n erreur : \n"+str(e))


    ################################## LE MENU EDITION : afficher l'état, les photos, lire une trace, afficher les nuages de points ############################
                                                
    def afficheEtat(self,entete="",finale=""):
        self.sauveParam()
        nbPly = 0
        photosSansCheminDebutFin = list(self.photosSansChemin)
        if len(self.photosSansChemin)>5:
            photosSansCheminDebutFin =photosSansCheminDebutFin[:2]+list('..',)+photosSansCheminDebutFin[-2:]
        try:                                                                    # rappel des valeurs par défauts (try car erreur si le format de la sauvegarde a changé cela plante) :
            texte = entete+'\nRépertoire des photos : \n'+afficheChemin(self.repertoireDesPhotos)
            if len(self.photosSansChemin)==0:
               texte = texte+'\n\n'+'Aucune photo sélectionnée.\n'              
            if len(self.photosSansChemin)>=1:                                   # Il ne peut en principe pas y avoir une seule photo sélectionnée 
               texte = texte+'\n\n'+str(len(self.photosSansChemin))+' photos sélectionnées : \n' +\
                         '\n'.join(photosSansCheminDebutFin)+finale
            if self.nombreDExtensionDifferentes(self.photosSansChemin)>1:       # il y a plus d'un format de photo !
                texte = texte+'\n\nATTENTION : plusieurs extensions différentes dans les photos choisies !\n Le traitement ne se fera que sur un type de fichier.'

            # Options pour Tapioca :

            if self.modeTapioca.get()!='':
                texte = texte+'\n\nTapioca :\nMode : '+self.modeTapioca.get()+'\n'
            if self.modeTapioca.get()=="All":
                texte = texte+'Echelle 1 : '+self.echelle1.get()+'\n'
            if self.modeTapioca.get()=="MulScale":
                texte = texte+'Echelle 1 : '+self.echelle2.get()+'\n'
                texte = texte+'Echelle 2 : '+self.echelle3.get()+'\n'
            if self.modeTapioca.get()=="Line":
                texte = texte+'Echelle : '+self.echelle4.get()+'\n'
                texte = texte+'Delta : '+self.delta.get()+'\n'


            # Options pour Tapas :
            
            if self.modeCheckedTapas.get()!='':
                texte = texte+'\nTapas :\nMode : '+self.modeCheckedTapas.get()+'\n'
            if self.arretApresTapas.get()==1:
                texte = texte+'Arrêt demandé après Tapas\n'

            # Calibration

            if self.controleCalibration():
                texte = texte+'\nCalibration présente\n'+self.etatCalibration
            else:
                if self.distance.get()=='0':
                    texte = texte+'\nCalibration annulée : distance=0\n'
                elif self.etatCalibration!=str():             # calibration incomplète
                    texte = texte+"\nCalibration incomplète :\n"+self.etatCalibration+"\n"   

            # Points GPS
            
            if self.controlePointsGPS():
                 texte = texte+self.etatPointsGPS
                 
            # Masque 3D pour D3DC ou alors Malt et image maitresse et masque :
            malt = True                                                             # a priori on éxécute malt
            if self.mm3dOK:                                                         # La version de MicMac autorise les masques 3D
                if self.existeMasque3D():
                    texte = texte+'\nC3DC : Masque 3D\n'
                    malt = False                                                    # on éxécutera C3DC
            else:
                texte = texte + "\nLa version installée de Micmac n'autorise pas les masques en 3D\n"

            if malt:
                if self.maitreSansChemin!='':
                    texte = texte+'\nMalt :\nMode : '+self.modeMalt.get()+'\nImage maitresse : '+self.maitreSansChemin
                else:
                    texte = texte+'\nMalt :\nMode : '+self.modeMalt.get()+"\nPas d'image maitresse."
                if self.masqueSansChemin!='':
                    texte = texte+'\nMasque : '+self.masqueSansChemin+'\n'
                else:
                    texte = texte+"\nPas de masque.\n"
                    
            # état du chantier :
            
            if self.etatDuChantier == 0:                                        # pas encore de chantier
                texte = texte+"\nChantier en cours de définition.\n"               
            if self.etatDuChantier >= 1:                                        # le chantier est créé : il y a des photos choisies (2 enregistré,
                                                                                # 3 en cours d'exécution,
                                                                                # 4 arrêt tapas, 5 terminé, 6 modifiable mais n'existe plus)
                texte = texte+"\nChantier : "+self.chantier+".\n"
            else:
                texte = texte+"\nChantier en attente d'enregistrement.\n"
            if self.etatDuChantier in (2,6) and self.etatSauvegarde=="":		
                texte = texte+"\nChantier enregistré.\n"
            if self.etatDuChantier==2:		
                texte = texte+"Chantier modifiable.\n"                
            if self.etatDuChantier == 3:		
                texte = texte+"\nChantier interrompu.\nRelancer micmac.\n"                      
            if self.etatDuChantier == 4:		
                texte = texte+"Arrêté aprés Tapas.\n"
            if self.etatDuChantier == 5:		
                texte = texte+"Chantier terminé.\n"
            if self.etatDuChantier == 6:		
                texte = texte+"\nChantier exécuté puis débloqué.\n"

            # Résultat des traitements :
            
              
            if os.path.exists('AperiCloud.ply'):
               texte = texte+"Nuage de point non densifié généré après Tapas.\n"
               nbPly=1
            if os.path.exists('modele3D.ply'):
               texte = texte+"Nuage de point densifié généré après Malt ou C3DC.\n"
               nbPly+=1
            if self.etatDuChantier in (4,5,6) and nbPly==0:
               texte = texte+"Aucun nuage de point généré.\n"

            # Affichage :
            os.chdir(self.repTravail) 
            self.encadre(texte,nouveauDepart='oui')
            
        except Exception as e:
            texte = "Les caractéristiques du chantier précédent \n"+self.chantier+"\n n'ont pas pu être lues correctement.\n"+\
                    "Le fichier des paramètres est probablement incorrect.\n"+\
                    "Un nouveau chantier a été ouvert afin de débloquer la situation.\n"+\
                    "Désolé pour l'incident.\n\n"+\
                    "Erreur : "+str(e) +"\n"+texte                        
            self.initialiseValeursParDefaut()
            os.chdir(self.repTravail)             
            self.encadre(texte,nouveauDepart='oui')
           
        
    def existeMasque3D(self):
        if self.repTravail==self.repertoireData:
            return False
        self.masque3D = os.path.join(self.repTravail,self.masque3DSansChemin)        
        if os.path.exists(self.masque3D):
            return True
        else:
            return False
        
    def existeMaitre2D(self):
        if self.repTravail==self.repertoireData:
            return False        
        if os.path.exists(self.maitre) and str(self.modeMalt.get())=="GeomImage":
            return True        
        if str(self.modeMalt.get())!="GeomImage":    # pas besoin d'image maitresse !
            return True
        else:                                       # le mode est geomimage et il n'y a pas d'image maitre
            return False      
        
    def afficherToutesLesPhotos(self):
        self.choisirUnePhoto(self.photosAvecChemin,
                             titre='Toutes les photos',
                             mode='single',
                             message="Toutes les photos",
                             messageBouton="Fermer")

    def afficherLesPointsGPS(self):
        photosAvecPointsGPS = [ e[1] for e in self.dicoPointsGPSEnPlace.keys() ]    # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
        if photosAvecPointsGPS.__len__()==0:
            self.encadre("Aucun point GPS saisi.")
            return
        self.choisirUnePhoto(photosAvecPointsGPS,
                             titre='Affichage des photos avec points GPS',
                             mode='single',
                             message="seules les photos avec points sont montrées.",
                             messageBouton="Fermer",
                             dicoPoints=self.dicoPointsGPSEnPlace)
        
    def afficherMasqueEtMaitre(self):
        if os.path.isfile(self.masque) and os.path.isfile(self.maitre)>0:
            masqueEtMaitre = [self.masque,self.maitre]
            self.choisirUnePhoto(masqueEtMaitre,
                                 titre="Visualiser l'image maitresse et le masque 2D",
                                 mode='single',
                                 message="Répertoire : \n"+os.path.dirname(self.maitre),
                                 messageBouton="Fermer")           
        else:
            self.encadre("Pas de masque 2D défini pour ce chantier")

    def afficheMasqueC3DC(self):
        if self.existeMasque3D()==False:
            self.encadre("Pas de masque 3D pour ce chantier.")
            return
        os.chdir(self.repTravail)
        
        self.topMasque3D = tkinter.Toplevel(relief='sunken')
        fenetreIcone(self.topMasque3D)           
        self.item900 = ttk.Frame(self.topMasque3D,height=5,relief='sunken',padding="0.3cm")        
        self.item901 = ttk.Button(self.item900,text='Visaliser le masque 3D',command=self.affiche3DApericloud)              
        self.item901.pack(ipady=2,pady=10)
        self.item903 = ttk.Button(self.item900,text='Fermer',command=lambda : self.topMasque3D.destroy())              
        self.item903.pack(ipady=2,pady=10)        
        self.item902 = ttk.Label(self.item900, text= "Affichage du masque 3D :\n\n"+\
                                                   "Les points blancs du nuage sont dans le masque\n"+\
                                                   "Ce masque C3DC a la priorité sur le masque 2D de Malt\n\n"+
                                                    "ATTENTION : FERMER la fenêtre 3D pour continuer")
        self.item902.pack(ipady=2,pady=10)        
        
        
        self.item900.pack()                                   
        fenetre.wait_window(self.topMasque3D)

    def afficherZonePlane(self):
        if len(self.monImage_MaitrePlan)>0:
            masqueEtMaitre = [self.monImage_PlanTif,self.monImage_MaitrePlan]
            if self.monImage_PlanTif==self.planProvisoireHorizontal:
                plan = "horizontale"
            else:
                plan = "verticale"
            self.choisirUnePhoto(masqueEtMaitre,
                                 titre="Visualiser l'image maitresse et le plan horizontal ou vertical",
                                 mode='single',
                                 message="Zone plane "+plan,
                                 messageBouton="Fermer")            
        else:
            self.encadre("Pas de plan horizontal ou vertical défini pour ce chantier")

    def afficherLigneHV(self):        
        photosAvecLigneH = [ e[1] for e in self.dicoLigneHorizontale.keys() ]
        photosAvecLigneV = [ e[1] for e in self.dicoLigneVerticale.keys() ]
        photosAvecLigne = list(set(photosAvecLigneH+photosAvecLigneV))
        dicoAvecLigne = dict()
        sens = str()
        for e in self.dicoLigneHorizontale:
            dicoAvecLigne[e] = self.dicoLigneHorizontale[e]
            sens = "HORIZONTALE"
        for e in self.dicoLigneVerticale:
            dicoAvecLigne[e] = self.dicoLigneVerticale[e]
            sens = "VERTICALE"
        if photosAvecLigne.__len__():    
            self.choisirUnePhoto(photosAvecLigne,
                                 titre='Affichage des photos avec ligne horizontale ou verticale',
                                 mode='single',
                                 message="ligne "+sens,
                                 messageBouton="Fermer",
                                 dicoPoints=dicoAvecLigne)
        else:
            self.encadre("Pas de ligne horizontale ou verticale définie pour ce chantier")            

    def afficherDistance(self):
        if self.distance.get()==str():
            self.encadre("Pas de distance définie pour ce chantier.")
        else:
            photosAvecDistance = list(set([ e[1] for e in self.dicoCalibre.keys() ]))
            self.choisirUnePhoto(photosAvecDistance,
                                 titre="Visualiser les photos avec distance",
                                 mode='single',
                                 message="Valeur de la distance : "+self.distance.get(),
                                 messageBouton="Fermer",
                                 dicoPoints=self.dicoCalibre)           

    def lectureTraceMicMac(self,complete=True):

        if self.pasDePhoto():return
          
        if complete:
            fichier = self.TraceMicMacComplete
        else:
            fichier = self.TraceMicMacSynthese
        os.chdir(self.repTravail)
        if os.path.exists(fichier):
            self.cadreVide()            
            trace=open(fichier,"r")
            contenu=trace.read()
            trace.close
            self.ajoutLigne(contenu)
            self.texte201.see("1.1")            
        else:
            texte = "Pas de trace de la trace !"
            self.encadre(texte)
            
    def lectureTraceSynthetiqueMicMac(self):
        self.lectureTraceMicMac(complete=False)

    def afficheApericloud(self):
        retour = self.lanceApericloudMeshlab()
        if retour == -1:
            self.encadre("Pas de nuage de points aprés Tapas.")
        if retour == -2:
            self.encadre("Programme pour ouvrir les .PLY non trouvéé.")

    def affiche3DNuage(self):
        retour = self.lanceMeshlab()
        if  retour == -1 :
             self.encadre("Pas de nuage de points aprés Malt ou C3DC.")                
        if retour == -2 :
            self.encadre("Programme pour ouvrir les .PLY non trouvé.")
                         
        
    ################################## Le menu PARAMETRAGE : répertoires MicMAc et Meshlab ###########################################################

    def afficheParam(self):
        texte =('\nRépertoire bin de MicMac : \n\n'+afficheChemin(self.micMac)+
                '\n------------------------------\n'+
                '\nOutil exiftool : \n\n'+afficheChemin(self.exiftool)+
                '\n------------------------------\n'+
                '\nOutil pour afficher les .ply : \n\n'+afficheChemin(self.meshlab)+
                '\n------------------------------\n'+
                "\nRépertoire d'AperoDeDenis : \n\n"+afficheChemin(self.repertoireScript)+
                '\n------------------------------\n'+
                "\nRépertoire des paramètres : \n\n"+afficheChemin(self.repertoireData)+
                '\n------------------------------\n')        
        self.encadre(texte)

    def repMicmac(self):
        if self.micMac=="":
            texte="Pas de chemin pour le répertoire MICMAC\\bin."
        else:
            texte="Répertoire bin sous MICMAC : "+afficheChemin(self.micMac)
        self.encadre(texte,nouveauDepart='non')               # pour éviter le redémarrage de la fenêtre      
        # Choisir le répertoire de MicMac
        existe = False
        exiftoolOK = False        
        source=tkinter.filedialog.askdirectory(title='Désigner le répertoire bin sous Micmac ',initialdir=self.micMac)
        if len(source)==0:
            texte="Abandon, pas de changement.\nRépertoire bin de Micmac : \n\n"+afficheChemin(self.micMac)
            self.encadre(texte)
            return
        if self.systeme=="nt":
            self.mm3d = os.path.join(source,"mm3d.exe")
            if os.path.exists(self.mm3d):
                self.micMac = source
                existe = True
            if self.pasDeExiftool():    
                exiftool = os.path.join(source+"aire-aux","exiftool.exe")   # recherche de l'existence de exiftool sous binaire-aux
                if os.path.exists(exiftool):
                    self.exiftool = exiftool
                    exiftoolOK = True
            else: exiftoolOK = True
                
        if self.systeme=="posix":
            self.mm3d = os.path.join(source,"mm3d")
            if os.path.exists(self.mm3d):
                self.micMac = source
                existe = True

        self.CameraXML = os.path.join(os.path.dirname(self.micMac),self.dicoCameraGlobalRelatif)
        executable = verifierSiExecutable(self.mm3d)
            
        if executable:                                                          # nouveau répertoire correct
            self.micMac = source
            texte="Nouveau répertoire de Micmac : \n\n"+afficheChemin(self.micMac)
            self.sauveParam()
            
        else:
            if existe:
                texte = "Le programme mm3d est présent mais ne peut s'exécuter.\n Vérifier si la version est compatible avec le système. :\n"
            else:
                texte = "Le programme mm3d est absent du répertoire choisi :\n"+source+"\n Répertoire bin sous MicMac incorrect. \nAbandon."

        if exiftoolOK:
            texte = texte + "\n\nChemin de exiftool :\n\n"+self.exiftool

        self.mm3dOK = verifMm3d(self.mm3d)                # Booléen indiquant si la version de MicMac permet la saisie de masque 3D         
        self.encadre(texte)
        
    def repExiftool(self):
        if self.exiftool=="":
            texte="Pas de chemin pour le programme exiftool"
        else:
            texte="Programme exiftool :\n"+afficheChemin(self.exiftool)
        self.encadre(texte,nouveauDepart='non')         
        
        # Choisir le répertoire de Meshlab ou CLoudCompare :
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.exiftool),                                                 
                                                  filetypes=[('exiftool','exiftool.*;*.app'),('tous','.*')],multiple=False,
                                                  title = "Recherche exiftool")
        if len(source)==0:
            texte="Abandon, pas de changement.\nFichier exiftool inchangé :\n\n"+afficheChemin(self.exiftool)
            self.encadre(texte)
            return
        self.exiftool=''.join(source)
        self.sauveParam()
        texte="\nProgramme exiftool :\n\n"+afficheChemin(self.exiftool)
        self.encadre(texte)

    def repMeslab(self):
        if self.meshlab=="":
            texte="Pas de chemin pour le programme ouvrant les .PLY"
        else:
            texte="Programme ouvrant les .PLY :\n"+afficheChemin(self.meshlab)
        self.encadre(texte,nouveauDepart='non')                       
        # Choisir le répertoire de Meshlab ou CLoudCompare :
        source=tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.meshlab),                                                 
                                                  filetypes=[('meshlab ou cloud compare','meshlab.*;*.app;cloud*;*'),('tous','.*')],multiple=False,
                                                  title = "Recherche fichier Meshlab sous VCG, ou CloudCompare")
        if len(source)==0:
            texte="Abandon, pas de changement.\nFichier Meshlab ou cloud compare :\n\n"+afficheChemin(self.meshlab)
            self.encadre(texte)
            return
        self.meshlab=''.join(source)
        self.sauveParam()
        texte="\nProgramme ouvrant les .PLY :\n\n"+afficheChemin(self.meshlab)
        self.encadre(texte)

    ################################## LE MENU MICMAC : Choisir les photos, les options, le traitement ##########################################################


    def lesPhotos(self):                                # Choisir des images dans un répertoire

        self.fermerVisuPhoto()                          #  s'il y a une visualisation en cours des photos ou du masque on la ferme             

        if self.etatDuChantier>2:                       # 1 = avec photo ; 2 = enregistré, plus = traitement effectué
            if self.deuxBoutons("Choisir de nouvelles photos réinitialisera le chantier.",
                                "Les résultats en cours seront effacés.\n",
                                "Abandon",
                                "Réinitialiser") == 0:
                return
             
         
        photos=tkinter.filedialog.askopenfilename(title='Choisir des JPEG',
                                                  initialdir=self.repertoireDesPhotos,
                                                  filetypes=[('Photos JPG',('*.JPG')),('tous','*.*')],
                                                  multiple=True)
        
        if len(photos)==0:
            self.encadre("Abandon, aucune sélection,\n le répertoire et les photos restent inchangés.\n")
            return 

        if self.nombreDExtensionDifferentes(photos)==0:
            self.encadre("Aucune extension acceptable pour des images. Abandon.")
            return
        
        if self.nombreDExtensionDifferentes(photos)>1:
            self.encadre("Plusieurs extensions différentes :\n"+",".join(self.lesExtensions)+".\n Impossible dans cette version. Abandon.")
            return

        if self.lesExtensions[0] not in ".JPG.JPEG":
            self.encadre("La version actuelle ne traite que les photos au format JPG, or le format des photos est "+self.lesExtensions[0]+". Désolé." )
            return
        
        self.extensionChoisie = self.lesExtensions[0]       # l'extension est OK
            
        self.encadre("Copie des photos en cours... Patience",nouveauDepart='non') #  pour éviter le redémarage
        
        retourExtraire=self.extrairePhotoEtCopier(photos)       # crée le repertoire de travail, copie les photos et renvoit le nombre de fichiers photos "aceptables"

        if retourExtraire.__class__()=='':              # si le retour est un texte alors erreur, probablement création du répertoire impossible
            self.encadre ("Impossible de créer le répertoire de travail.\nVérifier les droits en écriture sous le répertoire des photos\n"+str(retourExtraire))
            return 
        if retourExtraire==0:                           # extraction et positionne  self.repertoireDesPhotos, et les listes de photos avec et sanschemin (photosAvecChemin et photosSansChemin)
            self.encadre ("Aucun JPG sélectionné,\nle répertoire et les photos restent inchangés.\n")
            return

        # conséquences du choix de nouvelles photos : on supprime tous le répertoire de travail ancien
        #  - même si la photo maitre n'est pas choisie on supprime le maitre et le masque
        #  - s'il y a une visualisation en cours des photos ou du masque on la ferme
        
        self.masque                     =   str()           # nom du fichier image représentant le masque sur l'image maitresse
        self.masqueSansChemin           =   str()           # image masque : en TIF, choisi par l'utilisateur       
        self.maitreSansChemin           =   str()           # image maitresse
        self.maitreCommentaire          =   str()           # indique si l'image maitresse est choisie automatiquement
        self.maitre                     =   str()
        self.fichierMasqueXML           =   str()           # nom du fichier XML décrivant le masque
        self.nomMaitreSansExtension     =   str()

        self.etatSauvegarde="*"                                     # chantier modifié       
        self.afficheEtat()        
    
    # extraire les photos dans le résultat de l'opendialogfilename (celui-ci dépend de l'OS et du nombre 0,1 ou plus de fichier choisis) :
    # puis création du chantier (si impossible : erreur !


    ################################## COPIER LES FICHIERS DANS LE REPERTOIRE DE TRAVAIL ###########################################################       
    
    def extrairePhotoEtCopier(self,photos): # création repertoire du chantier,  copie les photos OK, chdir. retour : nombre de photos
                                            # photosPropresAvecChemin photosAvecChemin photosSansChemin                                  
        liste=[x for x in photos if x[-3:].upper() in 'JPGJPEG']        # on restreint aux deux formats d'images identifiés correct / JPG 

        if len(liste)==0:
            return 0
        liste.sort()
        oldRepertoireDesphotos =  self.repertoireDesPhotos  
        self.repertoireDesPhotos = os.path.dirname(liste[0])                                              # si positif alors on affecte le repertoire (string)
        self.photosAvecChemin = list(liste)                                                              # les photos avec les chemins initiaux 

        # création du répertoire du chantier si nouveau chantier
                      
        if self.etatDuChantier==0 or oldRepertoireDesphotos!=self.repertoireDesPhotos:     # nouveau répertoire si pas de photos ou changement de répertoire                                                              # si pas encore de nom pour le chantier on lui en donne un !
            retour = self.creationNouveauRepertoireTravail()
            if isinstance(retour, str):
                return retour               #y a un pb
            
        # copie des photos sous le répertoire de travail : (attention, il peut y en avoir d'autres, qui seront supprimées au lancement de Micmac, mais pas de la qualité)

        listeCopie=list()                   # liste des fichiers copiés, vide

        try:
            for f in self.photosAvecChemin:                                 # self.photosPropresAvecChemin est la  liste des photos nettoyées à copier
                if self.extensionChoisie.upper() in f.upper():              # ON NE COPIE QUE L'EXTENSION CHOISIE, en majuscule
                    dest=os.path.join(self.repTravail,os.path.basename(f).upper().replace(" ","_")) #sans blanc : mm3d plante !
                    if not os.path.exists(dest):                            # on ne copie que si le fichier n'est pas déjà présent
                        shutil.copy(f,dest)                                 # copie du fichier sous le répertoire de travail                            
                    ajout(listeCopie,dest)                                  # liste des fichiers à traiter
        except Exception as e:
            texte=  'erreur lors de la copie du fichier\n'+f+'\n dans le répertoire \n'+self.repTravail+"\nlibellé de l'erreur : \n"+str(e)+\
                    "\nCauses possibles : manque d'espace disque ou droits insuffisants."
            return texte
        
        self.photosPropresAvecChemin = list(listeCopie)                         # listes des photos copiées
        self.photosSansChemin=list([os.path.basename(x) for x in listeCopie])   # liste des noms de photos copiès, sans le chemin. [tuple]            

        supprimeArborescenceSauf(self.repTravail,self.photosSansChemin)     # suppression de tous sous le répertoire actuel : sauf photos sélectionnées, (résultats, traces, arbres)

        os.chdir(self.repTravail)
        self.etatDuChantier = 1                                 # les photos sont choisies, le répertoire de travail est créé

        # définit les fichiers trace vides, débuter la trace
        
        self.definirFichiersTrace()                             # positionne sous le répertoire de travail

        open(self.TraceMicMacSynthese,'w').close()              # création d'un fichier de trace, vide
        open(self.TraceMicMacComplete,'w').close()              # création d'un fichier de trace, vide

        self.ajoutLigne(heure()+ "\n\nChoix des photos :\n"+"\n".join(self.photosAvecChemin)+"\n")
        self.ajoutLigne(heure()+ "\n\nrépertoire du chantier :\n"+self.repTravail+"\n\n")
        self.ecritureTraceMicMac()
        
        return len(listeCopie)                                                                               # on retourne le nombre de fichi

    def creationNouveauRepertoireTravail(self):       
        self.indiceTravail+=1
        self.repTravail=os.path.join(self.repertoireDesPhotos,'MicMac_'+str(self.indiceTravail))
        while os.path.exists(self.repTravail):                                                      # détermine le nom du répertoire de travail (chantier)
            self.indiceTravail+=1                                                                   # numéro particulier au répertoire de travail créé
            self.repTravail=os.path.join(self.repertoireDesPhotos,'MicMac_'+str(self.indiceTravail))# répertoire différent à chaque éxécution (N° séquentiel)
        try: os.mkdir(self.repTravail)                                                                   # création répertoire du chantier
        except Exception as e : return "Impossible de créer le répertoire de travail : erreur = \n"+str(e)
        ajout(self.tousLesChantiers,self.repTravail)                                                # on ajoute le répertoire créé dans la liste des répertoires
        self.chantier = os.path.basename(self.repTravail)                                           # nom du chantier, puis état du chantier : 1 = créé, fixé

    ################################## LE SOUS MENU OPTIONS : TAPIOCA, TAPAS,APERICLOUD, MALT, C3DC : accès par onglets ###########################################################
    # les onglets permettent de modifier les options localement.
    # si l'utilisateur valide alors les options modifiées sont controlées et si OK elles sont sauvegardées
    # si l'utilisateur abandonne alors il y a restauration des options à partir du fichier de sauvegarde

    def optionsOnglet(self):

        # l'état du chantier permet-il de choisir des options :
           
        if self.etatDuChantier==3:		
            self.encadre("Le chantier est interrompu suite à incident. \n\n"+
                         "Si besoin créer un nouveau chantier ou débloquer le chantier en lancant micmac.")       
            return        

        if self.etatDuChantier==5:		
            self.encadre("Le chantier est terminé. Modification des options inutile.\n\n."+
                         "Si besoin créer un nouveau chantier ou débloquer le chantier en lancant micmac.")            
            return

        # L'état du chantier permet de choisir des options :

        # sauvegarde des valeurs modifiables :

        self.sauveParamChantier()
        self.menageEcran()
  
        if self.etatDuChantier in (0,1,2,6):                        # sinon self.etatDuChantier vaut 4 et on va direct à Malt ou C3DC
            self.onglets.add(self.item400)                          # tapioca
            self.onglets.add(self.item500)                          # tapas
            self.onglets.add(self.item950)                          # Calibration            
            self.optionsTapioca()                                   # les frames à afficher ne sont pas "fixes"
            self.item510.pack()                                     # la frame fixe de tapas
            self.item710.pack(pady=15)                              # Malt         
            self.item960.pack(padx=5,pady=10,ipady=2,ipadx=15)      # Calibration de 960 à 980
            self.item965.pack()                                     # calibration suite
            self.item970.pack(padx=5,pady=10,ipady=2,ipadx=15)      # calibration suite
            self.item975.pack()                                     # calibration suite
            self.item980.pack(padx=5,pady=10,ipady=2,ipadx=15)      # calibration suite
            self.item990.pack()      # calibration suite            
            selection = self.item400                                # onglet sélectionné par défaut
        else:
            
            self.onglets.hide(self.item400)                         # tapioca
            self.onglets.hide(self.item500)                         # tapas
            self.onglets.hide(self.item950)                         # Calibration
            self.item703.config(text="Masque = "+self.masqueSansChemin)
            self.item710.pack(pady=15)                              # Malt : toujours présent
            selection = self.item700
     
        if self.mm3dOK:                                             # ne pas proposer C3DC si MicMac ne l'accepte pas

            os.chdir(self.repTravail)
            supprimeFichier(self.masque3DSansChemin)                # suppression des anciens masques 3D 
            supprimeFichier(self.masque3DBisSansChemin)        
        else:
            try: self.onglets.hide(self.item800)
            except: pass

        # préparation du masque :
        
        self.masqueProvisoire = str()
        self.masqueSansCheminProvisoire = str()
        self.item703.config(text="Masque = "+self.masqueSansChemin)
        
        # dernier onglet (qui se régénére, forcément le dernier)

        self.optionsReperes()                                       # points GPS, en nombre variable # points de repères calés dans la scène

        self.onglets.pack(fill='none', padx=2, pady=0)              # on active la boite à onglet
        self.item450.pack()                                         # et les 2 boutons en bas
        self.onglets.select(selection)                       # onglet sélectionné par défaut
        
        fenetre.wait_window(self.onglets)                           # boucle d'attente : la fenêtre pricncipale attend la fin de l'onglet
        
    def finOptionsOK(self):                                         # l'utilisateur a valider l'ensemble des options
        texte = str()
        # Pour Tapioca : toutes les variables sont sauvées 
        # Pour tapas :
        # Pour Malt :
        
        self.maitreSansChemin = os.path.basename(self.maitre)       # photoMaitre sans chemin avec extension, en minuscule

        self.ecrireMasqueXML()                                      # création du fichier xml associé à l'image maitresse, si besoin, sinon efface

        try: del self.masqueRetour                                  # suppression de l'objet "saisie du masque" s'il existe
        except : pass

        # on enregistre les options de calibration et de GPS 
        
        self.finCalibrationGPSOK()                                      # mise à jour des options de calibration
        self.finRepereOK()                                              # mise à jour des options de repérage (axe Ox, plan horizontal, distance

        # Sauvegarde des nouvelles info :
        
        self.sauveParam()
        self.etatSauvegarde="*"                                         # chantier modifié  ="*"                     #Pour indiquer que le chantier a été modifié, sans être sauvegardé sous le répertoire du chantier
        
        if self.controleOptions()!=True:                                # Controle de cohérence de la saisie (valeur entière...)
            texte=("Saisie d'une option incomplète ou incorrecte.\nCorriger.\n"+str(self.controleOptions()))
        self.sauveParam()
        self.afficheEtat(texte)
        
    def finCalibrationGPSOK(self):                                  # crée le fichier xml qui va bien avec les données saisies
        supprimeFichier(self.dicoAppuis)
        supprimeFichier(self.mesureAppuis)
        self.actualiseListePointsGPS()                              # met a jour proprement la liste des 6-tuples (nom,x,y,z,actif,identifiantgps)
        if self.dicoPointsGPSEnPlace.__len__()==0:                  # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
            return
        if self.controlePoints():
            self.encadre("Points GPS non conformes. Vérifiez.",nouveauDepart='non')
            return
        os.chdir(self.repTravail)
        with open(self.dicoAppuis, 'w', encoding='utf-8') as infile: #écriture de la description de chaque point GPS
            infile.write(self.dicoAppuisDebut)
            self.actualiseListePointsGPS()
            for Nom,X,Y,Z,num,ident in self.listePointsGPS:        # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
                point=self.dicoAppuis1Point.replace("Nom",Nom)
                point=point.replace("X",X)
                point=point.replace("Y",Y)
                point=point.replace("Z",Z)            
                infile.write(point)
            infile.write(self.dicoAppuisFin)

        with open(self.mesureAppuis, 'w', encoding='utf-8') as infile:             
                                                                        # modification des xml 
                infile.write(self.mesureAppuisDebut)
                key = ""
                listeDico=list(self.dicoPointsGPSEnPlace.items())       # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
                listeDico.sort(key= lambda e:  e[0][1])
                for cle,p in listeDico:
                    if key!=cle[1]:
                        if key!="":
                            infile.write(self.mesureAppuisFinPhoto)                    
                        key = cle[1]   
                        photo = self.mesureAppuisDebutPhoto.replace("NomPhoto",os.path.basename(cle[1]))
                        infile.write(photo)
                        point = self.mesureAppuis1Point.replace("NomPoint",cle[0])
                        point = point.replace("X",self.dicoPointsGPSEnPlace[cle][0].__str__())
                        point = point.replace("Y",self.dicoPointsGPSEnPlace[cle][1].__str__())
                        infile.write(point)                    
                    else:
                        point = self.mesureAppuis1Point.replace("NomPoint",cle[0])
                        point = point.replace("X",self.dicoPointsGPSEnPlace[cle][0].__str__())
                        point = point.replace("Y",self.dicoPointsGPSEnPlace[cle][1].__str__())
                        infile.write(point)
                infile.write(self.mesureAppuisFinPhoto)
                infile.write(self.mesureAppuisFin)

    def controlePointsGPS(self):                # controle pour affiche etat : informer de la situation : si vrai alors self.etatPointsGPS sera affiché
        #si pas de chantier, pas de problème mais retour False :  pas de calibration
        self.etatPointsGPS = str()
        if self.repTravail==self.repertoireData:
            return False
        listePointsActifs = [ (e[0],e[5]) for e in self.listePointsGPS if e[4] and e[0]!="" ] # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)

        if len(listePointsActifs)>0:
            self.etatPointsGPS = ("\n"+str(len(self.dicoPointsGPSEnPlace))+" points GPS placés\n"+ # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
                                  "pour "+str(len(listePointsActifs))+" points GPS définis\n")
            return True

        if os.path.exists(os.path.join(self.repTravail,self.mesureAppuis))==False:
            self.etatPointsGPS+="Saisie incomplète : les points ne seront pas pris en compte\n"
            return False
        
    def controleCalibration(self):                   # controle de saisie globale du repère, arrêt à la première erreur, True si pas d'erreur, sinon message
        #si pas de chantier, pas de problème mais retour False :  pas de calibration
        self.etatCalibration = str()
        if self.repTravail==self.repertoireData:
            return False
        # fichier xml présent :
       
        if os.path.exists(os.path.join(self.repTravail,self.miseAEchelle))==False:
            return False
        #ligne :
        if len(self.dicoLigneHorizontale)+len(self.dicoLigneVerticale)!=2:
            self.etatCalibration = self.etatCalibration+"La ligne horizontale ou verticale ne comporte pas 2 points\n"
        # Plan :       
        if os.path.exists(self.monImage_PlanTif)==False:
            self.etatCalibration = self.etatCalibration+"Pas de plan horizontal ou vertical\n"
        # Distance
        try:
            d = float(self.distance.get())
            if d<0:
                self.etatCalibration = self.etatCalibration+"Distance "+self.distance.get()+" invalide.\n"
            if d==0:
                self.etatCalibration = "Calibration annulée.\n"                
        except: 
            self.etatCalibration = self.etatCalibration+"Pas de distance.\n"
            return False
        # métrique :      
        liste = list(self.dicoCalibre.items())
        if liste.__len__()!=4:
            self.etatCalibration = self.etatCalibration+"La distance n'est pas mesurée par 2 points repérés sur 2 photos.\n"

        if self.etatCalibration==str():
            return True                             # calibration OK, tout va bien
        else: return False

    def finRepereOK(self):                      # ne mettre à jour que pour les variables saisies :

        existe = False                          # par défaut : pas de xml, true si il existe une des variables "reperes"
        xml = self.miseAEchelleXml

        # Pattern des fichiers à traiter : 
        
        xml = xml.replace("Fichiers",str(' .*'+self.extensionChoisie))

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
        xml = xml.replace("X2H",liste[0][1][1].__str__())
        xml = xml.replace("Y1H",liste[1][1][0].__str__())
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

        xml = xml.replace("distance",self.distance.get())

        # le plan horizontal ou vertical (OK même si absent)

        self.monImage_PlanTif = str()
        if os.path.exists(self.planProvisoireHorizontal):
            self.monImage_PlanTif = self.planProvisoireHorizontal
            existe=True
        
        if os.path.exists(self.planProvisoireVertical):         
            self.monImage_PlanTif = self.planProvisoireVertical            
            existe=True
           
        xml = xml.replace("monImage_MaitrePlan",os.path.basename(self.monImage_MaitrePlan))                 # Nom de l'image maitresse du plan repere (sans extension)
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
        texte=str()
        echelle1 = int(self.echelle1.get())
        echelle2 = int(self.echelle2.get())
        echelle3 = int(self.echelle3.get())
        echelle4 = int(self.echelle4.get())        
        delta = int(self.delta.get())        
        if self.modeTapioca.get()=='MulScale':
            try:
                if 0<=echelle1<50:
                    texte="\nEchelle 1 trop petite : \n"+self.echelle1.get()+"\nMinimum = 50"
                    return texte
            except:
                texte = texte+"\nEchelle non numérique poutr Tapioca : \n"+self.echelle1.get()+"\n"
                return texte
            try:

                if echelle2!=-1:
                    if echelle3<echelle2:
                        texte="\nEchelle 2 \n"+self.echelle2.get()+"\n plus petite que echelle 1 : \n"+self.echelle3.get()+"\n"
                        return texte
                    if 0<=echelle2<50:
                        texte="\nEchelle 1 trop petite : \n"+self.echelle2.get()+"\nMinimum = 50"
                        return texte                    

            except:
                texte = texte+"\nEchelle 2 non numérique : \n"+self.echelle2.get()+"."
                return texte
            
        if self.modeTapioca.get()=='All':
            try:
                if 0<echelle1<50:
                    texte="\nEchelle 1 trop petite : \n"+self.echelle1.get()+"\n"
                    return texte
            except:
                texte = texte+"\nEchelle 1 non numérique : \n"+self.echelle1.get()+"\n"
                return texte
            
        if self.modeTapioca.get()=='Line':
            try:
                if delta<1:
                    texte="\nDelta trop petit : \n"+self.delta.get()+"\nMinimum = 1"
                    return texte    
            except:
                texte="\nDelta non numérique : \n"+self.delta.get()+"\n"
                return texte
            try:
                if 0<echelle4<50:
                    texte="\nEchelle 1 trop petite : \n"+self.echelle4.get()+"\n"
                    return texte
            except:
                texte = texte+"\nEchelle 1 non numérique : \n"+self.echelle4.get()+"\n"
                return texte            
            
        # vérif taille image :
        if len(self.photosAvecChemin)==0:
            return True
        if os.path.exists(self.photosAvecChemin[0])==False:
            texte = "La photo "+self.photosAvecChemin[0]+" n'existe plus."
            return texte
        
        photo1 = Image.open(self.photosAvecChemin[0])
        largeur,hauteur = photo1.size
        del photo1
        
        maxi = max(largeur,hauteur)
        if self.modeTapioca.get()=='All':
            if int(self.echelle1.get())>maxi:
                texte = "\nechelle1 = "+self.echelle1.get()+"\n plus grand que la dimension maxi de la photo : \n"+str(maxi)+".\n\nInutile et ralenti le traitement. Modifier."
                return texte
        if self.modeTapioca.get()=='MulScale':
            if int(self.echelle2.get())>maxi:
                texte = "\nechelle2 = "+self.echelle2.get()+"\n plus grand que la dimension maxi de la photo : \n"+str(maxi)+".\n\nInutile et ralenti le traitement. Modifier."
                return texte                    
        
        return True

    def finOptionsKO(self):

        if self.masque==str():                                             #le masque 2D a pu être supprimé définitivement
            self.restaureParamChantier(self.fichierParamChantierEnCours)
            if  self.masque==str():
                message = "Pas de changement./n"
            else:
                message = "Masque 2D supprimé./n"
            self.masque = str()
            self.masqueSansChemin = str()
            self.sauveParam()            
        else:
            self.restaureParamChantier(self.fichierParamChantierEnCours)
            message = "Pas de changement/n"
        self.afficheEtat(message)

        
    #"""""""""""""""""""""""   Options de TAPIOCA
        
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

    # Options de Malt        
        
    def imageMaitresse(self):
        self.choisirUnePhoto(self.photosPropresAvecChemin,
                             "Choisir l'image maitresse",
                             "Choisir l'image maitresse pour Malt",
                             boutonDeux="Supprimer l'image maitresse",
                             mode="single")
        if self.fermerVisu:                                             #sortie par second bouton
            self.item701.config(text="Pas d'image maîtresse.")
            self.item703.config(text="Pas de masque.")
            self.maitre = str()
            self.maitreSansChemin = str()
            self.masque = ""
            self.masqueSansChemin = ""                                  
            return
        if self.selectionPhotosAvecChemin.__len__()==0:             #sortie par fermeture fenêtre
            self.item701.config(text="Abandon. Choix inchangé :\n"+self.maitreSansChemin)
            return                                
        self.item703.config(text="pas de masque")                       # réinitialise le masque
        self.masque = ""
        self.masqueSansChemin = ""        
        self.maitreProvisoire = str(self.selectionPhotosAvecChemin[0])            # puis l'image maitresse
        self.maitreSansCheminProvisoire=os.path.basename(str(self.selectionPhotosAvecChemin[0]))             # photoMaitre sans chemin avec extension, en minuscule
        try: shutil.copy(self.maitreProvisoire,self.repTravail)
        except: pass
        self.maitre = os.path.join(self.repTravail,self.maitreSansCheminProvisoire)
        self.item701.config(text="image maitresse = "+self.maitreSansCheminProvisoire)

    def traceMasque(self):
        self.fermerVisuPhoto()

        # un peu brutal si la visu n'est pas celle de la photo maitre, évite les incohérences

        if os.path.exists(self.maitre):                                                         #l'image maître doit exister
            self.masqueProvisoire = os.path.splitext(self.maitre)[0]+"_Masq_provisoire.tif"     # Nom du fichier masque, à partir du fichier maître, imposé par micmac
            self.masqueSansCheminProvisoire = os.path.basename(self.masqueProvisoire)           # sans le chemin
            supprimeMasque(self.repTravail,"_Masq.tif")                                         # suppression des anciens masques
            supprimeFichier(self.fichierMasqueXML)
            self.masque = str()
            self.masquesansChemin = str()
            self.masqueRetour = TracePolygone(fenetre,self.maitre,self.masqueProvisoire)        # L'utilisateur peut tracer le masque sur l'image maitre 
            if self.masqueRetour.polygone == True:                                              # si retour OK (masqueRetour est un élément de la classe tracePolygone)
                self.item703.config(text="masque = "+self.masqueSansCheminProvisoire)           # affichage du nom du masque
            else:
                 self.masqueProvisoire = str()                                                  # pas de masque : détricotage
                 self.masqueSansCheminProvisoire = str()
                 self.item703.config(text="pas de masque")
        else:
            self.item703.config(text="Il faut une image maîtresse pour définir un masque.",
                                background="#ffffaa")

    def ecrireMasqueXML(self):
 
        if self.masqueProvisoire==str() or os.path.exists(self.masqueProvisoire)==False:                         # si pas de masque
            supprimeMasque(self.repTravail,"_Masq.tif")          # suppression des anciens masques s'ils existent
            supprimeFichier(self.fichierMasqueXML)                      # suppression ancien xml
            self.masque = str()
            self.masqueSansChemin = str()
            return
        self.masque = os.path.splitext(self.maitre)[0]+"_Masq.tif"                              # nom définitif du masque
        self.masqueSansChemin = os.path.basename(self.masque)
        if os.path.exists(self.masque):
            try:
                os.remove(self.masque)
            except:
                self.encadre ("Impossible de remplacer le fichier masque :\n"+self.masque+"\nVérifier s'il n'est pas ouvert.\n Masque inchangé.",
                              nouveauDepart='non')
                return
        os.rename(self.masqueProvisoire,self.masque)                            # on renomme le fichier (et on écrase l'ancien !)
        self.masqueProvisoire = str()                                           # plus de masque provisoire: détricotage
        self.masqueSansCheminProvisoire = str()
        
        self.masqueXML=self.masqueXML.replace("MonImage_Masq.tif",self.masqueSansChemin)                #écriture dans le fichier xml
        self.masqueXML=self.masqueXML.replace("largeur",str(self.masqueRetour.largeurImageFichier))
        self.masqueXML=self.masqueXML.replace("hauteur",str(self.masqueRetour.hauteurImageFichier))
        self.fichierMasqueXML=self.masque.replace(".tif",".xml")
        with open(self.fichierMasqueXML, 'w', encoding='utf-8') as infile:
            infile.write(self.masqueXML)



    def affiche3DApericloud(self):                              # lance SAisieMasqQT, sans le fermer.... attente de la fermeture (subprocess.call)
        os.chdir(self.repTravail)        
        if os.path.exists("AperiCloud.ply")==False:
            try:
                self.item803 = ttk.Label(self.item800,
                                       text= "pas de fichier AperiCloud.ply pour construire le masque :\nlancer Micmac pour en constituer un.",
                                       style="C.TButton")
                self.item803.pack(ipady=2,pady=10)
            except: pass
            return
        else:
            try: self.item803.destroy()
            except: pass
            
        masque3D = [self.mm3d,"SaisieMasqQT","AperiCloud.ply"]              # " SaisieAppuisInitQT AperiCloud.ply"
        self.apericloudExe=subprocess.call(masque3D,shell=self.shell)       # Lancement du programme et attente du retour
        try:                                                                #marche pas si on est en visu
            if self.existeMasque3D():
                self.item803 = ttk.Label(self.item800, text= "masque 3D créé")
                self.item803.pack(ipady=2,pady=10)
            else:
                self.item803 = ttk.Label(self.item800, text= "Abandon : pas de masque créé.",foreground='red')
                self.item803.pack(ipady=2,pady=10)
        except: pass
            
    #""""""""""""""""""""""" Options de CalibrationGPS : faire correspondre des points (x,y,z) numérotés de 1 à N, avec des pixels des images.

    def optionsReperes(self):				        # en entrée : self.listePointsGPS qui comporte la liste des points GPS a affiche, sauvegardée        

        try: self.item650.destroy()				# suppression de l'onglet s'il existait
        except: pass
        try: self.bulle.destroy()
        except: pass
        
        self.item650 = ttk.Frame(	self.onglets,		# création du cadre d'accueil de l'onglet
					height=5,
					relief='sunken')		

        # message en haut de fenêtre
        
        self.item670 = ttk.Frame(self.item650,height=10,relief='sunken')
        self.item671=ttk.Label(self.item670,text="Chaque point doit être placé sur au moins 2 photos",justify='left')
        self.item671.pack(pady=10,padx=10,ipady=2,ipadx=2)        
        self.item670.pack(side='top')


        if self.listePointsGPS.__len__()==0:			# ajout d'une ligne de saisie blanche si aucun point :
            self.listePointsGPS.append(["","","","",True,self.idPointGPS]) # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
            self.idPointGPS += 1
        # affichage des entêtes de colonne
        self.item660 = ttk.Frame(self.item650,height=5,relief='sunken')
        self.item661 = ttk.Label(self.item660,text='point').pack(side='left',pady=10,padx=60,fill="both")
        self.item662 = ttk.Label(self.item660,text='X').pack(side='left',pady=10,padx=40)                  
        self.item663 = ttk.Label(self.item660,text='Y').pack(side='left',pady=10,padx=70)
        self.item664 = ttk.Label(self.item660,text='Z').pack(side='left',pady=10,padx=70)
        self.item660.pack(side="top")
        
        # préparation des boutons en bas de liste
		
        self.item653=ttk.Button(self.item650,text='Ajouter un point',command=self.ajoutPointCalibrationGPS)
        self.item654=ttk.Button(self.item650,text='Supprimer des points',command=self.supprPointsGPS)                  
        self.item655=ttk.Button(self.item650,text='Placer les points',command=self.placerPointsGPS)

        self.item653.pack_forget()											#on oublie les boutons du bas s'ils étaient affichés
        self.item654.pack_forget()
        self.item655.pack_forget()

        
        # Affichage de la liste des points actuellement saisis:

        self.listeWidgetGPS = list()							# liste des widgets affichés, qui sera abondée au fur et à mesure par copie de self.listePointsGPS		
        for n,x,y,z,actif,ident in self.listePointsGPS:					# affichage de tous les widgets nom,x,y,z,actif ou supprimé (booléen), identifiant
            if actif:                                                                   # listePointsGPS : liste de tuples (nom du point, x gps, y gps, z gps, booléen actif, identifiant)
                self.affichePointCalibrationGPS(n,x,y,z,ident)					# ajoute une ligne d'affichage
        self.item653.pack(side='left',padx=20)							# affichage des boutons en bas d'onglet
        self.item654.pack(side='left',padx=20)
        self.item655.pack(side='left',padx=20)
        
        self.onglets.add(self.item650, text="GPS")                             # affichage onglet
        self.onglets.select(self.item650)                    			# active l'onglet  
		
    def affichePointCalibrationGPS(self,n,x,y,z,ident):
        
        f = ttk.Frame(self.item650,height=5,relief='sunken')			# cadre d'accueil de la ligne
        self.listeWidgetGPS.append(
				    (f,						# cadre : [0]
                                    ttk.Entry(f),				# zones de saisie de [1] à [4]
                                    ttk.Entry(f),
                                    ttk.Entry(f),
                                    ttk.Entry(f),
                                    ident)
				    )

        self.listeWidgetGPS[-1][0].pack(side='top')
        self.listeWidgetGPS[-1][1].pack(side='left',padx=5)
        self.listeWidgetGPS[-1][1].focus()        
        self.listeWidgetGPS[-1][2].pack(side='left')        
        self.listeWidgetGPS[-1][3].pack(side='left')
        self.listeWidgetGPS[-1][4].pack(side='left')
		
        self.listeWidgetGPS[-1][1].insert(0,n)              				        # affichage de la valeur dans le widget                  
        self.listeWidgetGPS[-1][2].insert(0,x)
        self.listeWidgetGPS[-1][3].insert(0,y)
        self.listeWidgetGPS[-1][4].insert(0,z)   
   
                                        

    def ajoutPointCalibrationGPS(self):
        self.actualiseListePointsGPS()
        if self.listePointsGPS.__len__()>5:                     
            self.infoBulle("Soyez raisonnable : pas plus de 5 points GPS !")
            return

        self.listePointsGPS.append(["","","","",True,self.idPointGPS])      # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
        self.idPointGPS += 1						    # identifiant du point suivant
        self.optionsReperes()						    # affichage avec le nouveau point
        self.actualiseListePointsGPS()
        
    def supprPointsGPS(self):
        try: self.bulle.destroy()
        except: pass        
        if self.listePointsGPS.__len__()==0:                # pas de points : on sort
            self.infoBulle("Aucun point à supprimer !")
            return
						
        self.actualiseListePointsGPS()                      # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
        listeIdentifiants = [ (e[0],e[5]) for e in self.listePointsGPS if e[4] ] # liste des noms,identifiants si point non supprimé

        self.messageSiPasDeFichier = 0                                           #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto([ f[0] for f in listeIdentifiants],
                                                 titre='Points à supprimer',
                                                 mode='extended',
                                                 message="Multiselection possible.",
                                                 boutonDeux="Annuler")
        self.messageSiPasDeFichier = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return

        listeIdentifiantsASupprimer = [g[1] for g in listeIdentifiants if g[0] in self.selectionPhotosAvecChemin]
        
        for i in self.listePointsGPS:                       #on met le flag i[4] à zéro : pour conserver le lien avec les points placés ??
            if i[5] in listeIdentifiantsASupprimer:
                self.listePointsGPS.remove(i)
                i[4] = False
                self.listePointsGPS.append(i)
        dico = dict(self.dicoPointsGPSEnPlace)              # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y        
        for keys in dico:		#supprime les points déjà placés
            if keys[2] in listeIdentifiantsASupprimer:
                del self.dicoPointsGPSEnPlace[keys]
                        
        self.optionsReperes()
    
        
    def actualiseListePointsGPS(self):                      # actualise les valeurs saisies pour les points GPS
        try: self.bulle.destroy()
        except: pass
        dico = dict(self.dicoPointsGPSEnPlace)              # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
        for a,nom,x,y,z,ident in self.listeWidgetGPS:
            for i in self.listePointsGPS:                   # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
                if i[5] == ident:
                    self.listePointsGPS.remove(i)
                    i[0] = nom.get()
                    i[0] = i[0].replace(" ","_")            # pour corriger une erreur : l'espace est interdit dans les tag d'item de canvas !
                    i[1] = x.get()
                    i[2] = y.get()
                    i[3] = z.get()					
                    self.listePointsGPS.append(i)
                    
                for e,v in dico.items():

                    if e[2]==i[5] and i[0]!=e[0]:           # l'identifiant du point placé = identifiant du point gps mais le nom du point est différent
                                                            #cela signifie que l'utilisateur à modifié le nom
                        self.dicoPointsGPSEnPlace[(i[0],e[1],e[2])] = v  # ajout d'une entrée quicorrige cette anomalie (on devrait utiliser l'identifiant...)
                        try:
                            del self.dicoPointsGPSEnPlace[e]  # suppression de l'ancienen entrée
                        except: pass

                    if e[2]==i[5] and i[4]==False:          #si l'identifiant est identique et le point GPS supprimé alors on supprime le point placé
                        try:
                            del self.dicoPointsGPSEnPlace[e]
                        except: pass                        
        
    def placerPointsGPS(self):

        self.actualiseListePointsGPS()

        if self.controlePoints():
            return
        liste = list ([(n,ident) for n,x,y,z,actif,ident in self.listePointsGPS if actif])    # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
        self.messageSiPasDeFichier  = 0                                             #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Choisir une photo pour placer les points GPS : ",
                             mode='single',
                             dicoPoints=self.dicoPointsGPSEnPlace)          # dicoPointsGPSEnPlace key = nom point, photo, identifiant, value = x,y
        self.messageSiPasDeFichier  = 1
        
        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
		
        # en retour une liste : self.selectionPhotosAvecChemin
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      self.dicoPointsGPSEnPlace,                                        # les points déjà placés key = nom point, photo, identifiant
                                      )                                                                 # value = x,y
        try: self.dicoPointsGPSEnPlace = self.calibre.dicoPointsJPG                                     # si pas de retour !
        except: pass
        
    def controlePoints(self):
        try: self.bulle.destroy()
        except: pass
        texte = ""
        ensemble=set(e[0] for e in self.listePointsGPS if e[4])     # listePointsGPS : 6-tuples (nom du point, x, y et z gps, booléen actif, identifiant)
        liste=list(e[0] for e in self.listePointsGPS if e[4])
        if ensemble.__len__()!=liste.__len__():
            texte = "Attention : Des points portent le même nom."
        if "" in ensemble:
            texte = "Attention : un point n'a pas de nom. "+texte
        if texte!="":
            self.infoBulle(texte)
            return True
        return False

           
    def ligneHorizontale(self):
        self.dicoLigneVerticale = dict()                        # on efface le dico horizontal (l'un ou l'autre)
        liste = (("Origine Ox",1),("Extrémité Ox",2))           # liste de tuple nom du point et identifiant du widget
        self.messageSiPasDeFichier  = 0                         #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Placer une ligne horizontale sur une seule photo : ",
                             mode='single',
                             dicoPoints=self.dicoLigneHorizontale)
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        
        horizonVierge = dict()
        try:
            if self.selectionPhotosAvecChemin[0]==list(self.dicoLigneHorizontale.items())[0][0][1]:       # si l'image choisie est la même on conserve le dico
                horizonVierge = self.dicoLigneHorizontale                                               # sinon nouveau dico
        except: pass
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      horizonVierge,                                                    # aucun point déjà placé
                                      )                                                              # value = x,y
        #il doit y avoir 2 points placés, sinon erreur :
        try:
            if self.calibre.dicoPointsJPG.__len__()!=2:
                self.infoBulle("il faut  placer les 2 points.")
                return
        except: pass
        try: self.dicoLigneHorizontale = self.calibre.dicoPointsJPG                                     # si pas de retour !
        except: pass

    def ligneVerticale(self):
        self.dicoLigneHorizontale = dict()                                                              # on efface le dico horizontal (l'un ou l'autre)
        self.messageSiPasDeFichier  = 0                  #  pour affichage de message dans choisirphoto, difficile a passer en paramètre
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Placer une ligne verticale sur une seule photo :  : ",
                             mode='single',
                             dicoPoints=self.dicoLigneVerticale)
        self.messageSiPasDeFichier  = 1
		
        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        
        liste = (("Origine Oy",1),("Extrémité Oy",2))                                                   # liste de tuple nom du point et identifiant du widget
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
                self.infoBulle("il faut  placer les 2 points.")
                return
        except Exception as e: pass
        try: self.dicoLigneVerticale = self.calibre.dicoPointsJPG                                     # si pas de retour !
        except Exception as e: pass

    def planVertical(self):

        self.planProvisoireHorizontal = str()        #un seul plan : le dernier
        self.planProvisoireVertical = str()
        self.messageSiPasDeFichier  = 0
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Une photo pour placer le plan vertical : ",
                             mode='single')
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return
        
        self.planProvisoireVertical = "planVertical.tif" #os.path.splitext(self.selectionPhotosAvecChemin[0])+"_planvertical.tif"     # Nom du fichier masque, à partir du fichier maître, imposé par micmac
        self.monImage_MaitrePlan = self.selectionPhotosAvecChemin[0]
        self.planV = TracePolygone(fenetre,
                                   self.monImage_MaitrePlan,
                                   self.planProvisoireVertical,
                                   labelBouton="Délimiter un plan vertical")                                       # L'utilisateur peut tracer le masque sur l'image maitre 

    def planHorizontal(self):
        
        self.planProvisoireHorizontal = str()    #un seul plan : le dernier
        self.planProvisoireVertical = str()
        self.messageSiPasDeFichier  = 0
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Une photo pour placer le plan horizontal : ",
                             mode='single')
        self.messageSiPasDeFichier  = 1

        # en retour une liste : self.selectionPhotosAvecChemin        

        if self.selectionPhotosAvecChemin.__len__()==0:
            return        

        self.planProvisoireHorizontal = "planHorizontal.tif" # os.path.splitext(self.selectionPhotosAvecChemin[0])+"_planhorizontal.tif"     # Nom du fichier masque, à partir du fichier maître, imposé par micmac
        self.monImage_MaitrePlan = self.selectionPhotosAvecChemin[0]
        self.planH = TracePolygone(fenetre,
                                   self.monImage_MaitrePlan,
                                   self.planProvisoireHorizontal,
                                   labelBouton="Délimiter un plan horizontal")                                       # L'utilisateur peut tracer le masque sur l'image maitre 
        
    def placer2Points(self):
        liste = (("Début",1),("Fin",2))                                                   # liste de tuple nom du point et identifiant du widget
        self.messageSiPasDeFichier  = 0
        self.choisirUnePhoto(
                             self.photosPropresAvecChemin,
                             message="Choisir deux fois une photo pour placer les 2 points  : ",
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
            self.infoBulle("Il y a dèjà 2 images avec des points 'distance'. Supprimer les points sur une des 2 images.")
            return
        
        self.calibre = CalibrationGPS(fenetre,
                                      self.selectionPhotosAvecChemin,                                   # image sur laquelle placer les points
                                      liste,                                                            # liste des identifiants en "string" des points
                                      self.dicoCalibre                                                 # les points déjà placés key = nom point, photo, identifiant
                                      )                                                 # value = x,y
        try: self.dicoCalibre = self.calibre.dicoPointsJPG                                              # si pas de retour !
        except: pass
        
       
    ################################## LANCEMENT DE MICMAC ###########################################################
        
    def lanceMicMac(self):                                      # vérification du choix de photos, de présence de l'éxécutable, du choix de l'extension, de la copie effective dans le répertoire de travail
    # Vérification de l'état du chantier :

    # si pas de photos choisies ou pas de paramètre : retour :

        if self.pasDePhoto():return        
        if self.pasDeMm3d():return
        
    # pas enregistré : on enregistre on poursuit
            
        if self.etatDuChantier==1:                              # Des photos mais fichier paramètre non encore enregistré, on enregistre et on poursuit
            self.enregistreChantier()                           # sauvegarde du fichier paramètre sous le répertoire du chantier : modif etatduchantier = 2

    # anormal : chantier planté lors de la dernière éxécution : on propose le déblocage mais on sort dans tous les cas
                
        if self.etatDuChantier==3:		                # En principe ne doit pas arriver : plantage en cours d'un traitement précédent 
            retour = self.deuxBoutons(  titre="Le chantier "+self.chantier+" a été interrompu en cours d'exécution.",
                                        question="Le chantier est interrompu.\nVous pouvez le débloquer, "+
                                        "ce qui permettra de modifier les options et de le relancer.\n",
                                        b1='Débloquer le chantier',b2='Abandon')
            if abs(retour)==1:                                  # 1 ou -1 : abandon ou fermeture de la fenêtre par la croix
                return
            if retour==0:
                self.nettoyerChantier()                          # le chantier est noté comme de nouveau modifiable
                self.sauveParam()
                self.afficheEtat("Chantier "+self.chantier+" de nouveau modifiable, paramètrable et exécutable.")                
                return

    # Chantier arrété après tapas : l'utilisateur a pu modifier les options et veut continuer ou reprendre au début suivant les résultats
    # poursuite du traitement ou arrêt suivant demande utilisateur

        if self.etatDuChantier==4:                              # Chantier arrêté après Tapas
            retour = self.deuxBoutons(  titre='Continuer le chantier '+self.chantier+' après tapas ?',
                                        question =  "Le chantier est arrêté après tapas.\nPoursuivre le traitement ou annuler le traitement précédent?\n"+
                                                    "Pour ne rien faire cliquer sur le bouton 'fermer' de la fenêtre",
                                        b1='Poursuivre',b2='Débloquer le chantier - garder les résultats')
            if retour == -1:                                    # fermeture de la fenêtre
                return

            if retour == 0:                                     # Lancer malt ou C3DC              
                self.menageEcran()                              # ménage écran        
                self.cadreVide()                                # fenêtre texte pour affichage des résultats.
                self.ajoutLigne(heure()+" Reprise du chantier "+self.chantier+" arrêté aprés TAPAS - La trace depuis l'origine sera disponible dans le menu édition.")
                self.suiteMicmac()                              # on poursuit par Malt ou C3DC
                return

            if retour==1:                                       # débloquer le chantier
                self.nettoyerChantier()
                self.afficheEtat("Chantier "+self.chantier+" de nouveau modifiable, paramètrable et exécutable.")
                return

    # Chantier terminé, l'utilisateur peur décider de le débloquer en conservant les résultats de tapas ou supprimer tous les résultats
    
        if self.etatDuChantier==5:		                # Chantier terminé
            retour = self.deuxBoutons(  titre='Le chantier '+self.chantier+' est terminé.',
                                        question="Le chantier est terminé.\nVous pouvez le nettoyer, "+
                                        "ce qui supprimera les calculs et permettra de le relancer.\n",                                    
                                        b1='Ne rien faire',b2='Nettoyer le chantier - garder les résultats')
            if retour==-1:                                       # -1 : fermeture fenêtre, abandon 
                return
            if retour==0:                                       # 0 : ne rien faire 
                return
            if retour==1:                                       # 1 : on nettoie, on passe à l'état 2
                self.nettoyerChantier()
                self.afficheEtat("Chantier "+self.chantier+" de nouveau modifiable, paramètrable et exécutable.")
                return

    # L'état du chantier est prêt pour l'exécution de Tapioca (2) ou débloqué (6) : sauvegarde des paramètres actuels puis traitement
        
        self.sauveParam()

        # Vérification que les photos, les options et les paramètres  autorisent l'exécution, sinon exit ATTENTION : on efface tout avant de recopier les photos
        
        retourAvantScene = self.avantScene()                    # Efface tout, Prépare le contexte, crée le répertoire de travail, copie les photos, ouvre les traces

        if retourAvantScene!=None:                              # Préparation de l'éxécution de MicMac
            texte = "Pourquoi MicMac s'arrête : \n"+retourAvantScene
            self.encadreEtTrace(texte)                          # si problème arrêt avec explication
            return

        # Prêt : modification de l'état, lancement du premier module Tapioca (recherche des points homologues)
       
        self.etatDuChantier = 3		                        # trés provisoirement (en principe cette valeur est transitoire sauf si avantScène plante)
        self.lanceTapioca()
        if not os.path.exists("Homol"):                         # le répertoire Homol contient les points homologues, si absent, pas de points en correspondancce
            message = "Pourquoi MicMac s'arrête : \n"+"Aucun point en correspondance sur 2 images n'a été trouvé par Tapioca.\n\n"+\
                      "Parmi les raisons de cet échec il peut y avoir :\n"+\
                      "soit l'exif des photos ne comporte pas la focale ou plusieurs focales sont présentes \n+"+\
                      "Soit l'appareil photo est inconnu de Micmac\n"+\
                      "soit la qualité des photos est en cause.\n"+\
                      "\nUtiliser les items du menu 'outils' pour vérifier ces points.\n\n"
            self.ajoutLigne(message)
            self.messageNouveauDepart =  message
            self.nouveauDepart()                                  # lance une fenêtre  nouvelle sous windows (l'actuelle peyt-être polluée par le traitement  
            return

        # points homologues trouvés, second module : Tapas positionne les prises de vue dans l'espace
        
        self.nbResiduTapas = 0                                  # booléen pour tester si taps fonctionne : si  aucune orientation alors échec de tapioca 
        self.lanceTapas()

        if self.nbResiduTapas == 0:                             # Tapioca n'a pu mettre en correspondance ce aucun point entre deux images : échec
            message = "Pourquoi MicMac s'arrête : \n"+"Pas d'orientation trouvé par tapas.\nPrises de vues non positionnées.\n"+\
                      "Verifier la qualité des photos (item du menu outil)\n\n"
            self.ajoutLigne(message)
            self.messageNouveauDepart =  message
            self.nouveauDepart()                                  # lance une fenêtre  nouvelle sous windows (l'actuelle peyt-être polluée par le traitement  
            return


        # Si un fichier de calibration valide est présent on lance apero

        if self.controleCalibration():              # calibration OK
                self.lanceApero()
                
        if self.etatCalibration!=str():             # calibration incomplète
                self.ajoutLigne(heure()+"Calibration incomplète : "+self.etatCalibration)

        # troisième module : Apericloud  crée le nuage 3D des points homologues puis visualisation :
        
        self.lanceApericloud()                                  # création d'un nuage de points 3D
        self.lanceApericloudMeshlab()                           # affiche le nuage 3D si il existe

        # Situation stable, changement d'état : 4 = Tapioca et Tapas exécutés, sauvegarde des paramètres
        
        self.etatDuChantier = 4		                        # état du chantier lors de l'arrêt aprés tapas
        self.sauveParam()
        self.ecritureTraceMicMac()                              # on écrit les fichiers trace
            
        # Faut-il poursuivre ?
        
        if self.arretApresTapas.get():                         # L'utilisateur a demandé l'arrêt
            ligne="\nArrêt après Tapas "+heure()+". Lancer MicMac pour reprendre le traitement. \n"              
            ligne=ligne+"\n\n************* Arrêt aprés Tapas sur demande utilisateur *******************\n\n"        
            self.ajoutLigne(ligne)
            self.copierParamVersChantier()                      # sauvegarde du fichier paramètre sous le répertoire du chantier
        else:
            self.suiteMicmac()                                  # PoursSuite : Malt ou C3DC, pouvant être appelé directement
            
        self.nouveauDepart()                                    # lance une fenêtre  nouvelle sous windows (l'actuelle peyt-être polluée par le traitement

    def nettoyerChantier(self):                                 # Le chantier est nettoyé : les résulats sous reptravail sont conservés, les arborescences de calcul effacés
        self.etatDuChantier = 2                
        self.enregistreChantier()     
        listeAConserver  = os.listdir(self.repTravail)
        supprimeArborescenceSauf(self.repTravail,listeAConserver)           
        
    def suiteMicmac(self):


        #on ne peut poursuivre que si il existe un fichier "apericloud.ply", et une image maitresse, 2D ou 3D.

        if os.path.exists("AperiCloud.ply")==False:
            ligne = ("Tapas n'a pas généré de nuage de points.\n"+
                     "Le traitement ne peut se poursuivre.\n"+
                     "Vérifier la qualité des photos, modifier les paramètres et relancer tapioca-tapas")
            self.ajoutLigne(ligne)
            self.encadre(ligne)
            return

        if not(self.existeMasque3D() or self.existeMaitre2D()):
            ligne = ("Pas de masque 3D, ou d'image maitresse pour Malt.\n"+
                     "Le traitement ne peut se poursuivre.\n"+
                     "Définir une image maitresse\n"+                     
                     "ou Changer le mode 'GeomImage' qui impose une image maitresse\n"+
                     "ou définir un masque 3D\n"+
                     "Pour cela utiliser l'item option/Malt ou option/C3DC du menu MicMac\n")
            self.ajoutLigne(ligne)
            self.encadre(ligne)
            return
        
        # calibrage de l'orientation suivant des points GPS, un axe ox, un plan déterminé par un masque
        # si il existe un fichier XML de points d'appuis : self.mesureAppuis
              
        if os.path.exists(self.mesureAppuis):
            self.lanceBascule()
                         
        # malt ou D3CD : suivant que le masque 3 D existe ou pas, avec préférence au masque 3D,
        # la production sera "modele3D.ply"
        
        if self.existeMasque3D():                               
            self.sauveParam()            
            self.lanceC3DC()                                    # C3DC crée directement le fichier modele3D.ply
        else:
            self.suiteMicmacMalt()
            if self.modeMalt.get()=="GeomImage":
                self.lanceNuage2PlyGeom()
            if self.modeMalt.get()=="UrbanMNE":
                self.lanceNuage2PlyUrban()
            if self.modeMalt.get()=="Ortho":
                self.lanceNuage2PlyUrban()

        # Final : affichage du modele3D.ply, sauvegarde, relance la fenêtre qui a pu être dégradé par le traitement externe

        retour = self.lanceMeshlab()
        texte = ""
        if  retour == -1 :
             texte = "Pas de nuage de points aprés Malt ou C3DC."
        if retour == -2 :
            texte = "Programme pour ouvrir les .PLY non trouvé."        
        ligne = texte + "\n\n************* Fin du traitement MicMac "+heure()+" *******************\n\n"
        self.etatDuChantier = 5 		                                                    # 5 : chantier terminé         
        self.ajoutLigne(ligne)

    # Que faire après Tapioca et Tapas ? malt ou D3DC
        
    def suiteMicmacMalt(self):

        if self.etatDuChantier==4:  	                        # en principe inutile : toujours vrai !
            if self.avantMalt()!=None:                          # copie l'image maitresse et le masque, sauve les paramètres
                self.messageNouveauDepart = "Pourquoi MicMac est arrêté : \n"+self.avantMalt()+"\n Corriger."
                self.ajoutLigne(self.messageNouveauDepart)                
                self.ecritureTraceMicMac()
                return
            self.lanceMalt()  
        else:
            self.ajoutLigne("Tapas non effectué, lancer Micmac depuis le menu. Etat du chantier = ",self.etatDuChantier)


##############################################################################################################"
        
    def avantMalt(self):

        # initialisation C3DC permet d'utiliser un masque e la photo maitresse pour MALT : il faut une image maitresse si le mode est geoimage

        if self.maitreSansChemin=='' and self.modeMalt.get()=="GeomImage":    # self.photoMaitre : nom de la photo sans extension ni chemin, l'extension est dans self.extensionChoisie                            
            return "Pas d'image maîtresse.\nCelle-ci est nécessaire pour l'option choisie geomImage de Malt.\nPour corriger modifier les options de Malt ou choississez un masque 3D avec C3DC."              
                         
        # copie du fichier masque, s'il existe, pour accélérer MALT ( MicMac recherche un fichier de nom "fixé", suivant le nom de l'image maitresse   
        self.nomMaitreSansExtension = os.path.splitext(self.maitreSansChemin)[0]                    # utile pour nuage2ply
        
        if os.path.exists(self.masque):                                                                       
            try: shutil.copy(self.masque,self.repTravail)                                                # on copie le masque
            except: pass
            try: shutil.copy(self.fichierMasqueXML,self.repTravail)                                      # copie du fichier XML Associé au masque
            except: pass
            self.ajoutLigne("Fichier masque associé à l'image maitresse pour la procédure MALT : \n\n"
                            +self.masqueSansChemin+"\n\n")                                          # PROBLEME SI L'EXTENSION CHOISIE pour les photos EST TIF
        else:
            self.ajoutLigne("\nPas de masque associé à l'image maîtresse.\n")
                                                            
        self.sauveParam()
       
        
    ################################## LES DIFFENTES PROCEDURES MICMAC ###########################################################       

    # ------------------ PREAMBULE --------------------

    def avantScene(self):
        self.menageEcran()                                      # ménage écran        
        self.cadreVide()                                        # fenêtre texte pour affichage des résultats.

        # vérification nécessaires :
        
        if len(self.photosAvecChemin)==0:                       # photos sans chemin
            texte='Aucune photo choisie. Abandon.'
            return texte
        
        if len(self.photosAvecChemin)==1:                       # photos sans chemin
            texte='Une seule photo choisie. Abandon.'
            return texte
            
        if self.controleOptions()!=True:
            return "\nOption incorrecte :\n"+str(self.controleOptions())
                 
        self.lignePourTrace = "****************************** TRACE DETAILLEE ****************************\n" # première ligne de la trace détaillée        
        self.ligneFiltre = "****************************** TRACE SYNTHETIQUE ****************************\n"  # première ligne de la trace synthétique
        
        texte='------------------------- DEBUT DU TRAITEMENT MICMAC ----   '+heure()+' ----------------------------------------\n\n\n'

        photosPropres=list([os.path.basename(x) for x in self.photosPropresAvecChemin])
        texte = texte+'Photos choisies : \n\n'+'\n'.join(photosPropres)+'\n\n'           
        texte = texte+"Ces photos sont recopiées dans le répertoire du chantier : \n\n"+self.repTravail+'\n\n'  
        self.ajoutLigne(texte)



    # ------------------ TAPIOCA --------------------
    
    
    def lanceTapioca(self):
        
        self.etape = 0
        if self.modeTapioca.get()=="All":
            self.echelle1PourMessage = self.echelle1.get()
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle1.get(),
                       "ExpTxt=1"]
            
        if self.modeTapioca.get()=="MulScale":
            self.echelle1PourMessage = self.echelle2.get()
            self.echelle2PourMessage = self.echelle3.get()            
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle2.get(),      
                       self.echelle3.get(),
                       "ExpTxt=1"]
            
        if self.modeTapioca.get()=="Line":
            self.echelle1PourMessage = self.echelle4.get()            
            tapioca = [self.mm3d,
                       "Tapioca",
                       self.modeTapioca.get(),
                       '.*'+self.extensionChoisie,
                       self.echelle4.get(),               
                       self.delta.get(),
                       "ExpTxt=1"]
            
        self.lanceCommande(tapioca,
                           self.filtreTapioca)
                                    
    def filtreTapioca(self,ligne):
        
        if ligne[0]=="|":
            return ligne        
        if 'points' in ligne and len(ligne)<=15:            
            return ligne
        if 'mises en' in ligne:
            return ligne
        if 'matches' in ligne:
            return ligne           
        if 'utopano' in ligne and self.etape==0:                    # début de la première étape sur la première échelle
            self.etape+=1
            return heure()+"\nRecherche des points remarquables et des correspondances sur une image de taille "+self.echelle1PourMessage+" pixels.\n\n"
        if 'utopano' in ligne and self.etape==1:                    # début de la seconde étape sur la seconde échelle
            self.etape+=1
            if self.echelle2PourMessage=="-1":
                return "\nRecherche des points remarquables et des correspondances sur l'image entière.\n\n"
            if self.echelle2PourMessage!="":
                return "\nRecherche des points remarquables et des correspondances sur une image de taille "+self.echelle2PourMessage+" pixels.\n\n"
            return ligne

    # ------------------ TAPAS -----------------------
        
    def lanceTapas(self):

        tapas = [self.mm3d,
                 "Tapas",
                 self.modeCheckedTapas.get(),
                 '.*'+self.extensionChoisie,
                 'Out=Arbitrary',
                 'ExpTxt=1']        
        self.lanceCommande(tapas,
                           self.filtreTapas,
                           "Calibration, pour trouver les réglages intrinsèques de l'appareil photo\nRecherche d'un point de convergence au centre de l'image.\n\n"        )

    def filtreTapas(self,ligne): 
        if ('RESIDU LIAISON MOYENS' in ligne) or ('Residual' in ligne) :   # Residual pour la version 5999
            self.nbResiduTapas+=1
            return ligne
        if ligne[0]=="|":
            return ligne      
        return

    # ------------------ APERO

    def lanceApero(self):

        apero = [self.mm3d,
                 "Apero",
                 os.path.basename(self.miseAEchelle)]
        self.lanceCommande(apero,
                           info="Fixe l'orientation (axe et plan) et met à l'échelle en fonction des options 'calibration'")

        
    # ------------------ APERICLOUD -----------------------
    
    def lanceApericloud(self):
        apericloud=[self.mm3d,
                    "AperiCloud",
                    '.*'+self.extensionChoisie,
                    self.orientation(),
                    "Out=AperiCloud.ply",
                    "ExpTxt=1"]
        self.lanceCommande(apericloud,
                           self.filtreApericloud,
                           "Positionne les appareils photos autour du sujet.\n\Création d'un nuage de points grossier.")

    def filtreApericloud(self,ligne):
        if ligne[0]=="|":
            return ligne        
        if "cMetaDataPhoto" in ligne:
            print("ligne avec meta : ",ligne)
            return "\n#### ATTENTION : Des Metadonnées nécessaires sont absentes des photos. Vérifier l'exif.\n\n" 

    # ------------------ Meslab 1 : ouvre AperiCloud.ply avec l'outil choisi par l'utilisateur --------------------------
    
    def lanceApericloudMeshlab(self):                       # ouvre le ply créé par AperiCloud avec l'outil prévu et le laisse ouvert
     
        if os.path.exists('AperiCloud.ply'):
            if not os.path.exists(self.meshlab):
                open_file('AperiCloud.ply')
                return             
            self.lanceCommande([self.meshlab,'AperiCloud.ply'],
                              info="Ouverture du nuage de points après Apericloud",
                              attendre=False)
        else:
           texte="\nPas de fichier AperiCloud.ply généré.\n"
           self.ajoutLigne(texte)
           self.messageNouveauDepart = texte+"Consulter la trace.\n"
           return -1


    def lanceBascule(self):
        GCPBascule = [  self.mm3d,
                        "GCPBascule",
                        '.*'+self.extensionChoisie,
                        self.orientation(),
                        "bascul",
                        os.path.basename(self.dicoAppuis),                             
                        os.path.basename(self.mesureAppuis)]
        self.lanceCommande(GCPBascule) 

           
    # ------------------ MALT -----------------------
    
    def lanceMalt(self):
        malt = [self.mm3d,
                "Malt",
                self.modeMalt.get(),
                ".*"+self.extensionChoisie,
                self.orientation(),
                "Master="+self.maitreSansChemin]
        self.lanceCommande(malt,
                           self.filtreMalt,
                           "ATTENTION : cette procédure est longue : patience !")

    def filtreMalt(self,ligne):
        if ligne[0]=="|":
            return ligne
        if 'BEGIN BLOC' in ligne:
            return ligne        
        
    # ------------------ C3DC : alternative à Malt avec un masque 3D -----------------------
        
    def lanceC3DC(self):
        # Si on a un masque 3D on l'utilise et on ne cherche pas plus loin :
        C3DC = [self.mm3d,
                "C3DC",
                "MicMac",
                ".*"+self.extensionChoisie,
                self.orientation(),
                "Masq3D="+self.masque3DSansChemin,
                "Out=modele3D.ply"]
        self.lanceCommande(C3DC,
                           self.filtreC3DC,
                           "ATTENTION : cette procédure est longue : patience !")

    def filtreC3DC(self,ligne):
        if ligne[0]=="|":
            return ligne
        if 'BEGIN BLOC' in ligne:
            return ligne
                
    # ------------------ NUAGE2PLY -----------------------
    # exemple après GeomImage : C:\MicMac64bits\bin\nuage2ply.exe MM-Malt-Img-P1000556\NuageImProf_STD-MALT_Etape_8.xml Attr=P1000556.JPG Out=modele3D.ply    
    def lanceNuage2PlyGeom(self):

        Nuage2Ply = [self.mm3d,
                     "Nuage2Ply",
                     'MM-Malt-Img-'+self.nomMaitreSansExtension+'/NuageImProf_STD-MALT_Etape_8.xml',
                     'Attr='+self.maitreSansChemin,
                     'Out=modele3D.ply']
        self.lanceCommande(Nuage2Ply)
                           
    # exemple aprés UrbanMNE : mm3d Nuage2Ply "MEC-Malt/NuageImProf_STD-MALT_Etape_8.xml" Scale=8 Attr="MEC-Malt/Z_Num8_DeZoom1_STD-MALT.tif" Out="modele3D.ply"
    def lanceNuage2PlyUrban(self):
        Nuage2Ply = [self.mm3d,
                     "Nuage2Ply",
                     "MEC-Malt/NuageImProf_STD-MALT_Etape_8.xml",
                     "Scale=8",
                     "Attr=MEC-Malt/Z_Num8_DeZoom1_STD-MALT.tif",
                     'Out=modele3D.ply']
        self.lanceCommande(Nuage2Ply)
    
    # ------------------ Meslab 2 --------------------------
    
    def lanceMeshlab(self):
        aOuvrir = os.path.join(self.repTravail,"modele3D.ply")  
        if not os.path.exists(aOuvrir):
           texte="Pas de fichier modele3D.ply généré.\n\nEchec du traitement MICMAC"
           self.ajoutLigne(texte)
           return -1
        if not os.path.exists(self.meshlab):
            open_file('AperiCloud.ply')
            return        
        meshlab = [self.meshlab, aOuvrir]        
        self.lanceCommande(meshlab,
                           info="Nuage de points modele3D.ply généré.",
                           attendre=False)

    ################################## UTILITAIRES MICMAC ###########################################################

    def OutilQualitePhotosLine(self):

        if self.pasDePhoto():return       
        if self.pasDeMm3d():return
        
    # on copie les photos dans un répertoire de test

        self.copieDansRepertoireDeTest()

        self.encadre("Détermine un indice de qualité des photos en mode 'line'\n\n"+
                     "Le résultat sera inscrit dans le fichier trace synthétique\n\nPatience...",nouveauDepart='non')

        self.ajoutLigne(heure()+"Debut de la recherche sur la qualité des photos mode 'Line'.")        
        self.qualiteTrouvee = list()
        qualite = [self.mm3d,
                   "Tapioca",
                   "Line",
                   ".*"+self.extensionChoisie,      #'"'+str(self.repTravail+os.sep+".*"+self.extensionChoisie)+'"',
                   "1000",               
                   "1",
                   "ExpTxt=1"]

            
        self.lanceCommande(qualite,
                           self.filtreQualite)

        # analyse des résultats :
        os.chdir(self.repTravail)
        self.analyseQualitePhotos()
        
        self.ajoutLigne("\n"+heure()+" : Fin de la recherche sur la qualité des photos mode 'Line'.")
        self.ajoutLigne("\n\n ******")
        ligneFiltre = self.ligneFiltre  #l'écriture de la trace efface self.ligneFiltre et encadre doit être en fin de paragraphe
        self.ecritureTraceMicMac()        
        self.encadre(ligneFiltre)    

    def OutilQualitePhotosAll(self):
        
        if self.pasDePhoto():return
        if self.pasDeMm3d():return
        
    # on copie les photos dans un répertoire de test

        self.copieDansRepertoireDeTest()

        self.encadre("Détermine un indice de qualité des photos en mode 'All' ou 'MulScale' \n\n"+
                     "Le résultat sera inscrit dans le fichier trace synthétique\n\nPatience...",nouveauDepart='non')    
        
         
        self.ajoutLigne(heure()+"Debut de la recherche sur la qualité des photos, mode 'All' ou 'MulScale'.")        
        self.qualiteTrouvee = list()
        
        qualite = [self.mm3d,
                   "Tapioca",
                   "All",
                   ".*"+self.extensionChoisie,
                   "1000",
                   "ExpTxt=1"]          
            
        self.lanceCommande(qualite,
                           self.filtreQualite)

        # analyse des résultats :
        os.chdir(self.repTravail)          # car copieDansRepertoireDeTest a changer le répertoire de travail
            
        self.analyseQualitePhotos()
        
        self.ajoutLigne("\n"+heure()+" : Fin de la recherche sur la qualité des photos, mode 'All' ou 'MulScale'.")
        self.ajoutLigne("\n\n ******")
        ligneFiltre = self.ligneFiltre  #l'écriture de la trace efface self.ligneFiltre et encadre doit être en fin de paragraphe
        self.ecritureTraceMicMac()        
        self.encadre(ligneFiltre)     
        
    def filtreQualite(self,ligne):
        
        if 'matches' in ligne:
            self.encadrePlus("***")
            self.qualiteTrouvee.append(ligne)
            return ligne           
        return ligne
    def analyseQualitePhotos(self):
        if self.pasDePhoto():return
        if self.pasDeMm3d():return
        #somme des scores de chaque photo :
        homol = dict()
        nb = dict()
        moyenne = dict()
        for p in self.photosSansChemin:
            image = os.path.splitext(p)[0]
            homol[image] = 0
            nb[image] = 0
        for e in self.qualiteTrouvee:
            for p in self.photosSansChemin:
                image = os.path.splitext(p)[0]
                if image+".tif.dat" in e:  # on a trouvé la photo dans la ligne
                    nombre = int(e.split()[-2])     #le nombre de points homologues est l'avant dernière info de la ligne 
                    homol[image] = homol[image] + nombre
                    nb[image] = nb[image] + 1
                    moyenne[image] = homol[image]/nb[image]
                    
        listeHomol = list(moyenne.items())
        listeHomol.sort(key=lambda e: e[1],reverse=True)
        self.effaceBufferTrace()
        self.ajoutLigne("\n ******\n\nClassement des photos par nombre de points homologues :\n\n")
        for e in listeHomol:
            self.ajoutLigne("photo "+e[0]+" score = "+str(int(e[1]))+"\n")

        if len(listeHomol)==0:
            self.ajoutLigne("Aucune photo n'a de point analogue avec une autre.\n")

         
    def exploiterHomol(self):
        self.ajoutLigne("\n ****** Qualité des photos suite au traitement : ")
        repHomol = self.repTravail+os.path.sep+'Homol'
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
                        print (e,fic,lignes.__len__())
        self.ajoutLigne("\n ****** Fin d'examen de qualité des photos.")

    def copieDansRepertoireDeTest(self):

        self.encadre("Copie des photos dans un répertoire de test.\n Patience...",nouveauDepart='non')
        self.repTest = self.repTravail+os.path.sep+"test"
        if os.path.exists(self.repTest):
            supprimeArborescenceSauf(self.repTest,os.listdir(self.repTest))
        else:
            os.mkdir(self.repTest)
            for e in os.listdir(self.repTravail):
                if e[-4:] == self.extensionChoisie:
                    shutil.copy(e,self.repTest)
        os.chdir(self.repTest)


    ###################### Appareil photo : affiche le nom de l'apapreil de la première photo, la focale, la taille du capteur dans dicocamera

    def OutilAppareilPhoto(self):

        if self.pasDePhoto():return
        if self.pasDeExiftool():return
              
        texte = " ******\nCaractéristiques de l'appareil photo : \n\n"
        self.fabricant =  self.tagExif("Make")
        if self.fabricant!=str():
            texte = texte + "fabricant : "+self.fabricant+"\n"
            
        self.nomCamera = self.tagExif("Model")
        if self.nomCamera==str():
            self.encadre ("Nom de l'appareil photo inacessible.")
            return
        else:
            texte = texte+"Nom de l'appareil photo : "+self.nomCamera+"\n"
            
        self.focale35MM = self.tagExif("FocalLengthIn35mmFormat")
            
        self.focale = self.tagExif("FocalLength")
        if self.focale==str():
            texte = texte +("\nPas de focale dans l'exif.")
        else:
            texte = texte+"\nFocale : "+ self.focale+"\n"

        if self.focale35MM=="" and "35" not in self.focale:
            texte = texte +("Pas de focale équivalente 35 mm dans l'exif :\nPrésence de la taille du capteur dans DicoCamera nécesssaire.")
        else:
            if self.focale35MM=="":
                texte = texte+"\nFocale équivalente 35 mm absente de l'exif\n" 
            else:
                texte = texte+"\nFocale équivalente 35 mm : "+ self.focale35MM+"\n"            

        if not os.path.isfile(self.CameraXML):
            texte = texte+"\nDicoCamera.xml non trouvé : paramètrer au préalable le chemin de MicMac\\bin."
        else:
            self.tailleCapteurAppareil()
            if self.tailleCapteur==str():
                texte = texte + "\n\nL'appareil est inconnu dans DicoCamera.XML.\n\n"                          
            else:
                texte = texte + "\n\nL'appareil est connu dans DicoCamera.XML.\n\n"+\
                          "Taille du capteur en mm : \n\n"+self.tailleCapteur+"."

        
        # écriture du résultat dans le fichier trace et présentation à l'écran
        
        self.effaceBufferTrace()
        self.ajoutLigne("\n\nAppareil photo :\n"+texte)
        self.ecritureTraceMicMac()        
        self.encadre(texte)

        
    # tag dans l'exif : renvoi la valeur du tag 'tag' dans l'exif de la première photo (on suppose qu'elles sont identiques pour toutes les photos)
                          
    def tagExif(self,tag):
        self.tag = str()        
        exif = (self.exiftool,
                "-"+tag,
                self.photosAvecChemin[0])            
        self.lanceCommande(exif,
                           self.FiltreTag)
        return self.tag

    def FiltreTag(self, ligne):                             # ne retourne rien (pour éviter la trace, mais positionne si possible self.tag
        if "can't open" in ligne:
            return "Erreur dans exiftool : "+ligne
        try: self.tag = ligne.split(":")[1].strip()         # pour récupérer le nom, et supprimer le retour chariot de fin de ligne
        except: pass
        return None

    # tags dans l'exif : renvoi la valeur du tag 'tag' dans l'exif de toutes les photos
                          
    def tagsExif(self,tag):
              
        self.tags = list()
        exif = (self.exiftool,
                "-"+tag,
                os.path.join(self.repTravail))
        self.lanceCommande(exif,
                           self.FiltreTags)
        return self.tags

    def FiltreTags(self, ligne):
        ajout = afficheChemin(ligne.strip().replace("=",""))
        ajout=ajout.replace(afficheChemin(self.repTravail),"")    # pour ne pas afficher le chemin
        self.tags.append(ajout+"\n")                              # pour récupérer le nom, et supprimer le retour chariot de fin de ligne
        return None
    
    # taille du capteur, si le nom est connu
                          
    def tailleCapteurAppareil(self):
        
        self.tailleCapteur = str()                      # par défaut retour ""
        if self.nomCamera == str():                     # si pas de nom d'appareil : retour
            return -1
                          
        self.dicoCamera = str()
        if os.path.exists(self.CameraXML):              # si pas de fichier dicoCamera : retour (il est vrai que la taille pourrait être ailleurs !) 
            with  open(self.CameraXML) as infile:
                self.dicoCamera = infile.readlines()    #lecture dicoCamera.xml
        else: return -2
                          
        texte = str()
        for e in self.dicoCamera:                       # recherche du nom de l'appareil dans dicoCamera
            if texte=="vu":
                if "SzCaptMm" in e:                     # le nom est repéré, voit-on la taille ?
                    self.tailleCapteur = e.replace("<SzCaptMm>","").replace("</SzCaptMm>","").strip().replace(" "," mm - ")+" mm"
                    return 1                            # la taille est trouvée : on quitte
                if "</CameraEntry>" in e:               # pas de taille trouvée sous ce nom
                    texte = str()                       # on poursuit
            if self.nomCamera in e:                     # nom trouvé
                texte="vu"
        
    # Mise à jour de DicoCamera

    def miseAJourDicoCamera(self):
        
        if self.pasDePhoto():return
        if self.pasDeMm3d():return
        if self.pasDeExiftool():return     
        
        self.nomCamera = self.tagExif("Model")
        if self.nomCamera==str():
            self.encadre("Pas trouvé de nom d'appareil photo dans l'exif.")
            return
        if not os.path.isfile(self.CameraXML):
          self.encadre("DicoCamera.xml non trouvé : paramètrer au préalable le chemin de MicMac\\bin.")
          return
        if self.tailleCapteurAppareil()==1:
            self.encadre(   "Le fichier DicoCamera.xml contient la taille du capteur pour l'appareil :\n\n"+
                             self.nomCamera+"\n\ntaille  = "+self.tailleCapteur+
                             "\n\nModification non prévue dans cette version de l'outil AperoDeDenis\n----------------")
            return            

        self.menageEcran()
        self.item1001.configure(text="Pour l'appareil "+self.nomCamera)
        self.item1000.pack()

    def dimensionCapteurOK(self):
        if not os.path.isfile(self.CameraXML):
            self.encadre("Paramètrer au préalable le chemin de MicMac\\bin.")
            return                                               
        dimension = self.item1003.get()
        # paragraphe à rajouter à DicoCamera  : texte
        texte = self.dicoCameraXMLTaille.replace("NomCourt",self.nomCamera)          
        texte = texte.replace("Nom",self.nomCamera)
        texte = texte.replace("tailleEnMM",dimension)

        #lecture dicocamera.xml :
        with  open(self.CameraXML) as infile:
            self.dicoCamera = infile.readlines()    #lecture dicoCamera.xml
        # ajout du paragraphe enfin de xml :
        newDico = "".join(self.dicoCamera).replace(self.dicoCameraXMLFin,texte+self.dicoCameraXMLFin)
        if os.path.getsize(self.CameraXML)>0:                       # pour éviter de copier un fichier "vide"
            try: shutil.copy(self.CameraXML,self.CameraXML+".sav")
            except: pass
        if os.path.exists(self.CameraXML+".sav"):
            try:
                with  open(self.CameraXML,mode="w") as outfile:
                    outfile.write(newDico)
            except:
                self.encadre("Erreur lors de l'écriture de DicoCamera.xml\nUne sauvegarde a été créée : DicoCamerra.xml.sav")
                return
        else:
            self.encadre("Dimensions du capteur non mis à jour\n")
            return

        self.encadre("Dimensions du capteur mis à jour\n"+texte)
        

    def dimensionCapteurKO(self):
        self.encadre("Dimensions du capteur non mis à jour")


    def toutesLesFocales(self):

        if self.pasDePhoto():return
        if self.pasDeExiftool():return        
        
        texte=self.tagsExif("FocalLength")
        texte=texte+["\n",]+self.tagsExif("FocalLengthIn35mmFormat")
        self.effaceBufferTrace()
        self.ajoutLigne(" ****** \nToutes les focales : \n\n"+"".join(texte)+"\n ****** \n")
        self.ecritureTraceMicMac() 
        self.encadre(texte)
        
    ################################## Le menu AIDE ###########################################################
                # provisoirement retirés :
                #"            Afficher les photos après nettoyage      : visualise les photos après nettoyage\n"
                #"       - Nettoyer les photos : permet de délimiter les zones ""utiles"" des photos.\n"
                #"         Cette option n'est pas active dans la version 1.0 de l'outil.\n"        
    def aide(self):
        aide1=  "Interface graphique pour lancer les modules de MICMAC.\n\n"+\
                "Utilisable sous Linux, Windows, Mac OS.\n"+\
                "Logiciel libre diffusé sous licence CeCILL-B.\n"+\
                "-----------------------------------------------------------------------------------------------------------------\n\n"+\
                "La barre de titre présente le nom du chantier et la version de l'outil. Une * indique que le chantier est à sauvegarder.\n\n"+\
                "Menu Fichier :\n\n"+\
                "       - Nouveau chantier : constitution d'un 'chantier' comportant les photos, les options d'exécution de Micmac et\n"+\
                "         les résultats des traitements.\n"+\
                "         Les paramètres du chantier sont conservés dans le fichier "+self.paramChantierSav+".\n"+\
                "         Enregistrer le chantier crée une arborescence dont la racine est le répertoire des photos et le nom du chantier.\n\n"+\
                "       - Ouvrir un chantier : revenir sur un ancien chantier pour le poursuivre ou consulter les résultats.\n\n"+\
                "       - Enregistrer le chantier : enregistre le chantier en cours sans l'exécuter.\n"+\
                "         Une * dans la barre de titre indique que le chantier a été modifié.\n"+\
                "         Le chantier en cours, même non enregistré, est conservé lors de la fermeture de l'application.\n\n"+\
                "       - Renommer le chantier : personnalise le nom du chantier.\n\n"+\
                "         Le chantier est déplacé dans l'arborescence en indiquant un chemin absolu ou relatif.\n"+\
                "         Par exemple : 'D:\\MonPremierChantier' nomme 'MonPremierChantier' sous la racine du disque D.\n"+\
                "         Attention : le changement de disque n'est pas possible dans cette version de l'outil.\n\n"+\
                "       - Du ménage ! : Supprimer les chantiers : Chaque chantier crée une arborescence de travail.\n"+\
                "         Cet item permet de supprimer les répertoires devenu inutiles.\n"+\
                "         Aprés un message demandant confirmation la suppression est définitive, sans récupération possible.\n\n"+\
                "       - Quitter : quitte l'application, le chantier en cours est conservé et sera ouvert lors de la prochaine exécution.\n\n"+\
                "Menu Edition :\n\n"+\
                "       - Afficher l'état du chantier : affiche les paramètres du chantier et son état d'exécution.\n"+\
                "         Par défaut l'état du chantier est affiché lors du lancement de l'application.\n"+\
                "         Cet item est utile après un message ou l'affichage d'une trace.\n\n"+\
                "       - Plusieurs items permettent de consulter les photos, les traces et les vues 3D du chantier en cours.\n\n"+\
                "            Visualiser toutes les photos sélectionnées : visualise les photos\n"+\
                "            Visualiser les points GPS                  : visu des seules photos avec points GPS.\n"+\
                "            Visualiser le masque 3D                    : visualise le masque 3D\n"+\
                "            Visualiser le masque 2D et l'image maitre  : visualise le masque 2D s'il existe et de l'image maître.\n"+\
                "            Visualiser la ligne horizontale/verticale  : visualise le repère Ox ou Oy.\n"+\
                "            Visualiser la zone plane                   : visualise la zone plane\n"+\
                "            Visualiser la distance                     : visualise de la distance et les points associés.\n"+\
                "\n"+\
                "            Afficher la trace complete du chantier     : visualise la trace complète, standard micmac\n"+\
                "            Afficher la trace synthétique du chantier  : visualise la trace filtrée par aperoDeDenis, moins bavarde\n"+\
                "            Afficher l'image 3D aprés Tapas            : lance l'outil pour ouvrir les .PLY sur l'image 3D produite par Tapas\n"+\
                "            Afficher l'image 3D aprés Malt             : visualise l'image densifiée produite par Malt.\n\n"+\
                "Menu MicMac :\n\n"+\
                "       - Choisir les photos : permet choisir les photos JPG pour le traitement.\n\n"+\
                "       Remarque  : les JPG doivent comporter un EXIF avec la focale utilisée pour la prise de vue..\n"+\
                "                   Consulter la documentation MicMac concernant les photos utilisables et le fichier DicoCamera.xml.\n\n"+\
                "       - Options : choisir les options des modules Tapioca, Tapas (nuage non densifié)  puis de Malt (nuage densifié) : \n\n"+\
                "         Les 3 options suivantes concernent le calcul du nuage de points NON densifié :\n\n"+\
                "                    - Tapioca : options et sous options associées (échelles, fichier xml)\n"+\
                "                    - Tapas   : Choix d'un mode de calcul, possibilité d'arrêter le traitement après tapas.\n"+\
                "                                L'arrêt après Tapas est nécessaire pour décrire le masque 3D de C3DCla.\n"+\
                "                                Produit une image 3D avec position des appareils photos.\n"+\
                "                    - Calibration : définir un axe, une zone plane, une distance pour définir le repère du chantier.\n\n"+\
                "         Les 3 options suivantes concernent le calcul du nuage de points densifié :\n\n"+\
                "                    - Malt    : choix du mode, désigner une image maitresse et dessiner le masque associé.\n"+\
                "                                Seuls les points visibles sur l'image maitre seront sur l'image 3D finale.\n"+\
                "                                Le masque limite la zone ""utile"" de l'image 3D finale.\n"+\
                "                                La molette permet de zoomer et le clic droit maintenu de déplacer l'image.\n"+\
                "                                Choisir une image maitresse réinitialise le masque.\n\n"+\
                "                    - C3DC    : dessiner le masque 3D sur le nuage de points AperiCloud généré par Tapas..\n"+\
                "                                Les touches fonctions à utiliser sont décrites dans l'onglet.\n"+\
                "                                Le masque limite la zone en 3 dimensions de l'image finale.\n"+\
                "                                L'outil de saisie est issu de micmac.\n\n"+\
                "                    - GPS     : Définir les points de calage GPS qui permettent de géolocaliser la scène.\n"+\
                "                                Pour être utilisé chaque point doit être placé sur au moins 2 photos.\n\n"+\
                "       - Lancer MicMac : Enregistre le chantier et lance le traitement avec les options par défaut ou choisies par l'item 'options'.\n"+\
                "                         Relance micmac si l'arrêt a été demandé après tapas.\n"+\
                "                         Lancer micmac bloque les photos et les options du chantier.\n"+\
                "                         Pour débloquer le chantier il faut lancer micmac à nouveau et choisir le débloquage.\n\n"+\
                "menu Outils :\n\n"+\
                "       - Nom et focale de l'appareil photo : fabricant, modéle et focale de la première photo.\n"+\
                "         Il y a 2 types de focales : focale effective et focale équivalente 35 mm.\n"+\
                "         Indique si l'appareil photo est connu dans '/XML MicMac/DicoCamera.xml' (uniquement dans ce fichier).\n"+\
                "       - Toutes les focales des photos : focales et focales equivalentes en 35mm.\n"+\
                "         Les focales doivent être identiques pour toutes les photos : si besoin créer plusieurs chantiers.\n"+\
                "       - Mettre à jour DicoCamera.xml : ajouter la taille du capteur dans '/XML MicMac/DicoCamera.xml'.\n\n"+\
                "         La taille du capteur dans DicoCamera.xml est requise si la focale équivalente 35mm est absente de l'exif.\n\n"+\
                "         La taille du capteur facilite les calculs et améliore les résultats.\n\n"+\
                "       - Qualité des photos 'Line' : calcule le nombre moyen de points homologues par photo en mode 'Line'.\n"+\
                "       - Qualité des photos 'MulScale ou All' : calcule le nombre moyen de points homologues par photo.'.\n"+\
                "         Ce nombre informe sur la qualité relative des photos au sein du chantier.\n"+\
                "         La présence de photos avec peu de points homologues peu faire échouer le traitement.\n"+\
                "         Il est préférable de traiter peu de photos mais de bonne qualité.\n\n"+\
                "menu Paramètrage :\n\n"+\
                "       - Affiche les paramètres : visualise les chemins de micmac\\bin, d'exiftool et du fichier Meshlab ou Cloud Compare.\n"+\
                "         Ces paramètres sont sauvegardés de façon permanente dans le fichier "+self.fichierParamMicmac+".\n\n"+\
                "       - Désigner le répertoire MicMac\\bin : répertoire où se trouvent les modules de MicMac \n"+\
                "       - Désigner l'application exiftool.\n"+\
                "       - Désigner l'application ouvrant les .PLY. Ce peut être  Meshlab, Cloud Compare ou autre.\n\n"+\
                "         Sous Windows Meshlab se trouve sous un répertoire nommé VCG.\n\n"+\
                "menu Aide :\n\n"+\
                "       - Aide \n"+\
                "       - Quelques conseils : sur la prise de vue et les paramètres.\n"+\
                "       - A propos\n\n\n"+\
                " Quelques précisions :\n"+\
                " Cette version a été développée sous Windows XP et Seven avec micmac rev 5508 d'avril 2015.\n"+\
                " L'utilisation d'autres versions de Micmac peut poser problème.\n"+\
                " Cette version n'admet que des photos au format JPG.\n"+\
                " L'outil libre XNView propose des conversions 'sans perte' à partir de multiples formats (via Imagemagick).\n\n"+\
                " Consulter la documentation de MicMac, outil réalisé par l'IGN.\n\n"+\
                " Consulter le guide d'installation et de prise en main d'AperoDeDenis.\n\n"+\
                "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"

        self.cadreVide()
        self.ajoutLigne(aide1)
        self.texte201.see("1.1")
        
    def conseils(self):
        aide2=  "Interface graphique pour lancer les modules de MICMAC : quelques conseils.\n\n"+\
                "Prises de vue  :\n"+\
                "                - Le sujet doit être immobile durant toutes la séance de prise de vue.\n"+\
                "                - Les photos doivent être nettes : attention à la profondeur de champ.\n"+\
                "                  Les photos de personnes ou d'objet en mouvement sont déconseillées\n"+\
                "                  Les surfaces lisses ou réfléchissantes sont défavorables.\n"+\
                "                - Si le sujet est central prendre une photo tous les 20°, soit 9 photos pour un 'demi-tour', 18 pour un tour complet.\n"+\
                "                - Si le sujet est en 'ligne' le recouvrement entre photos doit être des 2/3 au minimum.\n"+\
                "                - Tester la 'qualité' des photos au sein du chantier (voir les items du menu Outils).\n"+\
                "                  les photos ayant un mauvais score doivent être supprimées du chantier : elle peuvent faire échouer le traitement.\n"+\
                "                - La présence des dimensions du capteur de l'appareil dans DIcoCamera.xml améliore le traitement.\n"+\
                "                  Cette présence est obligatoire si l'exif ne présente pas la focale équivalente 35mm.\n"+\
                "                  Pour ajouter la taille du capteur utiliser le menu 'Outils//metre à jour DicoCamera'.\n"+\
                "Précautions :    \n"                                              +\
                "                 Toutes les photos doivent être prises avec la même focale, ne pas utiliser la fonction autofocus.\n"+\
                "                 Eviter aussi la fonction 'anti tremblement' qui agit en modfiant la position du capteur.\n\n"         +\
                "Options :\n"+\
                "               - Tapioca : Si le sujet est central conserver les paramètres par défaut.\n"                             +\
                "               - Tapioca : Si le sujet est en ligne choisir 'line' dans les options de Tapioca, \n"                    +\
                "                                                   puis delta = 1, si les photos se recouvrent au 2/3, \n"             +\
                "                                                   ou   delta = 2 voire +, si le recouvrement est plus important.\n\n" +\
                "               - Tapas : Si l'appareil photo est un compact ou un smartphone choisir RadialBasic, \n"                  +\
                "                         Si l'appareil photo est un reflex haut de gamme choisir RadialExtended \n"                    +\
                "                         Si l'appareil photo est de moyenne gamme choisir RadialStd  \n"                               +\
                "                         L'arrêt aprés Tapas est conseillé : la visualisation du nuage de points non densifié\n"       +\
                "                         permet de définir un masque, 2D ou 3D, pour l'étape suivante.\n\n"                            +\
                "               - Calibration : permet de définir un repère et une métrique(axe, plan et distance obligatoires).\n\n"+\
                "               - Malt : pour le mode GeomImage indiquer une image maitresse, choisir la plus représentative du résultat souhaité.\n"          +\
                "                        Seuls les points visibles sur cette image seront conservés dans le nuage de points.\n"                +\
                "                        Sur cette image maitresse tracer le masque en 2 Dimensions délimitant la partie 'utile' de la photo.\n"+\
                "                        Le traitement avec masque sera accéléré et le résultat plus 'propre'.\n\n"                                 +\
                "               - C3DC : propose de définir un masque en 3D qui conservera tout le volume concerné.\n"                  +\
                "                        Alternative à Malt, le traitement est beaucoup plus rapide. Nécessite la dernière version de MicMac.\n\n"+\
                "               - GPS  : définir des points cotés et les placer sur 2 photos. La trace indique s'ils sont pris en compte\n"+\
                "--------------------------------------------- "+self.titreFenetre+" ---------------------------------------------"
        self.encadre (aide2,50,aligne='left',nouveauDepart='non')

    def commencer(self):
        aide3=  \
                "   Pour commencer avec l'interface graphique MicMac :\n\n"+\
                "   Tout d'abord : Installer MicMac.\n"+\
                "   Puis : Installer Meshlab ou CloudCompare (pour afficher les nuages de points)\n\n"+\
                "   Ensuite, dans cette interface graphique :\n\n"+\
                "1) Paramétrer l'interface : indiquer ou se trouvent le répertoire bin de MicMac et l'éxécutable Meshlab ou CloudCompare.\n"+\
                "2) Choisir quelques photos, pas plus de 5 pour commencer (menu MicMac).\n"+\
                "3) Lancer MicMac en laissant les paramètres par défaut (menu MicMac).\n"+\
                "   Si tout va bien une vue en 3D non densifiée doit s'afficher, patience : cela peut être long.\n"+\
                "4) Si tout va bien alors modifier les paramétres pour la suite du traitement (Malt ou C3DC) (voir la doc).\n"+\
                "   Puis re lancer MicMac pour obtenir une vue 3D densifiée.\n\n"+\
                "5) Si tout ne va pas bien re 'lancer MicMac' et annuler le traitement, puis :\n"\
                "   Lire 'quelques conseils' (menu Aide).\n"+\
                "   Tester la qualité des photos (menu Outils, aprés avoir paramètré exiftool).\n"+\
                "   Examiner les traces (menu Edition),\n"+\
                "   Consulter l'aide (menu Aide),\n"+\
                "   Consulter le guide d'installation et de prise en main de l'interface.\n"+\
                "   Consulter le forum MicMac sur le net, consulter la doc MicMac.\n"+\
                "6) Si une solution apparaît : modifier les options (menu MicMac).\n"+\
                "   puis relancer le traitement.\n"+\
                "7) Si le problème persiste faire appel à l'assistance de l'interface (adresse mail dans l'A-propos)\n"
        self.encadre (aide3,50,aligne='left',nouveauDepart='non')
        
    def aPropos(self):
       
        aide2=self.titreFenetre+("\n\nRéalisation Denis Jouin 2015\n\nLaboratoire Régional de Rouen\n\n"+
                                "Direction Territoriale Normandie Centre\n\n CEREMA\n\ninterface-micmac@cerema.fr")

        self.encadre (aide2,aligne='center',nouveauDepart='non')
        
        #ajout du logo du cerema si possible
        
        try:
            self.logo = ttk.Frame(self.resul100)                                     # cadre dans la fenetre ; affiche la photo sélectionnée              
            self.canvasLogo = tkinter.Canvas(self.logo,width = 225, height = 80)       # Canvas pour revevoir l'image
            self.canvasLogo.pack(fill='both',expand = 1)
            self.logo.pack()
            self.imageLogo = Image.open(self.logoCerema) 
            self.img = self.imageLogo.resize((225,80))
            self.imgTk = ImageTk.PhotoImage(self.img)
            self.imgTk_id = self.canvasLogo.create_image(0,0,image = self.imgTk,anchor="nw") # affichage effectif de la photo dans canvasPhoto
            ttk.Label(self.logo,text="MicMac est une réalisation de l'IGN").pack(pady=5)            
        except:
            pass

        #ajout du logo IGN si possible
        if os.path.exists(self.logoIGN):
            try:
                self.logoIgn = ttk.Frame(self.resul100)                                     # cadre dans la fenetre ; affiche la photo sélectionnée              
                self.canvasLogoIGN = tkinter.Canvas(self.logoIgn,width = 149, height = 162)       # Canvas pour revevoir l'image
                self.canvasLogoIGN.pack(fill='both',expand = 1)
                self.logoIgn.pack(pady=5)
                self.imageLogoIGN = Image.open(self.logoIGN) # self.logoIGN = nom du fichier png
                self.imgIGN = self.imageLogoIGN.resize((149,162))
                self.imgTkIGN = ImageTk.PhotoImage(self.imgIGN)
                self.imgTk_idIGN = self.canvasLogoIGN.create_image(0,0,image = self.imgTkIGN,anchor="nw") # affichage effectif de la photo dans canvasPhoto
            except: pass
            

        
    ################################## Le menu FICHIER : nouveau, Ouverture, SAUVEGARDE ET RESTAURATION, PARAMETRES, outils divers ###########################################################       

    def sauveParam(self):                       # La sauvegarde ne concerne que 2 fichiers; fixes, sous le répertoire d'aperodedenis,
                                                # pour les paramètres généraux : self.fichierParamMicmac
                                                # pour le chantier en cours    : self.fichierParamChantierEnCours 
        self.sauveParamMicMac()
        self.sauveParamChantier()
    
    def sauveParamChantier(self):
        essai = (self.fichierParamChantierEnCours+"essai")       # pour éviter d'écraser le fichier si le diqsque est plein
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
                         self.modeMalt.get(),
                         self.fichierMasqueXML,
                         self.repTravail,
                         self.photosPropresAvecChemin,
                         self.extensionChoisie,
                         self.nomMaitreSansExtension,
                         self.etatDuChantier,
                         self.dicoPointsGPSEnPlace,                       
                         self.maitre,
                         self.masque,
                         self.idPointGPS,
                         self.dicoLigneHorizontale,
                         self.dicoLigneVerticale,
                         self.dicoCalibre,
                         self.distance.get(),
                         self.monImage_MaitrePlan,                                               # Nom de l'image maitresse du plan repere (sans extension)
                         self.monImage_PlanTif,                                                   # nom du masque correspondant
                         self.etatSauvegarde,
                         self.modeCheckedTapas.get(),
                         self.echelle4.get()
                         ),     
                        sauvegarde1)
            sauvegarde1.close()
            supprimeFichier(self.fichierParamChantierEnCours)
            os.rename(essai,self.fichierParamChantierEnCours)            
        except Exception as e:
            print ('erreur sauveParamChantier : ',str(e))

       
    def sauveParamMicMac(self):
        essai = (self.fichierParamMicmac+"essai")       # pour éviter d'écraser le fichier si le diqsque est plein
        try:
            sauvegarde2=open(essai,mode='wb')
            pickle.dump((self.micMac,
                         self.meshlab,
                         self.indiceTravail,
                         self.tousLesChantiers,
                         self.exiftool,
                         self.mm3d
                         ),     
                        sauvegarde2)
            sauvegarde2.close()
            supprimeFichier(self.fichierParamMicmac)
            os.rename(essai,self.fichierParamMicmac)
        except Exception as e:              # Controle que le programme a accès en écriture dans le répertoire d'installation
            print ('erreur sauveParamMicMac : ',str(e))
            texte = "L'interface doit être installée dans un répertoire ou vous avez les droits d'écriture.\n\n"+\
                    "Installer l'interface AperoDeDenis à un emplacement ou vous avez ce droit.\n\n"+\
                    "Répertoire actuel : "+self.repertoireData+".\n\n"+\
                    "Erreur rencontrée : "+str(e)
            self.deuxBoutons(titre="Problème d'installation",question=texte,b1='OK',b2='')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1            
            fin(1)


    ###### Restauration paramètres : la restauration d'un chantier peut concerner un chantier archivé, dans ce cas on restaure un fichier dont le nom est passé en paramètre
                 
    def restaureParamEnCours(self):

        try:
            self.restaureParamChantier(self.fichierParamChantierEnCours)
            sauvegarde2 = open(self.fichierParamMicmac,mode='rb')
            r2=pickle.load(sauvegarde2)
            sauvegarde2.close()
            self.micMac                     =   r2[0]
            self.meshlab                    =   r2[1]
            self.indiceTravail              =   r2[2]
            self.tousLesChantiers           =   r2[3]
            self.exiftool                   =   r2[4]
            self.mm3d                       =   r2[5]                               # spécifique linux/windows

            self.CameraXML = os.path.join(os.path.dirname(self.micMac),self.dicoCameraGlobalRelatif)

        except Exception as e: print("Erreur restauration param généraux : ",str(e))

        self.mm3dOK                         =   verifMm3d(self.mm3d)                # Booléen indiquant si la version de MicMac permet la saisie de masque 3D         
        
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
            self.modeTapioca.set(r[6])
            self.echelle1.set(r[7])
            self.echelle2.set(r[8])
            self.delta.set(r[9])
            self.echelle3.set(r[10])
            self.arretApresTapas.set(r[11])
            self.listePointsGPS             =   r[12]
            self.modeMalt.set(r[13])
            self.fichierMasqueXML           =   r[14]
            self.repTravail                 =   r[15]
            self.definirFichiersTrace()
            self.chantier                   =   os.path.basename(self.repTravail)        
            self.photosPropresAvecChemin    =   r[16]
            self.extensionChoisie           =   r[17]
            self.nomMaitreSansExtension     =   r[18]
            self.etatDuChantier             =   r[19]
            self.dicoPointsGPSEnPlace       =   r[20]         
            self.maitre                     =   r[21]
            self.masque                     =   r[22]
            self.idPointGPS                 =   r[23]
            self.dicoLigneHorizontale       =   r[24]
            self.dicoLigneVerticale         =   r[25]
            self.dicoCalibre                =   r[26]
            self.distance.set(r[27])
            self.monImage_MaitrePlan        =   r[28]                                               # Nom de l'image maitresse du plan repere (sans extension)
            self.monImage_PlanTif           =   r[29]                                               # nom du masque correspondant
            self.etatSauvegarde             =   r[30]
            self.modeCheckedTapas.set(r[31])
            self.echelle4.set(r[32])

            if self.maitreSansChemin==str():
                self.item701.config(text="Pas d'image maitresse.")              
            else:
                self.item701.config(text="image maitresse = "+self.maitreSansChemin)
                
            if self.masqueSansChemin!=str():
                self.item703.config(text="Masque = "+self.masqueSansChemin)                       # réinitialise le masque
            else:
                self.item703.config(text="Pas de masque.")
           
        except Exception as e:
            pass     


    ########################### affiche les messages à l'écran : cadre, état, boites de dialogues standards, ménage                

    def encadreEtTrace(self,texte,nbLignesmax=40,aligne='center'):
        self.ajoutLigne(texte)
        self.ecritureTraceMicMac()                          # on écrit la trace        
        self.encadre(texte,nbLignesmax,aligne)

    def encadre(self,texte,nbLignesmax=38,aligne='center',nouveauDepart='oui'):
        if texte.__class__==tuple().__class__:
            texte=' '.join(texte)
        if texte.__class__==list().__class__:
            texte=' '.join(texte)
        if texte.count('\n')>nbLignesmax:                           # limitation à nbLignesmax du nombre de lignes affichées 
            texte='\n'.join(texte.splitlines()[0:nbLignesmax-5]) +'\n.......\n'+'\n'.join(texte.splitlines()[-3:])
        self.menageEcran()
        self.nbEncadre+=1
        if self.nbEncadre>6 and nouveauDepart=='oui' and self.systeme=='nt':
            self.messageNouveauDepart =  texte
            self.nouveauDepart()                                  # lance une fenêtre  nouvelle sous windows (l'actuelle peyt-être polluée par le traitement
            return
        self.texte101.configure(text=texte,justify=aligne)
        self.texte101Texte = texte # pour encadrePlus
        self.resul100.pack()
        fenetre.title(self.etatSauvegarde+self.chantier+" - "+self.titreFenetre)
        fenetre.focus_force()                                       # force le focus (it is impolite !)
        fenetre.update()

    def encadrePlus(self,plus):
        self.texte101Texte+=plus
        if len(self.texte101Texte.split("\n")[-1])>60:
            self.texte101Texte+="\n" 
        self.texte101.configure(text=self.texte101Texte)
        fenetre.update()
        time.sleep(0.01)
        
    def menageEcran(self):                                          # suppression écran (forget) de tous les FRAMES
        self.listeFrames()
        for a in self.l:
            try: exec("self."+a+".pack_forget()")
            except Exception as e : print("Erreur menage : ",str(e))

    def listeFrames(self):                                          # CREE LA LISTE DE TOUS LES FRAMES de la fenetre self
        self.l=list()
        for v,t in self.__dict__.items():                           # un print (v,t) ici affiche l'identifiant arborescent des widgets (fenetre/frame/widget)
            if t.__class__ in [ttk.Frame().__class__,ttk.Notebook().__class__]:
                self.l.append(v)



    #################################### Supprime (ou conserve) les répertoires de travail
    
    def supprimeRepertoires(self):
        
        if len(self.tousLesChantiers)==0:
                texte='\nTous les répertoires de travail sont déjà supprimés.\n'
                self.encadre(texte)
                return          
        supprime = list()
        conserve = list()
        texte = str()
        attention = str()
        self.tousLesChantiers.sort(key=os.path.basename)                                    # tri suivant le nom du chantier
        self.choisirUnePhoto(self.tousLesChantiers,
                             titre='Chantiers à supprimer', 
                             mode='extended',
                             message="Multiselection possible.",
                             boutonDeux="Annuler",
                             objets='repertoires')      # renvoi  : self.selectionPhotosAvecChemi
        if len(self.selectionPhotosAvecChemin)==0:
            return
        
        if len(self.selectionPhotosAvecChemin)==1:
            self.deuxBoutons('Suppression des répertoires de travail superflus',
                             'Le répertoire suivant va être supprimé, sans mise en corbeille : \n\n'+'\n'.join(self.selectionPhotosAvecChemin),
                             'Confimez',
                             'Annuler')
        if len(self.selectionPhotosAvecChemin)>1:
            if self.repTravail in self.selectionPhotosAvecChemin:
                attention="ATTENTION : le chantier en cours va être supprimé.\n\n"
            self.deuxBoutons('Suppression des répertoires de travail superflus',
                             attention+'Vont être supprimés les répertoires suivants, sans mise en corbeille : \n\n'+'\n'.join(self.selectionPhotosAvecChemin),
                             'Confimez','Annuler')
        if self.bouton==1 or self.bouton==-1:       #abandon par annulation (1) ou par fermeture de la fenêtre (-1)
            return
        
        for e in self.selectionPhotosAvecChemin:
            if os.path.exists(e):
                if self.repTravail == e:
                    self.etatDuChantier = -1
                    texte="Le précédent chantier "" "+self.chantier+" "" est en cours de suppression.\n"                    
                    self.nouveauChantier()
                    time.sleep(0.1)
                try: shutil.rmtree(e)                           # il semble que la racine reste présente il faut ensuite la supprimer
                except: pass
                try:    os.rmdir(e)
                except: pass            
            if os.path.exists(e):
                ajout(conserve,e)
            else:
                try:
                    ajout(supprime,e)
                    self.tousLesChantiers.remove(e)
                except: pass
        if len(supprime)>=1:        
            texte = texte+"Compte rendu de la suppression : \n\nRepertoires supprimés : \n\n"+'\n'.join(supprime)+"\n"
        else:
            texte = texte+"Compte rendu de la suppression : \n\nAucun répertoire supprimé.\n\n"+'\n'.join(supprime)+"\n"
            
        if len(conserve)==0:
                texte = texte+'\n\nTous les chantiers demandés sont supprimés.'
        elif len(conserve)==1:
                texte = texte+'\n\nIl reste un chantier impossible à supprimer maintenant : \n\n'+'\n'.join(conserve)
        else:
                texte = texte+'\n\nIl reste des chantiers impossibles à supprimer maintenant : \n\n'+'\n'.join(conserve)                 
        self.sauveParam()                                   # mémorisation de la suppression
        self.encadre(texte)

    ############################### Message proposant une question et deux Boutons OK, Annuler
    # si b2="" alors pas de second bouton    
    def deuxBoutons(self,titre='Choisir',question="Choisir : ",b1='OK',b2='KO'):     # b1 rennvoie 0, b2 renvoie 1 ; fermer fenetre = -1, 
        try:
            self.bouton = -1
            self.resul300 = tkinter.Toplevel(height=50,relief='sunken')
            fenetreIcone(self.resul300)          
            self.resul300.title(titre)
            self.texte301=ttk.Label(self.resul300, text=question)
            self.texte301.pack(pady=10,padx=10)        
            self.texte302=ttk.Button(self.resul300, text=b1,command=self.bouton1)
            self.texte302.pack(pady=5)
            if b2!="":                    # autorise un seul bouton
                self.texte303=ttk.Button(self.resul300, text=b2,command=self.bouton2)
                self.texte303.pack(pady=5)
            self.resul300.transient(fenetre)                                    # 3 commandes pour définir la fenêtre comme modale pour l'application
            self.resul300.grab_set()
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

    ############################### Prépare un cadre pour Afficher une trace dans la fenêtre

        
    def cadreVide(self):
        self.menageEcran()
        fenetre.update()                                  # rafraichissement avant agrandissement            
        self.resul200 = ttk.Frame(fenetre,height=100,relief='sunken')  # fenêtre texte pour afficher le bilan
        self.scrollbar = ttk.Scrollbar(self.resul200)
        self.scrollbar.pack(side='right',fill='y',expand=1)           
        self.texte201 = tkinter.Text(self.resul200,width=200,height=100,yscrollcommand = self.scrollbar.set,wrap='word')
        self.texte201.pack()
        self.resul200.pack()      
        self.scrollbar.config(command=self.yviewTexte)

    def yviewTexte(self, *args):
        if args[0] == 'scroll':
            self.texte201.yview_scroll(args[1],args[2])
        elif args[0] == 'moveto':
            self.texte201.yview_moveto(args[1])

    ################################## lance une procédure et éxécute une commande sur chaque ligne de l'output ################################################

    def lanceCommande(self,commande,filtre=lambda e: e,info="",attendre=True):   
        commande = [e for e in commande if e.__len__()>0]       # suppression des arguments "vides"
        commandeTexte=" ".join(commande)                        # Format concaténé des arguments
        self.ajoutLigne("\n\n"+heure()+" : Lancement de "+commandeTexte+"\n\n"+info+"\n")
        exe = subprocess.Popen(commande,
                               shell=self.shell,
                               stdout=subprocess.PIPE,          # ne pas définir stdin car sinon il faut le satisfaire
                               #stdin=subprocess.PIPE,           # en fait il faut sans doute.... doute...
                               stderr=subprocess.STDOUT,
                               universal_newlines=True)
        
        if not attendre:                                        # par exemple pour lancer meshlab on n'attend pas la fin
            return
        
        ligne=exe.stdout.readline()
        
        while ligne:
            '''if ligne.find('tape enter')>=0:
                envoiRetourChariot(exe)'''
                
            if ligne.__class__!=str().__class__:        # doit être une chaine
                break                                   # sinon pb majeur : on arrête            
            self.ajoutLigne(filtre(ligne),ligne)        # on ajoute la ligne et la ligne filtrée dans les traces
                    
            try: ligne=exe.stdout.readline()            # ligne suivante, jusqu'à la fin du fichier, sauf décès (anormal) du processus père
            except:
                print("erreur lecture output : ",commandeTexte)
                break                                   # si la lecture ne se fait pas c'est que le processus est "mort", on arrête

        while exe.poll()==None:                          # on attend la fin du process, si pas fini (en principe : fini)
            time.sleep(0.1)
            pass
        
        self.ajoutLigne("\n"+heure()+" : Fin de "+commandeTexte+"\n")

    ########################## Fichiers TRACE

    def definirFichiersTrace(self):     # crée les fichiers à vide
        if self.repTravail != "":
            self.TraceMicMacSynthese = os.path.join(self.repTravail,'Trace_MicMac_Synthese.txt')
            self.TraceMicMacComplete = os.path.join(self.repTravail,'Trace_MicMac_Complete.txt')
            os.chdir(self.repTravail)                                                       # on se met dans le répertoire de travail, indispensable
            
    # ajout de lignes dans les traces

    def ajoutLigne(self,filtree,lue='',position='end'):       
        self.ajoutTraceComplete(lue)                                # toutes les lignes vont dans la trace compléte
        if lue!=filtree:                                            # si la ligne filtrée est != ligne lue, alors on la met dans la trace complète
            self.ajoutTraceComplete(filtree)
        self.ajoutTraceSynthese(filtree)                            # la ligne filtrée est mise dans la trace synthétique

    def ajoutTraceComplete(self,lue=''):
        try:
            if lue=='':
                return
            if lue==None:
                return            
            self.lignePourTrace = self.lignePourTrace+str(lue)             # la trace détaillée en fin de MicMac, dans le répertoire de travail, sous le nom traceTotale
            print(lue)
        except Exception as e: 
            print("Erreur ajout trace complète : ",str(lue)," erreur=",str(e))
            
    def ajoutTraceSynthese(self,filtree=''):
        try:
            if filtree=="":
                return
            if filtree==None:
                return
            self.ligneFiltre = self.ligneFiltre+str(filtree)         # la trace synthétique   
            self.texte201.insert('end',str(filtree))                  
            self.texte201.update()
            self.texte201.see('end') 
        except Exception as e: pass

    def effaceBufferTrace(self):
        
        self.lignePourTrace = str()
        self.ligneFiltre = str()

    # écrire dans les traces

    def ecritureTraceMicMac(self):                                          # écriture en Ajout des fichiers trace
        try:
            with open(self.TraceMicMacSynthese,'a') as infile:
                infile.write(self.ligneFiltre)

            with open(self.TraceMicMacComplete,'a') as infile:
                infile.write(self.lignePourTrace)
            
            self.effaceBufferTrace()
            
        except Exception as e:
            print ('erreur ecritureTraceMicMac : ',str(e),"\ntraces : ",self.TraceMicMacSynthese," et ",self.TraceMicMacComplete)

    
            
    ############################### Choix d'une image dans la liste des images retenues avec scrollbar : charge self.selectionPhotosAvecChemin, gadgets
        
        """ les deux autres présentations sous forme de dialogue :

            # deux boutons         
            # Mydialog
        """

# en retour : self.selectionPhotosAvecChemin
            
    def choisirUnePhoto(self,                                               # en retour liste : self.selectionPhotosAvecChemin
                        listeAvecChemin,
                        titre='Choisir une photo',
                        message="Cliquer pour choisir une ou plusieurs photos : ",
                        mode='extended',                                    # autre mode = "single"
                        messageBouton="OK",
                        boutonDeux=None,                                    # texte d'un second bouton : fermeture, renvoyant une liste vide
                        dicoPoints=None,
                        objets='photos'):                                   # défaut : pas de dictionnaire de points à afficher
        self.selectionPhotosAvecChemin = list()                             # sélection : vide pour l'instant !
        self.cherche = str()                                                # recherche
        self.fermerVisu = False                                             # permet d'identifier la sortie par le second bouton si = True (!= sortie par fermeture fenêtre)               
        if len(listeAvecChemin)==0:                                         # pas de photos : on sort
            self.encadre("Pas de photos pour cette demande.",
                         nouveauDepart="non")
            return
        l = [ e for e in listeAvecChemin if not os.path.exists(e)]         #si des photos manquent : abandon !
        if len(l)>0 and objets=='photos':
            texte="Les photos suivantes sont absentes du disque :"+"\n".join(l)+"\nDossier corrompu. Traitement interrompu."
            self.encadre(texte,nouveauDepart="non")
            return
        self.dicoPointsAAfficher = dicoPoints                               # pour passer l'info à retailleEtAffiche                       
        self.fermerVisuPhoto()                                              # pour éviter les fenêtres multiples
        self.listeChoisir = list(set(listeAvecChemin))                      # liste de choix par copie de la liste ou du tuple paramètre, sans doublons
        self.listeChoisir.sort()                                            #tri alpha
        listeSansChemin = [os.path.basename(e) for e in self.listeChoisir]       
        self.topVisuPhoto = tkinter.Toplevel(fenetre,relief='sunken')               # fenêtre principale de choix de la photo (maitre, ou autre)
        self.topVisuPhoto.title(titre)
        self.topVisuPhoto.geometry("400x400+100+200")
        fenetreIcone(self.topVisuPhoto)           
        """textvariable : associe le texte du label à une variable de type StringVar. Si la variable change
        de valeur, le texte change. Voir chapitre tk01 §7. Attention à l'utilisation des
        StringVar : il faut créer la variable, l'affecter par la méthode set(), la consulter
        par la méthode get()."""
        self.invitePhotoMessageInitial = message
        self.invitePhotoMessage = tkinter.StringVar()
        self.invitePhotoMessage.set(self.invitePhotoMessageInitial)
        self.invitePhoto = ttk.Label(self.topVisuPhoto,textvariable=self.invitePhotoMessage)                  # message entête
        self.invitePhoto.pack(padx=5,pady=5,ipadx=5,ipady=5)
        
        frameSelect = ttk.Frame(self.topVisuPhoto)                          # cadre dans la fenêtre: pour afficher la boite à liste        
        scrollbar = ttk.Scrollbar(frameSelect, orient='vertical')           #barre de défilement
        
        self.selectionPhotos = tkinter.Listbox(frameSelect,selectmode=mode,yscrollcommand=scrollbar.set)
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
        frameSelect.pack()                                                  # fin de la boite à liste
        
        self.b1 = ttk.Button(self.topVisuPhoto,text=messageBouton,command=self.validPhoto)  # le premier bouton (fermer ou OK
        if boutonDeux!=None:
            c = ttk.Button(self.topVisuPhoto,text=boutonDeux,command=self.cloreVisuPhoto)  #le second bouon si demandé
            self.b1.pack(pady=5)
            c.pack(pady=5)
        else:
            self.b1.pack(pady=5)
            
        foto = ttk.Frame(self.topVisuPhoto)                                     # cadre dans la fenetre ; affiche la photo sélectionnée              
        self.canvasPhoto = tkinter.Canvas(foto,width = 200, height = 200)       # Canvas pour revevoir l'image
        self.canvasPhoto.pack(fill='both',expand = 1)
        foto.pack()
        
        self.selectionPhotos.select_set(0)                                      # sélection de la première photos
        self.current = None                                                     # pas de photo choisie par l'utilisateur
        self.poll()                                                             # lance la boucle infinie d'attente

        self.topVisuPhoto.protocol("WM_DELETE_WINDOW", self.fermerVisuPhoto)    # Fonction a éxécuter lors de la sortie du programme
        self.topVisuPhoto.transient(fenetre)                                    # 3 commandes pour définir la fenêtre comme modale pour l'application
        self.topVisuPhoto.grab_set()
        fenetre.wait_window(self.topVisuPhoto)
        try : self.bulle.destroy()
        except: pass

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
                self.invitePhotoMessage.set(self.invitePhotoMessageInitial+"\nTrouvé : "+self.cherche)
            else:
                self.invitePhotoMessage.set(self.invitePhotoMessageInitial+"\nNon trouvé : "+self.cherche)
        else:
            self.cherche=str()
            self.invitePhotoMessage.set(self.invitePhotoMessageInitial)
            
    def poll(self):                                                             # boucle srutant la valeur sélectionnée en cours, 10 fois par seconde
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
            if self.retailleEtAffichePhoto(self.listeChoisir[selection[0]])=="KO":  # prend l'image, la retaille et l'affiche
                if self.messageSiPasDeFichier==1:
                    self.infoBulle(" Pas de fichier pour "+os.path.basename(self.listeChoisir[selection[0]]))  # message si pas de photo
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
            print("erreur infobulle : ",str(e)," pour ",texte)
        
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
            self.infoBulle("Aucun point placé sur cette photo")
        if nbpts==1:
            self.infoBulle("Un point placé sur cette photo")
        if nbpts>1:
            self.infoBulle(nbpts.__str__()+" points placés sur cette photo")
  
    def xyJPGVersCanvas(self,xJPG,yJPG,bouton=None):                         # xJPG,yJPG : position dans l'image originale (Jpeg)
        couleurTexte = 'black'
        xFrame = xJPG * self.scale             # xFrame,yFrame : position dans l'image dans le cadre
        yFrame = yJPG * self.scale
        self.canvasPhoto.create_text(xFrame-10, yFrame+10, text = bouton,tag=bouton,fill=couleurTexte)
        self.canvasPhoto.create_oval(xFrame-5, yFrame-5,xFrame+5, yFrame+5,fill='yellow',tag=bouton)
        
    ######################################## Retaille et Affiche : prépare une photo pour affichage dans une petite fenêtre 200*200 max
    
    def retailleEtAffichePhoto(self,photo):                                             # charge le canvas self.canvasPhoto
        if not os.path.exists(photo):                                                   # erreur de paramètrage
            try: self.canvasPhoto.delete(self.imgTk_id)                                 # supprimer la photo dans le canvas si elle existe
            except: pass
            return "KO"
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
        self.enCours = os.path.basename(photo)
        self.afficherTousLesPointsDuDico()

    ############################### Choix d'un répertoire dans la liste des répertoires de travail, avec scrollbar : charge self.selectionPhotosAvecChemin

    def choisirUnRepertoire(self,titre,mode='single'):              # mode="single" ou 'extended'
        self.retourChoixRepertoire="Abandon"
        self.fichierProposes = list()
        chantierSansParametre = list()
        for e in self.tousLesChantiers:                             # suppression des répertoires inexistants (parce que supprimés)
            if os.path.exists(e):
                fichierParamChantier  =   os.path.join(e,self.paramChantierSav)
                if os.path.exists(fichierParamChantier):            # le fichier paramètre existe :on le propose
                    ajout(self.fichierProposes,e)
                else:
                    chantierSansParametre.insert(0,e)
                    
        if len(self.fichierProposes)==0:
            return "Aucun chantier mémorisé."        
        self.selectionRepertoireAvecChemin=str()        
        self.topRepertoire = tkinter.Toplevel()
        self.topRepertoire.title(titre)
        self.topRepertoire.geometry("800x600+100+200")
        fenetreIcone(self.topRepertoire)   
        f = self.topRepertoire                                      #ttk.Frame(self.topRepertoire)       
        frameSelectRep = ttk.Frame(self.topRepertoire)
        invite = ttk.Label(self.topRepertoire,text="Choisir le chantier à ouvrir :")
        invite.pack(pady=10,padx=10,ipadx=5,ipady=5)
        scrollbarV = ttk.Scrollbar(frameSelectRep, orient='vertical')          
        scrollbarH = ttk.Scrollbar(frameSelectRep, orient='horizontal')
        self.selectionRepertoire = tkinter.Listbox(frameSelectRep,
                                                   selectmode=mode,
                                                   xscrollcommand=scrollbarH.set,
                                                   yscrollcommand=scrollbarV.set,
                                                   height= min(10,len(self.fichierProposes)),
                                                   width=  min(70,min(300,(5+max(len (r) for r in self.fichierProposes))))
                                                   )       
        self.selectionRepertoire.select_set(1)
        self.fichierProposes.sort(key=os.path.basename)
        for i in self.fichierProposes:
            texte=format2Colonnes(os.path.basename(i),afficheChemin(os.path.dirname(i)),100)
            self.selectionRepertoire.insert('end',texte)  
        scrollbarV.config(command=self.yviewRepertoire)
        scrollbarV.pack(side='right', fill='y')            
        scrollbarH.config(command=self.xviewRepertoire)
        scrollbarH.pack(side='bottom', fill='y')
        self.selectionRepertoire.pack(side='left', fill='both', expand=1)          
        frameSelectRep.pack()         
        self.selectionRepertoire.select_set(0)
        b = ttk.Button(f,text="Ouvrir",command=self.validRepertoire)
        b.pack(pady=5)
        c = ttk.Button(f,text="Annuler",command=self.cancelRepertoire)
        c.pack(pady=5)
        if len(chantierSansParametre)>0:
            d = ttk.Label(f,text="Il y a des chantiers incomplets,\n le fichier "+self.fichierParamChantierEnCours+" est absent.\n"+
                          "Ces chantiers ne peuvent être ouverts mais peuvent être supprimés :\n\n"+"\n".join(chantierSansParametre))
            d.pack(pady=5)            
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
        self.retourChoixRepertoire="Abandon utilisateur."

    def envPath(self):
        return

    def orientation(self):                              # définit le répertoire qui contient l'orientation la plus récente :
                                                        # soit Arbitrary soit echelle3d soit bascul

        if os.path.exists(os.path.join(self.repTravail,"Ori-bascul")):
            return "bascul"

        if os.path.exists(os.path.join(self.repTravail,"Ori-echelle3")):
            orientation = "echelle3"
            return "echelle3"

        return "Arbitrary"

    #################### Examen du nombre de points homologues  dans le répertoire homol

    def nombrePointsHomologues(self):
        print("===============================================================================================================================")
        repertoireHomol = os.path.join(self.repTravail,"Homol") # répertoire des homologues
        print(repertoireHomol)
        os.chdir(repertoireHomol)
        for e in os.listdir():                   # balaie tous les fichiers
            print(e)
            os.chdir(os.path.join(repertoireHomol,e))
            for f in os.listdir():
                if os.path.isfile(f):                               # fichier
                    with  open(f) as infile:
                        nbLignes = len(infile.readlines())    #lecture dicoCamera.xml   
                        print(e,f," = ",nbLignes)
        print("===============================================================================================================================")

    #################### Utilitaires : tests de la présence de photos, de mm3d, d'exiftool, envoi retour chariot et compte le nombre d'extensions différentes dans une list

    def pasDePhoto(self):

        if self.photosPropresAvecChemin.__len__()==0:
            self.encadre("Choisir des photos au préalable.",nouveauDepart="non")
            return True
        liste = [e for e in self.photosPropresAvecChemin if os.path.exists(e)==False]
        if liste.__len__()>0:
            texte="Attention  les photos suivantes sont absentes sur disque : \n"+"\n".join(liste)+"\nElles sont supprimées."
            self.photosPropresAvecChemin =         liste = [e for e in self.photosPropresAvecChemin if os.path.exists(e)]
            self.photosSansChemin =list([os.path.basename(x) for x in  self.photosPropresAvecChemin])
            repertoireInitial = os.path.dirname(self.photosAvecChemin[0])
            self.photosAvecChemin = [os.path.join(repertoireInitial,e) for e in self.photosSansChemin]
            self.deuxBoutons(titre="Problème de fichiers",question=texte,b1='OK',b2='')    # b1 renvoie 0, b2 renvoie 1 ; fermer fenetre = -1            
 
    def pasDeMm3d(self):
        if not os.path.exists(self.mm3d):
            self.encadre("Désigner le répertoire MicMac\\bin (menu paramètrage).",nouveauDepart="non")            
            return True

    def pasDeExiftool(self):
        if not os.path.exists(self.exiftool):
            self.encadre("Désigner le fichier exiftool (menu paramètrage).",nouveauDepart="non")            
            return True

    def envoiRetourChariot(self,dest):                                                      # dest étant le processus ouvert par popen
        dest.communicate(input='t\n')

    def nombreDExtensionDifferentes(self,liste):
        lesExtensions=set([os.path.splitext(x)[1].upper() for x in liste])                  # on vérifie l'unicité de l'extension :
        self.lesExtensions=list(lesExtensions)                                              # liste pour être slicable
        return len(self.lesExtensions)
        
    ########################################################   nouvelle fenêtre (relance utile pour vider les traces d'exécution de mm3d et autres)

    def nouveauDepart(self):

        self.copierParamVersChantier()                          # sauvegarde du chantier, des param...
        self.ecritureTraceMicMac()                              # on écrit les fichiers trace

# faut-t-il différencier linux et windows ?
        if self.systeme=='posix':
            if self.messageNouveauDepart==str():
                self.afficheEtat()
            else:
                self.encadre(self.messageNouveauDepart)
            self.messageNouveauDepart = str()
            
        if self.systeme=='nt':       
           global messageDepart
           messageDepart = self.messageNouveauDepart
           fenetre.destroy()

    # quitter
            
    def quitter(self):
        texte=""
        if self.etatDuChantier > 2 and self.etatSauvegarde =="*":
            if self.deuxBoutons("Enregistrer le chantier "+self.chantier+" ?","Chantier modifé depuis la dernière sauvegarde. Voulez-vous l'enregistrer ?","Enregistrer","Ne pas enregistrer.") == 0:
                self.copierParamVersChantier()
                texte="Chantier précédent enregistré : "+self.chantier+"\n"        
        print(heure()+" "+texte+" fin normale d'aperodedenis.")
        self.sauveParam()
        global continuer                                # pour éviter de boucler sur un nouveau départ
        continuer = False
        fenetre.destroy()
        time.sleep(0.5)
        
        
################################## FIN DE LA CLASSE INTERFACE ###########################################################


        
################################## Outils divers et outils POUR DEBUG ###########################################################

def pv(variable):       # affiche le nom de la variable, sa classe et sa valeur (pour debug uniquement)
    stack = traceback.extract_stack(limit=2)
    print('\n------------------')
    if '))' in stack[0][3]:
        nomVariable = stack[0][3].replace('pv(', '').replace('))', ')')
        typeVariable = "fonction"
        valeurVariable = "valeur en retour : "
    else:
        nomVariable = stack[0][3].replace('pv(', '').replace(')', '')
        typeVariable = "variable"
        valeurVariable = "valeur : "        
    print ("Détail de la "+typeVariable+" : ",nomVariable,
           '\nIdentifiant : ',id(variable),
           '\nType : ',type(variable),
           '\nclass = ',variable.__class__,
           '\nLes attributs : ',dir(variable),
           '\n\n'+valeurVariable,str(variable))
    print('\n------------------')
    
def heure():        #  time.struct_time(tm_year=2015, tm_mon=4, tm_mday=7, tm_hour=22, tm_min=56, tm_sec=23, tm_wday=1, tm_yday=97, tm_isdst=1)
        return "le "+str(time.localtime()[2])+"/"+str(time.localtime()[1])+"/"+str(time.localtime()[0])+" à "+str(time.localtime()[3])+":"+str(time.localtime()[4])

def supprimeFichier(fichier):
    try:
        os.remove(fichier)
    except:
        return

def supprimeMasque(repertoire,masque):
    for e in os.listdir(repertoire):
        if masque in e:
            supprimeFichier(e)

def blancAuNoir(p):
    if p == 255:
        return 0
    else:
        return 255

def ajout(liste,item):                                  # ajout d'un item dns une liste en s'assurant qu'il n'y a pas de doublons et avec un tri:
    if liste.__class__()==list():
        try:
            liste.append(item)
            c=list(set(liste))
            c.sort()
            liste.clear()
            for e in c:
                liste.append(e)
        except Exception as e:
            print ("erreur ajout : ",liste,"+",item," : ",str(e))

def supprimeArborescenceSauf(racine,listeSauf=list()):  # supprime toute une arborescence, sauf une liste de fichiers sous la racine
    listeSauf = [os.path.basename(e) for e in listeSauf]

    for fichier in os.listdir(racine):
        chemin = os.path.join(racine,fichier)
        if fichier in listeSauf:
           if os.path.isdir(chemin): 
                shutil.rmtree(chemin)
        else:
            if os.path.isfile(chemin):
                try:
                    os.remove(chemin)
                except Exception as e:
                    print(str(e))
                    return
            else:
                shutil.rmtree(chemin)           # on supprime tous les sous répertoires 'calculs, temporaires...)

                
def afficheChemin(texte):                               #avant d'afficher un chemin on s'assure que le séparateur est bien le bon suivant l'OS
    return texte.replace(interface.separateurAutre,interface.separateurChemin)

def format2Colonnes(col1,col2,largeurCol1EnPixels):
    lab=tkinter.Label(text=col1)
    long=lab.winfo_reqwidth()
    while long<largeurCol1EnPixels:
        col1=col1+" "
        lab=tkinter.Label(text=col1)
        long=lab.winfo_reqwidth() 
    return col1+" "+col2

def verifMm3d(mm3D):            # Il faudrait que la version de MicMac autorise la saisie de masque en 3D, sinon ancienne version, susceptible de donner des erreurs.
    if os.path.exists(mm3D)==False: return False
    try: helpMm3d = subprocess.check_output([mm3D,"-help"],universal_newlines=True)
    except Exception as e:
        return False
    if "SaisieMasqQT" in helpMm3d: return True
    else: return False

def verifierSiExecutable(exe):
    try:
        subprocess.check_call(exe)
        return True
    except:
        return False

def envoiRetourChariot(self,dest):                                                      # dest étant le processus ouvert par popen
    dest.communicate(input='t\n')

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def fenetreIcone(fenetre=""):       # Icone au format GIF pour être géré par tkinter sans utiliser Pillow
    if fenetre=="":
        return
    photo = tkinter.PhotoImage(data=iconeTexte)
    fenetre.tk.call('wm', 'iconphoto', fenetre._w, photo)

def fin(codeRetour=0):
    os._exit(codeRetour)
        
'''################################## Crée un fichier contenant l'icone de l'application et en renvoie le nom conserver pour exemple de ficheir temporaire

def iconeGrainSel():
    iconeTexte = "AAABAAIAICAQAAEABADoAgAAJgAAABAQEAABAAQAKAEAAA4DAAAoAAAAIAAAAEAAAAABAAQAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAgAAAAICAAIAAAACAAIAAgIAAAICAgADAwMAAAAD/AAD/AAAA//8A/wAAAP8A/wD//wAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADiLcAAAAAAAAAAAAAAAADeL/4hxAAAAAAAAAAAAMze4s7iP+DMAAAAAAAADi/i3kQELj//4hxAAAAAAv/+LkwAAAb//j/j/8AAAA4uIuxAAAAOIuIj/i/MAABO4v7kRAAAbu7uIiLixAAA4ObuzEQAAO3k4uIiLEAAAO7M5ORAAETk4m4/4sAAAADixMQAAETOTm3iP+zAAAAB7cxABMTOTM3uL//gQAAAAuDERNXiPuLe4j4+LAAAAAI8xA3iP/4uIj//7gwAAAAA4MReP///4i/j/ixAAAAAAO3MTiP+Ii/i4uzEAAAAAABezM7i4iL+7tzEAAAAAAAAYiJOTi/+LixEAAAAAAAAAP/+3ObiIiLcQAAAAAAAAAH//i4iLiIixAAAAAAAAAAA//7iLiL+7cAAAAAAAAAAAP/iIj7i3MwAAAAAAAAAAABiIv7+4kwAAAAAAAAAAAAAL+Ii4sQAAAAAAAAAAAAAAA7iIuRAAAAAAAAAAAAAAAAAbuDMAAAAAAAAAAAAAAAAAABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAAAAEAAAACAAAAABAAQAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAgAAAAICAAIAAAACAAIAAgIAAAICAgADAwMAAAAD/AAD/AAAA//8A/wAAAP8A/wD//wAA////AAAAAAAAAAAAAAAAAHMAAAAAAAM4v4cAAAAYixAL/4hwADi3EAi4iLEDs7EAG5v4MAOBEBOTiPMAB7AY+LiPgwABcY//i/swAACLO4i4EAAAA/iYv7EAAAAB/4i4MAAAAACL+zAAAAAAADixAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="        
    iconeBin = base64.b64decode(iconeTexte)                 # décodage pour revenir au binaire du fichier icone :
    with tempfile.NamedTemporaryFile(delete=False) as f:    # écriture de ce binaire dans un fichier temporaire
        f.write(iconeBin)
    return f.name
'''
################################## Classe : Dialogue minimum modal : demande une chaine de caractères ###########################"

class MyDialog:
   
    def __init__(self,parent,titre="Nouveau nom pour le chantier : ",basDePage='none'):
        self.saisie=str()
        top = self.top = tkinter.Toplevel(parent,width=200,relief='sunken')
        top.transient(parent)
        top.geometry("400x250+100+100")
        fenetreIcone(self.top)                
        l=ttk.Label(top, text=titre)
        l.pack(pady=10,padx=10)
        top.bind("<Return>",self.ok)
        self.e = ttk.Entry(top,width=30)
        self.e.pack()
        self.e.focus_set()
        b = ttk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        c = ttk.Button(top, text="Annuler", command=self.ko)
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
        return
    

################################## Style pur TTK  ###########################"

def monStyle():
    pass
    ttk.Style().configure("TButton", padding=6, relief="flat",background="#ccc")

       
################################## LANCEMENT DU PROGRAMME ###########################################################

# si on ouvre ce script comme programme principal alors on instancie un objet de la classe Interface sur la fenêtre principale de l'outil :

continuer = True
messageDepart = str()
compteur = 0
iconeTexte = "R0lGODlhIAAgAIcAMQQCBJSGJNTSPHQKBMTCpGxKBPziXJxmJIR6BOTCXPTybDwCBHR2TMTGhPTmjOzmpJxuBMy+pIRyLDweDPz+1MTGjOzuhDwmBMRaFPz+pHx6LKRiLPzibDQiDMzKZIxqTKR6NOy2fHxCBNTCdEwaBISGTPzqfBwCBPTmpJRuLMzCjKxqBPTmnKxuBOzqnNzGXJQ2BHxGBIx2FIR+fMzGfOTmtMS+vIRyPPz67PTubBQCBJyGJMTCtPzqVKRmHPzSfFQWBIRuTJxuFEQeBPz+vHx2RKxiLNTKXMzCnPzqZAQKBHROBHx6JPz+hPzihPTqfEwqLJxqLJR+XOS+bEwiBMzGhPzenAwCBIyKNNzKTMzCpHxyTOzqpIxyLEwqBJxmRMzKbKx6PIQ+BNTGdISCXMzGjIxCBNS6vPz+/PzqXKRqHPzeZGQOBPzqdPzmjMzOVGwSBMTGpGxGHIR6FPTyfKRuDMy+tDwiBPz+5MTGnEQqBPz+tIR2NKRmLDQiJMzOXJx6VEwWDIx6fPyubLR6FCwCBHRCHIx+BMy6vOS+hPzedPzilIxuPIR2PJSGNJR2hFQaBJRqPKxmFJyCNFwSBIR2JPTqjJQ+BPTqlOzmtKRuFNTOTHRKBIyGTCQCBNzGbJw2BIRGBPz+zPz+lFQiBHxyXMy6zPzmVMzKdPz+7PzuTEQiBHx6PPzuZPzmfKRyBAQGBHQOBJxqJMTKhDwqBKR+NEweBMzGnHRSBPTufMzKhAwGBIRCBPzuXIR+FPzmlFwWBMTCrPTydHR2VOzmrMy+rIRyNPz+3MTGlOzujPz+rHx6NDQiFIxqVNTCfPzqhPTmrMzClIRyRPTudMTCvKRmJIRuVJxuHEQeDPz+xNTKZOS+dIyKPOzqrIxyNNTGfISCZMzGlKRqJDwiDKRmNMzOZPzefPTqnOzmvMzKfPz+9PzubPzmhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAIAAgAAcI/gABCBxIsKDBgwgTKlxI8MoVHVcYShT4cMIdHRAnKtRxwZIlGsa+eIqo0eAVCey0/fHATgSkEyRLUrwCjUg6MH9yHXECZKRMih0IVKjAZY+FUexCGAryU+AWPHiQVchTJsO0F26waNAASyaDVKkodCOAzMERDxb2uEiGJaZEcOrUUdDF5du2KZiq5EEGxsEQHROvlEqFRxSLADIKWPmGLFgeD09A2HKbUAc2JGUSxYDAScYYLqJE6bKwKY2XVRgpFzwxpNOiKNXqOBnTrUI4ZN2U5VCVZlKQOw5VUzTmwtEGYIyiEQDLgwcBLsqyCKNBjIsEWycQwlpGowslSoC0/qAZj0bdsVmoLCjTJSrbNyurhAOYlc0YpQWRpJwxVf5YmWQeoNIAHuqkcgw0KnBlECzdNNAFEJTY8gEUjyASgSi/vJCLI9DcslwceFSByS4HlZBMALL0pMMEzQTyxQa8qAFBFJM4kE4Nxxg4Ai0HLfNHG6SoYYsnhRQJBDBGqBGDDyI4sQMYZYCFQheUwaKBAr28UkcoK8DAhidgDmGLLCJIMogZTqCCRyploJARQRq8ccgSBpyyBgYDBIKRDid0YQ4hMEjyggsE8IBMFQ5cENMVdyCgwCZJNLEGKHlC9NAdbfTSQxJPVNAcMlx4kChgADjEhAe5ePCHKz/EUkhGfRjJIIAA08wSBw/mqeDCHtKQKtAuLrRHxCeKmLGBJ3ueoEcbROTIw3jF4ACVarAMEwc6RCRgDghyTKDDRU44k0p56lBjwyN+SFQEH3w4wkKbc1gSjXjqFGNNKSXBou8uy5TQgHrH8EDNDOPIpxEDeeSRCThNLaRvwxBHLFFAADs="

repertoire_script=os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if not os.path.isdir(repertoire_script):
    repertoire_script = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(repertoire_script):
        repertoire_script = os.path.dirname(sys.argv[0])
        if not os.path.isdir(repertoire_script):
             repertoire_script = os.getcwd()
             
if os.name=="nt":             
    repertoire_data = os.getenv('APPDATA')+'\\AperoDeDenis'
    try: os.mkdir(repertoire_data)
    except: pass
    if not os.path.isdir(repertoire_data):
        repertoire_data = repertoire_script    
else:
    repertoire_data = repertoire_script
    
if __name__ == "__main__":
    while continuer:
        compteur += 1
        fenetre = tkinter.Tk()
        interface = Interface(fenetre)
        if messageDepart==str():
            interface.afficheEtat()
        else:
            interface.encadre(str(messageDepart))    # affiche les infos restaurées :
        fenetre.mainloop()                    # boucle tant que l'interface existe

