# streamlit_app_continuous.py
import streamlit as st
import joblib
import pandas as pd
import os
import torch
from smplx import SMPLX
from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    look_at_view_transform, FoVOrthographicCameras,
    PointLights, RasterizationSettings,
    MeshRenderer, MeshRasterizer, SoftPhongShader
)
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

st.title("Silhouette predictor (MVP) - Continuous betas")

# 🎯 Sélection du sexe
sexe = st.radio("Sexe :", ["Homme", "Femme"])

# 📂 Choix du dossier modèles
dossier_pipelines = "pipelines_all_dataset" if sexe=="Homme" else "pipelines_female_complets"

# 📦 Chargement des modèles et noms de cibles
models = load_all_models(dossier_pipelines)
target_names = get_target_names(dossier_pipelines)
wrapper = MultiTPOTWrapper(models)

# 📋 Formulaire utilisateur
taille = st.number_input("Taille (cm)", 150.0, 210.0, 175.0, step=0.5)
weight = st.number_input("Poids (kg)", 40.0, 200.0, 80.0, step=0.5)
age = st.number_input("Âge", 15, 90, 35, step=1)

# Mesures spécifiques
if sexe=="Homme":
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

# 🎯 Bouton de prédiction
if st.button("Prédire"):
    preds = wrapper.predict(input_data)
    predictions_dict = dict(zip(target_names, preds[0]))

    st.subheader("📊 Prédictions détaillées")
    for k, v in predictions_dict.items():
        st.write(f"**{k}** : {v:.2f}")

    # 🔹 Générer betas SMPLX directement à partir des mesures
    def compute_betas(preds):
        """
        Extrapole 10 coefficients SMPLX à partir des mesures clés.
        Ici, on fait un mapping linéaire simple, mais tu peux
        améliorer avec un réseau ou une fonction plus complexe.
        """
        betas = torch.zeros([1, 10])
        # Exemple simple
        taille = preds.get("taille", 175)
        tour_taille = preds.get("tour_taille", 80)
        tour_hanches = preds.get("tour_hanches", 95)
        tour_poitrine = preds.get("tour_poitrine", 100)

        # Les trois premiers betas contrôlent principalement la largeur du corps
        betas[0,0] = (tour_poitrine - 100)/50  # poitrine
        betas[0,1] = (tour_taille - 80)/50     # taille
        betas[0,2] = (tour_hanches - 95)/50    # hanches
        # Autres betas peuvent dépendre de proportions verticales
        betas[0,3] = (taille - 175)/50
        return betas

    betas = compute_betas(predictions_dict)

    # 🔹 Générer et afficher SMPLX
    device = torch.device("cpu")
    smplx_model = SMPLX(model_path=r"C:\Users\mbouke.besse\OneDrive - ESTIA\Documents\code-smplx\smplx\smplx\models\smplx", gender="male" if sexe=="Homme" else "female", 
                        use_pca=False).to(device)
    output = smplx_model(betas=betas)
    vertices = output.vertices[0]

    # PyTorch3D renderer (vue de face)
    R, T = look_at_view_transform(dist=2.5, elev=0, azim=0)
    cameras = FoVOrthographicCameras(device=device, R=R, T=T)
    lights = PointLights(device=device, location=[[0.0, 2.0, 2.0]])
    raster_settings = RasterizationSettings(image_size=512)
    renderer = MeshRenderer(
        rasterizer=MeshRasterizer(cameras=cameras, raster_settings=raster_settings),
        shader=SoftPhongShader(device=device, cameras=cameras, lights=lights)
    )

    mesh = Meshes(verts=[vertices], faces=[smplx_model.faces.astype(int)])
    image = renderer(mesh)[0, ..., :3].cpu().numpy()

    st.image(image, caption="Modèle SMPLX estimé (face)")
