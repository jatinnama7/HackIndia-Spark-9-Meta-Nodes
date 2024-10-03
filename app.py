import httpx
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your Pinata API credentials
PINATA_API_KEY = 'd875855d5cd258febe72'
PINATA_API_SECRET = '3fde2cfc70aa0c9f20301c73836fe5d6c0d88d7935680f20a2b3c6dafeec1200'

def pin_file_to_pinata(file_path):
    # Upload the file to Pinata (public IPFS node)
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_API_SECRET
    }
    
    with open(file_path, 'rb') as file:
        response = httpx.post(url, files={'file': file}, headers=headers)
    
    if response.status_code == 200:
        cid = response.json()['IpfsHash']
        public_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
        return cid, public_url
    else:
        return None, None

@app.route('/upload', methods=['POST'])
def upload_file():
    # Fetch the file from the request
    file = request.files['file']
    file.save(file.filename)
    
    # Pin the file to Pinata and get CID and public URL
    cid, public_url = pin_file_to_pinata(file.filename)
    
    if cid:
        return jsonify({"cid": cid, "public_url": public_url}), 200
    else:
        return jsonify({"error": "Failed to pin file"}), 500

if __name__ == "__main__":
    app.run(debug=True)
