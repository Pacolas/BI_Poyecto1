import React, { useState } from 'react';
import axios from 'axios';
import Training from './training'
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
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
    <Box mx paddingLeft="40px">
      <Stack>
        <Typography variant="h4" sx={{ fontWeight: 700 }} textAlign="center">
          Entrena un nuevo modelo
        </Typography>
        <Typography variant="h6" textAlign="center">
          Selecciona el archivo con el que deseas entrenar el modelo
        </Typography>
        <Box mx="auto">
          <TextField type="file" onChange={handleFileChange} />
        </Box>
        <Typography variant="h6" textAlign="center">
          Escribe el nombre con el que deseas guardar el archivo
        </Typography>
        <Box mx="auto" display="flex" alignItems="center">
          <TextField size="small" type="text" value={version} onChange={handleVersionChange} placeholder="Ingrese el nombre de la version" />
          <Button size="large" variant="contained" onClick={handleSubmit}>Enviar CSV</Button>
        </Box>
      </Stack>



      <Training />
    </Box>
  );
}

export default UploadCSV;
