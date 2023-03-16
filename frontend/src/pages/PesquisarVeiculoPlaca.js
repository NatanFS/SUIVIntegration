import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import debounce from 'lodash/debounce';

function PesquisarVeiculoPlaca() {

    const [vehicleData, setVehicleData] = useState({})
    const [selectedModel, setSelectedModel] = useState({})
    const [basicPack, setBasicPack] = useState({})
    const [techSpecs, setTechSpecs] = useState({})
    const [summary, setSummary] = useState()
    const [formData, setFormData] = useState({
        plate: '',
    });

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const recuperarResumo = () => {
        axios.get(`/api/Summary/byfipe?fipeId=${selectedModel.fipe_id}`)
            .then(response => {
                setSummary(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }

    const recuperarEspecificacoesTecnicas = () => {
        axios.get(`/api/TechnicalSpecs?plate=${formData.plate}`)
            .then(response => {
                setTechSpecs(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }

    const pesquisarPlaca = (event) => {
        event.preventDefault();
        debouncedPesquisarPlaca(formData)
    };

    const recuperarPacoteBasico = (event) => {
        event.preventDefault();
        debouncedRecuperarPacoteBasico(selectedModel)
    };

    const debouncedPesquisarPlaca = useCallback(debounce((formData) => {
        axios.get(`/api/VehicleInfo/byplate?plate=${formData.plate}`)
            .then(response => {
                setVehicleData(response.data);
                setSelectedModel({})
                setBasicPack({ basicPack })
                setSummary({})
            })
            .catch(error => {
                console.error(error);
            });
    }, 1000), []);

    const debouncedRecuperarPacoteBasico = useCallback(debounce((selectedModel) => {
        axios.get(`/api/BasicPack?fipeId=${selectedModel.fipe_id}&year=${selectedModel.year}`)
            .then(response => {
                setBasicPack(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }, 1000), []);

    useEffect(() => {
        recuperarResumo()
    }, [selectedModel])

    useEffect(() => {
        recuperarEspecificacoesTecnicas()
    }, [vehicleData])

    return (
        <div className="flex min-h-screen justify-center items-center">
            <div className="w-full p-4 lg:max-w-4xl xl:max-w-6xl">
                <form className="flex flex-col md:flex-row md:mb-4" onSubmit={pesquisarPlaca}>
                    <input
                        type="text"
                        placeholder="Digite a placa do veículo."
                        className="border border-gray-400 py-2 px-4 rounded-l-md mb-2 md:mb-0 md:mr-2 w-full md:w-1/2"
                        id="plate"
                        name="plate"
                        value={formData.plate}
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

                {summary && (
                    <div className="mx-auto rounded-md shadow-md overflow-hidden justify-center m-2">
                        <img className="mx-auto max-w-md w-full" src={summary.image_url} alt="Vehicle" />
                        <div className="flex justify-center items-center gap-8 p-4">
                            <div dangerouslySetInnerHTML={{ __html: summary.text }} />
                            <img className="w-24 mt-4" src={summary.maker_logo_url} alt="Maker Logo" />
                        </div>
                    </div>
                )}

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
                                            : selectedModel.model_description}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Descrição: </span>
                                        {vehicleData.description}
                                    </li>
                                    <li className="mb-2">
                                        <span className="font-bold">Montadora: </span>
                                        {vehicleData.fipe_id
                                            ? vehicleData.fipeDataCollection[vehicleData.fipe_id].maker_description
                                            : selectedModel.maker_description}
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
                                        {vehicleData.fipe_id ? vehicleData.fipe_id : selectedModel.fipe_id}
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
                                        {selectedModel && Object.keys(selectedModel).length > 0 ?
                                            selectedModel.current_value.toLocaleString('pt-br', { style: 'currency', currency: 'BRL' })
                                            : ''}
                                    </li>
                                    <li className="mb-2"><span className="font-bold">Versão: </span>
                                        {vehicleData.fipe_id ?
                                            vehicleData.fipeDataCollection[vehicleData.fipe_id].version_description
                                            : selectedModel.version_description}
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <h2 className="text-lg font-bold my-4">Selecione a versão do seu veículo</h2>

                        <div className="grid grid-cols-2 gap-4">
                            {vehicleData.fipeDataCollection.map((model, index) => (
                                <button
                                    key={index}
                                    className={`p-4 ${model === selectedModel ? "bg-blue-500 text-white" : "bg-white"
                                        }`}
                                    onClick={() => setSelectedModel(model)}
                                >
                                    {model.maker_description} {model.version_description} ({model.year})
                                </button>
                            ))}
                        </div>


                        {techSpecs.length > 0 && (
                            <div className="container mx-auto p-4">
                                {techSpecs.map((item) => (
                                    <div className="border border-gray-400 shadow rounded-md p-4 mb-4" key={item.id}>
                                        <h2 className="font-bold text-lg mb-2">{item.description}</h2>
                                        <ul>
                                            {item.specs.map((spec) => (
                                                <li key={spec.property} className="flex justify-between py-1">
                                                    <span className="font-medium">{spec.property}:</span>
                                                    <span>{spec.value}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        )}

                        
                        {Object.keys(selectedModel).length > 0 && (
                            <div className="w-full flex justify-center">
                                <button
                                    type="submit"
                                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold 
                                    py-2 px-4 rounded-md w-full m-4"
                                    onClick={recuperarPacoteBasico}>
                                    Exibir peças
                                </button>
                            </div>
                        )}

                        {basicPack.length > 0 && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                {basicPack.map((part) => (
                                    <div
                                        key={part.id}
                                        className="bg-white rounded-lg overflow-hidden shadow-lg"
                                    >
                                        <div className="px-6 py-4">
                                            <div className="font-bold text-xl mb-2">{part.nickname_description}</div>
                                            <p className="text-gray-700 text-base">{part.complement}</p>
                                            <p className="text-gray-700 text-base">{part.part_number}</p>
                                        </div>
                                        <div className="px-6 py-4">
                                            {part.aftermarket_maker_description && (
                                                <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">{part.aftermarket_maker_description}</span>
                                            )}
                                            <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700">{part.is_genuine ? 'Genuine' : 'Aftermarket'}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        


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