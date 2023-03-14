import React, { useEffect, useState } from "react";
import axios from "axios";

function PesquisarVeiculoPlaca() {
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
        })
        .catch(error => {
            console.error(error);
        });
        
    };


    return (
        <div className="flex min-h-screen justify-center items-center">
            <div>
                <form className="flex mb-4" onSubmit={pesquisarPlaca}>
                    <input type="text" placeholder="Digite a placa do veículo." className="border border-gray-400 py-2 px-4 rounded-l-md w-1/2"
                        id="placa"
                        name="placa"
                        value={formData.placa}
                        onChange={handleInputChange}
                        required
                    />
                    <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r-md w-1/2">Pesquisar</button>
                </form>

                <div className="bg-white rounded-lg p-4 shadow-md">
                    <h2 className="text-xl font-bold mb-4">Resultado da Pesquisa</h2>
                    <div className="flex gap-24">
                        <ul>
                            <li className="mb-2"><span className="font-bold">Placa:</span> ABC-1234</li>
                            <li className="mb-2"><span className="font-bold">Modelo:</span> Ford Fusion</li>
                            <li className="mb-2"><span className="font-bold">Montadora:</span> VW - VolksWagen </li>
                            <li className="mb-2"><span className="font-bold">Ano:</span> 2015</li>
                            <li className="mb-2"><span className="font-bold">Cor:</span> Prata</li>
                        </ul>
                        <ul>
                            <li className="mb-2"><span className="font-bold">VIN:</span> 9BWBH6BF8L4033336</li>
                            <li className="mb-2"><span className="font-bold">Valor atual:</span> R$ 108.858,00 </li>
                            <li className="mb-2"><span className="font-bold">Combustível:</span> Gasolina</li>
                            <li className="mb-2"><span className="font-bold">Código FIPE:</span> 005509-3</li>
                            <li className="mb-2"><span className="font-bold">Versão:</span> COMFORTLINE 1.0 TSI FLEX 5P AUT</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PesquisarVeiculoPlaca;