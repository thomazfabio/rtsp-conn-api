<template>
  <v-app id="inspire">
    <!-- Drawer de navegação -->
    <v-navigation-drawer v-model="drawer">
      <!-- Itens do menu -->
      <v-list>
        <v-list-item to="/">
          <v-list-item-title
            ><v-btn block color="primary">Home</v-btn></v-list-item-title
          >
        </v-list-item>
        <v-list-item to="/connectCam">
          <v-list-item-title
            ><v-btn block color="green"
              >Conectar câmeras</v-btn
            ></v-list-item-title
          >
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Barra de navegação -->
    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>RTSP API</v-app-bar-title>
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

const drawer = ref(false); // Inicializando o estado do drawer
</script>
