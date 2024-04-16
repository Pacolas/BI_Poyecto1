import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "bootstrap/dist/css/bootstrap.min.css";

function Appointments() {
    const [especializacion, setEspecializacion] = useState("");
    const [especializaciones, setEspecializaciones] = useState([]);
    const [horariosDisponibles, setHorariosDisponibles] = useState([]);
    const [dia, setDia] = useState(new Date());

    const ip = "localhost";

    const buscarEspecializacion = () => {
        fetch(`http://${ip}:8000/services`)
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    const especializacionesExistentes = data.map(
                        (item) => item.speciality
                    );
                    setEspecializaciones(especializacionesExistentes);
                }
            })
            .catch((error) => console.error("Error fetching services:", error));
    };

    useEffect(() => {
        buscarEspecializacion();
    }, []);

    const buscarHorariosDisponibles = () => {
        if (!especializacion) {
            console.error("Selecciona una especialización");
            return;
        }

        fetch(
            `http://${ip}:8000/appointments/services?speciality=${especializacion}`
        )
            .then((response) => response.json())
            .then((data) => {
                if (data) {
                    setHorariosDisponibles(data);
                    console.log(data);
                } 
            })
            .catch((error) =>
                console.error("Error fetching available schedules:", error)
            );
    };

    return (
        <div className="container mt-4">
            <h2 className="text-center mb-4">Citas Disponibles</h2>
            <form>
                <div className="row mb-3">
                    <div className="col-md-6">
                        <label htmlFor="especializacion" className="form-label">
                            Especialización
                        </label>
                        <select
                            value={especializacion}
                            onChange={(e) => setEspecializacion(e.target.value)}
                            className="form-select"
                            id="especializacion"
                        >
                            <option value="">Selecciona Especialización</option>
                            {especializaciones.map((especializacion) => (
                                <option
                                    key={especializacion}
                                    value={especializacion}
                                >
                                    {especializacion}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                {/* <div className="row mb-3">
                    <div className="col-md-6">
                        <label htmlFor="dia" className="form-label">
                            Fecha
                        </label>
                        <DatePicker
                            selected={dia}
                            onChange={(date) => setDia(date)}
                            dateFormat="dd/MM/yyyy"
                            className="form-control"
                            id="dia"
                        />
                    </div>
                </div> */}
                <div className="text-center">
                    <button
                        type="button"
                        onClick={buscarHorariosDisponibles}
                        className="btn btn-primary"
                    >
                        Buscar Citas
                    </button>
                </div>
            </form>
            {/* Mostrar resultados encontrados */}
            {Array.isArray (horariosDisponibles) && horariosDisponibles.length > 0 && (
    <>
       
        <div className="mt-4">
            <h3>Horarios Disponibles:</h3>
            <ul>
                {horariosDisponibles.map((horario) => (
                    <li key={horario.id}>
                        Hora: {horario.date}, {"Fecha: " + horario.time}, {"ID del doctor: " + horario.doctor_id}, {especializacion}
                    </li>
                ))}
            </ul>
        </div>
    </>
)}


        </div>
    );
}

export default Appointments;
