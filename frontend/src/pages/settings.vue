<template>

    <v-container>
        <v-card>
            <v-card-title>Configurações gerais</v-card-title>
            <v-divider />
            <v-row>
                <v-col>
                    <v-btn color="primary" @click="isManagerCam = !isManagerCam">Gerenciar Câmeras</v-btn>
                </v-col>

                <v-col>
                    <v-btn color="primary" @click="isManagerDeviceInfo = !isManagerDeviceInfo">Gerenciar
                        Dispositivos</v-btn>
                </v-col>
            </v-row>
            <v-divider />
            <v-container>

                <searchAndManageCamV1 v-if="isManagerCam" />
                <manageDeviceInfo v-if="isManagerDeviceInfo" />
            </v-container>
        </v-card>
    </v-container>

</template>

<script setup>
import manageDeviceInfo from '@/components/manage_device_info/manageDeviceInfo.vue';
import searchAndManageCamV1 from '@/components/manageCam/searchAndManageCamV1.vue';

const isManagerDeviceInfo = ref(false);
const isManagerCam = ref(false);
</script>