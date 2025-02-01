import axios from "axios";
const api_url_rtsp = axios.create({
    baseURL: "http://localhost:5000",
});

// export api_url_rtsp e api_url;
export { api_url_rtsp };
