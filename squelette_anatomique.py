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

def dessiner_squelette(
    taille=170,
    largeur_epaules=40,
    largeur_hanches=35,
    longueur_bras=60,
    longueur_jambes=80
):
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 12))
    
    # Couleurs pour les os
    couleur_os = '#F5F5DC'  # Beige clair
    couleur_contour = '#8B4513'  # Marron foncé
    couleur_crane = '#DEB887'  # Beige plus foncé
    
    # Calcul des proportions
    hauteur_crane = taille * 0.12
    hauteur_colonne = taille * 0.6
    hauteur_cou = taille * 0.04
    
    # Position Y des différentes parties
    y_crane = taille
    y_cou = taille - hauteur_crane
    y_epaules = taille - hauteur_crane - hauteur_cou
    y_cotes = y_epaules - 20
    y_colonne_vertebrale = y_epaules - hauteur_colonne
    y_bassin = y_colonne_vertebrale
    y_genoux = y_bassin - longueur_jambes
    y_pieds = 0
    
    # 1. CRÂNE
    crane = Ellipse((0, y_crane - hauteur_crane/2), hauteur_crane*0.7, hauteur_crane, 
                    facecolor=couleur_crane, edgecolor=couleur_contour, linewidth=2)
    ax.add_patch(crane)
    
    # Orbites des yeux
    orbite_gauche = Ellipse((-hauteur_crane*0.2, y_crane - hauteur_crane*0.4), 8, 6, 
                           facecolor='white', edgecolor=couleur_contour, linewidth=1)
    orbite_droite = Ellipse((hauteur_crane*0.2, y_crane - hauteur_crane*0.4), 8, 6, 
                           facecolor='white', edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(orbite_gauche)
    ax.add_patch(orbite_droite)
    
    # Cavité nasale
    cavite_nasale = Ellipse((0, y_crane - hauteur_crane*0.6), 4, 3, 
                           facecolor='white', edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(cavite_nasale)
    
    # 2. COLONNE VERTÉBRALE
    # Cervicales
    for i in range(7):
        vertebre = Rectangle((-2, y_cou - i*3), 4, 2, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
        ax.add_patch(vertebre)
    
    # Thoraciques
    for i in range(12):
        vertebre = Rectangle((-2, y_epaules - 20 - i*3), 4, 2, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
        ax.add_patch(vertebre)
    
    # Lombaires
    for i in range(5):
        vertebre = Rectangle((-2, y_colonne_vertebrale + i*3), 4, 2, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
        ax.add_patch(vertebre)
    
    # 3. CÔTES
    # Côtes gauches
    for i in range(12):
        y_pos = y_cotes - i*2.5
        longueur_cote = 15 + i*0.5
        cote_gauche = Ellipse((-longueur_cote/2, y_pos), longueur_cote, 1, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1, angle=15)
        ax.add_patch(cote_gauche)
    
    # Côtes droites
    for i in range(12):
        y_pos = y_cotes - i*2.5
        longueur_cote = 15 + i*0.5
        cote_droite = Ellipse((longueur_cote/2, y_pos), longueur_cote, 1, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1, angle=-15)
        ax.add_patch(cote_droite)
    
    # 4. CLAVICULES
    clavicule_gauche = Rectangle((-largeur_epaules/2 - 15, y_epaules), 15, 2, 
                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    clavicule_droite = Rectangle((largeur_epaules/2, y_epaules), 15, 2, 
                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(clavicule_gauche)
    ax.add_patch(clavicule_droite)
    
    # 5. OMBOPLATES (Épaules)
    omoplate_gauche = Ellipse((-largeur_epaules/2, y_epaules - 5), 8, 12, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    omoplate_droite = Ellipse((largeur_epaules/2, y_epaules - 5), 8, 12, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(omoplate_gauche)
    ax.add_patch(omoplate_droite)
    
    # 6. BRAS
    # Humérus gauche
    humerus_gauche = Rectangle((-largeur_epaules/2 - 3, y_epaules - longueur_bras), 6, longueur_bras, 
                              facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(humerus_gauche)
    
    # Humérus droit
    humerus_droit = Rectangle((largeur_epaules/2 - 3, y_epaules - longueur_bras), 6, longueur_bras, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(humerus_droit)
    
    # Coudes
    coude_gauche = Ellipse((-largeur_epaules/2, y_epaules - longueur_bras), 8, 4, 
                          facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    coude_droit = Ellipse((largeur_epaules/2, y_epaules - longueur_bras), 8, 4, 
                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(coude_gauche)
    ax.add_patch(coude_droit)
    
    # Avant-bras (radius et ulna)
    avant_bras_gauche = Rectangle((-largeur_epaules/2 - 2, y_epaules - longueur_bras - 30), 4, 30, 
                                 facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    avant_bras_droit = Rectangle((largeur_epaules/2 - 2, y_epaules - longueur_bras - 30), 4, 30, 
                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(avant_bras_gauche)
    ax.add_patch(avant_bras_droit)
    
    # Mains
    main_gauche = Ellipse((-largeur_epaules/2, y_epaules - longueur_bras - 35), 12, 8, 
                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    main_droite = Ellipse((largeur_epaules/2, y_epaules - longueur_bras - 35), 12, 8, 
                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(main_gauche)
    ax.add_patch(main_droite)
    
    # 7. BASSIN
    # Ilium (os du bassin)
    ilium_gauche = Ellipse((-largeur_hanches/2 - 5, y_bassin), 10, 8, 
                          facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ilium_droit = Ellipse((largeur_hanches/2 + 5, y_bassin), 10, 8, 
                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(ilium_gauche)
    ax.add_patch(ilium_droit)
    
    # Pubis
    pubis = Rectangle((-8, y_bassin - 5), 16, 3, 
                     facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(pubis)
    
    # 8. JAMBES
    # Fémurs
    femur_gauche = Rectangle((-largeur_hanches/2 - 3, y_bassin - longueur_jambes), 6, longueur_jambes, 
                            facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    femur_droit = Rectangle((largeur_hanches/2 - 3, y_bassin - longueur_jambes), 6, longueur_jambes, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(femur_gauche)
    ax.add_patch(femur_droit)
    
    # Rotules
    rotule_gauche = Ellipse((-largeur_hanches/2, y_genoux), 6, 3, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    rotule_droite = Ellipse((largeur_hanches/2, y_genoux), 6, 3, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(rotule_gauche)
    ax.add_patch(rotule_droite)
    
    # Tibias et péronés
    tibia_gauche = Rectangle((-largeur_hanches/2 - 2, y_genoux - 40), 4, 40, 
                            facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    tibia_droit = Rectangle((largeur_hanches/2 - 2, y_genoux - 40), 4, 40, 
                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(tibia_gauche)
    ax.add_patch(tibia_droit)
    
    # Chevilles
    cheville_gauche = Ellipse((-largeur_hanches/2, y_pieds + 15), 8, 4, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    cheville_droite = Ellipse((largeur_hanches/2, y_pieds + 15), 8, 4, 
                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(cheville_gauche)
    ax.add_patch(cheville_droite)
    
    # Pieds
    pied_gauche = Ellipse((-largeur_hanches/2, y_pieds + 5), 15, 8, 
                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    pied_droit = Ellipse((largeur_hanches/2, y_pieds + 5), 15, 8, 
                        facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(pied_gauche)
    ax.add_patch(pied_droit)
    
    # 9. STERNUM
    sternum = Rectangle((-3, y_cotes - 15), 6, 15, 
                       facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)
    ax.add_patch(sternum)
    
    # Configuration de l'affichage
    ax.set_xlim(-50, 50)
    ax.set_ylim(-10, taille + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Squelette Anatomique', fontsize=16, pad=20, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Interface interactive pour le squelette
def creer_interface_squelette():
    interact(
        dessiner_squelette,
        taille=FloatSlider(min=140, max=200, step=1, value=170, description='Taille (cm)'),
        largeur_epaules=FloatSlider(min=30, max=60, step=1, value=40, description='Largeur épaules (cm)'),
        largeur_hanches=FloatSlider(min=25, max=50, step=1, value=35, description='Largeur hanches (cm)'),
        longueur_bras=FloatSlider(min=40, max=80, step=1, value=60, description='Longueur bras (cm)'),
        longueur_jambes=FloatSlider(min=60, max=100, step=1, value=80, description='Longueur jambes (cm)')
    )

print("=== CODE POUR SQUELETTE ANATOMIQUE ===")
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
print("# Cellule 2 - Fonction squelette")
print("def dessiner_squelette(")
print("    taille=170,")
print("    largeur_epaules=40,")
print("    largeur_hanches=35,")
print("    longueur_bras=60,")
print("    longueur_jambes=80")
print("):")
print("    ")
print("    fig, ax = plt.subplots(1, 1, figsize=(8, 12))")
print("    ")
print("    # Couleurs pour les os")
print("    couleur_os = '#F5F5DC'  # Beige clair")
print("    couleur_contour = '#8B4513'  # Marron foncé")
print("    couleur_crane = '#DEB887'  # Beige plus foncé")
print("    ")
print("    # Calcul des proportions")
print("    hauteur_crane = taille * 0.12")
print("    hauteur_colonne = taille * 0.6")
print("    hauteur_cou = taille * 0.04")
print("    ")
print("    # Position Y des différentes parties")
print("    y_crane = taille")
print("    y_cou = taille - hauteur_crane")
print("    y_epaules = taille - hauteur_crane - hauteur_cou")
print("    y_cotes = y_epaules - 20")
print("    y_colonne_vertebrale = y_epaules - hauteur_colonne")
print("    y_bassin = y_colonne_vertebrale")
print("    y_genoux = y_bassin - longueur_jambes")
print("    y_pieds = 0")
print("    ")
print("    # 1. CRÂNE")
print("    crane = Ellipse((0, y_crane - hauteur_crane/2), hauteur_crane*0.7, hauteur_crane,")
print("                    facecolor=couleur_crane, edgecolor=couleur_contour, linewidth=2)")
print("    ax.add_patch(crane)")
print("    ")
print("    # Orbites des yeux")
print("    orbite_gauche = Ellipse((-hauteur_crane*0.2, y_crane - hauteur_crane*0.4), 8, 6,")
print("                           facecolor='white', edgecolor=couleur_contour, linewidth=1)")
print("    orbite_droite = Ellipse((hauteur_crane*0.2, y_crane - hauteur_crane*0.4), 8, 6,")
print("                           facecolor='white', edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(orbite_gauche)")
print("    ax.add_patch(orbite_droite)")
print("    ")
print("    # Cavité nasale")
print("    cavite_nasale = Ellipse((0, y_crane - hauteur_crane*0.6), 4, 3,")
print("                           facecolor='white', edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(cavite_nasale)")
print("    ")
print("    # 2. COLONNE VERTÉBRALE")
print("    # Cervicales")
print("    for i in range(7):")
print("        vertebre = Rectangle((-2, y_cou - i*3), 4, 2,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("        ax.add_patch(vertebre)")
print("    ")
print("    # Thoraciques")
print("    for i in range(12):")
print("        vertebre = Rectangle((-2, y_epaules - 20 - i*3), 4, 2,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("        ax.add_patch(vertebre)")
print("    ")
print("    # Lombaires")
print("    for i in range(5):")
print("        vertebre = Rectangle((-2, y_colonne_vertebrale + i*3), 4, 2,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("        ax.add_patch(vertebre)")
print("    ")
print("    # 3. CÔTES")
print("    # Côtes gauches")
print("    for i in range(12):")
print("        y_pos = y_cotes - i*2.5")
print("        longueur_cote = 15 + i*0.5")
print("        cote_gauche = Ellipse((-longueur_cote/2, y_pos), longueur_cote, 1,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1, angle=15)")
print("        ax.add_patch(cote_gauche)")
print("    ")
print("    # Côtes droites")
print("    for i in range(12):")
print("        y_pos = y_cotes - i*2.5")
print("        longueur_cote = 15 + i*0.5")
print("        cote_droite = Ellipse((longueur_cote/2, y_pos), longueur_cote, 1,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1, angle=-15)")
print("        ax.add_patch(cote_droite)")
print("    ")
print("    # 4. CLAVICULES")
print("    clavicule_gauche = Rectangle((-largeur_epaules/2 - 15, y_epaules), 15, 2,")
print("                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    clavicule_droite = Rectangle((largeur_epaules/2, y_epaules), 15, 2,")
print("                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(clavicule_gauche)")
print("    ax.add_patch(clavicule_droite)")
print("    ")
print("    # 5. OMBOPLATES (Épaules)")
print("    omoplate_gauche = Ellipse((-largeur_epaules/2, y_epaules - 5), 8, 12,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    omoplate_droite = Ellipse((largeur_epaules/2, y_epaules - 5), 8, 12,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(omoplate_gauche)")
print("    ax.add_patch(omoplate_droite)")
print("    ")
print("    # 6. BRAS")
print("    # Humérus gauche")
print("    humerus_gauche = Rectangle((-largeur_epaules/2 - 3, y_epaules - longueur_bras), 6, longueur_bras,")
print("                              facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(humerus_gauche)")
print("    ")
print("    # Humérus droit")
print("    humerus_droit = Rectangle((largeur_epaules/2 - 3, y_epaules - longueur_bras), 6, longueur_bras,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(humerus_droit)")
print("    ")
print("    # Coudes")
print("    coude_gauche = Ellipse((-largeur_epaules/2, y_epaules - longueur_bras), 8, 4,")
print("                          facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    coude_droit = Ellipse((largeur_epaules/2, y_epaules - longueur_bras), 8, 4,")
print("                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(coude_gauche)")
print("    ax.add_patch(coude_droit)")
print("    ")
print("    # Avant-bras (radius et ulna)")
print("    avant_bras_gauche = Rectangle((-largeur_epaules/2 - 2, y_epaules - longueur_bras - 30), 4, 30,")
print("                                 facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    avant_bras_droit = Rectangle((largeur_epaules/2 - 2, y_epaules - longueur_bras - 30), 4, 30,")
print("                                facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(avant_bras_gauche)")
print("    ax.add_patch(avant_bras_droit)")
print("    ")
print("    # Mains")
print("    main_gauche = Ellipse((-largeur_epaules/2, y_epaules - longueur_bras - 35), 12, 8,")
print("                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    main_droite = Ellipse((largeur_epaules/2, y_epaules - longueur_bras - 35), 12, 8,")
print("                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(main_gauche)")
print("    ax.add_patch(main_droite)")
print("    ")
print("    # 7. BASSIN")
print("    # Ilium (os du bassin)")
print("    ilium_gauche = Ellipse((-largeur_hanches/2 - 5, y_bassin), 10, 8,")
print("                          facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ilium_droit = Ellipse((largeur_hanches/2 + 5, y_bassin), 10, 8,")
print("                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(ilium_gauche)")
print("    ax.add_patch(ilium_droit)")
print("    ")
print("    # Pubis")
print("    pubis = Rectangle((-8, y_bassin - 5), 16, 3,")
print("                     facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(pubis)")
print("    ")
print("    # 8. JAMBES")
print("    # Fémurs")
print("    femur_gauche = Rectangle((-largeur_hanches/2 - 3, y_bassin - longueur_jambes), 6, longueur_jambes,")
print("                            facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    femur_droit = Rectangle((largeur_hanches/2 - 3, y_bassin - longueur_jambes), 6, longueur_jambes,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(femur_gauche)")
print("    ax.add_patch(femur_droit)")
print("    ")
print("    # Rotules")
print("    rotule_gauche = Ellipse((-largeur_hanches/2, y_genoux), 6, 3,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    rotule_droite = Ellipse((largeur_hanches/2, y_genoux), 6, 3,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(rotule_gauche)")
print("    ax.add_patch(rotule_droite)")
print("    ")
print("    # Tibias et péronés")
print("    tibia_gauche = Rectangle((-largeur_hanches/2 - 2, y_genoux - 40), 4, 40,")
print("                            facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    tibia_droit = Rectangle((largeur_hanches/2 - 2, y_genoux - 40), 4, 40,")
print("                           facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(tibia_gauche)")
print("    ax.add_patch(tibia_droit)")
print("    ")
print("    # Chevilles")
print("    cheville_gauche = Ellipse((-largeur_hanches/2, y_pieds + 15), 8, 4,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    cheville_droite = Ellipse((largeur_hanches/2, y_pieds + 15), 8, 4,")
print("                             facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(cheville_gauche)")
print("    ax.add_patch(cheville_droite)")
print("    ")
print("    # Pieds")
print("    pied_gauche = Ellipse((-largeur_hanches/2, y_pieds + 5), 15, 8,")
print("                         facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    pied_droit = Ellipse((largeur_hanches/2, y_pieds + 5), 15, 8,")
print("                        facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(pied_gauche)")
print("    ax.add_patch(pied_droit)")
print("    ")
print("    # 9. STERNUM")
print("    sternum = Rectangle((-3, y_cotes - 15), 6, 15,")
print("                       facecolor=couleur_os, edgecolor=couleur_contour, linewidth=1)")
print("    ax.add_patch(sternum)")
print("    ")
print("    # Configuration de l'affichage")
print("    ax.set_xlim(-50, 50)")
print("    ax.set_ylim(-10, taille + 10)")
print("    ax.set_aspect('equal')")
print("    ax.axis('off')")
print("    ")
print("    plt.title('Squelette Anatomique', fontsize=16, pad=20, fontweight='bold')")
print("    plt.tight_layout()")
print("    plt.show()")
print()
print("# Cellule 3 - Interface interactive")
print("interact(")
print("    dessiner_squelette,")
print("    taille=FloatSlider(min=140, max=200, step=1, value=170, description='Taille (cm)'),")
print("    largeur_epaules=FloatSlider(min=30, max=60, step=1, value=40, description='Largeur épaules (cm)'),")
print("    largeur_hanches=FloatSlider(min=25, max=50, step=1, value=35, description='Largeur hanches (cm)'),")
print("    longueur_bras=FloatSlider(min=40, max=80, step=1, value=60, description='Longueur bras (cm)'),")
print("    longueur_jambes=FloatSlider(min=60, max=100, step=1, value=80, description='Longueur jambes (cm)')")
print(")") 