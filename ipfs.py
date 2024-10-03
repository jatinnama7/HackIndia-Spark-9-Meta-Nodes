import httpx

def add_file(file_path):
    # Add the file to IPFS
    with open(file_path, 'rb') as file:
        response = httpx.post('http://127.0.0.1:5001/api/v0/add', files={'file': file})
        cid = response.json()['Hash']
        print(f"File added with CID: {cid}")
        
        # Pin the file to make sure it's stored locally and visible in the IPFS Desktop
        pin_response = httpx.post(f'http://127.0.0.1:5001/api/v0/pin/add?arg={cid}')
        if pin_response.status_code == 200:
            print(f"File with CID {cid} pinned successfully.")
        else:
            print(f"Failed to pin file with CID {cid}")
        
        return cid

def get_file(cid, output_path):
    # Download the file from IPFS
    response = httpx.post(f'http://127.0.0.1:5001/api/v0/cat?arg={cid}')
    with open(output_path, 'wb') as file:
        file.write(response.content)
    print(f"File with CID {cid} downloaded to {output_path}")

if __name__ == "__main__":
    # Example usage
    cid = add_file('example.txt')  # Replace with your file path
    get_file(cid, 'output2.txt')  # Specify where to save the downloaded file
