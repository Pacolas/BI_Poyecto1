import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';

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
    <Box mx>
      <Stack>
        <Typography variant="h4" sx={{ fontWeight: 700 }} textAlign="center">
          Clasificar una reseña individual
        </Typography>
        <Stack direction="row" spacing={2} mx="auto">
          <Typography variant="h6" textAlign="center" paddingTop="10px">
            Selecciona el modelo con el que quieres clasificar la reseña:
          </Typography>
          <Box mx="auto" paddingTop="10px" paddingBottom="10px">
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Modelo</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={version}
                onChange={handleVersionChange}
                label="model"
                size="small"
                sx={{width: "200px"}}
              >
                {versionsList.map((versionItem, index) => (
                  <MenuItem key={index} value={versionItem.name}>{versionItem.name}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </Stack>
        <Typography variant="h6" textAlign="center">
          Escribe la reseña a calificar:
        </Typography>

        <Box mx="auto" paddingTop="10px">
          <TextField sx={{ width: "600px", height: "200px" }} type="text" id="outlined-basic" label="Reseña" style={{ height: "50px" }} value={textInput} onChange={handleTextChange} placeholder="Ingrese el texto" />
        </Box>

        <Box mx="auto" paddingTop="20px"paddingBottom="20px" >
          <Button size="large" variant="contained" style={{ width: "200px" }} onClick={handleSubmit}>Calificar reseña</Button>
        </Box>

        {responseMessage && <Typography variant="h6" textAlign="center">Respuesta del modelo {version}: {responseMessage}</Typography>}
      </Stack>
    </Box>
  );



}

export default UploadCSV;

