import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;



export const useVisualizerCamV2Store = defineStore("control-stream", () => {
  async function startStream(camUrl) {
    const url = { url: camUrl };
    console.log(url.url)

    const endpoint = "visualizer_cam_v2/start_stream";
    const response = await api.post(endpoint, { url_rtsp: url.url });

    console.log(response.status)
    return response;
  }

  async function stopStream(camUrl) {
    const url = { url: camUrl };
    console.log(url.url)
    const endpoint = "visualizer_cam_v2/stop_stream";
    const response = await api.post(endpoint, { url: url.url });

    console.log(response.status)
    return response;
  }

  return { startStream, stopStream };
});
