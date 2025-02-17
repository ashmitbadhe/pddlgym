import matplotlib.pyplot as plt
import numpy as np
from .utils import get_asset_path, render_from_layout
from PIL import Image


# Define constants for the object types
NUM_OBJECTS = 4
AGENT, RESOURCE, PLATFORM, MAX= range(NUM_OBJECTS)

# Define images for the tokens
TOKEN_IMAGES = {
    AGENT: plt.imread(get_asset_path('doors_player.png')),
    RESOURCE: plt.imread(get_asset_path('goal.png')),
    PLATFORM: plt.imread(get_asset_path('hiking_water.png')),

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
    max_r, max_c = 2, 2
    for lit in obs:
        for v in lit.variables:
            if 'l-' in v:
                r, c = loc_str_to_loc(v)
                max_r = max(max_r, r)
                max_c = max(max_c, c)
    layout = np.zeros((max_r + 1, max_c + 1, NUM_OBJECTS))

    levels = {}
    for lit in obs:
        if lit.predicate.name == 'at-res':
            r, c = loc_str_to_loc(lit.variables[1])
            layout[r, c, RESOURCE] = 1
        elif lit.predicate.name == 'at-agent':
            r, c = loc_str_to_loc(lit.variables[0])
            layout[r, c, AGENT] = 1
        elif lit.predicate.name == 'level':
            r, c = loc_str_to_loc(lit.variables[0])
            level = int(lit.variables[1].split(':')[0].strip()[1])  # Extract level number
            layout[r, c, PLATFORM] = level
        elif lit.predicate.name == 'level-max':
            r, c = loc_str_to_loc(lit.variables[0])
            max_level = int(lit.variables[1].split(':')[0].strip()[1])  # Extract level number
            layout[r, c, MAX] = max_level
        elif lit.predicate.name == 'solid':
            r, c = loc_str_to_loc(lit.variables[0])
            layout[r, c, PLATFORM] = 1
            layout[r, c, MAX] = 1

    # 1 indexing
    layout = layout[1:, 1:]

    return layout

def get_token_images(obs_cell):
    if obs_cell[PLATFORM]:
        # Platform level determines the size of the rectangle
        level = obs_cell[PLATFORM]
        max_level = obs_cell[MAX]
        scale = level/max_level
        # Draw the rectangle (using matplotlib)
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.add_patch(plt.Rectangle((0, 0), 1*scale, 1*scale, color="black"))  # Draw the rectangle
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")  # Hide axes
        plt.tight_layout()

        # Convert the matplotlib figure to an image array
        fig.canvas.draw()
        platform_image = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close(fig)  # Close the figure to free resources

        yield platform_image  # Return the drawn rectangle as an image
    if obs_cell[RESOURCE]:
        yield TOKEN_IMAGES[RESOURCE]
    if obs_cell[AGENT]:
        yield TOKEN_IMAGES[AGENT]
    return


def render(state):
    """
    Render the state based on the provided `state` object, which includes the layout and objects.
    """
    layout = build_layout(state)

    return render_from_layout(layout, get_token_images)




