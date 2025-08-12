import streamlit as st
from wrapper import MultiTPOTWrapper
import joblib
import numpy as np
import pandas as pd

# =========================
# 1. Fonction pour charger le modèle
# =========================
def load_model(gender):
    if gender == "Homme":
        return joblib.load("full_pipeline_2.pkl")
    else:
        return joblib.load("full_pipeline_female.pkl")

# =========================
# 2. Interface Streamlit
# =========================
st.title("📏 Prédiction des mesures corporelles")

# Choix du genre
gender = st.selectbox("Sélectionnez votre genre :", ["Homme", "Femme"])

# Champs communs
st.subheader("Informations générales")
taille = st.number_input("Taille (cm)", min_value=100, max_value=250, step=1)
age = st.number_input("Âge", min_value=10, max_value=120, step=1)
weight = st.number_input("Poids (kg)", min_value=30, max_value=250, step=1)

# Champs spécifiques selon le genre
if gender == "Homme":
    categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
    categorie_torse = st.selectbox("Catégorie torse", ["Fin", "Moyen", "Large"])
    categorie_cuisses = st.selectbox("Catégorie cuisses", ["Fines", "Moyennes", "Larges"])
    # Encodage simple des catégories (à adapter à ton preprocessing)
    features = [taille, age, weight,
                ["Plat", "Moyen", "Rond"].index(categorie_ventre),
                ["Fin", "Moyen", "Large"].index(categorie_torse),
                ["Fines", "Moyennes", "Larges"].index(categorie_cuisses)]
else:
    categorie_ventre = st.selectbox("Catégorie ventre", ["Plat", "Moyen", "Rond"])
    categorie_bassin = st.selectbox("Catégorie bassin", ["Etroit", "Moyen", "Large"])
    taille_soutien_gorge = st.number_input("Taille soutien-gorge", min_value=60, max_value=120, step=1)
    bonnet_rang = st.number_input("Rang du bonnet", min_value=0, max_value=11, step=1)  # Directement entier
    # Encodage simple des catégories (à adapter à ton preprocessing)
    features = [taille, age, weight,
                ["Plat", "Moyen", "Rond"].index(categorie_ventre),
                ["Etroit", "Moyen", "Large"].index(categorie_bassin),
                taille_soutien_gorge,
                bonnet_rang]
    
# Préparation des features
if gender == "Homme":
    features = [taille, age, weight, categorie_ventre, categorie_torse, categorie_cuisses]
    columns = ["taille", "age", "weight", "categorie_ventre", "categorie_torse", "categorie_cuisses"]
else:
    features = [taille, age, weight, categorie_ventre, categorie_bassin, taille_soutien_gorge, bonnet_rang]
    columns = ["taille", "age", "weight", "categorie_ventre", "categorie_bassin", "taille_soutien_gorge", "bonnet_rang"]

# =========================
# 3. Prédiction
# =========================
if st.button("Prédire les mesures"):
    model = load_model(gender)

    # Conversion en DataFrame pour correspondre au format attendu par le pipeline
    input_df = pd.DataFrame([features], columns=columns)

    # Prédiction
    prediction = model.predict(input_df)[0]  # [0] si sortie en 2D

    # Récupération des noms de mesures si dispo
    if hasattr(model, "feature_names_out_"):
        mesures_names = model.feature_names_out_
    else:
        mesures_names = [f"Mesure {i+1}" for i in range(len(prediction))]

    # Affichage des résultats
    result_df = pd.DataFrame({
        "Mesure": mesures_names,
        "Valeur prédite (cm)": prediction
    })
    