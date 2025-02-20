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
            <v-expansion-panel title="Gerenciar Dispositivos"
                text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi, ratione debitis quis est labore voluptatibus! Eaque cupiditate minima">
            </v-expansion-panel>
        </v-expansion-panels>
    </v-container>
</template>

<script setup>
import manageDeviceInfo from '@/components/manage_device_info/manageDeviceInfo.vue';
import searchAndManageCamV1 from '@/components/manageCam/searchAndManageCamV1.vue';

const isManagerDeviceInfo = ref(false);
const isManagerCam = ref(false);
</script>