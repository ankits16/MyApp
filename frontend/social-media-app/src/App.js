import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";

export const Context = React.createContext();
function App() {
  const data = { message: "Hello, Context!" };
  return (
    <Context.Provider value={data}>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Context.Provider>
  );
}

export default App;
