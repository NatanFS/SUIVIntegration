import React from "react";
import {render} from "react-dom";

function App() {
  return (
    <div>Hello</div>
  );
}
  
export default App;

const appDiv = document.getElementById("app");
render(<App/>, appDiv)