import React from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.css';
import Home from "./pages/Home";
import ProtectedRoute from "./routes/ProtectedRoute";
import Registration from "./pages/Registration";
import Login from "./pages/Login";
import PostDetail from "./pages/PostDetail";

function App() {
  const data = { message: "Hello, Context!" };
  return (
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
        <Route path="/post/:postId/" element={
          <ProtectedRoute>
            <PostDetail/>
          </ProtectedRoute>
        }/>
      </Routes>
  );
}

export default App;
