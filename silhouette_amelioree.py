import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, FloatSlider, VBox, HBox, Layout
import matplotlib.patches as patches
from matplotlib.patches import Ellipse, Rectangle, Polygon
import warnings
warnings.filterwarnings('ignore')

# Configuration pour un affichage plus propre
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def dessiner_silhouette_amelioree(
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
    hauteur_de_la_taille=110
):
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 10))
    
    # Couleurs pour les différentes parties du corps
    couleurs = {
        'tete': '#FFE4B5',
        'cou': '#FFE4B5',
        'tronc': '#FFE4B5',
        'bras': '#FFE4B5',
        'jambes': '#FFE4B5',
        'contour': '#8B4513'
    }
    
    # Calcul des proportions
    hauteur_tete = taille * 0.08
    hauteur_cou = taille * 0.04
    hauteur_tronc = hauteur_de_poitrine - hauteur_tete - hauteur_cou
    
    # Position Y des différentes parties
    y_tete = taille
    y_cou = taille - hauteur_tete
    y_epaules = hauteur_des_epaules
    y_poitrine = hauteur_de_poitrine
    y_taille = hauteur_de_la_taille
    y_hanches = hauteur_des_hanches
    y_genoux = hauteur_des_genoux
    y_pieds = 0
    
    # Dessiner la tête
    tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete, 
                   facecolor=couleurs['tete'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(tete)
    
    # Dessiner le cou
    cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,
                    facecolor=couleurs['cou'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(cou)
    
    # Dessiner les épaules
    epaule_gauche = Ellipse((-largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                           facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)
    epaule_droite = Ellipse((largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                            facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(epaule_gauche)
    ax.add_patch(epaule_droite)
    
    # Dessiner le tronc (poitrine à hanches)
    # Poitrine
    poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,
                       facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(poitrine)
    
    # Taille
    taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,
                             facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(taille_ellipse)
    
    # Hanches
    hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,
                      facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(hanches)
    
    # Dessiner les bras
    longueur_bras = (y_epaules - y_taille) * 0.8
    # Bras gauche
    bras_gauche = Rectangle((-largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,
                           facecolor=couleurs['bras'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(bras_gauche)
    # Bras droit
    bras_droit = Rectangle((largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,
                          facecolor=couleurs['bras'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(bras_droit)
    
    # Dessiner les jambes
    # Jambe gauche
    jambe_gauche = Rectangle((-tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,
                             facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(jambe_gauche)
    # Jambe droite
    jambe_droite = Rectangle((tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,
                             facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(jambe_droite)
    
    # Dessiner les cuisses
    # Cuisse gauche
    cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                            facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(cuisse_gauche)
    # Cuisse droite
    cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                            facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(cuisse_droite)
    
    # Dessiner les pieds
    pied_gauche = Ellipse((-15, 10), 20, 10, facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    pied_droit = Ellipse((15, 10), 20, 10, facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)
    ax.add_patch(pied_gauche)
    ax.add_patch(pied_droit)
    
    # Ajouter des détails du visage
    # Yeux
    oeil_gauche = Ellipse((-hauteur_tete*0.15, y_tete - hauteur_tete*0.3), 3, 2, facecolor='black')
    oeil_droit = Ellipse((hauteur_tete*0.15, y_tete - hauteur_tete*0.3), 3, 2, facecolor='black')
    ax.add_patch(oeil_gauche)
    ax.add_patch(oeil_droit)
    
    # Nez
    nez = Polygon([(0, y_tete - hauteur_tete*0.4), (-2, y_tete - hauteur_tete*0.5), (2, y_tete - hauteur_tete*0.5)],
                  facecolor='#FFB6C1', edgecolor='black', linewidth=1)
    ax.add_patch(nez)
    
    # Bouche
    bouche = Ellipse((0, y_tete - hauteur_tete*0.7), 4, 2, facecolor='#FF69B4', edgecolor='black', linewidth=1)
    ax.add_patch(bouche)
    
    # Configuration de l'affichage
    ax.set_xlim(-60, 60)
    ax.set_ylim(-10, taille + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Titre avec les mesures
    plt.title(f'Silhouette - Taille: {taille}cm, Poitrine: {tour_de_poitrine}cm, Taille: {tour_de_taille}cm', 
              fontsize=12, pad=20)
    
    plt.tight_layout()
    plt.show()

# Création des sliders interactifs avec une mise en page améliorée
def creer_interface_interactive():
    # Sliders pour les mesures principales
    sliders = {
        'taille': FloatSlider(min=140, max=200, step=1, value=170, description='Taille (cm)', 
                              style={'description_width': '120px'}, layout=Layout(width='300px')),
        'tour_de_poitrine': FloatSlider(min=70, max=130, step=1, value=90, description='Tour poitrine (cm)',
                                        style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_de_poitrine': FloatSlider(min=100, max=160, step=1, value=130, description='Haut. poitrine (cm)',
                                           style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_d_entrejambe': FloatSlider(min=60, max=100, step=1, value=80, description='Haut. entrejambe (cm)',
                                            style={'description_width': '120px'}, layout=Layout(width='300px')),
        'largeur_des_hanches': FloatSlider(min=30, max=60, step=1, value=40, description='Larg. hanches (cm)',
                                           style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_des_hanches': FloatSlider(min=80, max=120, step=1, value=100, description='Haut. hanches (cm)',
                                           style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_des_genoux': FloatSlider(min=30, max=70, step=1, value=50, description='Haut. genoux (cm)',
                                          style={'description_width': '120px'}, layout=Layout(width='300px')),
        'largeur_d_epaule': FloatSlider(min=30, max=60, step=1, value=40, description='Larg. épaules (cm)',
                                        style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_des_epaules': FloatSlider(min=120, max=170, step=1, value=150, description='Haut. épaules (cm)',
                                           style={'description_width': '120px'}, layout=Layout(width='300px')),
        'tour_de_cuisse': FloatSlider(min=40, max=80, step=1, value=55, description='Tour cuisse (cm)',
                                      style={'description_width': '120px'}, layout=Layout(width='300px')),
        'tour_de_taille': FloatSlider(min=50, max=100, step=1, value=70, description='Tour taille (cm)',
                                      style={'description_width': '120px'}, layout=Layout(width='300px')),
        'hauteur_de_la_taille': FloatSlider(min=90, max=130, step=1, value=110, description='Haut. taille (cm)',
                                            style={'description_width': '120px'}, layout=Layout(width='300px'))
    }
    
    # Création de l'interface interactive
    interact(dessiner_silhouette_amelioree, **sliders)

# Code simplifié pour copier-coller directement dans le notebook
print("=== CODE À COPIER DANS TON NOTEBOOK JUPYTER ===")
print()
print("# Cellule 1 - Imports et configuration")
print("import matplotlib.pyplot as plt")
print("import numpy as np")
print("from ipywidgets import interact, FloatSlider, Layout")
print("import matplotlib.patches as patches")
print("from matplotlib.patches import Ellipse, Rectangle, Polygon")
print("import warnings")
print("warnings.filterwarnings('ignore')")
print()
print("plt.style.use('default')")
print("plt.rcParams['figure.facecolor'] = 'white'")
print("plt.rcParams['axes.facecolor'] = 'white'")
print()
print("# Cellule 2 - Fonction de dessin")
print("def dessiner_silhouette_amelioree(")
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
print("    fig, ax = plt.subplots(1, 1, figsize=(6, 10))")
print("    ")
print("    # Couleurs pour les différentes parties du corps")
print("    couleurs = {")
print("        'tete': '#FFE4B5',")
print("        'cou': '#FFE4B5',")
print("        'tronc': '#FFE4B5',")
print("        'bras': '#FFE4B5',")
print("        'jambes': '#FFE4B5',")
print("        'contour': '#8B4513'")
print("    }")
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
print("    # Dessiner la tête")
print("    tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete,")
print("                   facecolor=couleurs['tete'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(tete)")
print("    ")
print("    # Dessiner le cou")
print("    cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,")
print("                    facecolor=couleurs['cou'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(cou)")
print("    ")
print("    # Dessiner les épaules")
print("    epaule_gauche = Ellipse((-largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,")
print("                           facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)")
print("    epaule_droite = Ellipse((largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,")
print("                            facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(epaule_gauche)")
print("    ax.add_patch(epaule_droite)")
print("    ")
print("    # Dessiner le tronc")
print("    poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,")
print("                       facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(poitrine)")
print("    ")
print("    taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,")
print("                             facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(taille_ellipse)")
print("    ")
print("    hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,")
print("                      facecolor=couleurs['tronc'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(hanches)")
print("    ")
print("    # Dessiner les bras")
print("    longueur_bras = (y_epaules - y_taille) * 0.8")
print("    bras_gauche = Rectangle((-largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,")
print("                           facecolor=couleurs['bras'], edgecolor=couleurs['contour'], linewidth=2)")
print("    bras_droit = Rectangle((largeur_d_epaule/2 - 8, y_epaules - longueur_bras), 16, longueur_bras,")
print("                          facecolor=couleurs['bras'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(bras_gauche)")
print("    ax.add_patch(bras_droit)")
print("    ")
print("    # Dessiner les jambes")
print("    jambe_gauche = Rectangle((-tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,")
print("                             facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    jambe_droite = Rectangle((tour_de_cuisse/4 - 8, y_genoux), 16, y_genoux - y_pieds,")
print("                             facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(jambe_gauche)")
print("    ax.add_patch(jambe_droite)")
print("    ")
print("    # Dessiner les cuisses")
print("    cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                            facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                            facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(cuisse_gauche)")
print("    ax.add_patch(cuisse_droite)")
print("    ")
print("    # Dessiner les pieds")
print("    pied_gauche = Ellipse((-15, 10), 20, 10, facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    pied_droit = Ellipse((15, 10), 20, 10, facecolor=couleurs['jambes'], edgecolor=couleurs['contour'], linewidth=2)")
print("    ax.add_patch(pied_gauche)")
print("    ax.add_patch(pied_droit)")
print("    ")
print("    # Détails du visage")
print("    oeil_gauche = Ellipse((-hauteur_tete*0.15, y_tete - hauteur_tete*0.3), 3, 2, facecolor='black')")
print("    oeil_droit = Ellipse((hauteur_tete*0.15, y_tete - hauteur_tete*0.3), 3, 2, facecolor='black')")
print("    ax.add_patch(oeil_gauche)")
print("    ax.add_patch(oeil_droit)")
print("    ")
print("    nez = Polygon([(0, y_tete - hauteur_tete*0.4), (-2, y_tete - hauteur_tete*0.5), (2, y_tete - hauteur_tete*0.5)],")
print("                  facecolor='#FFB6C1', edgecolor='black', linewidth=1)")
print("    ax.add_patch(nez)")
print("    ")
print("    bouche = Ellipse((0, y_tete - hauteur_tete*0.7), 4, 2, facecolor='#FF69B4', edgecolor='black', linewidth=1)")
print("    ax.add_patch(bouche)")
print("    ")
print("    # Configuration de l'affichage")
print("    ax.set_xlim(-60, 60)")
print("    ax.set_ylim(-10, taille + 10)")
print("    ax.set_aspect('equal')")
print("    ax.axis('off')")
print("    ")
print("    plt.title(f'Silhouette - Taille: {taille}cm, Poitrine: {tour_de_poitrine}cm, Taille: {tour_de_taille}cm',")
print("              fontsize=12, pad=20)")
print("    ")
print("    plt.tight_layout()")
print("    plt.show()")
print()
print("# Cellule 3 - Interface interactive")
print("interact(")
print("    dessiner_silhouette_amelioree,")
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