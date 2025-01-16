import axios from "axios";

const api_url_rtsp = axios.create({
    baseURL: "http://localhost:5000",
});

export default api_url_rtsp;