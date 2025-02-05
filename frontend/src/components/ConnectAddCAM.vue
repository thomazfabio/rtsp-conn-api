<template>
  <v-stepper hide-actions ref="stepper" :items="['Passo 1', 'Passo 2', 'Passo 3', 'Passo 4']" v-model="step">
    <template v-slot:item.1>
      <v-card title="Selecione o tipo de dispositivo:" flat>
        <v-row>
          <v-container>
            <v-col cols="6">
              <v-select label="Selecione o tipo de dispositivo que deseja conectar"
                :items="['DVR', 'Camera IP', 'URL da Web']" variant="outlined" v-model="selectedDeviceType"></v-select>
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
                <v-col class="d-flex align-center" cols="auto">
                  <span>Protocolo de conexão:</span>
                </v-col>
                <v-col cols="auto">
                  <v-checkbox class="d-flex align-center" v-model="protocolCkeckBox" label="RTSP"
                    value="RTSP"></v-checkbox>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="3">
                  <v-select v-model="selectedManufacturer" :items="manufacturers" label="Fabricante" variant="outlined"
                    density="compact" @update:model-value="updateFabricante"></v-select>
                </v-col>
                <v-col cols="12" xl="4" lg="4" md="4" sm="4">
                  <v-select v-model="selectedModel" :items="models" label="Modelo" variant="outlined" density="compact"
                    :disabled="!selectedManufacturer" @update:model-value="updateModelo"></v-select>
                </v-col>
                <v-col cols="12" xl="4" lg="4" md="4" sm="5">
                  <v-text-field v-model="deviceFullInfo.ip" label="IP ou URL do DVR" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="2" lg="2" md="3" sm="3" class="d-flex align-center">
                  <v-text-field v-model="deviceFullInfo.porta" label="Porta" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>

                <v-col class="d-flex align-center">
                  <v-text-field v-model="deviceFullInfo.path" label="Path" variant="outlined" density="compact"
                    :disabled="true"></v-text-field>
                </v-col>
                <v-col cols="12" xl="3" lg="3" md="3" sm="3" class="d-flex align-center">
                  <v-text-field v-model="deviceFullInfo.channel" label="Numero do Canal ex: camera 4 o canal é 4"
                    variant="outlined" density="compact"></v-text-field>
                </v-col>
                <v-col cols="auto">
                  <v-checkbox v-model="preferedStream" label="Stream extra " color="info">
                  </v-checkbox>
                  {{ deviceFullInfo.preferedStream }}
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field v-model="deviceFullInfo.user" label="Usuario" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field v-model="deviceFullInfo.pass" label="Senha" variant="outlined"
                    density="compact"></v-text-field>
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
              <span class="text-primary font-weight-bold" v-if="
                selectedDeviceType === 'DVR' &&
                deviceFullInfo.fabricante === 'Intelbras'
              ">{{ fullUrl }}</span>
            </v-col>
          </v-row>
          <v-divider />
          <v-row class="mt-1">
            <v-col>
              <v-chip class="" :color="statusUrl.tagColor" label>
                <v-icon icon="mdi-label" start></v-icon>
                {{ statusUrl.status }}
              </v-chip></v-col>
          </v-row>
          <v-row class="mt-2">
            <v-col>
              <v-btn variant="outlined" color="yellow-darken-2" @click="teste_url">Testar URL</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </template>

    <template v-slot:item.4>
      <v-card title="Finalize e salve as configurações" flat>
        <v-container>
          <v-row>
            <v-col cols="auto">
              <span>Sua URL: </span>
            </v-col>
            <v-col>
              <span class="text-primary font-weight-bold" v-if="
                selectedDeviceType === 'DVR' &&
                deviceFullInfo.fabricante === 'Intelbras'
              ">{{ fullUrl }}</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" xl="5" lg="5" md="6" sm="8">
              <v-divider class="mb-4" />
              <v-row>
                <v-col>
                  <v-btn color="info" prepend-icon="mdi-play-speed" stacked variant="outlined" class="w-75"
                    @click="controleCamActions.startStream">play</v-btn>
                </v-col>
                <v-col class="d-flex justify-center">
                  <v-btn color="red" prepend-icon="mdi-stop-circle-outline" stacked variant="outlined" class="w-75"
                    @click="controleCamActions.stopStream">stop</v-btn>
                </v-col>
                <v-col class="d-flex justify-end">
                  <v-btn color="yellow-darken-2" prepend-icon="mdi-refresh" stacked variant="outlined"
                    class="w-75">refresh</v-btn>
                </v-col>
              </v-row>
              <v-divider class="mb-4 mt-4" />
              <v-form>
                <v-text-field v-model="camData.camName" variant="outlined" label="Nome da Câmera"
                  density="compact"></v-text-field>
                <v-text-field v-model="camData.grupo" variant="outlined" label="Grupo / Local"
                  density="compact"></v-text-field>
              </v-form>
              <v-divider class="mb-4" />
              <v-row>
                <v-col class="">
                  <v-btn color="green-darken-2" prepend-icon="mdi-content-save-cog-outline" rounded="xl"
                    variant="outlined" @click="saveCamData">salvar configurações</v-btn>
                </v-col>
              </v-row>
              <v-divider class="mb-4 mt-4" />
            </v-col>
            <v-col class="d-flex justify-center">
              <camSimpleVisualizer :cam-url="fullUrl" :visualizer-url="'/visualizer_cam_v2/stream'"
                :cam-name="camData.camName" :grupo="camData.grupo" :cam-chennel="deviceFullInfo.channel"
                @url-ready="urlReady" ref="controleCam" />
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </template>

    <v-stepper-actions next-text="Próximo" prev-text="Anterior" :disabled="disabledControl" @click:next="goToNextStep"
      @click:prev="goToPrevStep" color="green" />
  </v-stepper>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useCamUrlMenageStore } from "../stores/utils/camUrlMenage";
import { useCreateCamFullDataStore } from "../stores/deviceManage/createCamFullData";
import camSimpleVisualizer from "./camVizualizer/camSimpleVisualizer.vue";
const storeCamUrlMenage = useCamUrlMenageStore();
const storeCreateCamFullData = useCreateCamFullDataStore();

const disabledControl = computed(() => {
  if (step.value === 1 && selectedDeviceType.value === null) return true; // Desabilita o botão "Anterior" no primeiro passo
  if (step.value === 4) return "next"; // Desabilita o botão "Próximo" no último passo
  if (step.value === 2 && protocolCkeckBox.value != "RTSP") return "next";
});

const step = ref(1); // Estado atual do passo
const stepper = ref(null); // Referência ao v-stepper
const selectedDeviceType = ref(null);
const protocolCkeckBox = ref([]);
const selectedManufacturer = ref(null);
const selectedModel = ref(null);
const preferedStream = ref(false);
const urlStreamReady = ref(null);


//observando mudanças
watch([selectedManufacturer, selectedModel], ([newManufacturer, newModel]) => {
  if (newManufacturer === "Intelbras" && newModel === "HDCVI 1004 G2") {
    deviceFullInfo.value.path = "cam/realmonitor";
  }
});

watch(preferedStream, (newVal) => {
  if (newVal) {
    deviceFullInfo.value.preferedStream = "1";
  } else {
    deviceFullInfo.value.preferedStream = "0";
  }
});

// dados de imputs
function updateFabricante(value) {
  deviceFullInfo.value.fabricante = value;
}
function updateModelo(value) {
  deviceFullInfo.value.modelo = value;
}

// Dados do dispositivo
const deviceFullInfo = ref({
  fabricante: null,
  modelo: null,
  ip: null,
  porta: null,
  path: null,
  channel: null,
  preferedStream: "0",
  user: null,
  pass: null,
});

// dados do objeto camera para salvar "inclui dados de usuario"
const camData = ref({
  userId: null,
  deviceId: null,
  camName: null,
  grupo: null,
  camUrl: null,
  camStatus: null,
});


// URL completa rtsp
const fullUrl = computed(() => {
  return (
    protocolCkeckBox.value[0].toLowerCase() +
    "://" +
    deviceFullInfo.value.user +
    ":" +
    deviceFullInfo.value.pass +
    "@" +
    deviceFullInfo.value.ip +
    ":" +
    deviceFullInfo.value.porta +
    "/" +
    deviceFullInfo.value.path +
    "?channel=" +
    deviceFullInfo.value.channel +
    "&subtype=" +
    deviceFullInfo.value.preferedStream
  );
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
const manufacturers = ["Intelbras"];

// Modelos disponíveis por fabricante
const modelsByManufacturer = {
  Intelbras: ["HDCVI 1004 G2"],
};

// Computed para modelos dinâmicos
const models = computed(() => {
  return selectedManufacturer.value
    ? modelsByManufacturer[selectedManufacturer.value] || []
    : [];
});

//dados e fuunões do passo 3

// Computed para observar diretamente o valor reativo da store
const statusUrl = computed(() => {
  const statusCam = storeCamUrlMenage.cam.status;
  if (statusCam === "pendente") {
    return { status: "pendente", tagColor: "yellow" };
  }
  if (statusCam === "online") {
    return { status: "online", tagColor: "success" };
  }
  if (statusCam === "error") {
    return { status: "falha", tagColor: "error" };
  }
  return { status: "", tagColor: "" };
});

// Realiza alguma lógica ao montar
onMounted(() => {
  console.log("Status inicial:", statusUrl.value.status);
});

const teste_url = () => storeCamUrlMenage.testeUrlRtsp(fullUrl.value);

// lidando com controles do passo 4
const controleCam = ref(null);
const controleCamActions = {
  stopStream: () => {
    controleCam.value.stopStream();
  },
  startStream: () => {
    controleCam.value.startStream();
  },
};

// pega url de streaming do componente filho
function urlReady(url) {
  urlStreamReady.value = url;
  console.log(urlStreamReady.value);
}

// chamadas na store para salvar dados
const saveCamData = () => {
  const device =
  {
    "channel": deviceFullInfo.value.channel,
    "prefered_stream_quality": deviceFullInfo.value.preferedStream,
    "device_user": deviceFullInfo.value.user,
    "device_password_hash": deviceFullInfo.value.pass,
    "device_ip_url": deviceFullInfo.value.ip,
    "porta": deviceFullInfo.value.porta,
    "protocolo_entrada": protocolCkeckBox.value[0].toLowerCase(),
    "protocolo_saida": "http"
  }

  const fullCamData = {
    "user_id": "0101",
    "device_id": "0101",
    "cam_name": camData.value.camName,
    "grupo": camData.value.grupo,
    "full_cam_url_stream": urlStreamReady,
    "ful_cam_url_rtsp": fullUrl.value,
    "cam_status": "online",
    "device_config": device
  };
  storeCreateCamFullData.createCamFullData(fullCamData);
};
</script>
