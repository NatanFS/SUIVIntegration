import React, { useEffect, useState } from "react";
import axios from "axios";

function PesquisarVeiculoPlaca() {

    const [vehicleData, setVehicleData] = useState({})
    const [formData, setFormData] = useState({
        placa: '',
    });

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const pesquisarPlaca = (event) => {
        event.preventDefault();
        console.log("placa pesquisada")
        axios.get(`/api/InformacoesVeiculo/porplaca?placa=${formData.placa}`)
            .then(response => {
                console.log(response.data);
                setVehicleData(response.data)
                console.log(vehicleData)
            })
            .catch(error => {
                console.error(error);
            });

    };

    return (
        <div className="flex min-h-screen justify-center items-center">
            <div className="w-full p-4 lg:max-w-4xl xl:max-w-6xl">
                <form className="flex flex-col md:flex-row md:mb-4" onSubmit={pesquisarPlaca}>
                    <input
                        type="text"
                        placeholder="Digite a placa do veículo."
                        className="border border-gray-400 py-2 px-4 rounded-l-md mb-2 md:mb-0 md:mr-2 w-full md:w-1/2"
                        id="placa"
                        name="placa"
                        value={formData.placa}
                        onChange={handleInputChange}
                        required
                    />
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r-md w-full md:w-1/2"
                    >
                        Pesquisar
                    </button>
                </form>

                {vehicleData && vehicleData.fipeDataCollection && vehicleData.suivDataCollection && (
                    <>
                        <div className="bg-white rounded-lg p-4 shadow-md">
                            <h2 className="text-xl font-bold mb-4">Resultado da Pesquisa</h2>
                            <div className="flex flex-col md:flex-row md:gap-24">
                                <ul className="mb-4 md:mb-0">
                                    <li className="mb-2"><span className="font-bold">Tipo: </span>
                                        {vehicleData.type}
                                    </li>
                                    <li className="mb-2"><span className="font-bold">Placa: </span>
                                        {vehicleData.plate}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Modelo: </span>
                                        {vehicleData.fipe_id
                                            ? vehicleData.fipeDataCollection[vehicleData.fipe_id].model_description
                                            : "Não Informado"}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Descrição: </span>
                                        {vehicleData.description}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Montadora: </span>
                                        {vehicleData.fipe_id
                                            ? vehicleData.fipeDataCollection[vehicleData.fipe_id].maker_description
                                            : "Não Informado"}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Combustível: </span>
                                        {vehicleData.fuel}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Ano do modelo: </span>
                                        {vehicleData.year_model}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Código FIPE: </span>
                                        {vehicleData.fipe_id ? vehicleData.fipe_id : "Não informado"}
                                    </li>
                                </ul>
                                <ul>
                                    <li className="mb-2">
                                        <span className="font-bold">Ano de fabricação: </span>
                                        {vehicleData.year_fab}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Número do Motor: </span>
                                        {vehicleData.engine_number}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Procedência: </span>
                                        {vehicleData.is_national ? "Nacional" : "Internacional"}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Número de assentos: </span>
                                        {vehicleData.seat_count}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Potência: </span>
                                        {vehicleData.power} CV
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">VIN: </span>
                                        {vehicleData.chassis}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Valor atual: </span>
                                        {vehicleData.fipe_id ?
                                            vehicleData.fipeDataCollection[vehicleData.fipe_id].current_value
                                            : "Não Informado"}
                                    </li>
                                    <li className="mb-2"><span className="font-bold">Versão: </span>
                                        {vehicleData.fipe_id ?
                                            vehicleData.fipeDataCollection[vehicleData.fipe_id].version_description
                                            : "Não Informado"}
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div className="p-2">
                            Número de Requisições à SUIV: {vehicleData.suivRequestCount}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}

export default PesquisarVeiculoPlaca;