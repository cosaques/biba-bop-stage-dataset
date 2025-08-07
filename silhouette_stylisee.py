import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, FloatSlider, VBox, HBox, Layout
import matplotlib.patches as patches
from matplotlib.patches import Ellipse, Rectangle, Polygon, FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# Configuration pour un affichage plus propre
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def dessiner_silhouette_stylisee(
    taille=170,
    tour_de_poitrine=90,
    hauteur_de_poitrine=130,
    hauteur_d_entrejambe=80,
    largeur_des_hanches=40,
    hauteur_des_hanches=100,
    hauteur_des_genoux=50,
    largeur_d_epaule=40,
    hauteur_des_epaules=150,
    tour_de_cuisse=55,
    tour_de_taille=70,
    hauteur_de_la_taille=110,
    style='noir'  # 'noir' ou 'contour'
):
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))
    
    # Couleurs selon le style
    if style == 'noir':
        couleur_fill = 'black'
        couleur_contour = 'black'
    else:
        couleur_fill = 'white'
        couleur_contour = 'black'
    
    # Calcul des proportions
    hauteur_tete = taille * 0.08
    hauteur_cou = taille * 0.04
    
    # Position Y des différentes parties
    y_tete = taille
    y_cou = taille - hauteur_tete
    y_epaules = hauteur_des_epaules
    y_poitrine = hauteur_de_poitrine
    y_taille = hauteur_de_la_taille
    y_hanches = hauteur_des_hanches
    y_genoux = hauteur_des_genoux
    y_pieds = 0
    
    # Fonction pour dessiner une silhouette
    def dessiner_silhouette(ax, titre):
        # Tête
        tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete, 
                       facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(tete)
        
        # Cou
        cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,
                        facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(cou)
        
        # Tronc (forme plus stylisée)
        # Poitrine
        poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,
                           facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(poitrine)
        
        # Taille
        taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,
                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(taille_ellipse)
        
        # Hanches
        hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,
                          facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(hanches)
        
        # Épaules (plus stylisées)
        epaule_gauche = Ellipse((-largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                               facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        epaule_droite = Ellipse((largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(epaule_gauche)
        ax.add_patch(epaule_droite)
        
        # Bras (plus stylisés)
        longueur_bras = (y_epaules - y_taille) * 0.8
        # Bras gauche
        bras_gauche = Rectangle((-largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,
                               facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(bras_gauche)
        # Bras droit
        bras_droit = Rectangle((largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,
                              facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(bras_droit)
        
        # Jambes (plus stylisées)
        # Jambe gauche
        jambe_gauche = Rectangle((-tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,
                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(jambe_gauche)
        # Jambe droite
        jambe_droite = Rectangle((tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,
                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(jambe_droite)
        
        # Cuisses (plus stylisées)
        cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(cuisse_gauche)
        ax.add_patch(cuisse_droite)
        
        # Pieds (simplifiés)
        pied_gauche = Ellipse((-15, 10), 20, 10, facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        pied_droit = Ellipse((15, 10), 20, 10, facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)
        ax.add_patch(pied_gauche)
        ax.add_patch(pied_droit)
        
        # Configuration de l'affichage
        ax.set_xlim(-60, 60)
        ax.set_ylim(-10, taille + 10)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(titre, fontsize=14, pad=20)
    
    # Dessiner les deux silhouettes
    dessiner_silhouette(ax1, "Silhouette Noire")
    
    # Changer les couleurs pour la deuxième silhouette
    couleur_fill = 'white'
    couleur_contour = 'black'
    dessiner_silhouette(ax2, "Silhouette Contour")
    
    plt.tight_layout()
    plt.show()

# Interface interactive simplifiée
def creer_interface_stylisee():
    interact(
        dessiner_silhouette_stylisee,
        taille=FloatSlider(min=140, max=200, step=1, value=170, description='Taille (cm)'),
        tour_de_poitrine=FloatSlider(min=70, max=130, step=1, value=90, description='Tour poitrine (cm)'),
        hauteur_de_poitrine=FloatSlider(min=100, max=160, step=1, value=130, description='Haut. poitrine (cm)'),
        hauteur_d_entrejambe=FloatSlider(min=60, max=100, step=1, value=80, description='Haut. entrejambe (cm)'),
        largeur_des_hanches=FloatSlider(min=30, max=60, step=1, value=40, description='Larg. hanches (cm)'),
        hauteur_des_hanches=FloatSlider(min=80, max=120, step=1, value=100, description='Haut. hanches (cm)'),
        hauteur_des_genoux=FloatSlider(min=30, max=70, step=1, value=50, description='Haut. genoux (cm)'),
        largeur_d_epaule=FloatSlider(min=30, max=60, step=1, value=40, description='Larg. épaules (cm)'),
        hauteur_des_epaules=FloatSlider(min=120, max=170, step=1, value=150, description='Haut. épaules (cm)'),
        tour_de_cuisse=FloatSlider(min=40, max=80, step=1, value=55, description='Tour cuisse (cm)'),
        tour_de_taille=FloatSlider(min=50, max=100, step=1, value=70, description='Tour taille (cm)'),
        hauteur_de_la_taille=FloatSlider(min=90, max=130, step=1, value=110, description='Haut. taille (cm)')
    )

print("=== CODE POUR SILHOUETTE STYLISÉE ===")
print()
print("# Cellule 1 - Imports")
print("import matplotlib.pyplot as plt")
print("import numpy as np")
print("from ipywidgets import interact, FloatSlider")
print("import matplotlib.patches as patches")
print("from matplotlib.patches import Ellipse, Rectangle")
print("import warnings")
print("warnings.filterwarnings('ignore')")
print()
print("plt.style.use('default')")
print("plt.rcParams['figure.facecolor'] = 'white'")
print("plt.rcParams['axes.facecolor'] = 'white'")
print()
print("# Cellule 2 - Fonction de dessin stylisé")
print("def dessiner_silhouette_stylisee(")
print("    taille=170,")
print("    tour_de_poitrine=90,")
print("    hauteur_de_poitrine=130,")
print("    hauteur_d_entrejambe=80,")
print("    largeur_des_hanches=40,")
print("    hauteur_des_hanches=100,")
print("    hauteur_des_genoux=50,")
print("    largeur_d_epaule=40,")
print("    hauteur_des_epaules=150,")
print("    tour_de_cuisse=55,")
print("    tour_de_taille=70,")
print("    hauteur_de_la_taille=110")
print("):")
print("    ")
print("    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10))")
print("    ")
print("    # Calcul des proportions")
print("    hauteur_tete = taille * 0.08")
print("    hauteur_cou = taille * 0.04")
print("    ")
print("    # Position Y des différentes parties")
print("    y_tete = taille")
print("    y_cou = taille - hauteur_tete")
print("    y_epaules = hauteur_des_epaules")
print("    y_poitrine = hauteur_de_poitrine")
print("    y_taille = hauteur_de_la_taille")
print("    y_hanches = hauteur_des_hanches")
print("    y_genoux = hauteur_des_genoux")
print("    y_pieds = 0")
print("    ")
print("    def dessiner_silhouette(ax, titre, couleur_fill, couleur_contour):")
print("        # Tête")
print("        tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete,")
print("                       facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(tete)")
print("        ")
print("        # Cou")
print("        cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,")
print("                        facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(cou)")
print("        ")
print("        # Tronc")
print("        poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,")
print("                           facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(poitrine)")
print("        ")
print("        taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,")
print("                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(taille_ellipse)")
print("        ")
print("        hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,")
print("                          facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(hanches)")
print("        ")
print("        # Épaules")
print("        epaule_gauche = Ellipse((-largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,")
print("                               facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        epaule_droite = Ellipse((largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,")
print("                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(epaule_gauche)")
print("        ax.add_patch(epaule_droite)")
print("        ")
print("        # Bras")
print("        longueur_bras = (y_epaules - y_taille) * 0.8")
print("        bras_gauche = Rectangle((-largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,")
print("                               facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        bras_droit = Rectangle((largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,")
print("                              facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(bras_gauche)")
print("        ax.add_patch(bras_droit)")
print("        ")
print("        # Jambes")
print("        jambe_gauche = Rectangle((-tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,")
print("                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        jambe_droite = Rectangle((tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,")
print("                                 facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(jambe_gauche)")
print("        ax.add_patch(jambe_droite)")
print("        ")
print("        # Cuisses")
print("        cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                                facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(cuisse_gauche)")
print("        ax.add_patch(cuisse_droite)")
print("        ")
print("        # Pieds")
print("        pied_gauche = Ellipse((-15, 10), 20, 10, facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        pied_droit = Ellipse((15, 10), 20, 10, facecolor=couleur_fill, edgecolor=couleur_contour, linewidth=2)")
print("        ax.add_patch(pied_gauche)")
print("        ax.add_patch(pied_droit)")
print("        ")
print("        ax.set_xlim(-60, 60)")
print("        ax.set_ylim(-10, taille + 10)")
print("        ax.set_aspect('equal')")
print("        ax.axis('off')")
print("        ax.set_title(titre, fontsize=14, pad=20)")
print("    ")
print("    # Dessiner les deux silhouettes")
print("    dessiner_silhouette(ax1, 'Silhouette Noire', 'black', 'black')")
print("    dessiner_silhouette(ax2, 'Silhouette Contour', 'white', 'black')")
print("    ")
print("    plt.tight_layout()")
print("    plt.show()")
print()
print("# Cellule 3 - Interface interactive")
print("interact(")
print("    dessiner_silhouette_stylisee,")
print("    taille=FloatSlider(min=140, max=200, step=1, value=170, description='Taille (cm)'),")
print("    tour_de_poitrine=FloatSlider(min=70, max=130, step=1, value=90, description='Tour poitrine (cm)'),")
print("    hauteur_de_poitrine=FloatSlider(min=100, max=160, step=1, value=130, description='Haut. poitrine (cm)'),")
print("    hauteur_d_entrejambe=FloatSlider(min=60, max=100, step=1, value=80, description='Haut. entrejambe (cm)'),")
print("    largeur_des_hanches=FloatSlider(min=30, max=60, step=1, value=40, description='Larg. hanches (cm)'),")
print("    hauteur_des_hanches=FloatSlider(min=80, max=120, step=1, value=100, description='Haut. hanches (cm)'),")
print("    hauteur_des_genoux=FloatSlider(min=30, max=70, step=1, value=50, description='Haut. genoux (cm)'),")
print("    largeur_d_epaule=FloatSlider(min=30, max=60, step=1, value=40, description='Larg. épaules (cm)'),")
print("    hauteur_des_epaules=FloatSlider(min=120, max=170, step=1, value=150, description='Haut. épaules (cm)'),")
print("    tour_de_cuisse=FloatSlider(min=40, max=80, step=1, value=55, description='Tour cuisse (cm)'),")
print("    tour_de_taille=FloatSlider(min=50, max=100, step=1, value=70, description='Tour taille (cm)'),")
print("    hauteur_de_la_taille=FloatSlider(min=90, max=130, step=1, value=110, description='Haut. taille (cm)')")
print(")") 