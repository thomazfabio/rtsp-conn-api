import { defineStore } from "pinia";
import api_url_rtsp from "@/services/api";
import { ref } from "vue";

export const useCamUrlMenageStore = defineStore("cam-url-menage", () => {
  const camUrl = { url: "" };
  const cam = ref({
    id: "",
    user_id: "",
    device_info: "",
    cam_name: "",
    cam_group: "",
    url: "",
    teste: false,
    status: "pendente",
  });
  function setCamUrl(payload) {
    camUrl.url = payload;
  }
  async function testeUrlRtsp(payload) {
    const url = { url: payload };
    const status = await api_url_rtsp.post("/url_rtsp/teste_url", url);
    console.log(status.data);
    cam.value.status = status.data.status;
    return status;
  }
  return {
    cam,
    setCamUrl,
    testeUrlRtsp,
  };
});
