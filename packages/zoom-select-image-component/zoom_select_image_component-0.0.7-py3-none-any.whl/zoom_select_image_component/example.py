from os import path
import streamlit as st

from PIL import Image

from zoom_select_image_component import zoom_select_image_component

st.subheader("Image select")

@st.cache_resource
def load_image_as_pil(image_path: str):
    return Image.open(image_path)

image_path = path.join(path.dirname(__file__), 'image.jpg')
image = load_image_as_pil(image_path)

rectangles = zoom_select_image_component(image, 'A')

for rectangle in rectangles:
    if not rectangle['is_enabled']:
        continue

    with st.sidebar:
        st.image(rectangle['cropped_image'], clamp=True, use_column_width='always')

print(rectangles)
