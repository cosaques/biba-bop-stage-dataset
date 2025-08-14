# streamlit_app_smplx.py
import streamlit as st
import joblib
import pandas as pd
import os
import torch
import plotly.graph_objects as go
import smplx
from wrapper import MultiTPOTWrapper

# ------------- Fonctions utilitaires ----------------
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

@st.cache_resource
def load_smplx_model(model_path, gender='male', num_betas=26):
    model = smplx.create(model_path, model_type='smplx', gender=gender,
                          num_pca_comps=12, ext='npz', use_face_contour=True,
                          num_betas=num_betas)
    return model

def plot_smplx(vertices):
    # vertices: (N,3)
    x, y, z = vertices[:,0], vertices[:,1], vertices[:,2]
    fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z,
                                    color='lightpink', opacity=0.5)])
    fig.update_layout(width=600, height=600)
    return fig

# ---------------- Streamlit UI ---------------------
st.title("SMPL-X Human Body Predictor")

# 🎯 Sexe
sexe = st.radio("Sexe :", ["Homme", "Femme"])

# 📂 Choix du dossier modèles
if sexe == "Homme":
    dossier_pipelines = "pipelines_all_dataset"
else:
    dossier_pipelines = "pipelines_female_complets"

# 📦 Chargement des modèles TPOT
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
else:
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

# ------------- Prédiction ------------------
if st.button("Prédire"):
    preds = wrapper.predict(input_data)
    predictions_dict = dict(zip(target_names, preds[0]))
    
    st.subheader("📊 Prédictions SMPL-X")
    st.write(predictions_dict)

    # Convertir en tenseur torch
    predicted_betas = torch.tensor(preds[0], dtype=torch.float32)
    
    # Charger modèle SMPL-X
    smplx_model_path =r"C:\Users\mbouke.besse\OneDrive - ESTIA\Documents\code-smplx\smplx\smplx\models"  # dossier contenant smplx npz
    smpl_model = load_smplx_model(smplx_model_path, gender='male' if sexe=='Homme' else 'female',
                                  num_betas=10)

    # Ajuster la taille des betas
    if predicted_betas.numel() < smpl_model.num_betas:
        pad = torch.zeros(smpl_model.num_betas - predicted_betas.numel())
        betas = torch.cat([predicted_betas, pad]).unsqueeze(0)
    else:
        betas = predicted_betas[:smpl_model.num_betas].unsqueeze(0)
        
    
    # Générer vertices
    with torch.no_grad():
        output = smpl_model(betas=betas)
        vertices = output.vertices[0].cpu().numpy()

    # Affichage
    fig = plot_smplx(vertices)
    st.plotly_chart(fig)



