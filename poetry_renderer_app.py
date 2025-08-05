import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Page setup
st.set_page_config(page_title="Poetry Renderer", layout="centered")
st.title("🖋️ Poetry Renderer – Cormorant Garamond + Cinzel")

# Inputs
title = st.text_input("Poem Title", "Invocation")
poem_text = st.text_area("Paste your poem here (use hard returns for line breaks)", height=300)

# File paths
BODY_FONT_PATH = "static/CormorantGaramond-Regular.ttf"
ITALIC_FONT_PATH = "static/CormorantGaramond-Italic.ttf"
TITLE_FONT_PATH = "static/Cinzel-Regular.ttf"
BACKGROUND_PATH = "static/faded_paper.png"

# Load fonts and background
try:
    body_font = ImageFont.truetype(BODY_FONT_PATH, 36)
    italic_font = ImageFont.truetype(ITALIC_FONT_PATH, 36)
    title_font = ImageFont.truetype(TITLE_FONT_PATH, 48)
    background = Image.open(BACKGROUND_PATH).convert("RGB")
except Exception as e:
    st.error(f"⚠️ Could not load fonts or background: {e}")
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

        # Draw poem (italic if line starts and ends with underscores)
        lines = poem_text.strip().split("\n")
        for line in lines:
            is_italic = line.strip().startswith("_") and line.strip().endswith("_")
            font_to_use = italic_font if is_italic else body_font
            clean_line = line.strip("_").strip()

            wrapped = textwrap.wrap(clean_line, width=60)
            for wline in wrapped:
                draw.text((100, y), wline, font=font_to_use, fill=(0, 0, 0))
                y += 50
            y += 10

        # Save and display
        output_path = "rendered_poem.png"
        image.save(output_path)
        st.image(image, caption="Rendered Poem")
        with open(output_path, "rb") as file:
            st.download_button(label="Download PNG", data=file, file_name="poem.png", mime="image/png")

    except Exception as e:
        st.error(f"❌ Rendering failed: {e}")
