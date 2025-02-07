import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;

export const useSearchCamStore = defineStore("search-cam", () => {
    async function searchCamByUserId(user_id) {
        const id = user_id.user_id;

        const endpoint = "manage_cam_device/list_by_user_id"
    
        await api.get(endpoint, { params: { user_id: id} }).then((response) => {
            console.log(response.status);
            console.log(response.data);
            console.log("response");
            return response;

        }).catch((error) => {
            console.log(error);
            console.log("error");
            throw error; // Garante que o erro seja propagado para ser capturado no `catch`
        });
        // const response = await api.post(endpoint, camData);

        //  console.log(response.status)
        //  return response;
    }

    return { searchCamByUserId };
}
);