<template>
    <v-container>
        <v-expansion-panels>
            <v-expansion-panel title="Gerenciar Câmeras" text="Aqui você pode adicionar, remover e gerenciar câmeras.">
                <v-expansion-panel-text>
                    <v-row class="mb-3">
                        <v-col lg="3" md="4" sm="6">
                            <v-btn color="primary" block prepend-icon="mdi-clipboard-alert-outline"
                                @click="isManagerCam = !isManagerCam">Gerenciar
                                Câmeras</v-btn>
                        </v-col>

                        <v-col lg="3" md="4" sm="6">
                            <v-btn color="success" block prepend-icon="mdi-plus" to="/connectCam">Adicionar
                                Câmera</v-btn>
                        </v-col>
                    </v-row>

                    <searchAndManageCamV1 v-if="isManagerCam" />
                </v-expansion-panel-text>

            </v-expansion-panel>
            <v-expansion-panel title="Gerenciar Dispositivos base">
                <v-expansion-panel-text>

                    <v-row>
                        <v-col cols="10">
                            <span>Aqui vovê pode gerenciar seus dispositivos base.</span>
                        </v-col>
                        <v-col cols="2" class="text-right">
                            <v-btn  @click="isAlertInfoToUser" variant="tonal" color="info" density="compact" icon="mdi-information-variant"></v-btn>
                        </v-col>
                    </v-row>

                    <v-alert variant="tonal" v-if="alerts.alertInfoToUser.show" type="info" class="mt-2"
                        style="text-align: justify;">Dispositivo base é onde as câmeras se
                        conectam, como DVR, NVR ou uma câmera IP autônoma. Ele
                        armazena informações como fabricante, modelo e versão, mas cada câmera tem configurações
                        próprias quando são registradas em "Adicionar câmera".</v-alert>
                </v-expansion-panel-text>
                <v-expansion-panel-text>
                    <manageDeviceInfo />
                </v-expansion-panel-text>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>

<script setup>
import manageDeviceInfo from '@/components/manage_device_info/manageDeviceInfo.vue';
import searchAndManageCamV1 from '@/components/manageCam/searchAndManageCamV1.vue';

const isManagerDeviceInfo = ref(false);
const isManagerCam = ref(false);
const alerts = ref({ alertInfoToUser: { show: false } });

const isAlertInfoToUser = () => {
    alerts.value.alertInfoToUser.show = !alerts.value.alertInfoToUser.show;
};
</script>