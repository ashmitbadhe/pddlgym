import matplotlib.pyplot as plt
import numpy as np
from .utils import get_asset_path, render_from_layout


# Define constants for the object types
NUM_OBJECTS = 21
SOLID, CLEAR, LOCATION, RESOURCE1, RESOURCE2, RESOURCE3, RESOURCE4, RESOURCE5, RESOURCE_ON_SOLID, AGENT1, AGENT2, AGENT3, AGENT4, AGENT5, AGENT_ON_SOLID, LEAF1, LEAF2, LEAF3, LEAF4, LEAF5, WALL = range(NUM_OBJECTS)

# Define images for the tokens
TOKEN_IMAGES = {
    LOCATION: plt.imread(get_asset_path('perestroika_water.png')),
    RESOURCE1: plt.imread(get_asset_path('leaf_level1_with_resource.png')),
    RESOURCE2: plt.imread(get_asset_path('leaf_level2_with_resource.png')),
    RESOURCE3: plt.imread(get_asset_path('leaf_level3_with_resource.png')),
    RESOURCE4: plt.imread(get_asset_path('leaf_level4_with_resource.png')),
    RESOURCE5: plt.imread(get_asset_path('leaf_level5_with_resource.png')),
    RESOURCE_ON_SOLID: plt.imread(get_asset_path('resource_on_solid.png')),

    AGENT1: plt.imread(get_asset_path('leaf_level1_with_player.png')),
    AGENT2: plt.imread(get_asset_path('leaf_level2_with_player.png')),
    AGENT3: plt.imread(get_asset_path('leaf_level3_with_player.png')),
    AGENT4: plt.imread(get_asset_path('leaf_level4_with_player.png')),
    AGENT5: plt.imread(get_asset_path('leaf_level5_with_player.png')),
    AGENT_ON_SOLID: plt.imread(get_asset_path('player_on_solid.png')),

    LEAF1: plt.imread(get_asset_path('leaf_level1.png')),
    LEAF2: plt.imread(get_asset_path('leaf_level2.png')),
    LEAF3: plt.imread(get_asset_path('leaf_level3.png')),
    LEAF4: plt.imread(get_asset_path('leaf_level4.png')),
    LEAF5: plt.imread(get_asset_path('leaf_level5.png')),
    SOLID: plt.imread(get_asset_path('solid.png')),

}
empty_leaves = [LEAF1,LEAF2,LEAF3,LEAF4,LEAF5]
agent_on_leaves = [AGENT1, AGENT2, AGENT3, AGENT4, AGENT5]
resource_on_leaves = [RESOURCE1, RESOURCE2, RESOURCE3, RESOURCE4, RESOURCE5]

def get_locations(obs, thing):

    """
    Get the locations where a certain object (agent or resource) is found.
    """
    locs = []
    collected_res = set()
    for lit in obs:
        if lit.predicate.name == 'taken':
            collected_res.add(lit.variables[0])
    for lit in obs:
        if thing in lit.predicate.name:

            if thing == 'res':
                res_value = lit.variables[0]
                if res_value not in collected_res:
                    locs.append(loc_str_to_loc(lit.variables[-1]))
            else:
                locs.append(loc_str_to_loc(lit.variables[-1]))

    return locs

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
    max_r, max_c, max_level = -np.inf, -np.inf, -np.inf
    for lit in obs:
        if lit.predicate.name not in ['connected', 'free', 'none', 'level-max', 'level']:
            continue
        if lit.predicate.name == 'connected':
            r1, c1 = loc_str_to_loc(lit.variables[0])
            r2, c2 = loc_str_to_loc(lit.variables[1])
            max_r = max(max_r, r1, r2)
            max_c = max(max_c, c1, c2)
        elif lit.predicate.name == 'free':
            r, c = loc_str_to_loc(lit.variables[0])
            max_r = max(max_r, r)
            max_c = max(max_c, c)
        elif lit.predicate.name == 'level':
            r, c = loc_str_to_loc(lit.variables[0])
            max_r = max(max_r, r)
            max_c = max(max_c, c)
        elif lit.predicate.name == 'level-max':
            max_level = max(max_level, int(lit.variables[1].split(':')[0].strip()[1]))

    step = (4) / (max_level - 1)
    level_indexes = [round(1 + i * step)-1 for i in range(max_level)]
    # Create empty layout
    layout = CLEAR * np.ones((max_r+1, max_c+1), dtype=np.uint8)

    # Place objects according to the literals
    seen_locs = set()
    solids = set()
    dead = False
    for lit in obs:
        r, c = -1, -1
        if lit.predicate.name == 'connected':
            r1, c1 = loc_str_to_loc(lit.variables[0])
            r2, c2 = loc_str_to_loc(lit.variables[1])

            first_leaf_level = next((item[2] for item in seen_locs if item[:2] == (r1, c1)), None)

            if first_leaf_level is not None:
                level_index = level_indexes[first_leaf_level - 1]
                layout[r1, c1] = empty_leaves[level_index]
            else:
                if (r1, c1) not in solids:
                    layout[r1, c1] = LOCATION

            second_leaf_level = next((item[2] for item in seen_locs if item[:2] == (r2, c2)), None)

            if second_leaf_level is not None:
                level_index = level_indexes[second_leaf_level - 1]
                layout[r2, c2] = empty_leaves[level_index]
            else:
                if (r2,c2) not in solids:
                    layout[r2, c2] = LOCATION
        elif lit.predicate.name == 'none':
            r, c = loc_str_to_loc(lit.variables[0])
            layout[r, c] = LOCATION
        elif lit.predicate.name == 'solid':
            r, c = loc_str_to_loc(lit.variables[0])
            layout[r, c] = SOLID
            solids.add((r,c))
        elif lit.predicate.name == 'dead':
            dead = True

        if lit.predicate.name == 'level':
            r, c = loc_str_to_loc(lit.variables[0])
            int_level = int(lit.variables[1].split(':')[0].strip()[1])
            level_index = level_indexes[int_level-1]
            layout[r, c] = empty_leaves[level_index]
            seen_locs.add((r, c, int_level))

    # # Get resources' locations and place them on the layout
    for r, c in get_locations(obs, 'res'):
        leaf_level = next((item[2] for item in seen_locs if item[:2] == (r, c)), None)

        if leaf_level is not None:
            level_index = level_indexes[leaf_level - 1]
            layout[r, c] = resource_on_leaves[level_index]
        else:
            if (r, c) in solids:
                layout[r,c] = RESOURCE_ON_SOLID

    # Get agent's locations and place them on the layout
    for r, c in get_locations(obs, 'agent'):
        if not dead:
            leaf_level = next((item[2] for item in seen_locs if item[:2] == (r,c)), None)

            if leaf_level is not None:
                level_index = level_indexes[leaf_level - 1]
                layout[r, c] = agent_on_leaves[level_index]
            else:
                if (r, c) in solids:
                    layout[r, c] = AGENT_ON_SOLID



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

    return render_from_layout(layout, get_token_images, grid_colors=np.full((10, 10), '#0099ff'))




