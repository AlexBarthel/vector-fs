import os
import requests
from PIL import Image

# Constants
TILE_SIZE = 256  # Each tile is 256x256 pixels
GRID_SIZE = 16  # 16x16 grid
ZOOM_LEVEL = 4  # Zoom level
BASE_URL = "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
OUTPUT_IMAGE = "stitched_map.png"
IMAGE_FOLDER = "tiles"

# Ensure tile directory exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def download_tile(x, y):
    """Download a single tile and save it."""
    url = BASE_URL.format(x=x, y=y, z=ZOOM_LEVEL)
    tile_path = os.path.join(IMAGE_FOLDER, f"tile_{x}_{y}.png")

    if not os.path.exists(tile_path):  # Skip if already downloaded
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(tile_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download tile ({x}, {y})")
    
    return tile_path

def stitch_tiles():
    """Stitch downloaded tiles into a single image."""
    stitched_image = Image.new("RGB", (TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            tile_path = download_tile(x, y)
            try:
                tile = Image.open(tile_path)
                stitched_image.paste(tile, (x * TILE_SIZE, y * TILE_SIZE))
            except Exception as e:
                print(f"Error processing tile ({x}, {y}): {e}")

    stitched_image.save(OUTPUT_IMAGE)
    print(f"Map saved as {OUTPUT_IMAGE}")

if __name__ == "__main__":
    stitch_tiles()
