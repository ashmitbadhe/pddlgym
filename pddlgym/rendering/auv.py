import matplotlib.pyplot as plt
import numpy as np
from .utils import get_asset_path, render_from_layout


# Define constants for the object types
NUM_OBJECTS = 5
CLEAR, LOCATION, RESOURCE, AUV, SHIP = range(NUM_OBJECTS)

# Define images for the tokens
TOKEN_IMAGES = {
    LOCATION: plt.imread(get_asset_path('hiking_water.png')),
    RESOURCE: plt.imread(get_asset_path('doors_key.png')),
    AUV: plt.imread(get_asset_path('robot.png')),
    SHIP: plt.imread(get_asset_path('sar_chicken.png')),
}

def loc_str_to_loc(loc_str):
    """
    Convert a location string like 'l-1-4:location' into a tuple (row, column).
    """
    _, r, c = loc_str.split('-')
    return (int(r), int(c))


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
    layout = CLEAR * np.ones((max_r+1, max_c+1), dtype=np.uint8)

    # Place objects according to the literals
    seen_locs = []
    collected_res = set()
    for lit in obs:
        if lit.predicate.name == 'connected':
            r1, c1 = loc_str_to_loc(lit.variables[0])
            r2, c2 = loc_str_to_loc(lit.variables[1])
            if (r1, c1) not in seen_locs:
                layout[r1, c1] = LOCATION
            if (r2, c2) not in seen_locs:
                layout[r2, c2] = LOCATION
            max_r = max(max_r, r1, r2)
            max_c = max(max_c, c1, c2)
        elif lit.predicate.name == 'at-res':
            res_value = lit.variables[0]
            if res_value not in collected_res:
                r, c = loc_str_to_loc(lit.variables[-1])
                seen_locs.append((r,c))
                layout[r, c] = RESOURCE
        elif 'auv' in str(lit.variables) and lit.predicate.name == 'at':
            r, c = loc_str_to_loc(lit.variables[-1])
            seen_locs.append((r, c))
            layout[r, c] = AUV
        elif 'ship' in str(lit.variables) and lit.predicate.name == 'at':
            r, c = loc_str_to_loc(lit.variables[-1])
            seen_locs.append((r, c))
            layout[r, c] = SHIP

    # 1 indexing
    layout = layout[1:, 1:]

    # r-c flip
    layout = np.transpose(layout)

    return layout

def get_token_images(obs_cell):
    return [TOKEN_IMAGES[obs_cell]]


def render(state):
    """
    Render the state based on the provided `state` object, which includes the layout and objects.
    """
    layout = build_layout(state)

    return render_from_layout(layout, get_token_images, grid_colors=np.full((10, 10), '#0098ff'))