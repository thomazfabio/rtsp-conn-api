<template>
  <v-container>
    <v-row>
      <v-col xl="8">
        <h1>Assistente para conectar câmera via RTSP a api</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" xl="8">
        <ConnectAddCam/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import ConnectAddCam from "../components/ConnectAddCAM.vue";
import { ref, watch } from "vue";
const selectedDeviceType = ref(null); // Estado gerenciado na página
</script>
