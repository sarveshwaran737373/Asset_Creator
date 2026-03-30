import streamlit as st
import torch
import os
from shap_e.diffusion.sample import sample_latents
from shap_e.models.download import load_model
from shap_e.util.notebooks import decode_latent_mesh

st.set_page_config(page_title="Private 3D Asset Creator", layout="centered")
st.title("🧱 Unlimited Private 3D Asset Creator")
st.write("""
This app lets you generate 3D models from text prompts (and soon from images).
Everything runs locally, so it's unlimited use and only for you.
""")

OUTPUT_DIR = "generated_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

st.info("Loading Shap-E model... this may take a moment.")
model = load_model("shap-e")
st.success("Model loaded successfully!")

def generate_mesh_from_text(prompt: str, guidance_scale: float = 15.0):
    try:
        latents = sample_latents(
            batch_size=1,
            model=model,
            guidance_scale=guidance_scale,
            prompt=prompt,
            device=device,
        )
        mesh = decode_latent_mesh(latents[0], model)
        filename = os.path.join(OUTPUT_DIR, f"{prompt.replace(' ', '_')}.obj")
        mesh.save(filename)
        return filename
    except Exception as e:
        st.error(f"Error generating mesh: {e}")
        return None

def save_uploaded_file(uploaded_file):
    filepath = os.path.join(OUTPUT_DIR, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath

st.header("📝 Text to 3D Model")
prompt = st.text_input("Enter a description (e.g., 'Minecraft-style grass block')")
guidance_scale = st.slider("Guidance Scale (controls creativity)", 5.0, 20.0, 15.0)

if st.button("Generate from Text"):
    if prompt.strip() == "":
        st.warning("Please enter a description first.")
    else:
        st.info("Generating model... please wait.")
        filename = generate_mesh_from_text(prompt, guidance_scale)
        if filename:
            st.success("Model generated successfully!")
            with open(filename, "rb") as f:
                st.download_button("Download 3D Model (.obj)", f, file_name=os.path.basename(filename))

st.header("🖼️ Image to 3D Model")
uploaded_image = st.file_uploader("Upload an image (e.g., photo of a chair)", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    filepath = save_uploaded_file(uploaded_image)
    st.info(f"Image saved: {filepath}")
    st.warning("Image-to-3D pipeline not yet implemented. Will integrate TripoSR/Meshroom here.")

st.header("🔮 Coming Soon")
st.write("""
- Image-to-3D conversion using TripoSR or Meshroom.
- Voxelization to convert smooth meshes into Minecraft-style block assets.
- Preview window to view generated models directly in the browser.
- Style presets (realistic, voxel, low-poly, anime).
""")

st.write("---")
st.write("Built by Sarvesh's private AI. Runs locally, unlimited use, no external APIs.")
