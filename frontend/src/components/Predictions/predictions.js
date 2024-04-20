import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

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
  <Box mx paddingLeft="40px">
    <Stack>
      <Typography variant="h4" sx={{ fontWeight: 700 }} textAlign="center">
      Clasificar una reseña individual
      </Typography>
      <Typography variant="h6" textAlign="center">
        Ingrese el texto que desea clasificar:
      </Typography>
      <select style={{width: "200px"}} value={version} onChange={handleVersionChange}>
      <option value="">Seleccione una versión</option>
      {versionsList.map((versionItem, index) => (
        <option key={index} value={versionItem.name}>{versionItem.name}</option>
      ))}
    </select> 
    <input type="text" style={{height: "50px"}} value={textInput} onChange={handleTextChange} placeholder="Ingrese el texto" />
    <Button size="small" variant="contained"  style={{width: "200px"}} onClick={handleSubmit}>Enviar datos</Button>
    {responseMessage && <p>Respuesta del modelo {version}: {responseMessage}</p>}     
    </Stack>
  </Box>
);
  
  

}

export default UploadCSV;

