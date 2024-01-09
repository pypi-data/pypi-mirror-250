import os
import streamlit.components.v1 as components
import streamlit as st
from PIL import Image



_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "frames_zoom",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("frames_zoom", path=build_dir)


@st.cache_resource
def image_to_url(_image: Image, image_key: str):
    return st.elements.image.image_to_url(_image, _image.width, False, 'RGB', 'PNG', "frames_zoom" + image_key)


def frames_zoom(image: Image, rectangle_width:int=250, rectangle_height=250, image_key:str='', key:st = None):
    """Create a new instance of "frames_zoom".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """    
    image_url = image_to_url(image, image_key)

    rectangles = _component_func(
        image_url=image_url, 
        rectangle_width=rectangle_width, 
        rectangle_height=rectangle_height, default=[], key=None)
    
    for rectangle in rectangles:
        left = rectangle['left'] = round(rectangle['left'])
        top = rectangle['top'] = round(rectangle['top'])
        width = rectangle['width'] = round(rectangle['width'])
        height = rectangle['height'] = round(rectangle['height'])

        rectangle['is_enabled'] = rectangle['isEnabled']
        rectangle['cropped_image'] = image.crop((left, top, left + width, top + height))

        # del rectangle['focalPoint']
        del rectangle['isEnabled']
        # del rectangle['scale']


    return rectangles
