# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
import os
from wrapper import MultiTPOTWrapper

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

st.title("Silhouette predictor (MVP)")

# 🎯 Sélection du sexe
sexe = st.radio("Sexe :", ["Homme", "Femme"])

# 📂 Choix du dossier modèles
if sexe == "Homme":
    dossier_pipelines = "pipelines_all_dataset"
else:
    dossier_pipelines = "pipelines_female_complets"

# 📦 Chargement des modèles et noms de cibles
models = load_all_models(dossier_pipelines)
target_names = get_target_names(dossier_pipelines)
wrapper = MultiTPOTWrapper(models)

# 📋 Formulaire utilisateur
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

# 🎯 Bouton de prédiction
if st.button("Prédire"):
    preds = wrapper.predict(input_data)
    predictions_dict = dict(zip(target_names, preds[0]))

    st.subheader("📊 Prédictions détaillées")
    for k, v in predictions_dict.items():
        st.write(f"**{k}** : {v:.2f}")
