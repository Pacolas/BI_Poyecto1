import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Data from "./components/training/data";
import Predict from "./components/Predictions/predictions";
import Predicts from "./components/Predictions/s_prediction";
import Training from "./components/training/training";
import "bootstrap/dist/css/bootstrap.min.css"; // Agrega esta línea para importar los estilos de Bootstrap
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';



function App() {
    
    return (
        <Router>
            <Box maxWidth={1400} mx="auto" paddingTop="10px" paddingBottom="10px">
                <AppBar position="static" >
                    <Toolbar disableGutters>
                    <img src="https://i.ibb.co/WkDWrx8/TURISMO-LOS-ALPES-1.png" alt="Logo" style={{height: '100px', marginRight: '10px'}} /> 
                        <Box sx={{ flexGrow: 1 }} /> {/* Nuevo Box para empujar el ButtonGroup */}
                        <ButtonGroup color="inherit" variant="text" aria-label="Basic button group">
                            <Button>
                                <Link to="/data" className="nav-link">
                                    Entrenar un nuevo modelo
                                </Link>
                            </Button>
                            <Button>
                                <Link to="/predict" className="nav-link">
                                    Clasificar una reseña
                                </Link>
                            </Button>
                            <Button>
                                <Link to="/predicts" className="nav-link">
                                    Clasificar un archivo de reseñas
                                </Link>
                            </Button>
                        </ButtonGroup>
                    </Toolbar>
                </AppBar>
            </Box>
            <Routes>
                <Route path="/data" element={<Data />} />
                <Route path="/predict" element={<Predict />} />
                <Route path="/predicts" element={<Predicts />} />
                <Route path="/train" element={<Training />} />
            </Routes>

        </Router>
    );
}

export default App;
