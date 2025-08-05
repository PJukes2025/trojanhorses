import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Page setup
st.set_page_config(page_title="Poetry Renderer", layout="centered")
st.title("🖋️ Poetry Renderer – IM Fell + Cinzel")

# Inputs
title = st.text_input("Poem Title", "Invocation")
poem_text = st.text_area("Paste your poem here (use hard returns for line breaks)", height=300)

# File paths
FONT_PATH = "static/IMFellEnglish-Regular.ttf"
TITLE_FONT_PATH = "static/Cinzel-Regular.ttf"
BACKGROUND_PATH = "static/faded_paper.png"

# Load fonts and background
try:
    body_font = ImageFont.truetype(FONT_PATH, 36)
    title_font = ImageFont.truetype(TITLE_FONT_PATH, 48)
    background = Image.open(BACKGROUND_PATH).convert("RGB")
except Exception as e:
    st.error(f"⚠️ Could not load font or background: {e}")
    st.stop()

# Render button logic
if st.button("Render Poem as PNG"):
    try:
        width, height = background.size
        image = background.copy()
        draw = ImageDraw.Draw(image)

        # Draw title
        y = 100
        draw.text((width // 2, y), title.upper(), font=title_font, anchor="mm", fill=(0, 0, 0))
        y += 100

        # Draw poem
        lines = poem_text.strip().split("\n")
        for line in lines:
            wrapped = textwrap.wrap(line, width=60)
            for wline in wrapped:
                draw.text((100, y), wline, font=body_font, fill=(0, 0, 0))
                y += 50
            y += 10

        # Output
        output_path = "rendered_poem.png"
        image.save(output_path)
        st.image(image, caption="Rendered Poem")
        with open(output_path, "rb") as file:
            st.download_button(label="Download PNG", data=file, file_name="poem.png", mime="image/png")

    except Exception as e:
        st.error(f"❌ Rendering failed: {e}")
