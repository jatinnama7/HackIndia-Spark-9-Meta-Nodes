import httpx

def add_file(file_path):
    # Add the file to IPFS (via a local node)
    with open(file_path, 'rb') as file:
        response = httpx.post('http://127.0.0.1:5001/api/v0/add', files={'file': file}, timeout=30)
        response.raise_for_status()  # Raises an error for bad responses
        cid = response.json()['Hash']
        print(f"File added with CID: {cid}")
        
        # Pin the file to ensure it's stored locally
        pin_response = httpx.post(f'http://127.0.0.1:5001/api/v0/pin/add?arg={cid}', timeout=30)
        pin_response.raise_for_status()  # Raises an error for bad responses
        print(f"File with CID {cid} pinned successfully.")
        
        return cid

def get_file(cid, output_path):
    # Fetch the file from the public IPFS gateway
    gateway_url = f'https://ipfs.io/ipfs/{cid}'
    response = httpx.get(gateway_url, timeout=30)
    response.raise_for_status()  # Raises an error for bad responses

    with open(output_path, 'wb') as file:
        file.write(response.content)
    print(f"File with CID {cid} downloaded to {output_path}")

if __name__ == "__main__":
    # Example usage
    cid = add_file('example.txt')  # Replace with your file path
    get_file(cid, 'output2.txt')  # Specify where to save the downloaded file
