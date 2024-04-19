import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Data from "./components/training/data";
import Predict from "./components/Predictions/predictions";
import Training from "./components/training/training";
import "bootstrap/dist/css/bootstrap.min.css"; // Agrega esta línea para importar los estilos de Bootstrap
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';



function App() {
    
    return (
        <Router>

            <Box maxWidth={1400} mx="auto" paddingTop="10px" paddingBottom="10px">
                <AppBar position="static" >
                    <Toolbar disableGutters>
                        <Typography variant="h6" mx sx={{fontWeight: 700}}>
                            Turismo de los Alpes
                        </Typography>
                        <Box sx={{ flexGrow: 1 }} /> {/* Nuevo Box para empujar el ButtonGroup */}
                        <ButtonGroup color="inherit" variant="text" aria-label="Basic button group">
                            <Button>
                                <Link to="/data" className="nav-link">
                                    Entrenar un nuevo modelo
                                </Link>
                            </Button>
                            <Button>
                                <Link to="/predict" className="nav-link">
                                    Predecir una reseña
                                </Link>
                            </Button>
                        </ButtonGroup>
                    </Toolbar>
                </AppBar>
            </Box>
            <Routes>
                <Route path="/data" element={<Data />} />
                <Route path="/predict" element={<Predict />} />
                <Route path="/train" element={<Training />} />
            </Routes>

        </Router>
    );
}

export default App;
