# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from wrapper import MultiTPOTWrapper
from PIL import Image
from streamlit.components.v1 import html

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
def show_measure_help(measure_name):
    """Affiche l'image d'aide pour une mesure spécifique"""
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

    modal_script = f"""
    <script>
    // Créer la modale
    var modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '1000';
    
    // Contenu de la modale
    modal.innerHTML = `
        <div style="background: white; padding: 20px; border-radius: 10px; max-width: 80%; max-height: 80%; overflow: auto;">
            <img src="{img_path}" style="max-width: 100%; height: auto;" />
            <button onclick="this.parentElement.parentElement.remove()" style="display: block; margin: 10px auto;">Fermer</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    </script>
    """
    
    html(modal_script)
    
    default_img = "default.jpg"
    img_path = os.path.join(IMAGES_DIR, image_mapping.get(measure_name, default_img))
    
    try:
        img = Image.open(img_path)
        st.image(img, caption=f"Mesure: {measure_name}", use_column_width=True)
    except:
        st.warning(f"Image d'aide non trouvée pour {measure_name}")

def show_category_examples():
    """Affiche les exemples visuels pour les catégories"""
    st.subheader("📸 Exemples visuels des catégories")
    
    if sexe == "Homme":
        cols = st.columns(3)
        categories = {
            "Ventre": ["plat", "moyen", "rond"],
            "Torse": ["fin", "moyen", "large"],
            "Cuisses": ["fines", "moyennes", "larges"]
        }
        
        for cat_name, types in categories.items():
            with st.expander(f"Catégorie {cat_name}"):
                cols = st.columns(len(types))
                for i, typ in enumerate(types):
                    img_path = os.path.join(IMAGES_DIR, f"{cat_name.lower()}_{typ}.jpg")
                    try:
                        img = Image.open(img_path)
                        cols[i].image(img, caption=f"{cat_name} {typ}", width=150)
                    except:
                        cols[i].warning(f"Image non trouvée: {img_path}")



    else:
        cols = st.columns(3)
        categories = {
            "Ventre": ["plat", "moyen", "rond"],
            "Bassin": ["etroit", "moyen", "large"],
        }
        
        for cat_name, types in categories.items():
            with st.expander(f"Catégorie {cat_name}"):
                cols = st.columns(len(types))
                for i, typ in enumerate(types):
                    img_path = os.path.join(IMAGES_DIR, f"{cat_name.lower()}_{typ}.jpg")
                    try:
                        img = Image.open(img_path)
                        cols[i].image(img, caption=f"{cat_name} {typ}", width=150)
                    except:
                        cols[i].warning(f"Image non trouvée: {img_path}")

# =======================
# Interface Streamlit
# =======================
st.title("📏 Silhouette predictor (MVP)")

# 🎯 Sexe
sexe = st.radio("Sexe :", ["Homme", "Femme"])

# 📂 Choix du dossier modèles
if sexe == "Homme":
    dossier_pipelines = "pipelines_all_dataset"
else:
    dossier_pipelines = "pipelines_female_complets"

# 📦 Chargement
models = load_all_models(dossier_pipelines)
target_names = get_target_names(dossier_pipelines)
wrapper = MultiTPOTWrapper(models)

# ℹ️ Aide visuelle pour les catégories
show_category_examples()

# 📋 Formulaire
st.header("🔢 Entrez vos informations")

taille = st.number_input("Taille (cm)", 150.0, 210.0, 175.0, step=0.5)
weight = st.number_input("Poids (kg)", 40.0, 200.0, 80.0, step=0.5)
age = st.number_input("Âge", 15, 90, 35, step=1)

if sexe == "Homme":
    categorie_ventre = st.selectbox(
        "Catégorie ventre [?]", 
        ["Plat", "Moyen", "Rond"],
        help="Voir les exemples visuels ci-dessus"
    )
    categorie_torse = st.selectbox(
        "Catégorie torse [?]", 
        ["Fin", "Moyen", "Large"],
        help="Voir les exemples visuels ci-dessus"
    )
    categorie_cuisses = st.selectbox(
        "Catégorie cuisses [?]", 
        ["Fines", "Moyennes", "Larges"],
        help="Voir les exemples visuels ci-dessus"
    )

    input_data = pd.DataFrame([{
        "taille": taille,
        "age": age,
        "weight": weight,
        "categorie_ventre": categorie_ventre.lower(),
        "categorie_torse": categorie_torse.lower(),
        "categorie_cuisses": categorie_cuisses.lower()
    }])

else:  # Femme
    categorie_ventre = st.selectbox(
        "Catégorie ventre [?]", 
        ["Plat", "Moyen", "Rond"],
        help="Voir les exemples visuels ci-dessus"
    )
    categorie_bassin = st.selectbox(
        "Catégorie bassin [?]", 
        ["Etroit", "Moyen", "Large"],
        help="Voir les exemples visuels ci-dessus"
    )
    taille_soutien_gorge = st.number_input(
        "Taille soutien-gorge [?]", 
        min_value=60, max_value=125, step=1,
        help="Tour de poitrine en cm"
    )
    bonnet_rang = st.number_input(
        "Rang du bonnet [?]", 
        min_value=0, max_value=11, step=1,
        help="0 = A, 1 = B, ..., 11 = L"
    )

    input_data = pd.DataFrame([{
        "taille": taille,
        "age": age,
        "weight": weight,
        "categorie_ventre": categorie_ventre.lower(),
        "categorie_bassin": categorie_bassin.lower(),
        "taille_soutien_gorge": taille_soutien_gorge,
        "bonnet_rang": bonnet_rang
    }])

# 🎯 Bouton prédiction
if st.button("✨ Prédire la silhouette"):
    preds = wrapper.predict(input_data)
    predictions_dict = dict(zip(target_names, preds[0]))

    st.header("📊 Résultats de prédiction")
    
    # Affichage des mesures avec aide
    for measure_name, value in predictions_dict.items():
        cols = st.columns([0.8, 0.2])
        with cols[0]:
            st.metric(label=measure_name.replace("_", " ").title(), value=f"{value:.1f} cm")
        with cols[1]:
            if st.button("❓", key=f"help_{measure_name}"):
                show_measure_help(measure_name)

    # 🖼️ Dessin silhouette
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
st.markdown("ℹ️ Cliquez sur les icônes ❓ pour voir des explications visuelles des mesures")