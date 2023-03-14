import React, { useState } from "react";
import { render } from "react-dom";
import PesquisarVeiculoPlaca from "./pages/PesquisarVeiculoPlaca";

function App() {
  
  return (
    <PesquisarVeiculoPlaca></PesquisarVeiculoPlaca>
  );
}

export default App;

const appDiv = document.getElementById("app");
render(<App />, appDiv)