# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from wrapper import MultiTPOTWrapper
from PIL import Image

# =======================
# Configuration des chemins
# =======================
IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

# =======================
# Chargement des modèles
# =======================
@st.cache_resource
def load_all_models(folder_path):
    models = []
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".pkl"):
            model_path = os.path.join(folder_path, file)
            model = joblib.load(model_path)
            models.append(model)
    return models

@st.cache_resource
def get_target_names(folder_path):
    return [
        f.replace("pipeline_tpot_", "").replace(".pkl", "")
        for f in sorted(os.listdir(folder_path)) if f.endswith(".pkl")
    ]

# =======================
# Fonction de dessin
# =======================
def draw_body_2d(
    taille,
    hauteur_de_la_taille,
    hauteur_de_poitrine,
    hauteur_des_epaules,
    hauteur_des_genoux,
    hauteur_des_hanches,
    largeur_d_epaule,
    longueur_d_avant_bras,
    longueur_du_bras,
    largeur_de_cuisse,
    largeur_de_hanches,
    largeur_de_poitrine,
    largeur_de_la_taille,
    largeur_du_cou,
):
    fig, ax = plt.subplots(figsize=(3, 8))
    ax.cla()

    # Points clés du tronc gauche
    p_hanches_left = (-largeur_de_hanches/2, hauteur_des_hanches)
    p_taille_left = (-largeur_de_la_taille/2, hauteur_de_la_taille)
    p_poitrine_left = (-largeur_de_poitrine/2, hauteur_de_poitrine)
    p_epaules_left = (-largeur_d_epaule/2, hauteur_des_epaules)

    # Points clés du tronc droit
    p_hanches_right = (largeur_de_hanches/2, hauteur_des_hanches)
    p_taille_right = (largeur_de_la_taille/2, hauteur_de_la_taille)
    p_poitrine_right = (largeur_de_poitrine/2, hauteur_de_poitrine)
    p_epaules_right = (largeur_d_epaule/2, hauteur_des_epaules)

    # Polygone tronc
    trunk_points = [
        p_hanches_left,
        p_taille_left,
        p_poitrine_left,
        p_epaules_left,
        p_epaules_right,
        p_poitrine_right,
        p_taille_right,
        p_hanches_right,
    ]
    trunk = Polygon(trunk_points, closed=True, facecolor="#F1948A", edgecolor="black", alpha=0.8)
    ax.add_patch(trunk)

    # Jambes
    cuisse_left = Polygon([
        (-largeur_de_hanches/4 - largeur_de_cuisse/2, 0),
        (-largeur_de_hanches/4 + largeur_de_cuisse/2, 0),
        (-largeur_de_hanches/4 + largeur_de_cuisse/4, hauteur_des_hanches),
        (-largeur_de_hanches/4 - largeur_de_cuisse/4, hauteur_des_hanches),
    ], closed=True, facecolor="#955251", edgecolor="black", alpha=0.9)
    ax.add_patch(cuisse_left)

    cuisse_right = Polygon([
        (largeur_de_hanches/4 - largeur_de_cuisse/2, 0),
        (largeur_de_hanches/4 + largeur_de_cuisse/2, 0),
        (largeur_de_hanches/4 + largeur_de_cuisse/4, hauteur_des_hanches),
        (largeur_de_hanches/4 - largeur_de_cuisse/4, hauteur_des_hanches),
    ], closed=True, facecolor="#955251", edgecolor="black", alpha=0.9)
    ax.add_patch(cuisse_right)

    # Bras
    bras_gauche = Polygon([
        (-largeur_d_epaule/2 - longueur_du_bras, hauteur_des_epaules - longueur_du_bras),
        (-largeur_d_epaule/2 - longueur_du_bras + largeur_de_cuisse/4, hauteur_des_epaules - longueur_du_bras),
        (-largeur_d_epaule/2 + largeur_de_cuisse/6, hauteur_des_epaules),
        (-largeur_d_epaule/2, hauteur_des_epaules),
    ], closed=True, facecolor="#92A8D1", edgecolor="black", alpha=0.9)
    ax.add_patch(bras_gauche)

    bras_droit = Polygon([
        (largeur_d_epaule/2 + longueur_du_bras, hauteur_des_epaules - longueur_du_bras),
        (largeur_d_epaule/2 + longueur_du_bras - largeur_de_cuisse/4, hauteur_des_epaules - longueur_du_bras),
        (largeur_d_epaule/2 - largeur_de_cuisse/6, hauteur_des_epaules),
        (largeur_d_epaule/2, hauteur_des_epaules),
    ], closed=True, facecolor="#92A8D1", edgecolor="black", alpha=0.9)
    ax.add_patch(bras_droit)

    # Cou
    cou = Ellipse((0, hauteur_des_epaules + largeur_du_cou/2), largeur_du_cou * 1.3, largeur_du_cou * 1.6, facecolor="#6B5B95", edgecolor="black")
    ax.add_patch(cou)

    # Tête
    tete = Ellipse((0, hauteur_des_epaules + largeur_du_cou*2.5), largeur_du_cou * 2.2, largeur_du_cou * 3, facecolor="#FF6F61", edgecolor="black", alpha=0.9)
    ax.add_patch(tete)

    ax.set_xlim(-80, 80)
    ax.set_ylim(0, taille + 20)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

# =======================
# Fonctions d'aide visuelle
# =======================
def show_measure_details(measure_name, value):
    """Affiche le détail d'une mesure avec image dans un expander"""
    image_mapping = {
        "hauteur_d_entrejambe": "entrejambe.jpg",
        "hauteur_de_la_taille": "taille.jpg",
        "hauteur_de_poitrine": "poitrine.jpg",
        "hauteur_des_epaules": "epaules.jpg",
        "hauteur_des_genoux": "genoux.jpg",
        "hauteur_des_hanches": "hanches.jpg",
        "largeur_d_epaule": "largeur_epaule.jpg",
        "largeur_de_mamelon_a_mamelon": "mamelon.jpg",
        "largeur_des_epaules_a_l_horizontales": "epaules_horizontal.jpg",
        "longueur_d_avant_bras": "avant_bras.jpg",
        "longueur_de_la_colonne_vertebrale_jusqu_au_poignet": "colonne_vertebrale.jpg",
        "longueur_du_bras":"longueur_du_bras.jpg",
        "taille_de_poitrine":"taille_de_poitrine.jpg",
        "tour_de_cheville": "tour_de_cheville.jpg",
        "tour_de_cuisse": "tour_de_cuisse.jpg",
        "tour_de_hanches": "tour_de_hanches.jpg",
        "tour_de_poitrine": "tour_de_poitrine.jpg",
        "tour_de_sous_poitrine": "tour_de_sous_poitrine.jpg",
        "tour_de_taille": "tour_de_taille.jpg",
        "tour_du_cou": "tour_du_cou.jpg"
    }
    
    measure_descriptions = {
        "hauteur_de_la_taille": {
            "description": "Distance du sol jusqu'au tour de taille naturel.",
            "method": "Mesurer debout, pieds joints, depuis le sol jusqu'au point le plus fin du torse."
        },
        "hauteur_d_entrejambe": {
            "description": "Distance du sol à l'entrejambe.",
            "method": "Mesurer debout, pieds joints, depuis le sol jusqu'à l'entrejambe."
        },
        "hauteur_de_poitrine": {
            "description": "Distance du sol jusqu'à la pointe de la poitrine.",
            "method": "Mesurer debout, pieds joints, depuis le sol jusqu'à la pointe du sein (ou pectoraux)."
        },
        "hauteur_des_epaules": {
            "description": "Distance du sol jusqu'au sommet des épaules.",
            "method": "Mesurer debout, pieds joints, depuis le sol jusqu'au point le plus haut de l'épaule."
        },
        "hauteur_des_genoux": {
            "description": "Distance du sol jusqu'au centre de la rotule.",
            "method": "Mesurer debout, depuis le sol jusqu'au centre du genou."
        },
        "hauteur_des_hanches": {
            "description": "Distance du sol jusqu'à la partie la plus large des hanches.",
            "method": "Mesurer debout, pieds joints, depuis le sol jusqu'à la partie la plus large du bassin."
        },
        "largeur_d_epaule": {
            "description": "Largeur d'une épaule à l'autre.",
            "method": "Mesurer horizontalement d'une extrémité d'épaule à l'autre."
        },
        "largeur_de_mamelon_a_mamelon": {
            "description": "Distance entre les deux mamelons.",
            "method": "Mesurer horizontalement entre les pointes des seins."
        },
        "largeur_des_epaules_a_l_horizontales": {
            "description": "Largeur des épaules à l'horizontale.",
            "method": "Mesurer d'une épaule à l'autre, bras relâchés."
        },
        "longueur_d_avant_bras": {
            "description": "Longueur de l'avant-bras.",
            "method": "Mesurer du coude au poignet, bras plié à 90°."
        },
        "longueur_de_la_colonne_vertebrale_jusqu_au_poignet": {
            "description": "Longueur de la colonne vertébrale jusqu'au poignet.",
            "method": "Mesurer du bas du cou (vertèbre C7) jusqu'au poignet, bras le long du corps."
        },
        "longueur_du_bras": {
            "description": "Longueur totale du bras.",
            "method": "Mesurer de l'épaule au poignet, bras tendu le long du corps."
        },
        "taille_de_poitrine": {
            "description": "Tour de poitrine au niveau du mamelon.",
            "method": "Mesurer horizontalement autour de la poitrine, sur la pointe des seins."
        },
        "tour_de_cheville": {
            "description": "Tour de la cheville.",
            "method": "Mesurer autour de la partie la plus fine de la cheville."
        },
        "tour_de_cuisse": {
            "description": "Tour de la cuisse.",
            "method": "Mesurer autour de la partie la plus large de la cuisse."
        },
        "tour_de_hanches": {
            "description": "Tour de hanches.",
            "method": "Mesurer autour de la partie la plus large du bassin/fesses."
        },
        "tour_de_poitrine": {
            "description": "Tour de poitrine.",
            "method": "Mesurer horizontalement autour de la poitrine, sur la pointe des seins."
        },
        "tour_de_sous_poitrine": {
            "description": "Tour sous-poitrine.",
            "method": "Mesurer juste sous la poitrine, horizontalement."
        },
        "tour_de_taille": {
            "description": "Tour de taille.",
            "method": "Mesurer autour du point le plus fin du torse, généralement au-dessus du nombril."
        },
        "tour_du_cou": {
            "description": "Tour du cou.",
            "method": "Mesurer autour de la base du cou."
        }
    }
    
    with st.expander(f"📏 {measure_name.replace('_', ' ').title()} : {value:.1f} cm", expanded=False):
        col1, col2 = st.columns([1, 2])
        
        # Colonne image
        with col1:
            img_path = os.path.join(IMAGES_DIR, image_mapping.get(measure_name, "default.jpg"))
            try:
                st.image(img_path, use_container_width=True)
            except:
                st.warning("Image non disponible")
        
        # Colonne description
        with col2:
            desc = measure_descriptions.get(measure_name, {
                "description": "Description non disponible",
                "method": "Méthode de mesure non spécifiée"
            })
            st.markdown(f"""
            **Description**  
            {desc['description']}
            
            **Méthode de mesure**  
            {desc['method']}
            """)

def show_category_examples():
    """Affiche les exemples visuels pour les catégories"""
    st.subheader("📸 Exemples visuels des catégories")
    
    if sexe == "Homme":
        categories = {
            "Ventre": ["plat", "moyen", "rond"],
            "Torse": ["fin", "moyen", "large"],
            "Cuisses": ["fines", "moyennes", "larges"]
        }
    else:
        categories = {
            "Ventre": ["plat", "moyen", "rond"],
            "Bassin": ["etroit", "moyen", "large"]
        }
    
    for cat_name, types in categories.items():
        with st.expander(f"Catégorie {cat_name}"):
            cols = st.columns(len(types))
            for i, typ in enumerate(types):
                img_path = os.path.join(IMAGES_DIR, "categories", f"{cat_name.lower()}_{typ}.jpg")
                try:
                    img = Image.open(img_path)
                    cols[i].image(img, caption=f"{cat_name} {typ}", width=150)
                except:
                    cols[i].warning(f"Image non trouvée: {img_path}")

# =======================
# Interface Streamlit
# =======================
st.title("📏 Prédiction de Silhouette")

# 1. Sélection du sexe
sexe = st.radio("Sexe :", ["Homme", "Femme"])

# 2. Chargement des modèles
if sexe == "Homme":
    dossier_pipelines = "pipelines_all_dataset"
else:
    dossier_pipelines = "pipelines_female_complets"

models = load_all_models(dossier_pipelines)
target_names = get_target_names(dossier_pipelines)
wrapper = MultiTPOTWrapper(models)

# 3. Aide visuelle pour les catégories
show_category_examples()

# 4. Formulaire de saisie
with st.form("prediction_form"):
    st.header("🔢 Entrez vos informations")
    
    taille = st.number_input("Taille (cm)", 150, 210, 175)
    poids = st.number_input("Poids (kg)", 40, 200, 70)
    age = st.number_input("Âge", 15, 90, 30)
    
    if sexe == "Homme":
        categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
        categorie_torse = st.selectbox("Catégorie torse", ["Fin", "Moyen", "Large"])
        categorie_cuisses = st.selectbox("Catégorie cuisses", ["Fines", "Moyennes", "Larges"])
    else:
        categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
        categorie_bassin = st.selectbox("Catégorie bassin", ["Étroit", "Moyen", "Large"])
        taille_soutien_gorge = st.number_input("Taille soutien-gorge", 60, 120, 80)
        bonnet = st.selectbox("Bonnet", ["A", "B", "C", "D", "E"])

    submitted = st.form_submit_button("✨ Prédire la silhouette")

# 5. Affichage des résultats
if submitted:
    # Préparation des données
    if sexe == "Homme":
        input_data = {
            "taille": taille,
            "weight": poids,
            "age": age,
            "categorie_ventre": categorie_ventre.lower(),
            "categorie_torse": categorie_torse.lower(),
            "categorie_cuisses": categorie_cuisses.lower()
        }
    else:
        input_data = {
            "taille": taille,
            "weight": poids,
            "age": age,
            "categorie_ventre": categorie_ventre.lower(),
            "categorie_bassin": categorie_bassin.lower(),
            "taille_soutien_gorge": taille_soutien_gorge,
            "bonnet": bonnet
        }
    
    # Prédiction
    preds = wrapper.predict(pd.DataFrame([input_data]))
    predictions_dict = dict(zip(target_names, preds[0]))
    
    # Affichage des résultats
    st.header("📊 Résultats de prédiction")
    for measure_name, value in predictions_dict.items():
        show_measure_details(measure_name, value)
    
    # Visualisation de la silhouette
    st.header("🎨 Visualisation de votre silhouette")
    fig = draw_body_2d(
        taille=taille,
        hauteur_de_la_taille=predictions_dict.get("hauteur_de_la_taille", 110),
        hauteur_de_poitrine=predictions_dict.get("hauteur_de_poitrine", 135),
        hauteur_des_epaules=predictions_dict.get("hauteur_des_epaules", 150),
        hauteur_des_genoux=predictions_dict.get("hauteur_des_genoux", 50),
        hauteur_des_hanches=predictions_dict.get("hauteur_des_hanches", 95),
        largeur_d_epaule=predictions_dict.get("largeur_d_epaule", 40),
        longueur_d_avant_bras=predictions_dict.get("longueur_d_avant_bras", 28),
        longueur_du_bras=predictions_dict.get("longueur_du_bras", 65),
        largeur_de_cuisse=predictions_dict.get("largeur_de_cuisse", 20),
        largeur_de_hanches=predictions_dict.get("largeur_de_hanches", 40),
        largeur_de_poitrine=predictions_dict.get("largeur_de_poitrine", 38),
        largeur_de_la_taille=predictions_dict.get("largeur_de_la_taille", 30),
        largeur_du_cou=predictions_dict.get("largeur_du_cou", 12),
    )
    st.pyplot(fig)

# Pied de page
st.markdown("---")
st.markdown("ℹ️ Développé avec Streamlit par BiBa Bop - © 2025")