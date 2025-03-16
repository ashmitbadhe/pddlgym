from .utils import get_asset_path, fig2data, draw_token
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np


# Define constants for the object types
NUM_OBJECTS = 7
ROOM, BACK, CLEAR, LOCATION, RESOURCE, AUV, SHIP = range(NUM_OBJECTS)

IM_SCALE = 1.0

# Define images for the tokens
TOKEN_IMAGES = {
    ROOM: plt.imread(get_asset_path('room_tile.png')),
    BACK: plt.imread(get_asset_path('auv_water.png')),
    LOCATION: plt.imread(get_asset_path('hiking_water.png')),
    RESOURCE: plt.imread(get_asset_path('blue_plant.png')),
    AUV: plt.imread(get_asset_path('musketeer.png')),
    SHIP: plt.imread(get_asset_path('skeleton.png')),
}

def loc_str_to_loc(loc_str):
    split = loc_str.split("-")
    assert split[0] == 'l' and len(split) == 3
    return (int(split[1]), int(split[2]))


def build_layout(obs):
    """
    Create the layout of the board by extracting relevant information from the observation.
    """


    # Get location boundaries
    max_r, max_c = -np.inf, -np.inf
    for lit in obs:
        if lit.predicate.name == 'connected':
            r1, c1 = loc_str_to_loc(lit.variables[0])
            r2, c2 = loc_str_to_loc(lit.variables[1])
            max_r = max(max_r, r1, r2)
            max_c = max(max_c, c1, c2)


    # Create empty layout
    layout = np.zeros((max_r + 1, max_c + 1, NUM_OBJECTS))

    # Place objects according to the literals
    seen_locs = []
    collected_res = set()
    for lit in obs:
        # if lit.predicate.name == 'connected':
        #     r1, c1 = loc_str_to_loc(lit.variables[0])
        #     r2, c2 = loc_str_to_loc(lit.variables[1])
        #     layout[r1, c1, ROOM] = 1
        #     layout[r2, c2, ROOM] = 1
        if lit.predicate.name == 'at-res':
            res_value = lit.variables[0]
            if res_value not in collected_res:
                r, c = loc_str_to_loc(lit.variables[-1])
                seen_locs.append((r,c))
                layout[r, c, RESOURCE] = 1
        elif 'auv' in str(lit.variables) and lit.predicate.name == 'at':
            r, c = loc_str_to_loc(lit.variables[-1])
            seen_locs.append((r, c))
            layout[r, c, AUV] = 1
        elif 'ship' in str(lit.variables) and lit.predicate.name == 'at':
            r, c = loc_str_to_loc(lit.variables[-1])
            seen_locs.append((r, c))
            layout[r, c, SHIP] = 1

    # 1 indexing
    layout = layout[1:, 1:]

    return layout

def get_token_images(obs_cell):
    if obs_cell[BACK]:
        yield TOKEN_IMAGES[BACK]
    if obs_cell[ROOM]:
        yield TOKEN_IMAGES[ROOM]
    if obs_cell[SHIP]:
        yield TOKEN_IMAGES[SHIP]
    if obs_cell[RESOURCE]:
        yield TOKEN_IMAGES[RESOURCE]
    if obs_cell[AUV]:
        yield TOKEN_IMAGES[AUV]



def render(state):
    """
    Render the state based on the provided `state` object, which includes the layout and objects.
    """
    layout = build_layout(state)

    return render_from_layout(layout, get_token_images, grid_colors=np.full((10, 10), '#0098ff'))


def render_from_layout(layout, get_token_images, dpi=150, grid_colors=None):
    height, width = layout.shape[:2]

    fig, ax = initialize_figure(height, width, grid_colors=grid_colors, background_png=TOKEN_IMAGES[BACK])

    for r in range(height):
        for c in range(width):
            token_images = get_token_images(layout[r, c])
            for im in token_images:
                draw_token(im, r, c, ax, height, width)

    im = fig2data(fig, dpi=dpi)
    plt.close(fig)

    im = Image.fromarray(im)
    new_width, new_height = (int(im.size[0] * IM_SCALE), int(im.size[1] * IM_SCALE))
    # TODO : switch resize method to Image.Resampling.LANCZOS when pillow>=10 is supported
    im = im.resize((new_width, new_height), Image.Resampling.LANCZOS)
    im = np.array(im)

    return im


def initialize_figure(height, width, fig_scale=1., grid_colors=None, background_png=None):
    fig = plt.figure(figsize=((width + 2) * fig_scale, (height + 2) * fig_scale))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0),
                      aspect='equal', frameon=False,
                      xlim=(-0.05, width + 0.05),
                      ylim=(-0.05, height + 0.05))
    if isinstance(background_png, np.ndarray):  # If already an array, convert it
        bg_img = Image.fromarray((background_png * 255).astype(np.uint8))  # Scale to 0-255
    else:
        bg_img = Image.open(background_png).convert("RGBA")  # Load from file if it's a path
    ax.imshow(bg_img, extent=[0, width, 0, height], origin="upper")

    return fig, ax