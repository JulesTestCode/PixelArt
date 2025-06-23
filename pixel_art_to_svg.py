# Function to convert the grid pixel art into animated svg
def grid_to_animated_svg(grid, colors, animated_objects = None, filename="animated_grid.svg", cell_size=10, padding=2):
    rows = len(grid)
    cols = len(grid[0])
    width = cols * (cell_size + padding) + padding
    height = rows * (cell_size + padding) + padding

    # Créer un mapping pixel → données d’animation
    pixel_map = {}
    if animated_objects != None :
        for obj in animated_objects:
            if obj["type"] == "blink":
                # Add in pixel_map
                for coord in obj["pixels"]:
                    pixel_map[coord] = {
                        "pixel_colors": obj["colors"],
                        "duration": obj["duration"]
                    }
                # Remove it from that animated_objects lists
                animated_objects.remove(obj)

    # SVG Head Code File
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" shape-rendering="crispEdges">']

    # Convertion (grid to svg coord for static pixels)
    for y in range(rows):
        for x in range(cols):
            #if grid[y][x]:
            rect_x = x * (cell_size + padding) + padding
            rect_y = y * (cell_size + padding) + padding

            # Animated pixels
            if (y, x) in pixel_map:
                pixel = pixel_map[(y, x)]
                pixel_colors = pixel["pixel_colors"]
                duration = pixel["duration"]
                #print(pixel)

                svg.append(f'''
<rect x="{rect_x}" y="{rect_y}" width="{cell_size}" height="{cell_size}">
    <animate attributeName="fill"
            values="{' ;'.join(pixel_colors)}"
            dur="{duration}s"
            repeatCount="indefinite"
            calcMode="discrete"/>
</rect>''')

            # Color background/empty pixels without animation
            else:
                svg.append(f'<rect x="{rect_x}" y="{rect_y}" width="{cell_size}" height="{cell_size}" fill="{colors[grid[y][x]]}"/>\n')


    # Add pixels animations (translations/rotations/etc..)
    for obj in animated_objects:
        if obj["type"] == "trajectory":
            svg.append(f'''
<rect x="{obj['x_values'].split(';')[0]}" y="{obj['y_values'].split(';')[0]}" width="{obj['cell_size']}" height="{obj['cell_size']}" fill="{obj['color']}">
    <animate attributeName="x"
             values="{obj['x_values']}"
             keyTimes="{obj['key_times']}"
             begin="{obj['begin']}s"
             dur="{obj['duration']}s"
             repeatCount="indefinite"
             fill="freeze"
             calcMode="linear"/>
    <animate attributeName="y"
             values="{obj['y_values']}"
             keyTimes="{obj['key_times']}"
             begin="{obj['begin']}s"
             dur="{obj['duration']}s"
             repeatCount="indefinite"
             fill="freeze"
             calcMode="linear"/>
</rect>''')

    svg.append("</svg>")

    with open(filename, "w") as f:
        f.write("\n".join(svg))

    print(f"✅ SVG written to {filename}")