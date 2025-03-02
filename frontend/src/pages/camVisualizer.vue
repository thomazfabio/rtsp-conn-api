<template>
  <v-container>
    <v-row>
      <v-col v-for="(cam, index) in allCamDData" :key="index" cols="12" lg="4" md="6">
        <visualizeCamV2  :stream-url="cam.full_cam_url_stream" :cam-name="cam.cam_name" :cam-grup="cam.grupo" :cam-channel="cam.device_config.channel" :url-rtsp="cam.full_cam_url_rtsp"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import visualizeCamV2 from '../components/manageCam/visualizeCamV2.vue';
import { useSearchCamStore } from '../stores/deviceManage/searchCam';


const searchCamStore = useSearchCamStore();
const allCamDData = ref([]);


async function searchCamByUserId() {
  const user_id = {user_id: 1};
  try {
    const res = await searchCamStore.searchCamByUserId(user_id);

    // Adiciona os elementos individualmente caso res.data seja um array
    if (Array.isArray(res.data)) {
      allCamDData.value.push(...res.data);
    } else {
      allCamDData.value.push(res.data);
    }

    console.log(allCamDData.value);
  } catch (err) {
    console.error("Erro ao buscar câmeras:", err);
  }
}

// Chama a função assim que o componente for montado
onMounted(() => {
  searchCamByUserId();
});
</script>
