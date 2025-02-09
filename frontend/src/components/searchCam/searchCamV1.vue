<template>
    <div class="text-h5 mb-3">Aqui você pode listar e encontrar suas câmeras</div>
    <v-toolbar bordder density="compact">
        <v-btn color="primary" @click="setSearchType('all')" variant="text">
            buscar todas
        </v-btn>
        <v-btn color="primary" @click="searchCamByUserId()" variant="text">
            Atualizar
        </v-btn>
    </v-toolbar>
    <v-alert v-if="alerts.alertDelete.status" :type="alerts.alertDelete.type" dismissible closable class="mt-2"
        variant="outlined">
        {{ alerts.alertDelete.message }}
    </v-alert>
    <v-container v-if="searchType" class="pl-0 pr-0">
        <v-row v-if="searchType == 'all'">
            <v-col>
                <v-data-table-server :headers="headers" color="blue" :items-length="0" item-key="name"
                    loading-text="Loading... Please wait" :loading="loading" :items="serverItems">
                    <template v-slot:item.full_cam_url_stream="{ item }">
                        {{ truncateUrl(item.full_cam_url_stream) }}
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <v-dialog v-model="dialogEdit" max-width="290" persistent opacity="0.1">
                            <template v-slot:activator="{ props: activatorProps }">

                                <v-icon v-bind="activatorProps" color="primary" @click="editCam(item.id)" small
                                    class="mr-4" v-tooltip="'clique aqui para editar'">
                                    mdi-pencil-outline
                                </v-icon>
                            </template>
                            <v-card>
                                <v-card-title>Editar Câmera</v-card-title>
                                <v-card-text>
                                    {{ item.id }}
                                </v-card-text>
                                <v-card-actions>
                                    <v-btn color="red" @click="dialogEdit = false">Fechar</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                        <v-dialog v-model="dialogDelete" max-width="450" persistent opacity="0.1">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-icon @click="openDeleteDialog(item)" v-bind="activatorProps" color="red" small
                                    v-tooltip="'clique aqui para deletar'">
                                    mdi-trash-can-outline
                                </v-icon>
                            </template>
                            <v-card>
                                <v-card-title>Tem certeza que deseja deletar a câmera?</v-card-title>
                                <v-card-text>
                                    <v-row>
                                        <v-col>
                                            ID: {{ selectedItem.id }}
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            Câmera: {{ selectedItem.cam_name }}
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            Grupo: {{ selectedItem.grupo }}
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions>
                                    <v-btn color="green" @click="dialogDelete = false">Cancelar</v-btn>
                                    <v-btn color="red" @click="deleteCam(selectedItem.id)">Deletar</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>

                    </template>
                </v-data-table-server>
            </v-col>
        </v-row>
    </v-container>

</template>

<script setup>
import { ref, watch } from 'vue';
import { useSearchCamStore } from '../../stores/deviceManage/searchCam';
const searchType = ref(null);
const loading = ref(false);
const alerts = ref({ alertDelete: { status: false, message: '', type: '' }, alertEdit: { status: false, message: '', type: '' } });
const dialogEdit = ref(false);
const dialogDelete = ref(false);
const selectedItem = ref(null);

const storeSearchCam = useSearchCamStore();
const serverItems = ref([]);
const headers = [
    { title: 'Nome', key: 'cam_name', align: 'start', sortable: false },
    { title: 'ID', key: 'id' },
    { title: 'Grupo / Local', key: 'grupo' },
    { title: 'Status', key: 'cam_status' },
    { title: 'URL de Streaming', key: 'full_cam_url_stream' },
    { title: 'Ações', key: 'actions', sortable: false, align: 'end' },
];

function setSearchType(type) {
    searchType.value = type;
}

watch(searchType, (newValue, oldValue) => {
    if (newValue == 'all') {
        searchCamByUserId();
    } else if (newValue == 'byGroup') {

    }
});

const truncateUrl = (url) => {
    if (url.length > 50) {
        return url.substring(0, 50) + '...';
    }
    return url;
};

async function searchCamByUserId() {
    loading.value = true;
    const dataShowInTable = ["id", "cam_name", "grupo", "cam_status", "full_cam_url_stream"];
    const id = { "user_id": 1 };
    await storeSearchCam.searchCamByUserId(id).then((res) => {
        const dataFilter = res.data.map((item) => {
            return dataShowInTable.reduce((acc, key) => {
                acc[key] = item[key];
                return acc;
            }, {});
        });
        serverItems.value = dataFilter;
        loading.value = false;
    });
}

// dialogos de edição e exclusão

const openEditDialog = (item) => {
    selectedItem.value = item;
    dialogEdit.value = true;
};

const openDeleteDialog = (item) => {
    selectedItem.value = item;
    dialogDelete.value = true;
};

async function editCam(item) {

}

const isDialogDelete = () => {
    dialogDelete.value = true;
}

async function deleteCam(id) {
    alerts.value.alertDelete.status = false;
    await storeSearchCam.deleteCamById(id).then((res) => {
        console.log(res.status);
        if (res.status == 200) {
            alerts.value.alertDelete.type = 'warning';
            alerts.value.alertDelete.status = true;
            alerts.value.alertDelete.message = 'Câmera deletada com sucesso!';
            dialogDelete.value = false;
            searchCamByUserId();
        }
        if (res.status == 500) {
            alerts.value.alertDelete.type = 'error';
            alerts.value.alertDelete.status = true;
            alerts.value.alertDelete.message = 'Erro ao deletar câmera!';
            dialogDelete.value = false;
        }
    }).catch((err) => {
        console.log(err);
        alerts.value.alertDelete.type = 'error';
        alerts.value.alertDelete.status = true;
        alerts.value.alertDelete.message = 'Erro ao deletar câmera!';
        dialogDelete.value = false;
    });
}
</script>