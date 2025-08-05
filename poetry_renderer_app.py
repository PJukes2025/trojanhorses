
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configure the app
st.set_page_config(page_title="Poetry Renderer", layout="centered")

st.title("🖋️ Poetry Renderer - Greco-Roman Style")

# Text input
title = st.text_input("Poem Title", "Invocation")
poem_text = st.text_area("Paste your poem here (use hard returns for line breaks)", height=300)

# Load fonts from the static directory
FONT_PATH = "static/EBGaramond-Regular.ttf"
TITLE_FONT_PATH = "static/Cinzel-Regular.ttf"

try:
    body_font = ImageFont.truetype(FONT_PATH, 36)
    title_font = ImageFont.truetype(TITLE_FONT_PATH, 48)
except:
    st.error("Make sure EBGaramond-Regular.ttf and Cinzel-Regular.ttf are in the 'static' folder.")
    st.stop()

# Render button
if st.button("Render Poem as PNG"):
    # Create image
    width, height = 1200, 1800
    image = Image.new("RGB", (width, height), color=(253, 250, 243))  # faded paper
    draw = ImageDraw.Draw(image)

    y = 100
    draw.text((width // 2, y), title.upper(), font=title_font, anchor="mm", fill=(0, 0, 0))
    y += 100

    lines = poem_text.strip().split("\n")
    for line in lines:
        wrapped = textwrap.wrap(line, width=60)
        for wline in wrapped:
            draw.text((100, y), wline, font=body_font, fill=(0, 0, 0))
            y += 50
        y += 10

    # Save and show
    output_path = "rendered_poem.png"
    image.save(output_path)
    st.image(image, caption="Rendered Poem")
    with open(output_path, "rb") as file:
        st.download_button(label="Download PNG", data=file, file_name="poem.png", mime="image/png")
