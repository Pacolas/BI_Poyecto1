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
        },
        responseType: 'blob' // Esperamos un blob como respuesta
      });

      // Crear un objeto Blob con los datos recibidos
      const csvBlob = new Blob([response.data], { type: 'text/csv' });

      // Crear una URL del objeto Blob
      const csvUrl = window.URL.createObjectURL(csvBlob);

      // Crear un enlace para descargar el archivo CSV
      const link = document.createElement('a');
      link.href = csvUrl;
      link.download = `predictions_${version}.csv`; // Nombre de archivo sugerido
      document.body.appendChild(link);

      // Hacer clic en el enlace para iniciar la descarga
      link.click();

      // Limpiar la URL del objeto Blob
      window.URL.revokeObjectURL(csvUrl);

      setResponseMessage('Archivo CSV recibido exitosamente.');

    } catch (error) {
      console.error('Error al recibir el archivo CSV:', error);
      alert('Error al recibir el archivo CSV.');
    }
  };

  return (
    <Box mx paddingLeft="40px">
      <Stack>
        <Typography variant="h4" sx={{ fontWeight: 700 }} textAlign="center">
          Clasificar un archivo de reseñas
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
