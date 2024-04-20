import React, { useState } from 'react';
import axios from 'axios';
import Training from './training'
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { blue, green } from '@mui/material/colors';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Unstable_Grid2';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';

function UploadCSV() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [file, setFile] = useState(null);
  const [version, setVersion] = useState('');
  const [image, setImage] = useState(null);
  const [precision, setPrecision] = useState('-');
  const [accuracy, setAccuracy] = useState('-');
  const [recall, setRecall] = useState('-');
  const [f1, setF1] = useState('-');


  const buttonSx = {
    ...(success && {
      bgcolor: green[500],
      '&:hover': {
        bgcolor: green[700],
      },
    }),
  };

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
      setSuccess(false);
      setLoading(true);
      await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setSuccess(true);
      setLoading(false);
      alert('Archivo CSV enviado exitosamente.');


      const matrix = await fetch('http://localhost:8000/metrics/' + version + '/matrix');
      const blob = await matrix.blob();
      const imageUrl = URL.createObjectURL(blob);
      setImage(imageUrl);

      fetch('http://localhost:8000/metrics/' + version)
        .then(function (response) {
          return response.json();
        }).then(function (data) {
          setAccuracy(Math.round(data[0].percent * 1000) / 1000)
          setPrecision(Math.round(data[1].percent * 1000) / 1000)
          setRecall(Math.round(data[2].percent * 1000) / 1000)
          setF1(Math.round(data[3].percent * 1000) / 1000)
          console.log(data);
        });






    } catch (error) {
      setLoading(false);
      console.error('Error al modelar:', error);
      alert('Error al realizar el modelo.');
    }
  };



  return (
    <Box mx>
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
          <TextField size="small" type="text" value={version} onChange={handleVersionChange} placeholder="Ingrese la versión" />
          <Box paddingLeft="10px">
            <Button size="large" variant="contained" disabled={loading} onClick={handleSubmit} sx={buttonSx}> Entrenar modelo </Button>
          </Box>
          {loading && (
            <Box paddingLeft="10px" paddingTop="10px">
              <CircularProgress
                size={24}
                sx={{
                  color: green[500],
                }}
              />
            </Box>
          )}
        </Box>
      </Stack>
      <Grid container spacing={2} columns={16} paddingTop="10px">
        <Grid xs={8}>
          <Typography variant="h6" textAlign="center">
            Métricas
          </Typography>
          <Grid container spacing={1} columns={16} paddingTop="10px" sx={{
            justifyContent: "center",
            alignContent: "center",
            display: "flex"
          }}>
            <Grid sx={{
              xs: 8,
              justifyContent: "center",
              alignContent: "center",
              display: "flex"
            }}>
              <Card sx={{
                width: "150px",
                height: "150px",
                background: "#eeeee4",
                justifyContent: "center",
                alignContent: "center",
                display: "flex"
              }}>
                <CardContent>
                  <Typography variant="h6" textAlign="Center">
                    {precision}
                  </Typography>
                  <Typography variant="h6" textAlign="Center">
                    Precisión
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid sx={{
              xs: 8,

              justifyContent: "center",
              alignContent: "center",
              display: "flex"
            }}>
              <Card sx={{
                width: "150px",
                height: "150px",
                background: "#eeeee4",
                justifyContent: "center",
                alignContent: "center",
                display: "flex"
              }}>
                <CardContent>
                  <Typography variant="h6" textAlign="Center">
                    {accuracy}
                  </Typography>
                  <Typography variant="h6" textAlign="Center">
                    Exactitud
                  </Typography>
                </CardContent>
              </Card>
            </Grid>


            <Grid sx={{
              xs: 8,

              justifyContent: "center",
              alignContent: "center",
              display: "flex"
            }}>
              <Card sx={{
                width: "150px",
                height: "150px",
                background: "#eeeee4",
                justifyContent: "center",
                alignContent: "center",
                display: "flex"
              }}>
                <CardContent>
                  <Typography variant="h6" textAlign="Center">
                    {recall}
                  </Typography>
                  <Typography variant="h6" textAlign="Center">
                    Recall
                  </Typography>
                </CardContent>
              </Card>
            </Grid>


            <Grid sx={{
              xs: 8,
              justifyContent: "center",
              alignContent: "center",
              display: "flex"
            }}>
              <Card sx={{
                width: "150px",
                height: "150px",
                background: "#eeeee4",
                justifyContent: "center",
                alignContent: "center",
                display: "flex"
              }}>
                <CardContent>
                  <Typography variant="h6" textAlign="Center">
                    {f1}
                  </Typography>
                  <Typography variant="h6" textAlign="Center">
                    F1
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

          </Grid>



        </Grid>
        <Grid xs={8}>
          <Typography variant="h6" textAlign="center">
            Matriz de confusión
          </Typography>
          <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
            {image? 
            <img src={image} alt="Imagen" width="500px" />
            : "Por favor carga un modelo para poder ver sus resultados"}
            
          </Box>


        </Grid>
      </Grid>
    </Box>
  );
}

export default UploadCSV;
