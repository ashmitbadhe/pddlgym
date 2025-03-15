from .utils import get_asset_path, fig2data, draw_token
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import RegularPolygon
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np

IM_SCALE = 1

# Define constants for the object types
NUM_OBJECTS = 7
PLATFORM2, BACK, SKY, AGENT, RESOURCE, PLATFORM, MAX= range(NUM_OBJECTS)

# Define images for the tokens
TOKEN_IMAGES = {
    BACK: plt.imread(get_asset_path('Background_0.png')),
    SKY: plt.imread(get_asset_path('background.png')),
    AGENT: plt.imread(get_asset_path('wizard.png')),
    RESOURCE: plt.imread(get_asset_path('resourceful_platform.png')),
    PLATFORM: plt.imread(get_asset_path('floating_plat.png')),
    PLATFORM2: plt.imread(get_asset_path('resource_empty_platform.png')),

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
    all_resources = {}
    taken = []
    agent_loc = None
    agent_dead = False
    for lit in obs:
        if lit.predicate.name == 'connected':
            r1, c1 = loc_str_to_loc(lit.variables[0])
            r2, c2 = loc_str_to_loc(lit.variables[1])
            layout[r1, c1, SKY] = 1
            layout[r2, c2, SKY] = 1
        elif lit.predicate.name == 'at-res':
            r, c = loc_str_to_loc(lit.variables[1])
            res_id = lit.variables[0].split(":")[0].strip()
            all_resources[res_id] = r, c
            layout[r, c, PLATFORM2] = 1
            if res_id not in taken:
                layout[r, c, RESOURCE] = 1
        elif lit.predicate.name == 'at-agent':
            r, c = loc_str_to_loc(lit.variables[0])
            agent_loc = r, c
            if agent_dead == False:
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
        elif lit.predicate.name == 'taken':
            res_id = lit.variables[0].split(":")[0].strip()
            taken.append(res_id)
            if res_id in all_resources:
                r, c = all_resources[res_id]
                layout[r, c, RESOURCE] = 0
        elif lit.predicate.name == 'dead':
            agent_dead = True
            if agent_loc is not None:
                r, c = agent_loc
                layout[r, c, AGENT] = 0


    # 1 indexing
    layout = layout[1:, 1:]

    return layout

def get_token_images(obs_cell):
    if obs_cell[BACK]:
        yield TOKEN_IMAGES[BACK]
    # if obs_cell[SKY]:
    #     yield TOKEN_IMAGES[SKY]
    if obs_cell[PLATFORM2]:
        yield TOKEN_IMAGES[PLATFORM2]
    if obs_cell[PLATFORM]:
        # Platform level determines the size of the rectangle
        level = obs_cell[PLATFORM]
        max_level = obs_cell[MAX]
        scale = level / max_level  # Ensure scale is between 0 and 1

        # Get base image
        base_image = TOKEN_IMAGES[PLATFORM]
        image_array = np.array(base_image)
        image_array = (image_array * 255).astype(np.uint8)  # Convert float (0-1) to uint8 (0-255)
        pil_image = Image.fromarray(image_array)

        # Resize correctly
        width, height = pil_image.size
        width = width-60
        height = height-60
        new_size = (60+int(width * scale), 60+int(height))  # Convert to integers

        platform_image = pil_image.resize(new_size, Image.NEAREST)

        yield np.array(platform_image)  # Convert back to NumPy array
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

    light_blue = np.array([132/255, 204/255, 230/255])  # RGB for light blue

    # Create a grid of light red color for all cells
    grid_colors = np.full((10, 10, 3), light_blue)  # Shape (height, width, 3)
    return render_from_layout(layout, get_token_images, dpi=300)



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
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
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
