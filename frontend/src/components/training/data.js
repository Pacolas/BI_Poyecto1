import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { green } from '@mui/material/colors';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Unstable_Grid2';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

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
  const [versionsList, setVersionsList] = useState([]);
  const [versionMetrics, setVersionMetrics] = useState();
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [image3, setImage3] = useState(null);
  const [image4, setImage4] = useState(null);
  const [image5, setImage5] = useState(null);

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

  const handleVersionMetrics = (event) => {
    setVersionMetrics(event.target.value);
    showInfo(event.target.value);
  };


  const showInfo = async (versionMetrics) =>{
    const matrix = await fetch('http://localhost:8000/metrics/' + versionMetrics + '/matrix');
      const blob = await matrix.blob();
      const imageUrl = URL.createObjectURL(blob);
      setImage(imageUrl);

      fetch('http://localhost:8000/metrics/' + versionMetrics)
        .then(function (response) {
          return response.json();
        }).then(function (data) {
          if (data && data[0]) {
            setAccuracy(Math.round(data[0].percent * 1000) / 1000)
            setPrecision(Math.round(data[1].percent * 1000) / 1000)
            setRecall(Math.round(data[2].percent * 1000) / 1000)
            setF1(Math.round(data[3].percent * 1000) / 1000)
            console.log(data);
          }
        });

      const wordCloud1 = await fetch('http://localhost:8000/wordcloud/' + versionMetrics + '/1');
      const blob1 = await wordCloud1.blob();
      const wordCloudUrl1 = URL.createObjectURL(blob1);
      setImage1(wordCloudUrl1);

      const wordCloud2 = await fetch('http://localhost:8000/wordcloud/' + versionMetrics + '/2');
      const blob2 = await wordCloud2.blob();
      const wordCloudUrl2 = URL.createObjectURL(blob2);
      setImage2(wordCloudUrl2);

      const wordCloud3 = await fetch('http://localhost:8000/wordcloud/' + versionMetrics + '/3');
      const blob3 = await wordCloud3.blob();
      const wordCloudUrl3 = URL.createObjectURL(blob3);
      setImage3(wordCloudUrl3);

      const wordCloud4 = await fetch('http://localhost:8000/wordcloud/' + versionMetrics + '/4');
      const blob4 = await wordCloud4.blob();
      const wordCloudUrl4 = URL.createObjectURL(blob4);
      setImage4(wordCloudUrl4);

      const wordCloud5 = await fetch('http://localhost:8000/wordcloud/' + versionMetrics + '/5');
      const blob5 = await wordCloud5.blob();
      const wordCloudUrl5 = URL.createObjectURL(blob5);
      setImage5(wordCloudUrl5);

  }

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
      showInfo();

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
        <Typography variant="h6" textAlign="center">
          Ahora selecciona el modelo del que deseas conocer más información
        </Typography>
        <Box mx="auto">
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Modelo</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={versionMetrics}
                onChange={handleVersionMetrics}
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

          <Typography variant="h6" textAlign="center" paddingTop="10px">
            Palabras más frecuentes
          </Typography>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1-content"
              id="panel1-header"
            >
              Clase 1
            </AccordionSummary>
            <AccordionDetails>
              <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
                {image1 ?
                  <img src={image1} alt="Imagen" width="500px" />
                  : "Por favor carga un modelo para poder ver sus resultados"}
              </Box>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              Clase 2
            </AccordionSummary>
            <AccordionDetails>
              <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
                {image2 ?
                  <img src={image2} alt="Imagen" width="500px" />
                  : "Por favor carga un modelo para poder ver sus resultados"}
              </Box>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              Clase 3
            </AccordionSummary>
            <AccordionDetails>
              <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
                {image2 ?
                  <img src={image3} alt="Imagen" width="500px" />
                  : "Por favor carga un modelo para poder ver sus resultados"}
              </Box>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              Clase 4
            </AccordionSummary>
            <AccordionDetails>
              <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
                {image2 ?
                  <img src={image4} alt="Imagen" width="500px" />
                  : "Por favor carga un modelo para poder ver sus resultados"}
              </Box>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2-content"
              id="panel2-header"
            >
              Clase 5
            </AccordionSummary>
            <AccordionDetails>
              <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
                {image2 ?
                  <img src={image5} alt="Imagen" width="500px" />
                  : "Por favor carga un modelo para poder ver sus resultados"}
              </Box>
            </AccordionDetails>
          </Accordion>
        </Grid>
        <Grid xs={8}>
          <Typography variant="h6" textAlign="center">
            Matriz de confusión
          </Typography>
          <Box mx="auto" display="flex" alignItems="center" justifyContent="center">
            {image ?
              <img src={image} alt="Imagen" width="500px" />
              : "Por favor carga un modelo para poder ver sus resultados"}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}

export default UploadCSV;
