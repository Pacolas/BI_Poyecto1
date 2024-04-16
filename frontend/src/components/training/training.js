import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UploadCSV() {
  const [version, setVersion] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [versionsList, setVersionsList] = useState([]);

  useEffect(() => {
    const fetchVersions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/versions');
        setVersionsList(response.data); 
      } catch (error) {
        console.error('Error al obtener la lista de versiones:', error);
      }
    };

    fetchVersions();
  }, []);

  const handleVersionChange = (event) => {
    setVersion(event.target.value);
  };

 

  const handleSubmit = async () => {
    try {
      const response = await axios.get('http://localhost:8000/train/'+ version, null);
      setResponseMessage(response.data.message);
    } catch (error) {
      console.error('Error al enviar los datos:', error);
      alert('Error al enviar los datos.');
    }
  };

  return (
    <div>
      <select value={version} onChange={handleVersionChange}>
        <option value="">Seleccione una versión</option>
        {versionsList.map((versionItem, index) => (
          <option key={index} value={versionItem.name}>{versionItem.name}</option>
        ))}
      </select>
      <button onClick={handleSubmit}>Enviar Datos</button>
      {responseMessage && <p>Respuesta del {version}: {responseMessage}</p>}
    </div>
  );
}

export default UploadCSV;
