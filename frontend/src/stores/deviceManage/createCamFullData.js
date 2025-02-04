import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;

export const useCreateCamFullDataStore = defineStore("cam-manage", () => {  
    async function createCamFullData(camData) {
        const endpoint = "create_cam_full_data";
        console.log(camData)
       // const response = await api.post(endpoint, camData);
        
      //  console.log(response.status)
      //  return response;
    }
    
    return { createCamFullData };
    });