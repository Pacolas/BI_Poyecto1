import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import Appointments from "./components/Appointments/Appointments";
import Medicaments from "./components/Medicaments/Medicaments";
import "bootstrap/dist/css/bootstrap.min.css"; // Agrega esta línea para importar los estilos de Bootstrap

function App() {
    return (
        <Router>
            <div className="container mt-4">
                <nav>
                    <ul className="nav nav-tabs">
                        <li className="nav-item">
                            <Link to="/agendar" className="nav-link">
                                Pedir Citas Médicas
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/medicamentos" className="nav-link">
                                Medicamentos
                            </Link>
                        </li>
                    </ul>
                </nav>
                <Routes>
                    <Route path="/agendar" element={<Appointments />} />
                    <Route path="/medicamentos" element={<Medicaments />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
