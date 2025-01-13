<template>
  <v-container>
    <v-row>
      <v-col xl="8">
        <h1>Assistente para conectar câmeras a api via RTSP</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col xl="8">
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
