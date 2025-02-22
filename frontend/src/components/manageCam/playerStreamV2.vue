<template>
    <v-container class="pb-0 mb-0">
        <v-img :src="url" contain class="w-100 h-100" />
    </v-container>
    <!-- controles do stream -->
    <v-container class="pt-0 mt-0">
        <v-row class="d-flex justify-center">
            <v-col cols="4"> <v-btn color="green" prepend-icon="mdi-play"  size="small" variant="text">play</v-btn>
            </v-col>
            <v-col cols="4" class="d-flex justify-center"> <v-btn color="red" prepend-icon="mdi-stop"  size="small" variant="text">stop</v-btn>
            </v-col>
            <v-col cols="4" class="d-flex justify-end"> <v-btn color="blue" prepend-icon="mdi-refresh"  size="small" variant="text">refresh</v-btn>
            </v-col>
        </v-row>
    </v-container>
    <v-divider /> 
</template>

<script setup>
import { ref, computed } from 'vue'
const url = 'http://localhost:5000/visualizer_cam_v2/stream?url=rtsp%3A%2F%2Fadmin%3A227802%40192.168.15.150%3A554%2Fcam%2Frealmonitor%3Fchannel%3D1%26subtype%3D0&refresh=null';

</script>
<style scoped></style>