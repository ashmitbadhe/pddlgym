import matplotlib.pyplot as plt
import numpy as np
from .utils import get_asset_path, render_from_layout
from PIL import Image


# Define constants for the object types
NUM_OBJECTS = 4
AGENT, RESOURCE, PLATFORM, MAX= range(NUM_OBJECTS)

# Define images for the tokens
TOKEN_IMAGES = {
    AGENT: plt.imread(get_asset_path('perestroika_agent.png')),
    RESOURCE: plt.imread(get_asset_path('perestroika_resource.png')),
    PLATFORM: plt.imread(get_asset_path('perestroika_ring.png')),

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
        if lit.predicate.name == 'at-res':
            r, c = loc_str_to_loc(lit.variables[1])
            res_id = lit.variables[0].split(":")[0].strip()
            all_resources[res_id] = r, c
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
        new_size = (60+int(width * scale), 60+int(height * scale))  # Convert to integers

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

    light_grey = np.array([211/255, 211/255, 211/255])  # RGB for light grey

    # Create a grid of light red color for all cells
    grid_colors = np.full((10, 10, 3), light_grey)  # Shape (height, width, 3)
    return render_from_layout(layout, get_token_images, dpi=300, grid_colors=grid_colors)




