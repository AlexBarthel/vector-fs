from flask import Flask, request, jsonify
import requests
from PIL import Image
import io

app = Flask(__name__)

TILE_SIZE = 32

@app.route('/geo/chunk', methods=['GET'])
def geo_get_chunk():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)
    zoom = 4

    sat_tile = f"https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={zoom}"
    ter_tile = f"https://mt.google.com/vt/lyrs=t&x={x}&y={y}&z={zoom}"

    sat_response = requests.get(sat_tile)
    ter_response = requests.get(ter_tile)

    sat_image = Image.open(io.BytesIO(sat_response.content))
    ter_image = Image.open(io.BytesIO(ter_response.content))
        
    if sat_image.mode != 'RGB':
        sat_image = sat_image.convert('RGB')
        
    if ter_image.mode != 'RGB':
        ter_image = ter_image.convert('RGB')
        
    sat_image = sat_image.resize((TILE_SIZE, TILE_SIZE))
    ter_image = ter_image.resize((TILE_SIZE, TILE_SIZE))

    satellite = []
        
    width, height = sat_image.size
    sat_data = sat_image.load()

    for py in range(height):
        row = []
        for px in range(width):
            r, g, b = sat_data[px, py]
            row.append([r, g, b])
        satellite.append(row)

    terrain = []
    width, height = ter_image.size
    ter_data = ter_image.load()
    for py in range(height):
        row = []
        for px in range(width):
            r, g, b = ter_data[px, py]
            row.append([r, g, b])
        terrain.append(row)
    
    return jsonify({
        "satellite": satellite,
        "terrain": terrain,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
