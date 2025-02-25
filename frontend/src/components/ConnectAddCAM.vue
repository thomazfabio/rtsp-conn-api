<template>
  <v-stepper :mobile="isMobile" hide-actions ref="stepper" :items="['Passo 1', 'Passo 2', 'Passo 3', 'Passo 4']"
    v-model="step">
    <template v-slot:item.1>
      <v-card title="Tipo de dispositivo" flat>
        <v-row>
          <v-container>
            <v-col cols="12" lg="6" md="6" sm="8">
              <v-select label="Selecione o tipo" :items="['DVR', 'Camera IP', 'URL da Web']" variant="outlined"
                v-model="selectedDeviceType"></v-select>
            </v-col>
          </v-container>
        </v-row>
      </v-card>
    </template>

    <template v-slot:item.2>
      <v-card>
        <v-card-title class="pr-0 pl-0">Detalhes da conexão</v-card-title>
        <v-form>
          <template v-if="selectedDeviceType === 'DVR'">
            <v-card-subtitle class="pr-0 pl-0">Informações do DVR</v-card-subtitle>
            <v-divider class="mt-3 mb-3" />
            <v-container class="pr-0 pl-0" fluid>
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
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field v-model="deviceFullInfo.user" label="Usuario" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>
                <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                  <v-text-field v-model="deviceFullInfo.pass" label="Senha" variant="outlined"
                    density="compact"></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </template>
          <template v-else-if="selectedDeviceType === 'Camera IP'">
            <!-- Configurações para Câmera IP -->
            <v-divider class="mt-1 mb-8" />
            <v-row>
              <v-col cols="12" lg="12" class="pb-0 pt-0 mt-0 mb-0">
                <v-row>
                  <v-checkbox class="pl-1 mr-5" v-model="protocolCkeckBox" label="RTSP" value="RTSP"
                    color="info"></v-checkbox>
                  <v-checkbox class="pl-1" v-model="preferedStream" label="Stream extra " color="info"></v-checkbox>
                </v-row>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-select v-model="selectedManufacturer" :items="manufacturers" label="Fabricante" variant="outlined"
                  density="compact" @update:model-value="updateFabricante"></v-select>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-select v-model="selectedModel" :items="models" label="Modelo" variant="outlined" density="compact"
                  :disabled="!selectedManufacturer" @update:model-value="updateModelo"></v-select>
              </v-col>


              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.ip" label="IP ou URL da Câmera" variant="outlined"
                  density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.path" label="Path" variant="outlined" density="compact"
                  :disabled="true"></v-text-field>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.porta" label="Porta" variant="outlined"
                  density="compact"></v-text-field>
              </v-col>
              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.channel" label="Numero do canal" variant="outlined"
                  density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.user" label="Usuario" variant="outlined"
                  density="compact"></v-text-field>
              </v-col>

              <v-col cols="12" xl="4" lg="4" md="4" sm="8">
                <v-text-field v-model="deviceFullInfo.pass" label="Senha" variant="outlined"
                  density="compact"></v-text-field>
              </v-col>

            </v-row>
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
      <v-alert class="mb-1" v-if="alerts.alert_teste_url.status" :type="alerts.alert_teste_url.type" variant="outlined" closable
        dismissible>
        {{ alerts.alert_teste_url.msg }}
      </v-alert>
      <v-card :loading="loading.await_status_url" :disabled="loading.await_status_url">
        <v-card-title class="pr-0 pl-0">Teste a URL</v-card-title>
        <v-divider />
        <v-card-text class="pr-0 pl-0">Essa é sua URL:</v-card-text>
        <v-container class="pr-0 pl-0">
          <v-row class="mb-4">
            <v-col>
              <span class="text-primary font-weight-bold">{{ fullUrl }}</span>
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
      <v-alert v-if="alerts.alert_save_cam.status" :type="alerts.alert_save_cam.type" variant="outlined" closable
        dismissible>
        {{ alerts.alert_save_cam.msg }}
      </v-alert>
      <v-card :loading="loading.await_status_save_cam" :disabled="loading.await_status_save_cam">
        <v-card-title class="pr-0 pl-0">Finalize a configuração</v-card-title>
        <v-container class="pr-0 pl-0">
          <v-row>
            <v-col>
              <span class="font-weight-bold">URL :  </span>
              <span class="text-primary font-weight-bold"> {{ fullUrl }}</span>
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
// import stores
import { useCamUrlMenageStore } from "../stores/utils/camUrlMenage";
import { useCreateCamFullDataStore } from "../stores/deviceManage/createCamFullData";
import { useManageDeviceInfoStore } from "../stores/deviceManage/manageDeviceInfo";
import camSimpleVisualizer from "./camVizualizer/camSimpleVisualizer.vue";
import { useDisplay } from "vuetify";

// instanciando stores
const storeManageDeviceInfo = useManageDeviceInfoStore();
const storeCamUrlMenage = useCamUrlMenageStore();
const storeCreateCamFullData = useCreateCamFullDataStore();

const { xs } = useDisplay();
const isMobile = computed(() => xs.value);

const disabledControl = computed(() => {
  if (step.value === 1 && selectedDeviceType.value === null) return true; // Desabilita o botão "Anterior" no primeiro passo
  if (step.value === 4) return "next"; // Desabilita o botão "Próximo" no último passo
  if (step.value === 2 && protocolCkeckBox.value != "RTSP") return "next";
  if (step.value === 3 && statusUrl.value.status !== "online") return "next";
});

const step = ref(1); // Estado atual do passo
const stepper = ref(null); // Referência ao v-stepper
const selectedDeviceType = ref(null);
const protocolCkeckBox = ref([]);
const selectedManufacturer = ref(null);
const selectedModel = ref(null);
const preferedStream = ref(false);
const urlStreamReady = ref(null);
const loading = ref({ await_status_url: false, await_status_save_cam: false });
const alerts = ref({ alert_teste_url: { type: "", status: false, msg: "" }, alert_save_cam: { type: "", status: false, msg: "" } });
const manufacturers = ref([]);


// Lista de dispositivos carregados do backend
const allDevices = ref([]);


//observando mudanças
watch([selectedManufacturer, selectedModel], ([newManufacturer, newModel]) => {
  if (newManufacturer === "intelbras" && newModel === "HDCVI 1004 G2") {
    deviceFullInfo.value.path = "cam/realmonitor";
  }
});

//carrega dados do dispositivo
watch(selectedDeviceType, async (newVal) => {
  if (newVal === "DVR") {
    console.log("DVR selecionado");
    const device = await storeManageDeviceInfo.searchDeviceInfoByType("dvr").then((res) => {
      console.log(res.data);

      // Armazena todos os dispositivos retornados
      allDevices.value = res.data;

      // Extrai os fabricantes e remove duplicatas
      const uniqueManufacturers = [...new Set(res.data.map(item => item.fabricante))];

      // Atualiza a variável reativa
      manufacturers.value = uniqueManufacturers;
    }).catch((err) => {
      console.error(err);
    });
  }

  if (newVal === "Camera IP") {
    console.log("Camera IP selecionada");
    const device = await storeManageDeviceInfo.searchDeviceInfoByType("ip_cam").then((res) => {
      console.log(res.data);
      // Armazena todos os dispositivos retornados
      allDevices.value = res.data;

      // Extrai os fabricantes e remove duplicatas
      const uniqueManufacturers = [...new Set(res.data.map(item => item.fabricante))];

      // Atualiza a variável reativa
      manufacturers.value = uniqueManufacturers;
    }).catch((err) => {
      console.error(err);
    });
  }

  if (newVal === "URL da Web") {
    console.log("URL da Web selecionada");
    const device = await storeManageDeviceInfo.searchDeviceInfoByType("web_url").then((res) => {
      console.log(res.data);
    }).catch((err) => {
      console.error(err);
    });
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

// Observa mudanças no fabricante e modelo selecionados
watch([selectedManufacturer, selectedModel], ([newManufacturer, newModel]) => {
  if (newManufacturer && newModel) {
    // Busca o dispositivo correspondente na lista carregada
    const foundDevice = allDevices.value.find(
      (item) => item.fabricante === newManufacturer && item.modelo === newModel
    );

    // Atualiza o path dinamicamente
    deviceFullInfo.value.path = foundDevice ? foundDevice.path_rtsp : "";

    // atualiza camData deviceid
    camData.value.deviceId = foundDevice ? foundDevice.id : null;
  }
});

// Computed para obter os modelos conforme o fabricante selecionado
const models = computed(() => {
  return selectedManufacturer.value
    ? allDevices.value
      .filter(item => item.fabricante === selectedManufacturer.value)
      .map(item => item.modelo)
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

const teste_url = async () => {
  loading.value.await_status_url = true;
  alerts.value.alert_teste_url.status = false;
  alerts.value.alert_teste_url.msg = "";
  alerts.value.alert_teste_url.type = "";
  await storeCamUrlMenage.testeUrlRtsp(fullUrl.value).then((res, err) => {
    loading.value.await_status_url = false;
    if (res.data.status === "online") {
      alerts.value.alert_teste_url.status = true;
      alerts.value.alert_teste_url.type = "success";
      alerts.value.alert_teste_url.msg = "URL valida. Testada com sucesso!";
    }
    if (res.data.status === "error") {
      alerts.value.alert_teste_url.status = true;
      alerts.value.alert_teste_url.type = "error";
      alerts.value.alert_teste_url.msg = "Falha ao testar URL. Verifique os dados do dispositivo e tente novamente";
    }
    if (err) {
      alerts.value.alert_teste_url.status = true;
      alerts.value.alert_teste_url.type = "error";
      alerts.value.alert_teste_url.msg = "Falha ao testar URL. Verifique os dados do dispositivo e tente novamente";
    }
  });
}

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
const saveCamData = async () => {
  console.log(camData.value.deviceId);
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
    "user_id": "1",
    "device_id": camData.value.deviceId,
    "cam_name": camData.value.camName,
    "grupo": camData.value.grupo,
    "full_cam_url_stream": urlStreamReady.value,
    "ful_cam_url_rtsp": fullUrl.value,
    "cam_status": "online",
    "device_config": device
  };

  loading.value.await_status_save_cam = true;
  alerts.value.alert_save_cam.status = false;
  try {
    const response = await storeCreateCamFullData.createCamFullData(fullCamData);
    loading.value.await_status_save_cam = false;
    
   
    alerts.value.alert_save_cam.status = true;
    alerts.value.alert_save_cam.type = "success";
    alerts.value.alert_save_cam.msg = "Dados da câmera salvo com sucesso!";
  } catch (err) {
    loading.value.await_status_save_cam = false;;
    console.error("Erro capturado:", err);
    console.log("Erro ao salvar dados da câmera componente ConnectAddCAM.vue");
    alerts.value.alert_save_cam.status = true;
    alerts.value.alert_save_cam.type = "error";
    alerts.value.alert_save_cam.msg = "Erro ao salvar dados da câmera!";
  }
};
</script>