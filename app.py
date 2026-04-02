import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
import os

st.set_page_config(page_title="AI Asset Creator", layout="centered")
st.title("🧱 AI Asset Creator (Diffusers)")
st.write("Generate images from text prompts. Runs locally or on Streamlit Cloud.")

OUTPUT_DIR = "generated_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load Stable Diffusion model
device = "cuda" if torch.cuda.is_available() else "cpu"
st.info("Loading Stable Diffusion model... please wait.")
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to(device)
st.success("Model loaded successfully!")

def generate_image(prompt: str):
    image = pipe(prompt).images[0]
    filename = os.path.join(OUTPUT_DIR, f"{prompt.replace(' ', '_')}.png")
    image.save(filename)
    return filename

# Text-to-Image section
st.header("📝 Text to Image")
prompt = st.text_input("Enter a description (e.g., 'Minecraft-style grass block')")
if st.button("Generate Image"):
    if prompt.strip() == "":
        st.warning("Please enter a description first.")
    else:
        st.info("Generating image... please wait.")
        filename = generate_image(prompt)
        st.success("Image generated successfully!")
        st.image(filename, caption="Generated Asset")
        with open(filename, "rb") as f:
            st.download_button("Download Image (.png)", f, file_name=os.path.basename(filename))

st.write("---")
st.write("Built with Hugging Face Diffusers. Works on Streamlit Cloud (CPU).")
