from pyscript import document, fetch
from js import window


# ============================================================
# GitHub Repository
# ============================================================

GITHUB_USER = "sampetersonxyz"
GITHUB_REPO = "Portfolio"



script = document.currentScript
folder = script.getAttribute("data-folder")

IMAGE_FOLDER = script.getAttribute("data-folder")

GITHUB_API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_USER}/{GITHUB_REPO}/contents/{IMAGE_FOLDER}"
)


# ============================================================
# Find This Gallery
# ============================================================

gallery = script.previousElementSibling

gallery_image = gallery.querySelector(".gallery-image")
gallery_counter = gallery.querySelector(".gallery-counter")

previous_button = gallery.querySelector(".gallery-prev")
next_button = gallery.querySelector(".gallery-next")


# ============================================================
# Gallery State
# ============================================================

images = []
current_image = 0


# ============================================================
# Load Images From GitHub
# ============================================================

async def load_images():

    global images

    print("Loading images from:")
    print(GITHUB_API_URL)

    try:

        response = await fetch(GITHUB_API_URL)

        print("GitHub response:", response.status)

        if not response.ok:
            print("GitHub API request failed.")
            gallery_counter.innerText = (
                f"GitHub error: {response.status}"
            )
            return

        files = await response.json()

        print("Files returned:", len(files))

        valid_extensions = (
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".webp"
        )

        images.clear()

        for file in files:

            if file["type"] != "file":
                continue

            filename = file["name"].lower()

            if filename.endswith(valid_extensions):
                images.append(
                    f"/{IMAGE_FOLDER}/{file['name']}"
                )

        images.sort()

        print("Images found:", len(images))

        if len(images) == 0:

            gallery_counter.innerText = "No images found"
            return

        show_image(0)

    except Exception as error:

        print("Gallery error:")
        print(error)

        gallery_counter.innerText = "Error loading images"


# ============================================================
# Show Image
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
# Events
# ============================================================

previous_button.onclick = previous_image
next_button.onclick = next_image

gallery_image.onclick = next_image


# ============================================================
# Start
# ============================================================

gallery_counter.innerText = "Loading images..."

await load_images()