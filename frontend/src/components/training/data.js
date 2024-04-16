import React, { useState } from 'react';
import axios from 'axios';

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [version, setVersion] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleVersionChange = (event) => {
    setVersion(event.target.value);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('csv_file', file);
    formData.append('version', version);

    try {
      await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert('Archivo CSV enviado exitosamente.');
    } catch (error) {
      console.error('Error al enviar el archivo CSV:', error);
      alert('Error al enviar el archivo CSV.');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <input type="text" value={version} onChange={handleVersionChange} placeholder="Ingrese la versión" />
      <button onClick={handleSubmit}>Enviar CSV</button>
    </div>
  );
}

export default UploadCSV;
