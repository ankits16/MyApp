import axios from "axios";
import createAuthRefreshInterceptor from "axios-auth-refresh";
import {
  getAccessToken,
  getRefreshToken,
  getUser,
} from "../hooks/user.actions";

export const BASE_URL = "http://localhost:8000/api";
const axiosService = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosService.interceptors.request.use(async (config) => {
  //object-destructuring syntax to extract property values from an object
  config.headers.Authorization = `Bearer ${getAccessToken()}`;
  return config;
});

axiosService.interceptors.response.use(
  (res) => Promise.resolve(res),
  (err) => Promise.reject(err)
);

const refreshAuthLogic = async (failedRequest) => {
  return axios
    .post(
      "/auth/refresh/",
      {
        refresh: getRefreshToken(),
      },
      {
        baseURL: BASE_URL,
      }
    )
    .then((resp) => {
      const { access } = resp.data;
      failedRequest.response.config.headers[
        "Authorization"
      ] = `Bearer ${access}`;
      localStorage.setItem(
        "auth",
        JSON.stringify({ access, refresh: getRefreshToken(), user: getUser() })
      );
    })
    .catch(() => {
      localStorage.removeItem("auth");
    });
};

createAuthRefreshInterceptor(axiosService, refreshAuthLogic);

export function fetcher(url) {
  console.log(`*** fetcher is called ${Date.now()}`);
  return axiosService.get(url).then((response) => response.data);
}

export default axiosService;
