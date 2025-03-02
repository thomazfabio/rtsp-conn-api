<template>
  <v-card class="mx-auto">
    <playerStreamV2 :stream-url="streamUrl" :url-rtsp="urlRtsp"/>

    <v-card-title>
      Grupo: {{ camGrup }}
    </v-card-title>

    <v-card-subtitle>
      Local: {{ camName }}
    </v-card-subtitle>

    <v-card-subtitle>
      Canal: {{ camChannel }}
    </v-card-subtitle>

    <v-card-actions>
      <v-btn color="orange-lighten-2" text="Processar com IA"></v-btn>

      <v-spacer></v-spacer>

      <v-btn :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="show = !show"></v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>

        <v-card-text>
          Aqui você controla todas as opçoes de IA disponiveis para este video.
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import playerStreamV2 from '@/components/manageCam/playerStreamV2.vue'

defineProps({
  streamUrl: String,
  urlRtsp: String,
  camName: String,
  camGrup: String,
  camChannel: String,
  camType: String,
});

const show = ref(false)
</script>