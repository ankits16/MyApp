import axios from "axios";
import { useNavigate } from "react-router-dom";
import { BASE_URL } from "../helpers/axios";

const useUserActions = () => {
  const navigate = useNavigate();
  return {
    login,
    register,
    logout,
  };

  function login(data) {
    return axios
      .post(`${BASE_URL}/auth/login/`, data)
      .then((res) => {
        setUserData(res.data);
        navigate("/");
      })
  }

  function logout() {
    localStorage.removeItem("auth");
    navigate("/login");
  }

  function register() {}

  function setUserData(data) {
    localStorage.setItem(
      "auth",
      JSON.stringify({
        access: data.access,
        refresh: data.refresh,
        user: data.user,
      })
    );
  }
};

function getUser() {
  const auth = JSON.parse(localStorage.getItem("auth"));
  if (auth !== null) {
    return auth.user;
  }
  return null;
}

// Get the access token
function getAccessToken() {
  const auth = JSON.parse(localStorage.getItem("auth"));
  return auth.access;
}
// Get the refresh token
function getRefreshToken() {
  const auth = JSON.parse(localStorage.getItem("auth"));
  return auth.refresh;
}

export { useUserActions, getUser, getAccessToken, getRefreshToken };
