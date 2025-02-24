<template>
    <v-container class="mb-0 pb-0">
        <v-img :src="url" contain class="w-100 h-100" />
    </v-container>
    <!-- controles do stream -->
    <v-container class="pt-0 mt-0">
        
            <v-sheet color="blue-grey-darken-4" class="d-flex justify-center">
                <v-btn color="green" prepend-icon="mdi-play" size="x-small" stacked variant="plain"></v-btn>

                <v-btn color="red" prepend-icon="mdi-stop" size="x-small" stacked variant="plain"></v-btn>

                <v-btn color="blue" prepend-icon="mdi-refresh" size="x-small" stacked variant="plain"></v-btn>
            </v-sheet>
        
    </v-container>
    <v-divider />
</template>

<script setup>
import { ref, computed } from 'vue'
const url = 'http://localhost:5000/visualizer_cam_v2/stream?url=rtsp%3A%2F%2Fadmin%3A227802%40192.168.15.150%3A554%2Fcam%2Frealmonitor%3Fchannel%3D1%26subtype%3D0&refresh=null';

</script>
<style scoped></style>