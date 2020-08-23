import os
import secrets
from flask import render_template, flash, url_for, redirect, request, session
from flask_login import login_user, current_user, login_required
from PIL import Image
from .. import create_app
from .. import db
from functools import wraps
from ..models import Categorie, Produit



def menu_principale():
    cate_principale=[]
    cate_secondaire=[]
    categories=Categorie.query.filter_by(statut=True).order_by(Categorie.id.desc()).all()
    
    for categorie in categories:
        if categorie.priorite == True:
            id=categorie.id
            nom=categorie.nom
            cat=[id,nom]
            cate_principale.insert(0,cat)
        else:
            id=categorie.id
            nom=categorie.nom
            cat=[id,nom]
            cate_secondaire.insert(0,cat)
            
    return cate_principale, cate_secondaire

def liste_produit():
    ensemble_produit=dict()
    #Requete de selection des produits
    produit_encours=Produit.query.filter(Produit.statut==True).order_by(Produit.id.asc()).all()
    # Dictionnaire trié selon les 4 produit
    trier_produit=dict()
    
    if len(ensemble_produit)==0:
        for i in produit_encours:
            if i.categorie_produit.priorite==True:
                if i.categorie_produit.nom in ensemble_produit:
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom]
                    ensemble_produit[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom]
                    ensemble_produit[i.categorie_produit.nom]=[produit_liste]
            else:
                pass
    else:
        for i in produit_encours:
            if i.categorie_produit.priorite==True:
                if i.categorie_produit.nom in ensemble_produit:
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom]
                    ensemble_produit[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom]
                    ensemble_produit[i.categorie_produit.nom]=[produit_liste]
            else:
                pass
    #Trie du dictionniare
    for produit in ensemble_produit:
        for i in range(len(ensemble_produit[produit])):
            if produit in trier_produit:
                if len(trier_produit[produit]) <= 3:
                   trier_produit[produit].insert(0, ensemble_produit[produit][i])
                else:
                    pass
            else:
                trier_produit[produit]=[ensemble_produit[produit][i]]
    
    return trier_produit

# La fonction des carousel
def caroussel_produit():
    ensemble_produit=dict()
    #Requete de selection des produits
    produit_encours=Produit.query.filter(Produit.statut==True).order_by(Produit.id.desc()).all()
    # Dictionnaire triй selon les catйgories non priorisйes 
    trier_produit=dict()
    #Produit non prioritaore
    non_prioritaie=dict()
    #Les produit carousel
    liste_caroussel=[]
    
    if len(ensemble_produit)==0:
        for i in produit_encours:
            if i.categorie_produit.priorite==True:
                if i.categorie_produit.nom in ensemble_produit:
                    
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(i.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    ensemble_produit[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(i.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    ensemble_produit[i.categorie_produit.nom]=[produit_liste]
            else:
                pass
    else:
        for i in produit_encours:
            if i.categorie_produit.priorite==True:
                if i.categorie_produit.nom in ensemble_produit:
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(i.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    ensemble_produit[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(i.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    ensemble_produit[i.categorie_produit.nom]=[produit_liste]
            else:
                pass

    dictionnaire_compte=dict()

    for p in ensemble_produit:
        dictionnaire_compte[p]=len(ensemble_produit[p])
    #Produit du dictionaire
    for compte in dictionnaire_compte:
        for produit in ensemble_produit:
            if produit == compte:
                if int(dictionnaire_compte[compte]) >4:
                    somme_boucle=int(dictionnaire_compte[compte]) - 4
                    for i in range(somme_boucle):
                        if produit in trier_produit:
                            trier_produit[produit].insert(0, ensemble_produit[produit][i])
                        else:
                            trier_produit[produit]=[ensemble_produit[produit][i]]
                    dictionnaire_compte[compte]=int(dictionnaire_compte[compte]) - 1
    #Les produits non prioritaire
    if len(non_prioritaie)==0:
        for i in produit_encours:
            if i.categorie_produit.priorite==False:
                if i.categorie_produit.nom in non_prioritaie:
                    
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(sum.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    non_prioritaie[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(sum.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    non_prioritaie[i.categorie_produit.nom]=[produit_liste]
            else:
                pass
    else:
        for i in produit_encours:
            if i.categorie_produit.priorite==True:
                if i.categorie_produit.nom in non_prioritaie:
                    
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(sum.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    non_prioritaie[i.categorie_produit.nom].insert(0,produit_liste)
                else:
                    production=float(i.cout_vente_detaille) - float(i.cout_vente_engros)
                    pourcentage=(production/float(sum.cout_vente_detaille)) *100
                    reduction=float(i.cout_vente_detaille) + production
                    
                    produit_liste=[i.id, i.avatar, i.nom, i.cout_vente_detaille, i.description, i.categorie_produit.nom, reduction, pourcentage]
                    non_prioritaie[i.categorie_produit.nom]=[produit_liste]
            else:
                pass

    for p in trier_produit:
        for i in range(len(trier_produit[p])):
            liste_caroussel.insert(0,trier_produit[p][i])
    
    for p in non_prioritaie:
        for i in range(len(non_prioritaie[p])):
            liste_caroussel.insert(0,non_prioritaie[p][i])
    

    return liste_caroussel

def ligne(nombre, liste_car):
    ligne_caroussel=[]
    
    nombre_ligne=None
    veri_ligne=len(liste_car)/nombre
    ligne_modulo=len(liste_car) % nombre
    #Dictionnaire des données
    dicti_d=dict()
    diction_nombre=dict()
    # Modulo du dictionnaire
    if ligne_modulo != 0:
        nombre_ligne=int(veri_ligne) + 1
    else:
        nombre_ligne=veri_ligne
    
def sumulaire_pro(id,categorie):
    liste=[]
    sum_produit=Produit.query.filter(Produit.id!=id, Produit.categorie_id==categorie, Produit.statut==True).all()
    for sum in sum_produit:
        production=float(sum.cout_vente_detaille) - float(sum.cout_vente_engros)
        pourcentage=(production/float(sum.cout_vente_detaille)) *100
        reduction=float(sum.cout_vente_detaille) + production
        p=[sum.id, sum.nom, sum.cout_vente_detaille, sum.avatar, sum.description, pourcentage, reduction]
        liste.insert(0, p)

    return liste
        
def connexion_client():
    id=None
    if current_user.is_authenticated:
        if current_user.type_user=='Client':
            id=current_user.id
    else:
        pass
    return id
        
        
    
        
                
                
                
            
        
        
                
                
                
 
    
        
        
        
        
         
                
                
    
    
    
    
