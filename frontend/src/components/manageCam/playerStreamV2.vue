<template>
    <v-container class="mb-0 pb-0">
        <v-img v-if="isStreaming" :src="streamurl" contain class="w-100 h-100" />
    </v-container>
    <!-- controles do stream -->
    <v-container class="pt-0 mt-0">

        <v-sheet color="blue-grey-darken-4" class="d-flex justify-center">
            <v-btn class="pa-0" color="green" prepend-icon="mdi-play-speed" height="50" stacked variant="plain"
                @click="startStream(urlRtsp)"></v-btn>

            <v-btn class="pa-0" color="red" prepend-icon="mdi-stop-circle-outline" height="50" stacked
                variant="plain" @click="stopStream(stream_id)"></v-btn>

            <v-btn class="pa-0" color="blue" prepend-icon="mdi-refresh" height="50" stacked variant="plain"></v-btn>
        </v-sheet>

    </v-container>
   
</template>

<script setup>
import { defineProps, onMounted } from 'vue';
import { ref } from 'vue';
import { useVisualizerCamV2Store } from '@/stores/controlStream/visualizerCamV2';

const visualizerCamV2Store = useVisualizerCamV2Store();
const isStreaming = ref(true);
const refreshStream = ref(null);

const props = defineProps({
    urlRtsp: String,
});

//essa url que o backend devolve
const streamurl = ref(null);
const stream_id = ref(null);


async function startStream(x) {
    const urlRtsp = x;
    try {
        const  response = await visualizerCamV2Store.startStream(urlRtsp);
        streamurl.value = response.data.stream_url;
        stream_id.value = response.data.stream_id;
        console.log(response.data);
    } catch (err) {
        console.error("Erro ao iniciar stream:", err);
    }
}

async function stopStream(x) {
    const urlRtsp = x;
    try {
        await visualizerCamV2Store.stopStream(urlRtsp);
        isStreaming.value = false;
    } catch (err) {
        console.error("Erro ao parar stream:", err);
    }
}

</script>
<style scoped></style>