# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from wrapper import MultiTPOTWrapper

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
# Interface Streamlit
# =======================
st.title("Silhouette predictor (MVP)")

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

# 📋 Formulaire
taille = st.number_input("Taille (cm)", 150.0, 210.0, 175.0, step=0.5)
weight = st.number_input("Poids (kg)", 40.0, 200.0, 80.0, step=0.5)
age = st.number_input("Âge", 15, 90, 35, step=1)

if sexe == "Homme":
    categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
    categorie_torse = st.selectbox("Catégorie torse", ["Fin", "Moyen", "Large"])
    categorie_cuisses = st.selectbox("Catégorie cuisses", ["Fines", "Moyennes", "Larges"])

    input_data = pd.DataFrame([{
        "taille": taille,
        "age": age,
        "weight": weight,
        "categorie_ventre": categorie_ventre.lower(),
        "categorie_torse": categorie_torse.lower(),
        "categorie_cuisses": categorie_cuisses.lower()
    }])

else:  # Femme
    categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
    categorie_bassin = st.selectbox("Catégorie bassin", ["Etroit", "Moyen", "Large"])
    taille_soutien_gorge = st.number_input("Taille soutien-gorge", min_value=60, max_value=120, step=1)
    bonnet_rang = st.number_input("Rang du bonnet", min_value=0, max_value=11, step=1)

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
if st.button("Prédire"):
    preds = wrapper.predict(input_data)
    predictions_dict = dict(zip(target_names, preds[0]))

    st.subheader("📊 Prédictions détaillées")
    for k, v in predictions_dict.items():
        st.write(f"**{k}** : {v:.2f}")

    # 🖼️ Dessin silhouette
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
