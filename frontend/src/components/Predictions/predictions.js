import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UploadCSV() {
  const [version, setVersion] = useState('');
  const [textInput, setTextInput] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [versionsList, setVersionsList] = useState([]);

  useEffect(() => {
    // Consultar el endpoint para obtener la lista de versiones existentes
    const fetchVersions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/versions');
        setVersionsList(response.data); // Asignar la lista de versiones a versionsList
      } catch (error) {
        console.error('Error al obtener la lista de versiones:', error);
      }
    };

    fetchVersions();
  }, []);

  const handleVersionChange = (event) => {
    setVersion(event.target.value);
  };

  const handleTextChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/predict/quotes', null, {
        params: {
          version: version,
          texto: textInput
        }
      });
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
      <input type="text" value={textInput} onChange={handleTextChange} placeholder="Ingrese el texto" />
      <button onClick={handleSubmit}>Enviar CSV</button>
      {responseMessage && <p>Respuesta del modelo {version}: {responseMessage}</p>}
    </div>
  );
}

export default UploadCSV;
