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
import { ref, watch } from 'vue';
import { useSearchCamStore } from '../../stores/deviceManage/searchCam';
const searchType = ref(null);
const loading = ref(false);
const cardsActive = ref({ cardSearchAll: false, cardSearchByGroup: false });
const storeSearchCam = useSearchCamStore();

function setSearchType(type) {
    searchType.value = type;
    console.log(searchType.value);
}

watch(searchType, (newValue, oldValue) => {
    if (newValue == 'all') {
        searchCamByUserId();
    } else if (newValue == 'byGroup') {

    }
});

async function searchCamByUserId() {
    try {
        const id = {"user_id": 1};
        const response = await storeSearchCam.searchCamByUserId(id);
        console.log(response);
    } catch (error) {
        console.log(error);
    } finally {
        loading.value = false;
    }
}
</script>