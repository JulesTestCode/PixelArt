from random import randint
from math import sqrt

#region animated pixels

# Function to draw "Hello" with blink animation
def hello_anim(pixel_art, animation_duration, colors, x_offset=0, y_offset=0):
    animated_letters = []

    def add_letter(name, value, pixels, colors):
        for y, x in pixels:
            pixel_art[y][x] = value
        animated_letters.append({
            "type": "blink",
            "char": name,
            "pixels": pixels,
            "colors": colors,
            "duration": animation_duration
        })

    # H
    h_pixels = [(j+y_offset, x_offset) for j in range(5)] + [(j+y_offset, 2+x_offset) for j in range(5)] + [(2+y_offset, 1+x_offset)]
    add_letter("H", 0, h_pixels, colors)

    # E
    e_pixels = [(j+y_offset, 4 +x_offset) for j in range(5)] + [(y_offset, 5 +x_offset), (y_offset, 6 +x_offset), (2+y_offset, 5 +x_offset), (4+y_offset, 5 +x_offset), (4+y_offset, 6 +x_offset)]
    add_letter("E", 1, e_pixels, colors[1:] + colors[:1])

    # L1
    l1_pixels = [(j+y_offset, 8 +x_offset) for j in range(5)] + [(4+y_offset, 9 +x_offset), (4+y_offset, 10 +x_offset)]
    add_letter("L1", 2, l1_pixels, colors[2:] + colors[:2])

    # L2
    l2_pixels = [(j+y_offset, 12 +x_offset) for j in range(5)] + [(4+y_offset, 13 +x_offset), (4+y_offset, 14 +x_offset)]
    add_letter("L2", 3, l2_pixels, colors[3:] + colors[:3])

    # O
    o_pixels = [(j+y_offset, 16 +x_offset) for j in range(5)] + [(j+y_offset, 18 +x_offset) for j in range(5)] + [(y_offset, 17 +x_offset), (4+y_offset, 17 +x_offset)]
    add_letter("O", 0, o_pixels, colors)

    return animated_letters

def create_pixel_trajectory(start, path, color, duration, begin=0, cell_size=10, padding=2):
    """
    Crée un objet animé pour un pixel suivant un trajet défini.
    
    :param start: (x, y) point de départ
    :param path: [(x1, y1), (x2, y2), ...] liste de points à suivre
    :param color: Couleur du pixel
    :param duration: Durée totale de l'animation
    :param begin: Temps de départ
    :param cell_size: Taille du pixel (rectangle)
    :return: Dictionnaire représentant l'objet animé
    """
    full_path = [start] + path
    #total_steps = len(full_path)
    #key_times = ";".join([f"{i / (total_steps - 1):.2f}" for i in range(total_steps)])
    
    # Compute distances between steps
    distances = []
    for i in range(1, len(full_path)):
        x0, y0 = full_path[i - 1]
        x1, y1 = full_path[i]
        distance = sqrt((x1 - x0)**2 + (y1 - y0)**2)
        distances.append(distance)

    total_distance = sum(distances)

    # Calculate keyTimes proportional to distances
    cumulative_time = 0
    key_times = [0.0]
    for d in distances:
        cumulative_time += d / total_distance
        key_times.append(round(cumulative_time, 3))  # Round for cleaner output

    #key_times = ";".join([f"{i / (total_steps - 1):.2f}" for i in range(total_steps)])
    key_times = ";".join([str(t) for t in key_times])
    x_values = ";".join([str(x * (cell_size + padding) + padding) for x, y in full_path])
    y_values = ";".join([str(y * (cell_size + padding) + padding) for x, y in full_path])
    
    return {
        "type": "trajectory",
        "color": color,
        "begin": begin,
        "duration": duration,
        "x_values": x_values,
        "y_values": y_values,
        "key_times": key_times,
        "cell_size": cell_size
    }

#endregion

#region static pixels

# Function to draw a conveyor
def conveyor(pixel_art, start=7, stop=40):
    for i in range(start, stop):
        pixel_art[6][i] = 0

# Function to draw a pyramid of cubes
def pyramid_of_squares(pixel_art):
    start = 0
    for j in range(7):
        for i in range(start + 45, 52):
            pixel_art[6-j][i] = randint(0, 3)
        start += 1
    pixel_art[6][44] = randint(0, 3)
    pixel_art[6][43] = randint(0, 3)

# Function to draw a robot arm
def robot_arm(pixel_art, x_offset):
    for i in range(5):
        pixel_art[6][i+x_offset] = 0

    pixel_art[5][1+x_offset] = 0
    pixel_art[5][2+x_offset] = 0
    pixel_art[5][3+x_offset] = 0

    pixel_art[4][2+x_offset] = 0
    pixel_art[3][2+x_offset] = 0
    pixel_art[2][2+x_offset] = 0
    pixel_art[1][2+x_offset] = 0

    for i in range(3, 9):
        pixel_art[1][i+x_offset] = 0

    pixel_art[2][8+x_offset] = 0
    pixel_art[3][8+x_offset] = 0
    pixel_art[3][7+x_offset] = 0
    pixel_art[3][9+x_offset] = 0
    pixel_art[4][7+x_offset] = 0
    pixel_art[4][9+x_offset] = 0

# Function to draw a mechanical gripper robot
def gripper_robot(pixel_art, x_offset):
    for i in range(x_offset, x_offset + 11):
        pixel_art[0][i] = 0

    pixel_art[1][5 + x_offset] = 0
    pixel_art[2][5 + x_offset] = 0
    pixel_art[3][5 + x_offset] = 0
    pixel_art[3][4 + x_offset] = 0
    pixel_art[3][6 + x_offset] = 0
    pixel_art[4][4 + x_offset] = 0
    pixel_art[4][6 + x_offset] = 0
    #pixel_art[4][5] = randint(2, 4)

#endregion

# Function to manage the pixel art
def manage_pixel_art(grid, colors, cell_size=10, padding=2):
    
    # Static objects
    conveyor(grid, start=7, stop=40)
    pyramid_of_squares(grid)
    robot_arm(grid,x_offset=0)
    gripper_robot(grid, x_offset=37)

    # Animated objects
    animated_objects = hello_anim(grid, 2, colors[:4], x_offset=14, y_offset=0)

    pixel_path=[(35, 5), (6, 5), (6, 6)]
    pixels_move = []
    # Define pixels move
    pixels_move.append(create_pixel_trajectory(
        start=(35, 0),
        path=pixel_path,
        color=colors[0],
        duration=8,
        begin=0,
        cell_size=cell_size,
        padding=padding
    ))
    pixels_move.append(create_pixel_trajectory(
        start=(35, 0),
        path=pixel_path,
        color=colors[3],
        duration=8,
        begin=2,
        cell_size=cell_size,
        padding=padding
    ))
    pixels_move.append(create_pixel_trajectory(
        start=(35, 0),
        path=pixel_path,
        color=colors[1],
        duration=8,
        begin=4,
        cell_size=cell_size,
        padding=padding
    ))
    pixels_move.append(create_pixel_trajectory(
        start=(35, 0),
        path=pixel_path,
        color=colors[2],
        duration=8,
        begin=6,
        cell_size=cell_size,
        padding=padding
    ))
    for pixel in pixels_move:
        animated_objects.append(pixel)

    return grid, animated_objects