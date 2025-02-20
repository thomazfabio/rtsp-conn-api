import { defineStore } from "pinia";
import { api_url_rtsp } from "../../services/api";
const api = api_url_rtsp;

export const useManageDeviceInfoStore = defineStore("manage-device-info", () => {

    async function searchDeviceInfoAll() {
        const endpoint = "device_info/get_all";
        try {
            const response = await api.get(endpoint);
            return response;
        } catch (error) {
            console.error("Erro na requisição:", error);
            throw error;
        }
    }

    async function searchDeviceInfoByUserId(user_id) {
        const id = user_id.user_id;
        const endpoint = "device_info/list_by_user_id";

        try {
            const response = await api.get(endpoint, { params: { user_id: id } });
            return response;  // Agora realmente retorna os dados
        } catch (error) {
            console.error("Erro na requisição:", error);
            throw error; // Propaga o erro para ser tratado externamente
        }
    }

    async function deleteDeviceInfoById(device_id) {
        const endpoint = "device_info/delete";
        try {
            const response = await api.delete(endpoint, { params: { id: device_id } });
            return response;
        } catch (error) {
        
            throw error;
        }
    }

    async function updateDeviceInfoById(data) {
        const endpoint = "device_info/update";
        try {
            const response = await api.put(endpoint, data );
            return response;
        } catch (error) {
            throw error;
        }
    }

    return { searchDeviceInfoAll, searchDeviceInfoByUserId, deleteDeviceInfoById, updateDeviceInfoById };
}
);
