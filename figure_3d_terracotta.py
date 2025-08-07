import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, FloatSlider, VBox, HBox, Layout
import matplotlib.patches as patches
from matplotlib.patches import Ellipse, Rectangle, Polygon, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# Configuration pour un affichage plus propre
plt.style.use('default')
plt.rcParams['figure.facecolor'] = '#2F2F2F'  # Fond gris foncé
plt.rcParams['axes.facecolor'] = '#2F2F2F'

def dessiner_figure_3d_terracotta(
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
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    
    # Couleurs terre cuite avec dégradés 3D
    couleur_base = '#CD853F'  # Terre cuite
    couleur_ombre = '#8B4513'  # Marron foncé
    couleur_highlight = '#DEB887'  # Beige clair
    
    # Création d'un dégradé pour l'effet 3D
    cmap_terracotta = LinearSegmentedColormap.from_list('terracotta', 
                                                       [couleur_ombre, couleur_base, couleur_highlight])
    
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
    
    # Fonction pour créer un effet 3D avec ombre
    def dessiner_partie_3d(ax, forme, couleur_principale, x_offset=0, y_offset=0):
        # Forme principale
        forme.set_facecolor(couleur_principale)
        forme.set_edgecolor(couleur_ombre)
        forme.set_linewidth(1.5)
        ax.add_patch(forme)
        
        # Ombre portée (légèrement décalée)
        ombre = forme.copy()
        ombre.set_facecolor(couleur_ombre)
        ombre.set_edgecolor(couleur_ombre)
        ombre.set_alpha(0.3)
        ombre.set_xy((forme.get_xy()[0] + 2, forme.get_xy()[1] - 2))
        ax.add_patch(ombre)
    
    # 1. TÊTE (avec détails faciaux)
    # Crâne principal
    tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete, 
                   facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, tete, couleur_base)
    
    # Yeux
    oeil_gauche = Ellipse((-hauteur_tete*0.15, y_tete - hauteur_tete*0.35), 3, 2, 
                         facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)
    oeil_droit = Ellipse((hauteur_tete*0.15, y_tete - hauteur_tete*0.35), 3, 2, 
                        facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)
    ax.add_patch(oeil_gauche)
    ax.add_patch(oeil_droit)
    
    # Nez
    nez = Polygon([(0, y_tete - hauteur_tete*0.4), (-1.5, y_tete - hauteur_tete*0.5), (1.5, y_tete - hauteur_tete*0.5)],
                  facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1)
    ax.add_patch(nez)
    
    # Bouche
    bouche = Ellipse((0, y_tete - hauteur_tete*0.65), 3, 1.5, 
                    facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)
    ax.add_patch(bouche)
    
    # Oreilles
    oreille_gauche = Ellipse((-hauteur_tete*0.35, y_tete - hauteur_tete*0.4), 2, 4, 
                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=1)
    oreille_droite = Ellipse((hauteur_tete*0.35, y_tete - hauteur_tete*0.4), 2, 4, 
                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=1)
    ax.add_patch(oreille_gauche)
    ax.add_patch(oreille_droite)
    
    # 2. COU
    cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,
                    facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, cou, couleur_base)
    
    # 3. TORSO (avec muscles définis)
    # Poitrine (pectoraux)
    poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,
                       facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, poitrine, couleur_base)
    
    # Définition des pectoraux
    pectoral_gauche = Ellipse((-tour_de_poitrine*0.15, y_poitrine - 5), 8, 12, 
                             facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.3)
    pectoral_droit = Ellipse((tour_de_poitrine*0.15, y_poitrine - 5), 8, 12, 
                            facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.3)
    ax.add_patch(pectoral_gauche)
    ax.add_patch(pectoral_droit)
    
    # Taille
    taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,
                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, taille_ellipse, couleur_base)
    
    # Abdomen (muscles)
    for i in range(4):
        muscle = Rectangle((-4, y_taille - 10 - i*3), 8, 2, 
                          facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.2)
        ax.add_patch(muscle)
    
    # Hanches
    hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,
                      facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, hanches, couleur_base)
    
    # 4. ÉPAULES (en T-pose)
    # Épaules principales
    epaule_gauche = Ellipse((-largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                           facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    epaule_droite = Ellipse((largeur_d_epaule/2, y_epaules), largeur_d_epaule*0.3, largeur_d_epaule*0.2,
                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, epaule_gauche, couleur_base)
    dessiner_partie_3d(ax, epaule_droite, couleur_base)
    
    # 5. BRAS (en T-pose, étendus horizontalement)
    longueur_bras = (y_epaules - y_taille) * 0.8
    
    # Bras gauche (horizontal)
    bras_gauche = Rectangle((-largeur_d_epaule/2 - longueur_bras, y_epaules - 8), longueur_bras, 16,
                           facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, bras_gauche, couleur_base)
    
    # Bras droit (horizontal)
    bras_droit = Rectangle((largeur_d_epaule/2, y_epaules - 8), longueur_bras, 16,
                          facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, bras_droit, couleur_base)
    
    # Coudes
    coude_gauche = Ellipse((-largeur_d_epaule/2 - longueur_bras, y_epaules), 8, 6, 
                          facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    coude_droit = Ellipse((largeur_d_epaule/2 + longueur_bras, y_epaules), 8, 6, 
                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    ax.add_patch(coude_gauche)
    ax.add_patch(coude_droit)
    
    # Avant-bras
    avant_bras_gauche = Rectangle((-largeur_d_epaule/2 - longueur_bras - 20, y_epaules - 6), 20, 12,
                                 facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    avant_bras_droit = Rectangle((largeur_d_epaule/2 + longueur_bras, y_epaules - 6), 20, 12,
                                facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, avant_bras_gauche, couleur_base)
    dessiner_partie_3d(ax, avant_bras_droit, couleur_base)
    
    # Mains (paumes vers le bas en T-pose)
    main_gauche = Ellipse((-largeur_d_epaule/2 - longueur_bras - 25, y_epaules), 12, 8, 
                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    main_droite = Ellipse((largeur_d_epaule/2 + longueur_bras + 25, y_epaules), 12, 8, 
                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    ax.add_patch(main_gauche)
    ax.add_patch(main_droite)
    
    # 6. JAMBES
    # Cuisses
    cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,
                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, cuisse_gauche, couleur_base)
    dessiner_partie_3d(ax, cuisse_droite, couleur_base)
    
    # Définition musculaire des cuisses
    for i in range(3):
        muscle_gauche = Rectangle((-tour_de_cuisse/4 - 3, (y_hanches + y_genoux)/2 - 10 + i*5), 6, 3, 
                                 facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.2)
        muscle_droit = Rectangle((tour_de_cuisse/4 - 3, (y_hanches + y_genoux)/2 - 10 + i*5), 6, 3, 
                                facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.2)
        ax.add_patch(muscle_gauche)
        ax.add_patch(muscle_droit)
    
    # Genoux
    genou_gauche = Ellipse((-tour_de_cuisse/4, y_genoux), 8, 4, 
                          facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    genou_droit = Ellipse((tour_de_cuisse/4, y_genoux), 8, 4, 
                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    ax.add_patch(genou_gauche)
    ax.add_patch(genou_droit)
    
    # Jambes
    jambe_gauche = Rectangle((-tour_de_cuisse/4 - 4, y_genoux - 40), 8, 40, 
                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    jambe_droite = Rectangle((tour_de_cuisse/4 - 4, y_genoux - 40), 8, 40, 
                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    dessiner_partie_3d(ax, jambe_gauche, couleur_base)
    dessiner_partie_3d(ax, jambe_droite, couleur_base)
    
    # Mollets
    mollet_gauche = Ellipse((-tour_de_cuisse/4, y_genoux - 20), 6, 8, 
                           facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.3)
    mollet_droit = Ellipse((tour_de_cuisse/4, y_genoux - 20), 6, 8, 
                          facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1, alpha=0.3)
    ax.add_patch(mollet_gauche)
    ax.add_patch(mollet_droit)
    
    # Chevilles
    cheville_gauche = Ellipse((-tour_de_cuisse/4, y_pieds + 15), 6, 4, 
                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    cheville_droite = Ellipse((tour_de_cuisse/4, y_pieds + 15), 6, 4, 
                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    ax.add_patch(cheville_gauche)
    ax.add_patch(cheville_droite)
    
    # Pieds (légèrement écartés)
    pied_gauche = Ellipse((-tour_de_cuisse/4 - 5, y_pieds + 5), 12, 6, 
                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    pied_droit = Ellipse((tour_de_cuisse/4 + 5, y_pieds + 5), 12, 6, 
                        facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)
    ax.add_patch(pied_gauche)
    ax.add_patch(pied_droit)
    
    # 7. PLAN DE SOL (gris clair)
    sol = Rectangle((-50, -5), 100, 5, 
                   facecolor='#808080', edgecolor='#606060', linewidth=1)
    ax.add_patch(sol)
    
    # Configuration de l'affichage
    ax.set_xlim(-60, 60)
    ax.set_ylim(-10, taille + 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Figure 3D - T-Pose Terracotta', fontsize=16, pad=20, fontweight='bold', color='white')
    plt.tight_layout()
    plt.show()

# Interface interactive
def creer_interface_3d():
    interact(
        dessiner_figure_3d_terracotta,
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

print("=== CODE POUR FIGURE 3D TERRACOTTA ===")
print()
print("# Cellule 1 - Imports")
print("import matplotlib.pyplot as plt")
print("import numpy as np")
print("from ipywidgets import interact, FloatSlider")
print("import matplotlib.patches as patches")
print("from matplotlib.patches import Ellipse, Rectangle, Polygon")
print("from matplotlib.colors import LinearSegmentedColormap")
print("import warnings")
print("warnings.filterwarnings('ignore')")
print()
print("plt.style.use('default')")
print("plt.rcParams['figure.facecolor'] = '#2F2F2F'  # Fond gris foncé")
print("plt.rcParams['axes.facecolor'] = '#2F2F2F'")
print()
print("# Cellule 2 - Fonction figure 3D")
print("def dessiner_figure_3d_terracotta(")
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
print("    fig, ax = plt.subplots(1, 1, figsize=(8, 10))")
print("    ")
print("    # Couleurs terre cuite")
print("    couleur_base = '#CD853F'  # Terre cuite")
print("    couleur_ombre = '#8B4513'  # Marron foncé")
print("    couleur_highlight = '#DEB887'  # Beige clair")
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
print("    # Fonction pour créer un effet 3D avec ombre")
print("    def dessiner_partie_3d(ax, forme, couleur_principale):")
print("        # Forme principale")
print("        forme.set_facecolor(couleur_principale)")
print("        forme.set_edgecolor(couleur_ombre)")
print("        forme.set_linewidth(1.5)")
print("        ax.add_patch(forme)")
print("        ")
print("        # Ombre portée")
print("        ombre = forme.copy()")
print("        ombre.set_facecolor(couleur_ombre)")
print("        ombre.set_edgecolor(couleur_ombre)")
print("        ombre.set_alpha(0.3)")
print("        ombre.set_xy((forme.get_xy()[0] + 2, forme.get_xy()[1] - 2))")
print("        ax.add_patch(ombre)")
print("    ")
print("    # 1. TÊTE")
print("    tete = Ellipse((0, y_tete - hauteur_tete/2), hauteur_tete*0.6, hauteur_tete,")
print("                   facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, tete, couleur_base)")
print("    ")
print("    # Yeux")
print("    oeil_gauche = Ellipse((-hauteur_tete*0.15, y_tete - hauteur_tete*0.35), 3, 2,")
print("                         facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)")
print("    oeil_droit = Ellipse((hauteur_tete*0.15, y_tete - hauteur_tete*0.35), 3, 2,")
print("                        facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)")
print("    ax.add_patch(oeil_gauche)")
print("    ax.add_patch(oeil_droit)")
print("    ")
print("    # Nez et bouche")
print("    nez = Polygon([(0, y_tete - hauteur_tete*0.4), (-1.5, y_tete - hauteur_tete*0.5), (1.5, y_tete - hauteur_tete*0.5)],")
print("                  facecolor=couleur_ombre, edgecolor=couleur_ombre, linewidth=1)")
print("    bouche = Ellipse((0, y_tete - hauteur_tete*0.65), 3, 1.5,")
print("                    facecolor='#2F2F2F', edgecolor=couleur_ombre, linewidth=1)")
print("    ax.add_patch(nez)")
print("    ax.add_patch(bouche)")
print("    ")
print("    # 2. COU")
print("    cou = Rectangle((-hauteur_tete*0.15, y_cou - hauteur_cou), hauteur_tete*0.3, hauteur_cou,")
print("                    facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, cou, couleur_base)")
print("    ")
print("    # 3. TORSO")
print("    poitrine = Ellipse((0, y_poitrine), tour_de_poitrine*0.4, (y_poitrine - y_taille)*0.8,")
print("                       facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, poitrine, couleur_base)")
print("    ")
print("    taille_ellipse = Ellipse((0, y_taille), tour_de_taille*0.4, (y_taille - y_hanches)*0.8,")
print("                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, taille_ellipse, couleur_base)")
print("    ")
print("    hanches = Ellipse((0, y_hanches), largeur_des_hanches*0.8, (y_hanches - y_genoux)*0.3,")
print("                      facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, hanches, couleur_base)")
print("    ")
print("    # 4. BRAS (T-pose)")
print("    longueur_bras = (y_epaules - y_taille) * 0.8")
print("    bras_gauche = Rectangle((-largeur_d_epaule/2 - longueur_bras, y_epaules - 8), longueur_bras, 16,")
print("                           facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    bras_droit = Rectangle((largeur_d_epaule/2, y_epaules - 8), longueur_bras, 16,")
print("                          facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, bras_gauche, couleur_base)")
print("    dessiner_partie_3d(ax, bras_droit, couleur_base)")
print("    ")
print("    # 5. JAMBES")
print("    cuisse_gauche = Ellipse((-tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    cuisse_droite = Ellipse((tour_de_cuisse/4, (y_hanches + y_genoux)/2), tour_de_cuisse*0.3, (y_hanches - y_genoux)*0.8,")
print("                            facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, cuisse_gauche, couleur_base)")
print("    dessiner_partie_3d(ax, cuisse_droite, couleur_base)")
print("    ")
print("    jambe_gauche = Rectangle((-tour_de_cuisse/4 - 4, y_genoux - 40), 8, 40,")
print("                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    jambe_droite = Rectangle((tour_de_cuisse/4 - 4, y_genoux - 40), 8, 40,")
print("                             facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    dessiner_partie_3d(ax, jambe_gauche, couleur_base)")
print("    dessiner_partie_3d(ax, jambe_droite, couleur_base)")
print("    ")
print("    # Pieds")
print("    pied_gauche = Ellipse((-tour_de_cuisse/4 - 5, y_pieds + 5), 12, 6,")
print("                         facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    pied_droit = Ellipse((tour_de_cuisse/4 + 5, y_pieds + 5), 12, 6,")
print("                        facecolor=couleur_base, edgecolor=couleur_ombre, linewidth=2)")
print("    ax.add_patch(pied_gauche)")
print("    ax.add_patch(pied_droit)")
print("    ")
print("    # Plan de sol")
print("    sol = Rectangle((-50, -5), 100, 5,")
print("                   facecolor='#808080', edgecolor='#606060', linewidth=1)")
print("    ax.add_patch(sol)")
print("    ")
print("    # Configuration de l'affichage")
print("    ax.set_xlim(-60, 60)")
print("    ax.set_ylim(-10, taille + 10)")
print("    ax.set_aspect('equal')")
print("    ax.axis('off')")
print("    ")
print("    plt.title('Figure 3D - T-Pose Terracotta', fontsize=16, pad=20, fontweight='bold', color='white')")
print("    plt.tight_layout()")
print("    plt.show()")
print()
print("# Cellule 3 - Interface interactive")
print("interact(")
print("    dessiner_figure_3d_terracotta,")
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