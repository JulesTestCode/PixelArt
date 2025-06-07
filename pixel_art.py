import os
import subprocess
from datetime import datetime, timedelta
import random

# Construction d'une grille 7x52
PIXEL_ART = [[0]*52 for _ in range(7)]

# Function to create a robot arm in a grid
def robot_arm(pixel_art):
    for i in range(5):
        pixel_art[6][i] = 1

    pixel_art[5][1] = 1
    pixel_art[5][2] = 1
    pixel_art[5][3] = 1

    pixel_art[4][2] = 1
    pixel_art[3][2] = 1
    pixel_art[2][2] = 1
    pixel_art[1][2] = 1

    for i in range(6):
        pixel_art[1][3+i] = 1

    pixel_art[2][8] = 1
    pixel_art[3][8] = 1
    pixel_art[3][7] = 1
    pixel_art[3][9] = 1
    pixel_art[4][7] = 1
    pixel_art[4][9] = 1


# Function to create the conveyor with cubes on it
def conveyor(pixel_art):
    for i in range(7, 39):
        pixel_art[6][i] = 1

    # Set things on it
    for i in range(8, 39, 2):
        pixel_art[5][i] = random.randint(2, 4)

# Function to write "Hello"
def hello(pixel_art):
    # H
    for j in range(5):
        pixel_art[j][13] = 1
        pixel_art[j][15] = 1
    pixel_art[2][14] = 1

    # E
    for j in range(5):
        pixel_art[j][17] = 1
    pixel_art[0][18] = 1
    pixel_art[0][19] = 1
    pixel_art[2][18] = 1
    pixel_art[4][18] = 1
    pixel_art[4][19] = 1

    # L (x2)
    for j in range(5):
        pixel_art[j][21] = 1
        pixel_art[j][25] = 1
    pixel_art[4][22] = 1
    pixel_art[4][23] = 1
    pixel_art[4][26] = 1
    pixel_art[4][27] = 1

    # O
    for j in range(5):
        pixel_art[j][29] = 1
        pixel_art[j][31] = 1
    pixel_art[0][30] = 1
    pixel_art[4][30] = 1


# Function to create a conveyor robot in a grid
def conveyor_robot(pixel_art):
    for i in range(34, 47):
        pixel_art[0][i] = 1

    pixel_art[1][42] = 1
    pixel_art[2][42] = 1
    pixel_art[3][42] = 1
    pixel_art[3][41] = 1
    pixel_art[3][43] = 1
    pixel_art[4][41] = 1
    pixel_art[4][43] = 1
    pixel_art[4][42] = random.randint(2, 4)


# Function to create a pyramid of cubes
def pyramid_of_squares(pixel_art):
    start = 0
    for j in range(7):
        for i in range(start + 44, 52):
            pixel_art[6-j][i] = random.randint(2, 4)
        start = start + 1


# Function to fill the pixel art grid
def create_art():
    robot_arm(pixel_art=PIXEL_ART)
    conveyor(pixel_art=PIXEL_ART)
    hello(pixel_art=PIXEL_ART)
    conveyor_robot(pixel_art=PIXEL_ART)
    pyramid_of_squares(pixel_art=PIXEL_ART)


# Function to return the right square according the the cell value
def color_square(cell):
    match cell:
        case 1:
            return "🟩"
        case 2:
            return "🟨"
        case 3:
            return "🟦"
        case 4:
            return "🟪"
        case _:
            return "⬛"


def visualize_art():
    print("\nGitHub Contribution Pixel Art (Drone – 7x52):\n")
    for row in PIXEL_ART:
        print("".join(f"{color_square(cell)}" for cell in row))

def generate_commits(start_date_str="2024-01-01", commits_per_day=1):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    for col in range(52):
        for row in range(7):
            if PIXEL_ART[row][col]:
                commit_date = start_date + timedelta(weeks=col, days=row)
                for _ in range(commits_per_day):
                    with open("pixel_art.txt", "a") as f:
                        f.write(f"Commit on {commit_date.isoformat()}\n")
                    env = {
                        "GIT_AUTHOR_DATE": commit_date.isoformat(),
                        "GIT_COMMITTER_DATE": commit_date.isoformat(),
                    }
                    subprocess.run(["git", "add", "pixel_art.txt"])
                    subprocess.run(["git", "commit", "-m", f"Pixel art commit: {commit_date.date()}"], env={**os.environ, **env})

def push_to_github(repo_url, branch="main"):
    subprocess.run(["git", "branch", "-M", branch])
    subprocess.run(["git", "remote", "add", "origin", repo_url])
    subprocess.run(["git", "push", "-u", "origin", branch])

if __name__ == "__main__":
    create_art()
    visualize_art()
    # Adapter la date pour démarrer un an avant aujourd'hui
    #generate_commits(start_date_str="2024-06-06", commits_per_day=3)
    # push_to_github("https://github.com/<TON-UTILISATEUR>/<TON-DEPOT>.git")
