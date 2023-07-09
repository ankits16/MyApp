import axios from 'axios';
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export const BASE_URL = 'http://localhost:8000/api'
const axiosService = axios.create({
    baseURL : BASE_URL,
    headers : {
        "Content-Type": "application/json"
    },
})

axiosService.interceptors.request.use(async (config) =>{
    //object-destructuring syntax to extract property values from an object
    const { accessToken } = JSON.parse(localStorage.getItem('auth'))
    config.headers.Authorization = `Bearer ${accessToken}`;
    return config
});

axiosService.interceptors.response.use(
    (res) => Promise.resolve(res),
    (err) => Promise.reject(err),
);

const refreshAuthLogic = async (failedRequest) => {
    const {refresh} = JSON.parse(localStorage.getItem("auth"))
    return axios.post('/auth/refresh/', null, {
        baseURL: BASE_URL,
        headers : {
            Authorization : `Bearer ${refresh}`
        },
    })
    .then((resp) => {
        const {access, refresh} = resp.data;
        failedRequest.response.config.headers["Authorization"] = `Bearer ${access}`
        localStorage.setItem("auth", JSON.stringify({access, refresh}));
    })
    .catch(()=>{
        localStorage.removeItem("auth")
    });
};

createAuthRefreshInterceptor(axiosService, refreshAuthLogic)

export function fetcher(url) {
    return axiosService.get(url).then((response) => response.data);
}

export default axiosService;