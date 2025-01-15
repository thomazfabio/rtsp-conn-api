<template>
  <v-app id="inspire">
    <!-- Drawer de navegação -->
    <v-navigation-drawer v-model="drawer">
      <!-- Itens do menu -->
      <v-list>
        <v-list-item prepend-icon="mdi-home" title="Home" to="/" />
        <v-list-item prepend-icon="mdi-eye" title="Visualizar" to="" />
        <v-list-item
          prepend-icon="mdi-cctv"
          title="Adicionar câmera"
          to="connectCam"
        />
        <v-list-item prepend-icon="mdi-cog-transfer" title="Configurações" to="" />
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn block color="red"> Logout </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Barra de navegação -->
    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>RTSP API</v-app-bar-title>
      <v-switch
        class="d-flex align-center justify-end mr-4"
        true-value="Dark"
        false-value="Light"
        color="purple"
        :label="`Tema: ${switchTheme.toString()}`"
        v-model="switchTheme"
      ></v-switch>
    </v-app-bar>

    <!-- Conteúdo principal da página -->
    <v-main>
      <router-view />
      <!-- Aqui será injetado o conteúdo da página específica -->
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from "vue";
import { watch } from "vue";
import { useTheme } from "vuetify";

const drawer = ref(false); // Inicializando o estado do drawer

//ajustando thema vuetufy
const theme = useTheme();
const switchTheme = ref("Dark");

watch(switchTheme, () => {
  if (switchTheme.value == "Dark") {
    theme.global.name.value = "dark";
  }
  if (switchTheme.value == "Light") {
    theme.global.name.value = "light";
  }
});
</script>
