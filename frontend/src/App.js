import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Data from "./components/training/data";
import Predict from "./components/Predictions/predictions";
import  Training from "./components/training/training";
import "bootstrap/dist/css/bootstrap.min.css"; // Agrega esta línea para importar los estilos de Bootstrap

function App() {
    return (
        <Router>
            <div className="container mt-4">
                <nav>
                    <ul className="nav nav-tabs">
                        <li className="nav-item">
                            <Link to="/data" className="nav-link">
                                Cargar datos para un modelo
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/predict" className="nav-link">
                                Predecir con un modelo
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/train" className="nav-link">
                                Entrenar modelo
                            </Link>
                        </li>
                    </ul>
                </nav>
                <Routes>
                    <Route path="/data" element={<Data />} />
                    <Route path="/predict" element={<Predict />} />
                    <Route path="/train" element={<Training />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
