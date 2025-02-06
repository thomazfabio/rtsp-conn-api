import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;

export const useCreateCamFullDataStore = defineStore("cam-manage", () => {  
    async function createCamFullData(camData) {
        const endpoint = "manage_cam_device/create";
        console.log(camData)
        await api.post(endpoint, camData).then((response) => {
            console.log(response.status)
            return response;
        }).catch((error) => {
            console.log(error)
        });
       // const response = await api.post(endpoint, camData);
        
      //  console.log(response.status)
      //  return response;
    }
    
    return { createCamFullData };
    });