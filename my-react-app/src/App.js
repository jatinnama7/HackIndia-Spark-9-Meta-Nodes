import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [cid, setCid] = useState("");
  const [publicUrl, setPublicUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      setCid(data.cid);
      setPublicUrl(data.public_url);
    } else {
      alert("Upload failed");
    }
  };

  return (
    <div>
      <h1>IPFS File Uploader</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload to IPFS</button>

      {cid && (
        <div>
          <p>File CID: {cid}</p>
          <a href={publicUrl} target="_blank" rel="noopener noreferrer">
            View File on IPFS
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
