import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
function UploadCSV() {
  const [version, setVersion] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [versionsList, setVersionsList] = useState([]);
  const [file, setFile] = useState(null);

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
      const response = await axios.post('http://localhost:8000/upload/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setResponseMessage(response.data.message);;
      alert('Archivo CSV enviado exitosamente.');
    } catch (error) {
      console.error('Error al enviar el archivo CSV:', error);
      alert('Error al enviar el archivo CSV.');
    }
    };

  return (
    <Box mx paddingLeft="40px">
      <Stack>
        <Typography variant="h4" sx={{ fontWeight: 700 }} textAlign="center">
          Etiquetar reseñas.
        </Typography>
        <Typography variant="h6" textAlign="center">
          Selecciona el archivo con el que deseas categorizar las reseñas
        </Typography>
        <Box mx="auto">
          <TextField type="file" onChange={handleFileChange} />
        </Box>
        <Typography variant="h6" textAlign="center">
          Escribe el nombre con el que deseas guardar el archivo
        </Typography>
        <Box mx="auto" display="flex" alignItems="center">
          
         
       
      <div>
      <select value={version} onChange={handleVersionChange}>
        <option value="">Seleccione una versión</option>
        {versionsList.map((versionItem, index) => (
          <option key={index} value={versionItem.name}>{versionItem.name}</option>
        ))}
      </select>
      <Button size="large" variant="contained" onClick={handleSubmit}>Enviar CSV</Button>
      {responseMessage && <p>Respuesta del modelo {version}: {responseMessage}</p>}
    </div>
        

    </Box>
        
        </Stack>
      
    </Box>
    
  );
}

export default UploadCSV;
