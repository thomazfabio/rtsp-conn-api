import { defineStore } from "pinia";

export const useCamUrlMenageStore = defineStore("cam-url-menage", () => {
  const camUrl = ref("http://localhost:5000/video_feed");
  const setCamUrl = (url) => {
    camUrl.value = url;
  };
  function testeUrlRtsp(payload) {
    console.log(payload);
  }
  return {
    camUrl,
    setCamUrl,
    testeUrlRtsp,
  };
});
