import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import re
import os

# Page config
st.set_page_config(page_title="Poetry Renderer", layout="centered")
st.title("🖋️ Poetry Renderer – Markdown Poetry Book")

# User input
poem_text = st.text_area("Paste your Markdown-formatted poem here", height=400)

# Paths
FONT_REGULAR = "static/CormorantGaramond-Regular.ttf"
FONT_ITALIC = "static/CormorantGaramond-Italic.ttf"
FONT_TITLE = "static/Cinzel-Regular.ttf"
BACKGROUND = "static/faded_paper.png"

# Settings
FONT_SIZE = 36
LINE_HEIGHT = 52
PAGE_WIDTH, PAGE_HEIGHT = 1200, 1800
LEFT_MARGIN = 100
TOP_MARGIN = 150
BOTTOM_MARGIN = 150

# Load fonts and background
try:
    font_regular = ImageFont.truetype(FONT_REGULAR, FONT_SIZE)
    font_italic = ImageFont.truetype(FONT_ITALIC, FONT_SIZE)
    font_title = ImageFont.truetype(FONT_TITLE, 60)
    font_chapter = ImageFont.truetype(FONT_TITLE, 48)
    font_subheading = ImageFont.truetype(FONT_TITLE, 40)
    background = Image.open(BACKGROUND).resize((PAGE_WIDTH, PAGE_HEIGHT)).convert("RGB")
except Exception as e:
    st.error(f"Error loading fonts or background: {e}")
    st.stop()

# Helpers
def parse_markdown_line(line):
    if line.startswith("# "):
        return ("title", line[2:].strip())
    elif line.startswith("## "):
        return ("chapter", line[3:].strip())
    elif line.startswith("### "):
        return ("subheading", line[4:].strip())
    else:
        return ("text", line)

def draw_markdown_line(draw, x, y, text, font, max_width):
    segments = re.split(r"(_[^_]+_)", text)
    cursor = x
    for seg in segments:
        if seg.startswith("_") and seg.endswith("_"):
            seg_text = seg.strip("_")
            w, _ = draw.textsize(seg_text, font=font_italic)
            draw.text((cursor, y), seg_text, font=font_italic, fill=(0, 0, 0))
        else:
            w, _ = draw.textsize(seg, font=font_regular)
            draw.text((cursor, y), seg, font=font_regular, fill=(0, 0, 0))
        cursor += w
    return y + LINE_HEIGHT

def render_pages(lines):
    pages = []
    current_image = background.copy()
    draw = ImageDraw.Draw(current_image)
    y = TOP_MARGIN
    page_number = 1

    for idx, (line_type, content) in enumerate(lines):
        # Calculate height needed
        if line_type == "title":
            height_needed = 80
        elif line_type == "chapter":
            height_needed = 65
        elif line_type == "subheading":
            height_needed = 55
        else:
            height_needed = LINE_HEIGHT

        # Page break if needed
        if y + height_needed > PAGE_HEIGHT - BOTTOM_MARGIN:
            draw_page_number(draw, page_number)
            pages.append(current_image)
            current_image = background.copy()
            draw = ImageDraw.Draw(current_image)
            y = TOP_MARGIN
            page_number += 1

        # Render line
        if line_type == "title":
            draw.text((PAGE_WIDTH // 2, y), content.upper(), font=font_title, anchor="mm", fill=(0, 0, 0))
            y += 80
        elif line_type == "chapter":
            draw.text((LEFT_MARGIN, y), content, font=font_chapter, fill=(0, 0, 0))
            y += 65
        elif line_type == "subheading":
            draw.text((LEFT_MARGIN, y), content, font=font_subheading, fill=(0, 0, 0))
            y += 55
        elif content.strip() == "":
            y += LINE_HEIGHT // 2
        else:
            wrapped_lines = textwrap.wrap(content, width=60)
            for wrapped_line in wrapped_lines:
                y = draw_markdown_line(draw, LEFT_MARGIN, y, wrapped_line, font_regular, PAGE_WIDTH - LEFT_MARGIN * 2)
            y += 10

    draw_page_number(draw, page_number)
    pages.append(current_image)
    return pages

def draw_page_number(draw, page_number):
    footer_font = ImageFont.truetype(FONT_REGULAR, 24)
    draw.text((PAGE_WIDTH // 2, PAGE_HEIGHT - 80), f"Page {page_number}", font=footer_font, anchor="mm", fill=(0, 0, 0))

# Render
if st.button("Render Poem as PNG Pages"):
    lines = [parse_markdown_line(line) for line in poem_text.strip().splitlines()]
    pages = render_pages(lines)

    for idx, img in enumerate(pages, start=1):
        st.image(img, caption=f"Page {idx}")
        output_path = f"rendered_poem_page_{idx}.png"
        img.save(output_path)
        with open(output_path, "rb") as file:
            st.download_button(
                label=f"Download Page {idx}",
                data=file,
                file_name=output_path,
                mime="image/png"
            )
