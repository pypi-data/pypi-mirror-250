import os
import io

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "zoom_select_image_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("zoom_select_image_component", path=build_dir)

# image_id is not used, but needs to be there so that cache is busted when _image referentially changes
# note that the _ in front of image means that this argument is ignored for caching
@st.cache_resource()
def image_to_bytes(_image: Image, image_id: int):
    image_bytes = io.BytesIO()
    _image.save(image_bytes, format='PNG')
    return image_bytes.getvalue()

# it's tempting to cache the result of this function (and merge it with the function above), however this
# has the problem that Streamlit's garbage collector sometimes removes the file from the media file manager,
# so we should call `add` every time we want to use an url and let the media manager decide if it wants to create
# a new file or re-use the existing one
def image_to_url(image: Image):
    media_file_manager = st.runtime.get_instance().media_file_mgr
    image_bytes = image_to_bytes(image, id(image))

    return media_file_manager.add(image_bytes, 'image/png', '')

def zoom_select_image_component(image: Image, key: str, rectangle_width=500, rectangle_height=500):
    """Create a new instance of "zoom_select_image_component".

    Parameters
    ----------
    image: PIL.Image
        The image to display in the component.
        This should be referentially stable, otherwise there will be an noticeable delay each time your app runs.
        One way to achieve this is by loading it through a function decorated with @st.cache_resource.
    key: str
        A key that identifies this instance of the component.
        Can be set to any value as long as it's unique throughout the app.
        Changing this value on an existing instance will rerender the whole component and reset state.
    rectangle_width: number
        The width of the zoom rectangle in image pixels.
    rectangle_height: number
        The height of the zoom rectangle in image pixels.

    Returns
    -------
    array
        An array of selected rectangles, with keys 'left', 'top', 'width', 'height', 'isEnabled' and 'crop'.
        The first four keys give the boundaries of the rectangle, 'is_enabled' is true if the checkbox in the rectangle
        is checked and 'cropped_image' contains the part of the image bounded by the rectangle.
    """

    image_url = image_to_url(image)
    rectangles = _component_func(image_url=image_url, key=key, rectangle_width=rectangle_width, rectangle_height=rectangle_height, default=[])

    for rectangle in rectangles:
        left = rectangle['left'] = round(rectangle['left'])
        top = rectangle['top'] = round(rectangle['top'])
        width = rectangle['width'] = round(rectangle['width'])
        height = rectangle['height'] = round(rectangle['height'])

        rectangle['is_enabled'] = rectangle['isEnabled']
        rectangle['cropped_image'] = image.crop((left, top, left + width, top + height))

        del rectangle['focalPoint']
        del rectangle['isEnabled']
        del rectangle['scale']

    return rectangles
