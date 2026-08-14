from pyscript import document
from pyodide.http import pyfetch


# ============================================================
# GitHub Repository
# ============================================================

GITHUB_USER = "sampetersonxyz"
GITHUB_REPO = "Portfolio"
IMAGE_FOLDER = "images"

GITHUB_API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USER}/{GITHUB_REPO}/contents/{IMAGE_FOLDER}"
)


# ============================================================
# Gallery State
# ============================================================

images = []
current_image = 0


# ============================================================
# HTML Elements
# ============================================================

gallery_image = document.querySelector("#gallery-image")
gallery_counter = document.querySelector("#gallery-counter")

previous_button = document.querySelector("#gallery-prev")
next_button = document.querySelector("#gallery-next")


# ============================================================
# Get Images From GitHub
# ============================================================

async def load_images():

    global images

    response = await pyfetch(GITHUB_API_URL)

    if not response.ok:
        print("Failed to load images from GitHub")
        print("HTTP status:", response.status)
        return

    files = await response.json()

    # Only include image files
    valid_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp"
    )

    images = []

    for file in files:

        if file["type"] != "file":
            continue

        filename = file["name"].lower()

        if filename.endswith(valid_extensions):

            images.append(file["download_url"])


    # Sort images alphabetically
    images.sort()


    # Display first image
    if len(images) > 0:
        show_image(0)

    else:
        gallery_counter.innerText = "No images found"


# ============================================================
# Display Image
# ============================================================

def show_image(index):

    global current_image

    if len(images) == 0:
        return

    current_image = index

    gallery_image.src = images[current_image]

    gallery_counter.innerText = (
        f"{current_image + 1} / {len(images)}"
    )


# ============================================================
# Previous Image
# ============================================================

def previous_image(event):

    global current_image

    if len(images) == 0:
        return

    current_image -= 1

    if current_image < 0:
        current_image = len(images) - 1

    show_image(current_image)


# ============================================================
# Next Image
# ============================================================

def next_image(event):

    global current_image

    if len(images) == 0:
        return

    current_image += 1

    if current_image >= len(images):
        current_image = 0

    show_image(current_image)


# ============================================================
# Button Events
# ============================================================

previous_button.onclick = previous_image
next_button.onclick = next_image


# ============================================================
# Clicking Image
# ============================================================

gallery_image.onclick = next_image


# ============================================================
# Start Gallery
# ============================================================

gallery_counter.innerText = "Loading images..."
