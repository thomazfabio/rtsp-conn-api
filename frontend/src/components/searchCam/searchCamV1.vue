<template>
    <div class="text-h5 mb-3">Aqui você pode listar e encontrar suas câmeras</div>
    <v-toolbar bordder density="compact">
        <v-btn color="primary" @click="setSearchType('all')">
            buscar todas
        </v-btn>

        <v-btn color="primary" @click="setSearchType('byGroup')">
            buscar por grupo
        </v-btn>

    </v-toolbar>

    <v-container v-if="searchType" class="pl-0 pr-0">
        <v-row v-if="searchType == 'all'">
            <v-col>
                <v-btn color="success" @click="searchCameras('all')" prepend-icon="mdi-magnify" class="mb-3">
                    listar todas as câmeras
                </v-btn>
                <v-data-table-server :items-length="0" item-key="name" loading-text="Loading... Please wait"
                    loading></v-data-table-server>
            </v-col>
        </v-row>
        <v-card v-else-if="searchType == 'byGroup'">
            <v-row>
                <v-col>
                    <v-select label="Selecione um grupo" item-text="name" item-value="id" return-object></v-select>
                </v-col>
            </v-row>
        </v-card>

    </v-container>

</template>

<script setup>
import { ref } from 'vue';
const searchType = ref(null);
const loading = ref(false);
const cardsActive = ref({ cardSearchAll: false, cardSearchByGroup: false });

function setSearchType(type) {
    searchType.value = type;
    console.log(searchType.value);
}

function searchCameras(type) {
    if (type == 'all') {
        cardsActive.value.cardSearchAll = true;
        loading.value = true;
        console.log('searching all cameras');
    } else if (type == 'byGroup') {
        searchCamerasByGroup();
    }
}

</script>