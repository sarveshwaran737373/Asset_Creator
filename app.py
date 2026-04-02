import streamlit as st
from tripoSR import TripoSR
import os

st.set_page_config(page_title="Private 3D Asset Creator", layout="centered")
st.title("🧱 Unlimited Private 3D Asset Creator (TripoSR)")
st.write("Generate 3D models from text prompts or images. Runs locally or on Streamlit Cloud.")

OUTPUT_DIR = "generated_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize TripoSR model
model = TripoSR()

def generate_from_text(prompt: str):
    mesh = model.text_to_3d(prompt)
    filename = os.path.join(OUTPUT_DIR, f"{prompt.replace(' ', '_')}.obj")
    mesh.export(filename)
    return filename

def generate_from_image(image_file):
    mesh = model.image_to_3d(image_file)
    filename = os.path.join(OUTPUT_DIR, f"{image_file.name}.obj")
    mesh.export(filename)
    return filename

# Text-to-3D section
st.header("📝 Text to 3D Model")
prompt = st.text_input("Enter a description (e.g., 'Minecraft-style grass block')")
if st.button("Generate from Text"):
    if prompt.strip() == "":
        st.warning("Please enter a description first.")
    else:
        st.info("Generating model... please wait.")
        filename = generate_from_text(prompt)
        st.success("Model generated successfully!")
        with open(filename, "rb") as f:
            st.download_button("Download 3D Model (.obj)", f, file_name=os.path.basename(filename))

# Image-to-3D section
st.header("🖼️ Image to 3D Model")
uploaded_image = st.file_uploader("Upload an image (e.g., photo of a chair)", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    st.info("Generating model from image... please wait.")
    filename = generate_from_image(uploaded_image)
    st.success("Model generated successfully!")
    with open(filename, "rb") as f:
        st.download_button("Download 3D Model (.obj)", f, file_name=os.path.basename(filename))

st.write("---")
st.write("Built with TripoSR. Runs locally or on Streamlit Cloud.")
