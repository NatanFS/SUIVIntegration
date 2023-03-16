import React from "react";

const Equipments = ({ equipments }) => {
  return (
    <div className="mx-auto">
      <h2 className="text-2xl font-bold mb-4">Acessórios</h2>
      {equipments.map((equipment) => (
        <div
          key={equipment.id}
          className="flex items-center justify-between py-2 border-b"
        >
          <div>
            <h3 className="text-lg font-medium">{equipment.description}</h3>
            <p className="text-gray-500">{equipment.is_series ? "Série" : ""}</p>
          </div>
          <div>
            <p className="text-gray-500">{equipment.year}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Equipments;