import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home";
import ProtectedRoute from "./routes/ProtectedRoute";
import Registration from "./pages/Registration";
import Login from "./pages/Login";

export const Context = React.createContext();
function App() {
  const data = { message: "Hello, Context!" };
  return (
    <Context.Provider value={data}>
      <Routes>
        <Route path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="/login/" element={<Login/>} />
        <Route path="/register/" element={<Registration/>} />
      </Routes>
    </Context.Provider>
  );
}

export default App;
