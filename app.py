from flask import Flask, request, jsonify
import requests
from PIL import Image
import io

app = Flask(__name__)

SATELLITE_URL = "https://mt.google.com/vt/lyrs=s"
TERRAIN_URL = "https://mt.google.com/vt/lyrs=t"

@app.route('/get_chunk_satellite', methods=['GET'])
def get_chunk_satellite():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)
    zoom = request.args.get('zoom', type=int)

    if x is None or y is None or zoom is None:
        return jsonify({"error": "Missing parameters: x, y, and zoom are required"}), 400
    
    tile_url = f"{SATELLITE_URL}&x={x}&y={y}&z={zoom}"
    
    try:
        response = requests.get(tile_url, stream=True)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        width, height = image.size
        
        pixels = []
        pixel_data = image.load()
        
        for py in range(height):
            row = []
            for px in range(width):
                r, g, b = pixel_data[px, py]
                row.append([r, g, b])
            pixels.append(row)
        
        return jsonify({
            "status": "success",
            "x": x,
            "y": y,
            "zoom": zoom,
            "width": width,
            "height": height,
            "pixels": pixels
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch tile: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

@app.route('/get_chunk_terrain', methods=['GET'])
def get_chunk_terrain():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)
    zoom = request.args.get('zoom', type=int)

    if x is None or y is None or zoom is None:
        return jsonify({"error": "Missing parameters: x, y, and zoom are required"}), 400
    
    tile_url = f"{TERRAIN_URL}&x={x}&y={y}&z={zoom}"
    
    try:
        response = requests.get(tile_url, stream=True)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        width, height = image.size
        
        pixels = []
        pixel_data = image.load()
        
        for py in range(height):
            row = []
            for px in range(width):
                r, g, b = pixel_data[px, py]
                row.append([r, g, b])
            pixels.append(row)
        
        return jsonify({
            "status": "success",
            "x": x,
            "y": y,
            "zoom": zoom,
            "width": width,
            "height": height,
            "pixels": pixels
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch tile: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Image processing error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

