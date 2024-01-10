from os import path
import streamlit as st

from PIL import Image

import numpy as np
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from seaborn import color_palette

from zoom_select_image_component import zoom_select_image_component

# To run this example, you need to install these packages:
# pip install git+https://github.com/facebookresearch/segment-anything.git
# pip install torch torchvision seaborn

# To run this example you need to download a checkpoint for the ViT-H SAM model
# See https://github.com/facebookresearch/segment-anything for download instructions.
# The checkpoint file is assumed to be named 'sam_vit_h_4b8939.pth' and placed in the same directory as this file:
# change the path below if necessary:
sa_checkpoint_path = path.join(path.dirname(__file__), 'sam_vit_h_4b8939.pth')
image_path = path.join(path.dirname(__file__), 'image.jpg')

st.subheader("Image select")

@st.cache_resource
def load_image_as_pil(image_path: str):
    return Image.open(image_path)

@st.cache_resource
def load_sa_model(sa_checkpoint_path: str):
    sam = sam_model_registry["default"](checkpoint=sa_checkpoint_path)
    return SamAutomaticMaskGenerator(sam)

@st.cache_data
def generate_annotations(sa_checkpoint_path: str, image: np.array):
    mask_generator = load_sa_model(sa_checkpoint_path)
    return mask_generator.generate(image)

image = load_image_as_pil(image_path)
rectangles = zoom_select_image_component(image, 'B')

for rectangle in rectangles:
    if not rectangle['is_enabled']:
        continue

    cropped_image = np.array(rectangle['cropped_image'])
    annotations = generate_annotations(sa_checkpoint_path, cropped_image)

    sorted_annotations = sorted(annotations, key=(lambda x: -x['area']))
    colors = color_palette("husl", len(sorted_annotations))

    # we will do some algebra to overlay the masks on the image, so we convert to float values and rescale color
    # values to [0,1]
    cropped_image = cropped_image.astype(np.float64) / 255
    masks = np.zeros_like(cropped_image)

    for color, annotation in zip(colors, sorted_annotations):
        # the key 'segmentation' contains a boolean 2D array (HW) that is true on the image pixels that are
        # contained in the segmentation
        m = annotation['segmentation']
        # we combine all the segmmentations as an image in a 3D array (HWC)
        masks[m] += color

    with st.sidebar:
        blended_image = 0.4 * cropped_image + 0.6 * masks
        st.image(blended_image, clamp=True, use_column_width='always')
