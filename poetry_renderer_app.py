import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configure the app
st.set_page_config(page_title="Poetry Renderer", layout="centered")
st.title("🖋️ Poetry Renderer – IM Fell + Cinzel")

# Text input
title = st.text_input("Poem Title", "Invocation")
poem_text = st.text_area("Paste your poem here (use hard returns for line breaks)", height=300)

# Font and background paths
FONT_PATH = "static/IMFellEnglish-Regular.ttf"
TITLE_FONT_PATH = "static/Cinzel-Regular.ttf"
BACKGROUND_PATH = "static/faded_paper.png"

# Load fonts and background
try:
    body_font = ImageFont.truetype(FONT_PATH, 36)
    title_font = ImageFont.truetype(TITLE_FONT_PATH, 48)
    background = Image.open(BACKGROUND_PATH).convert("RGB")
except Exception as e:
    st.error(f"Missing file: {e}")
    st.stop()

# Render button
if st.button("Render Poem as PNG"):
    width, height = background.size
    image = background.co

