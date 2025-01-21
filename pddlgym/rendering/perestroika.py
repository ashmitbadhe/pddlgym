import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from .utils import fig2data

def get_location_params(locations, width, height, table_height, agent_height):
    num_locations = len(locations)
    horizontal_padding = 0.025 * width
    location_width = width / num_locations - 2 * horizontal_padding
    location_height = (height - table_height - agent_height) / num_locations - 0.05 * height

    location_positions = {}
    for loc_i, loc in enumerate(locations):
        x = horizontal_padding + loc_i * (location_width + 2 * horizontal_padding)
        y = table_height + loc_i * location_height
        location_positions[loc] = (x, y)

    return location_width, location_height, location_positions

def draw_table(ax, width, table_height):
    rect = patches.Rectangle((0, 0), width, table_height,
                             linewidth=1, edgecolor=(0.2, 0.2, 0.2), facecolor=(0.5, 0.2, 0.0))
    ax.add_patch(rect)

def draw_agent(ax, agent_width, agent_height, midx, midy, is_alive, location_width, location_height):
    x = midx - agent_width / 2
    y = midy - agent_height / 2
    color = (0.4, 0.4, 0.4) if is_alive else (0.6, 0.6, 0.6)
    rect = patches.Rectangle((x, y), agent_width, agent_height,
                             linewidth=1, edgecolor=(0.2, 0.2, 0.2), facecolor=color)
    ax.add_patch(rect)

def draw_location(ax, location_width, location_height, location_positions):
    for loc_name, (x, y) in location_positions.items():
        rect = patches.Rectangle((x, y), location_width, location_height,
                                 linewidth=1, edgecolor=(0.2, 0.2, 0.2), facecolor=(0.8, 0.8, 0.8))
        ax.add_patch(rect)
        ax.text(x + location_width / 2, y + location_height / 2, loc_name,
                color='black', ha='center', va='center', fontweight='bold')

def draw_resources(ax, resource_positions, resource_color=(0.1, 0.9, 0.1)):
    for res_name, (x, y) in resource_positions.items():
        rect = patches.Circle((x, y), radius=0.05, linewidth=1, edgecolor=(0.2, 0.2, 0.2), facecolor=resource_color)
        ax.add_patch(rect)
        ax.text(x, y, res_name, color='black', ha='center', va='center', fontweight='bold')

def render(obs, mode='human', close=False):
    width, height = 3.2, 3.2
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), aspect='equal', frameon=False,
                      xlim=(-0.05, width + 0.05), ylim=(-0.05, height + 0.05))

    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(plt.NullFormatter())
        axis.set_major_locator(plt.NullLocator())

    table_height = height * 0.15
    agent_height = height * 0.1

    # Assuming the observation contains location, resources, and agent's state
    locations = obs.get("locations", [])
    resources = obs.get("resources", [])
    agent_state = obs.get("agent", {"position": None, "alive": True})

    location_width, location_height, location_positions = get_location_params(locations, width, height,
                                                                             table_height, agent_height)

    agent_width = location_width * 1.2
    agent_midx = width / 2
    agent_midy = height - agent_height / 2

    draw_table(ax, width, table_height)
    draw_location(ax, location_width, location_height, location_positions)
    draw_agent(ax, agent_width, agent_height, agent_midx, agent_midy, agent_state["alive"], location_width, location_height)
    draw_resources(ax, resources)

    return fig2data(fig)
