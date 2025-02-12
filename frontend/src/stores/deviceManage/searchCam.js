import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;

export const useSearchCamStore = defineStore("search-cam", () => {
    async function searchCamByUserId(user_id) {
        const id = user_id.user_id;
        const endpoint = "manage_cam_device/list_by_user_id";

        try {
            const response = await api.get(endpoint, { params: { user_id: id } });
            return response;  // Agora realmente retorna os dados
        } catch (error) {
            console.error("Erro na requisição:", error);
            throw error; // Propaga o erro para ser tratado externamente
        }
    }

    async function deleteCamById(cam_id) {
        const endpoint = "manage_cam_device/delete";
        try {
            const response = await api.delete(endpoint, { params: { id: cam_id } });
            return response;
        } catch (error) {
        
            throw error;
        }
    }

    async function updateCamById(data) {
        const endpoint = "manage_cam_device/update";
        try {
            const response = await api.put(endpoint, data );
            return response;
        } catch (error) {
            throw error;
        }
    }

    return { searchCamByUserId, deleteCamById, updateCamById };
}
);