<template>
  <v-card variant="tonal" class="pa-4 d-flex flex-row-reverse">
    <div style="width: 480px">
      <v-row>
        <v-col cols="12" >
          <v-row>
            <v-col>
              <span> Grupo : {{ grupo }} </span>
            </v-col>
            <v-col>
              <span class="d-flex justify-center">
                Câmera : {{ camName }}</span
              >
            </v-col>

            <v-col>
              <span class="d-flex flex-row-reverse">
                Canal: : {{ camChennel }}</span
              >
            </v-col>
          </v-row>
          <div >
            <div>
              <!-- Conecta ao endpoint /stream sem passar a URL -->
              <img
                :src="streaming"
                alt="Stream ao vivo"
                style="max-width: 100%; height: auto"
              />
              {{ camUrl }}
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from "vue";
import { defineProps } from "vue"; 
const streaming = "http://localhost:5000/visualizer_cam_v2/stream?url=rtsp%3A%2F%2Fadmin%3A227802%40192.168.15.150%3A554%2Fcam%2Frealmonitor%3Fchannel%3D1%26subtype%3D0"
const props = defineProps({
  camUrl: String,
  camName: String,
  grupo: String,
  camChennel: String,
});
</script>
