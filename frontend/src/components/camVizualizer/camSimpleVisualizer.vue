<template>
  <v-card variant="tonal" class="pa-4 d-flex flex-row-reverse">
    <div style="width: 640px">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-col>
              <span> Grupo / Local : {{ dadosStrening.grupo }} </span>
            </v-col>
            <v-col>
              <span class="d-flex justify-center">
                Câmera : {{ dadosStrening.camName }}</span
              >
            </v-col>

            <v-col>
              <span class="d-flex flex-row-reverse">
                Canal: : {{ dadosStrening.camChennel }}</span
              >
            </v-col>
          </v-row>
          <div style="width: 640px; height: 640px;">
            <div>
    <h1>Stream de Vídeo</h1>
    <img src="http://localhost:5000/visualizer_cam/simple">
 
            </div>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from "vue";

const dadosStrening = ref({
  camUrl: "http://",
  camName: "Cam 1",
  grupo: "Trabalho",
  camChennel: "1",
});


</script>
