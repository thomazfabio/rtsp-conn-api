<template>
    <v-alert v-if="alerts.alertEdit.status" closable variant="outlined" :type="alerts.alertEdit.type" dismissible
        class="mb-4">
        {{ alerts.alertEdit.message }}
    </v-alert>
    <v-data-table-server :mobile="isMobile" v-model:items-per-page="itemsPerPage" :headers="headers"
        :items="serverItems" :items-length="totalItems" :loading="loading" :search="search" item-value="name"
        @update:options="loadItems" :items-per-page-options="itemsPerPageOptions" items-per-page-text="items por página"
        loading-text="Loading... Please wait">

        <template v-slot:top>
            <v-sheet border="md opacity-12" rounded="lg" class="pa-2">
                <v-row>
                    <v-col class="d-flex align-center" cols="12" lg="6" md="6" sm="6">
                        <h4 class="text-h5 font-weight-bold pl-1">Gerenciar dispositivo base</h4>
                    </v-col>
                    <v-col cols="12" lg="6" md="6" sm="6" class="d-flex flex-row-reverse">
                        <v-dialog v-model="dialogNewDevice" max-width="490" persistent opacity="0.1">
                            <template v-slot:activator="{ attrs }">

                                <v-btn :block="isMobile" color="success" v-bind="attrs" @click="dialogNewDevice = true"
                                    prepend-icon="mdi-plus-circle-outline" variant="flat">
                                    Adicionar
                                </v-btn>

                            </template>
                            <v-card>
                                <v-card-title>Adicionar novo dispositivo base</v-card-title>
                                <v-divider />
                                <v-container>
                                    <v-row>
                                        <v-col>
                                            <v-select v-model="deviceInfo.tipo" label="Tipo" variant="outlined"
                                                :items="deviceTypes" item-title="label" item-value="value">
                                            </v-select>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field v-model="deviceInfo.fabricante" label="Fabricante"
                                                variant="outlined"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field v-model="deviceInfo.modelo" label="Modelo"
                                                variant="outlined"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field v-model="deviceInfo.path_rtsp" label="Path RTSP"
                                                variant="outlined"></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field v-model="deviceInfo.versao" label="Versão"
                                                variant="outlined"></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-container>
                                <v-card-actions>
                                    <v-btn color="red" @click="dialogNewDevice = false">cancelar</v-btn>
                                    <v-btn color="green" :disabled="!isFormValid"
                                        @click="addDevice(deviceInfo)">salvar</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-col>
                </v-row>
            </v-sheet>
        </template>


        <template v-slot:item.actions="{ item }">
            <v-row class="d-flex justify-end">
                <v-dialog v-model="dialogEdit" max-width="490" persistent opacity="0.1">
                    <template v-slot:activator="{ props: activatorProps }">

                        <v-icon v-bind="activatorProps" color="primary" @click="openEditDialog(item)" small class="mr-4"
                            v-tooltip="'clique aqui para editar'">
                            mdi-pencil-outline
                        </v-icon>
                    </template>
                    <v-card>
                        <v-card-title>Editar dispositivo base</v-card-title>
                        <v-divider />
                        <v-container>
                            <v-row>
                                <v-col>
                                    <v-select :model-value="selectedItem.tipo" label="Tipo" variant="outlined"
                                        readonly></v-select>
                                </v-col>
                                <v-col>
                                    <v-text-field :model-value="selectedItem.fabricante"
                                        @update:model-value="(val) => inEdit.fabricante = val" label="Fabricante"
                                        variant="outlined"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field :model-value="selectedItem.modelo"
                                        @update:model-value="(val) => inEdit.modelo = val" label="Modelo"
                                        variant="outlined"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field :model-value="selectedItem.path_rtsp"
                                        @update:model-value="(val) => inEdit.path_rtsp = val" label="Path RTSP"
                                        variant="outlined"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field :model-value="selectedItem.versao"
                                        @update:model-value="(val) => inEdit.versao = val" label="Versão"
                                        variant="outlined"></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-card-actions>
                            <v-btn color="red" @click="dialogEdit = false">cancelar</v-btn>
                            <v-btn color="green" @click="editDevice(selectedItem)">salvar</v-btn>
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
                        <v-card-title>Tem certeza que deseja deletar o dispositivo?</v-card-title>
                        <v-card-text>
                            <v-row>
                                <v-col>
                                    Fabricante: {{ selectedItem.fabricante }}
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    Modelo: {{ selectedItem.modelo }}
                                </v-col>
                            </v-row>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="green" @click="dialogDelete = false">Cancelar</v-btn>
                            <v-btn color="red" @click="deleteDevice(selectedItem.id)">Deletar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-row>
        </template>

    </v-data-table-server>
</template>

<script setup>
import { ref } from 'vue'
import { useManageDeviceInfoStore } from '../..//stores/deviceManage/manageDeviceInfo'
const storeManageDevice = useManageDeviceInfoStore()
import { useDisplay } from 'vuetify'
import { computed } from 'vue'

const itemsPerPageOptions = [{ title: '5', value: 5 }, { title: '10', value: 10 }, { title: '15', value: 15 }, { title: '20', value: 20 }, { title: 'todos', value: -1 }];
const { xs } = useDisplay();
const isMobile = computed(() => xs.value);

const headers = [
    { title: 'Tipo', key: 'tipo', sortable: false },
    { title: 'Fabricante', key: 'fabricante', sortable: false },
    { title: 'Modelo', key: 'modelo', sortable: false },
    { title: 'Path RTSP', key: 'path_rtsp', sortable: false },
    { title: 'Versão', key: 'versao', sortable: false },
    { title: 'Ações', key: 'actions', sortable: false, align: 'end' }
]

const itemsPerPage = ref(5)
const totalItems = ref(0)
const loading = ref(false)
const search = ref('')
const serverItems = ref([])
const selectedItem = ref(null)
const dialogNewDevice = ref(false)
const dialogEdit = ref(false)
const dialogDelete = ref(false)
const inEdit = ref({})
const alerts = ref({ alertEdit: { status: false, type: '', message: "" } })
const deviceInfo = ref({ tipo: '', fabricante: '', modelo: '', path_rtsp: '', versao: '' })
const auxPage = ref(1)
const auxItemsPerPage = ref(5)

// mapeando para nomes mais amigaveis
const typeMapping = {
    ip_cam: "Câmera IP",
    dvr: "DVR",
    nvr: "NVR"
};


// devices types
const deviceTypes = [
    { label: "Selecione um tipo...", value: "", disabled: true },
    { label: 'Câmera IP', value: 'ip_cam' },
    { label: 'DVR', value: 'dvr' },
    { label: 'NVR', value: 'nvr' },
]


// Computed para verificar se todos os campos estão preenchidos
const isFormValid = computed(() => {
    return (
        deviceInfo.value.tipo !== "" &&
        deviceInfo.value.fabricante.trim() !== "" &&
        deviceInfo.value.modelo.trim() !== "" &&
        deviceInfo.value.path_rtsp.trim() !== "" &&
        deviceInfo.value.versao.trim() !== ""
    );
});


// dialogos de edição e exclusão

const openEditDialog = (item) => {
    selectedItem.value = item;
    dialogEdit.value = true;
    inEdit.value = { ...item }; // Copia os valores existentes
};

const openDeleteDialog = (item) => {
    selectedItem.value = item;
    dialogDelete.value = true;
};

// add device
const addDevice = async (item) => {
    const { tipo, fabricante, modelo, path_rtsp, versao } = item
    const data = { tipo, fabricante, modelo, path_rtsp, versao }
    alerts.value.alertEdit.status = false
    await storeManageDevice.createDeviceInfo(data).then((response) => {
        console.log(response)
        if (response.status === 201) {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'success'
            alerts.value.alertEdit.message = 'Dispositivo adicionado com sucesso!'
            deviceInfo.value = { tipo: '', fabricante: '', modelo: '', path_rtsp: '', versao: '' }
        } else {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'error'
            alerts.value.alertEdit.message = 'Erro ao adicionar dispositivo!'
        }
        dialogNewDevice.value = false
        loadItems({ auxPage, auxItemsPerPage })
    }).catch((error) => {
        alerts.value.alertEdit.status = true
        alerts.value.alertEdit.type = 'error'
        alerts.value.alertEdit.message = 'Erro ao adicionar dispositivo!'
        console.log(error)
        dialogNewDevice.value = false
    })
}

// edit device
const editDevice = async (item) => {
    const { id } = item
    const { fabricante, modelo, path_rtsp, versao } = inEdit.value
    const data = { id, fabricante, modelo, path_rtsp, versao }
    alerts.value.alertEdit.status = false
    await storeManageDevice.updateDeviceInfoById(data).then((response) => {
        if (response.status === 200) {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'success'
            alerts.value.alertEdit.message = 'Dispositivo editado com sucesso!'
        } else {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'error'
            alerts.value.alertEdit.message = 'Erro ao editar dispositivo!'
        }
        dialogEdit.value = false
        loadItems({ auxPage, auxItemsPerPage })
    }).catch((error) => {
        alerts.value.alertEdit.status = true
        alerts.value.alertEdit.type = 'error'
        alerts.value.alertEdit.message = 'Erro ao editar dispositivo!'
        console.log(error)
        dialogEdit.value = false
    })
}

// delete device
const deleteDevice = async (id) => {
    alerts.value.alertEdit.status = false
    await storeManageDevice.deleteDeviceInfoById(id).then((response) => {
        if (response.status === 200) {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'warning'
            alerts.value.alertEdit.message = 'Dispositivo deletado com sucesso!'
        } else {
            alerts.value.alertEdit.status = true
            alerts.value.alertEdit.type = 'error'
            alerts.value.alertEdit.message = 'Erro ao deletar dispositivo!'
        }
        dialogDelete.value = false
        loadItems({ auxPage, auxItemsPerPage })
    }).catch((error) => {
        alerts.value.alertEdit.status = true
        alerts.value.alertEdit.type = 'error'
        alerts.value.alertEdit.message = 'Erro ao deletar dispositivo!'
        console.log(error)
        dialogDelete.value = false
    })
}


const loadItems = async ({ page = auxPage.value, itemsPerPage = auxItemsPerPage.value } = {}) => {
    auxPage.value = page
    auxItemsPerPage.value = itemsPerPage
    loading.value = true
    const dataShowInTable = ['id', 'tipo', 'fabricante', 'modelo', 'path_rtsp', 'versao']
    await storeManageDevice.searchDeviceInfoAll().then((res) => {
        console.log(res.data)
        const dataFilter = res.data.map((item) => {
            return dataShowInTable.reduce((acc, key) => {
                acc[key] = key === "tipo" ? typeMapping[item[key]] || item[key] : item[key];
                return acc;
            }, {});
        });
        // Paginação manual (caso a API não pagine automaticamente)
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = itemsPerPage === -1 ? totalItems.value : startIndex + itemsPerPage;
        serverItems.value = dataFilter.slice(startIndex, endIndex);
        totalItems.value = res.data.length
        loading.value = false
    })
}
</script>

<style scoped></style>