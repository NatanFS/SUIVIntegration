import React from "react";

const RevisionPlan = ({ revisionPlan }) => {
    return (
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Plano de revisão
                </h3>
            </div>
            <div className="border-t border-gray-200">
                <dl>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Quilômetros</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {revisionPlan.kilometers}
                        </dd>
                    </div>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Meses</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {revisionPlan.months}
                        </dd>
                    </div>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Preço</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {revisionPlan.full_price.toLocaleString('pt-br', { style: 'currency', currency: 'BRL' })}
                        </dd>
                    </div>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Preço parcelado</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            {revisionPlan.parcel_price.toLocaleString('pt-br', { style: 'currency', currency: 'BRL' })}
                        </dd>
                    </div>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Partes modificadas</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            <ul className="border border-gray-200 rounded-md divide-y divide-gray-200">
                                {revisionPlan.changed_parts.map((part, index) => (
                                    <li
                                        key={index}
                                        className="pl-3 pr-4 py-3 flex items-center justify-between text-sm"
                                    >
                                        <div className="w-0 flex-1 flex items-center">
                                            <span className="ml-2 flex-1 w-0 truncate">
                                                {part.description} x {part.amount}
                                            </span>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </dd>
                    </div>
                    <div className="px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt className="text-sm font-medium text-gray-500">Inspeções</dt>
                        <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                            <ul className="border border-gray-200 rounded-md divide-y divide-gray-200">
                                {revisionPlan.inspections.map((inspection, index) => (
                                    <li
                                        key={index}
                                        className="pl-3 pr-4 py-3 flex items-center justify-between text-sm"
                                    >
                                        <div className="w-0 flex-1 flex items-center">
                                            <span className="ml-2 flex-1 w-0 truncate">
                                                {inspection}
                                            </span>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </dd>
                    </div>
                </dl>
            </div>
        </div>
    );
}

export default RevisionPlan;