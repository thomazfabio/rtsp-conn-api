<template>
  <v-card variant="tonal" class="pa-4 d-flex flex-row-reverse">
    <div style="width: 480px">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col>
              <span> Grupo : {{ grupo }} </span>
            </v-col>
            <v-col>
              <span class="d-flex justify-center"> Câmera : {{ camName }}</span>
            </v-col>

            <v-col>
              <span class="d-flex flex-row-reverse">
                Canal: : {{ camChennel }}</span
              >
            </v-col>
          </v-row>
          <div>
            <div>
              <!-- Conecta ao endpoint /stream sem passar a URL -->
              <img
                v-if="isStreaming"
                :src="streamingURL"
                alt="Stream ao vivo"
                style="max-width: 100%; height: auto"
              />
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script setup>
import { ref, computed } from "vue";
import { defineProps } from "vue";
import { defineExpose } from "vue";
import { useVisualizerCamV2Store } from "../../stores/controlStream/visualizerCamV2";
const visualizerCamV2Store = useVisualizerCamV2Store();
const isStreaming = ref(true);
const refreshStream = ref(null);
const baseURL = "http://localhost:5000";


const props = defineProps({
  camUrl: String,
  camName: String,
  grupo: String,
  camChennel: String,
  visualizerUrl: String,
});

// Gerar a URL de streaming corretamente
const streamingURL = computed(() => {
  return `${baseURL}${props.visualizerUrl}?url=${encodeURIComponent(
    props.camUrl
  )}&refresh=${refreshStream.value}`;
});



// url da camera
const camUrl = ref(props.camUrl);

// metodos de controle
const stopStream = async () => {
  const response = await visualizerCamV2Store.stopStream(camUrl.value);
  if (response.status == 200) {
    console.log(streamingURL.value);
    isStreaming.value = false;
  }
};

const startStream = async () => {
  const response = await visualizerCamV2Store.startStream(camUrl.value);
  if (response.status === 200) {
    refreshStream.value = Date.now(); // Força uma mudança na URL
    console.log(streamingURL.value);
    isStreaming.value = true;
  }
};

// Expor metodos
defineExpose({
  stopStream,
  startStream,
});
</script>
