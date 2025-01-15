<template>
  <v-stepper
    hide-actions
    ref="stepper"
    :items="['Passo 1', 'Passo 2', 'Passo 3', 'Passo 4']"
    v-model="step"
  >
    <template v-slot:item.1>
      <v-card title="Selecione o tipo de dispositivo:" flat>
        <v-row>
          <v-container>
            <v-col cols="6">
              <v-select
                label="Selecione o tipo de dispositivo que deseja conectar"
                :items="[
                  'DVR',
                  'Camera IP',
                  'URL da Web',
                  'Inserir manualmente',
                  'Outro',
                ]"
                variant="outlined"
                v-model="selectedDeviceType"
              ></v-select>
            </v-col>
          </v-container>
        </v-row>
      </v-card>
    </template>

    <template v-slot:item.2>
      <v-card title="Detalhes de Conexão" flat>
        <v-form>
          <template v-if="selectedDeviceType === 'DVR'">
            <v-card-subtitle>Informações do DVR</v-card-subtitle>
            <v-divider class="mt-3 mb-3" />
            <v-container>
              <!-- Configurações para DVR -->
              <v-row>
                <v-col>
                  <v-checkbox
                    v-model="protocolCkeckBox"
                    label="RTSP"
                    value="RTSP"
                  ></v-checkbox>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="3">
                  <v-select
                    v-model="selectedManufacturer"
                    :items="manufacturers"
                    label="Fabricante"
                    variant="outlined"
                    density="compact"
                    @update:model-value="updateFabricante"
                  ></v-select>
                </v-col>
                <v-col cols="12" xl="4" lg="4" md="4" sm="4">
                  <v-select
                    v-model="selectedModel"
                    :items="models"
                    label="Modelo"
                    variant="outlined"
                    density="compact"
                    :disabled="!selectedManufacturer"
                    @update:model-value="updateModelo"
                  ></v-select>
                </v-col>
                <v-col cols="12" xl="4" lg="4" md="4" sm="5">
                  <v-text-field
                    v-model="deviceFullInfo.ip"
                    label="IP ou URL do DVR"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="2" lg="2" md="3" sm="3">
                  <v-text-field
                    v-model="deviceFullInfo.porta"
                    label="Porta"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="deviceFullInfo.path"
                    label="Path no Dispositivo ex: /minitorrealtime/cam"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" xl="2" lg="2" md="2" sm="3">
                  <v-text-field
                    v-model="deviceFullInfo.channel"
                    label="Numero do Canal ex: camera 4 o canal é 4"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field
                    v-model="deviceFullInfo.user"
                    label="Usuario"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field
                    v-model="deviceFullInfo.pass"
                    label="Senha"
                    variant="outlined"
                    density="compact"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </template>
          <template v-else-if="selectedDeviceType === 'Camera IP'">
            <!-- Configurações para Câmera IP -->
            <v-text-field label="URL da Câmera IP"></v-text-field>
            <v-text-field></v-text-field>
            <v-text-field></v-text-field>
          </template>
          <template v-else-if="selectedDeviceType === 'URL da Web'">
            <!-- Configurações para NVR -->
            <v-text-field></v-text-field>
            <v-text-field></v-text-field>
            <v-text-field></v-text-field>
          </template>
          <template v-else>
            <p>Selecione um tipo de dispositivo para configurar os detalhes.</p>
          </template>
        </v-form>
      </v-card>
    </template>

    <template v-slot:item.3>
      <v-card title="Verificação da URL" flat>
        <v-divider />
        <v-card-text>Essa é sua URL:</v-card-text>
        <v-container>
          <v-row class="mb-4">
            <v-col>
              <span
                class="text-primary font-weight-bold"
                v-if="
                  selectedDeviceType === 'DVR' &&
                  deviceFullInfo.fabricante === 'Intelbras'
                "
                >{{
                  protocolCkeckBox[0].toLowerCase() +
                  "://" +
                  deviceFullInfo.user +
                  ":" +
                  deviceFullInfo.pass +
                  "@" +
                  deviceFullInfo.ip +
                  ":" +
                  deviceFullInfo.porta +
                  "/" +
                  deviceFullInfo.path +
                  "?channel=" +
                  deviceFullInfo.channel +
                  "&subtype=1"
                }}</span
              >
            </v-col>
          </v-row>
          <v-divider />
          <v-row class="mt-1">
            <v-col>
              <v-chip class="" :color='statusUrl.tagColor' label>
                <v-icon icon="mdi-label" start></v-icon>
                {{ statusUrl.status }}
              </v-chip></v-col
            >
          </v-row>
          <v-row class="mt-2">
            <v-col>
              <v-btn variant="outlined" color="yellow-darken-2"
                >Testar URL</v-btn
              >
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </template>

    <template v-slot:item.4>
      <v-card title="Passo 4" flat>Conteúdo do Passo 4...</v-card>
    </template>

    <v-stepper-actions
      next-text="Próximo"
      prev-text="Anterior"
      :disabled="disabledControl"
      @click:next="goToNextStep"
      @click:prev="goToPrevStep"
    />
  </v-stepper>
</template>

<script setup>
import { computed, ref } from "vue";
import { red } from "vuetify/util/colors";

const disabledControl = computed(() => {
  if (step.value === 1 && selectedDeviceType.value === null) return true; // Desabilita o botão "Anterior" no primeiro passo
  if (step.value === 4) return "next"; // Desabilita o botão "Próximo" no último passo
});

const step = ref(1); // Estado atual do passo
const stepper = ref(null); // Referência ao v-stepper
const selectedDeviceType = ref(null);
const protocolCkeckBox = ref([]);

// dados de imputs
function updateFabricante(value) {
  deviceFullInfo.value.fabricante = value;
}
function updateModelo(value) {
  deviceFullInfo.value.modelo = value;
}
const deviceFullInfo = ref({
  fabricante: null,
  modelo: null,
  ip: null,
  porta: null,
  path: null,
  channel: null,
  user: null,
  pass: null,
});

// Funções para navegação
const goToNextStep = () => {
  stepper.value?.next(); // Avança para o próximo passo
};

const goToPrevStep = () => {
  stepper.value?.prev(); // Volta para o passo anterior
};

//lidando com dvr passo 2
// Lista de fabricantes
const manufacturers = ["Intelbras", "Genérico", "Outro"];

// Estado selecionado pelo usuário
const selectedManufacturer = ref(null);
const selectedModel = ref(null);

// Modelos disponíveis por fabricante
const modelsByManufacturer = {
  Intelbras: ["HDCVI 1004 G2", "VIP 1120 B", "Mibo Cam"],
  Genérico: ["Modelo Genérico 1", "Modelo Genérico 2"],
  Outro: ["Modelo Personalizado"],
};

// Computed para modelos dinâmicos
const models = computed(() => {
  return selectedManufacturer.value
    ? modelsByManufacturer[selectedManufacturer.value] || []
    : [];
});

//dados e fuunões do passo 3
const statusUrl = ref({
  status: "pendente",
  error: null,
  tagColor: "yellow"
});

</script>
