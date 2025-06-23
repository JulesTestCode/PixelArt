from pixel_art_manager import manage_pixel_art
from pixel_art_to_svg import grid_to_animated_svg

if __name__ == '__main__':
    # Grid contruction 7x52  (here nb days per week * nb weeks per year) : 
    grid = [[4]*52 for _ in range(7)]

    # Colors definition : (here github contribution)
    light_theme = False
    colors = ["#216e39", "#30a14e", "#40c463", "#9be9a8", "#ebedf0"] if light_theme else ["#00c647", "#0f6d31", "#034525", "#01311f", "#161b22"]

    # Cell and padding size
    cell_size=10
    padding=2

    # Create the pixel art
    grid, animated_objects = manage_pixel_art(grid, colors, cell_size, padding)

    # Create the svg file
    filename = "pixel_art"
    filename += "-light.svg" if light_theme else "-dark.svg"
    grid_to_animated_svg(grid, colors=colors, animated_objects=animated_objects, filename=filename, cell_size=cell_size, padding=padding)
